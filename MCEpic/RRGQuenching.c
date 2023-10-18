#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <time.h> //L'ho aggiunto io (RC) per inizializzare il generatore

#define C 3
#define p 3
#define nDisorderCopies 1 // number of instances for each disorder configuration TO BE IMPLEMENTED

#define t_start 100 // number of MC Sweeps at the beginning of the simulation to take track of
#define t_meas 100  // number of MC Sweep between measures after t     t_end-t_start better be a multiple of t_meas
#ifndef ANNEAL
#define t_end 2000 // number of Monte Carlo sweeps
#endif

/* variabili globali per il generatore random */
unsigned int myrand, _ira[256];
unsigned char _ip, _ip1, _ip2, _ip3;

int N, numPosJ, *graph, *deg, *J, **neigh, *s, n_int,is = 0;
int ener0, mag;
double prob[C + 1], T, H;
long long unsigned int t;
char Tp_string[7];
FILE *out;


#define FNORM (2.3283064365e-10)
#define RANDOM ((_ira[_ip++] = _ira[_ip1++] + _ira[_ip2++]) ^ _ira[_ip3++])
#define FRANDOM (FNORM * RANDOM)
#define pm1 ((FRANDOM > 0.5) ? 1 : -1)

unsigned int randForInit(void)
{
    unsigned long long int y;

    y = myrand * 16807LL;
    myrand = (y & 0x7FFFFFFF) + (y >> 31);
    myrand = (myrand & 0x7FFFFFFF) + (myrand >> 31);
    return myrand;
}

void initRandom(void)
{
    int i;

    _ip = 128;
    _ip1 = _ip - 24;
    _ip2 = _ip - 55;
    _ip3 = _ip - 61;

    for (i = _ip3; i < _ip; i++)
    {
        _ira[i] = randForInit();
    }
}

float gaussRan(void)
{
    static int iset = 0;
    static float gset;
    float fac, rsq, v1, v2;

    if (iset == 0)
    {
        do
        {
            v1 = 2.0 * FRANDOM - 1.0;
            v2 = 2.0 * FRANDOM - 1.0;
            rsq = v1 * v1 + v2 * v2;
        } while (rsq >= 1.0 || rsq == 0.0);
        fac = sqrt(-2.0 * log(rsq) / rsq);
        gset = v1 * fac;
        iset = 1;
        return v2 * fac;
    }
    else
    {
        iset = 0;
        return gset;
    }
}

void error(char *string)
{
    fprintf(stderr, "ERROR: %s\n", string);
    exit(EXIT_FAILURE);
}

double sqrtOrZero(double toSqrt)
{
    if (toSqrt < 0. && toSqrt > -0.0001)
    {
        return 0.;
    }
    return sqrt(toSqrt);
}

void allocateAll(void)
{
    deg = (int *)calloc(N, sizeof(int));
    graph = (int *)calloc(p * n_int, sizeof(int));    // i-th p-block is the i-th interaction p-plet
    J = (int *)calloc(C * N, sizeof(int));            // i-th c-block is given by the (at most) c J values of interactions of i-th spin
    neigh = (int **)calloc(N, sizeof(int *));         // one array for each spin
    neigh[0] = (int *)calloc(N * p * C, sizeof(int)); // for each spin there is a
    for (int i = 1; i < N; i++)
        neigh[i] = neigh[0] + i * p * C;
    s = (int *)calloc(N, sizeof(int));
}

int *whereEqual(int *a) // returns the first element of the a-array which is equal to another element of a (if not present: NULL)
{
    int i, j;

    for (i = 0; i < p - 1; i++)
        for (j = i + 1; j < p; j++)
            if (a[i] == a[j])
                return a + j;
    return NULL;
}

void initRRGraph(void)
{
    int i, j = 0, k = 0, changes, tmp, site, *pointer;

    for (i = 0; i < N; i++)
    {
        k += C - (i * C > n_int * p);
        for (; j < k; j++)
        {
            graph[j] = i;
        }
    }

    for (i = 0; i < p * n_int; i++) // running over all the array and doing casual switches (one for each position)
    {
        j = (int)(FRANDOM * p * n_int);
        tmp = graph[j];
        graph[j] = graph[i];
        graph[i] = tmp;
    } // at the end we'll have smth like [3 4 5  1 4 6  3 3 5 ...]
    do
    {
        changes = 0;
        for (i = 0; i < n_int; i++)
        {
            pointer = whereEqual(graph + i * p); // checking whether there is an interaction with a spin appearing more than once
            if (pointer != NULL)                 // in the affirmative case, the first occurrence is switched with a random entry
            {
                j = (int)(FRANDOM * p * n_int);
                tmp = graph[j];
                graph[j] = *pointer;
                *pointer = tmp;
                changes++;
            }
        }
    } while (changes); // keep doing it until no more switches are needed (i.e., no variable is self-interacting)
    for (i = 0; i < N; i++)
        deg[i] = 0;

    for (i = 0; i < numPosJ; i++) // associate first numPosJ c-plets of graph to interactions with J=1
    {
        for (j = 0; j < p; j++) // For each site in the p-plet
        {
            site = graph[i * p + j];
            for (k = 0; k < p; k++)
                neigh[site][p * deg[site] + k] = graph[i * p + k]; // For each site, in the array neigh[site] we ll have
                                                                   // interaction c-plets to which it participates
            J[C * site + deg[site]] = 1;                           // in the C s + d position of the array I ll have the coupling
                                                                   // of the d interaction of the s spin
            deg[site]++;
        }
    }
    for (; i < n_int; i++)
    {
        for (j = 0; j < p; j++)
        {
            site = graph[i * p + j];
            for (k = 0; k < p; k++)
                neigh[site][p * deg[site] + k] = graph[i * p + k];
            J[C * site + deg[site]] = -1;
            deg[site]++;
        }
    }
    // for (i = 0; i < N; i++){                        //Useful to check on degrees
    // if (deg[i] != C && deg[i] != C-1)
    // printf("Weird degrees situation at site %d, with deg = %d\n",i, deg[i]);}
}

void initProb(double beta, double field)
{
    int i;
    i = C;
    while (i >= 0)
    {
        prob[i] = exp(-2. * beta * (i - field));
        i -= 2;
    }
    i = C - 1;
    while (i >= 0)
    {
        prob[i] = exp(-2. * beta * (i + 1 + field));
        i -= 2;
    }
}

int ener(void)
{
    int i, j, prod, res = 0;

    for (i = 0; i < numPosJ; i++)
    {
        prod = 1;
        for (j = 0; j < p; j++)
            prod *= s[graph[p * i + j]];
        res += prod;
    }
    for (; i < n_int; i++)
    {
        prod = -1;
        for (j = 0; j < p; j++)
            prod *= s[graph[p * i + j]];
        res += prod;
    }
    return -res;
}

void oneMCStep(long long int t)
{
    int i, j, k, ind, prod, sum;

    for (i = 0; i < N; i++)
    {

        sum = 0;
        for (j = 0; j < C; j++) // loop over the interactions of the site
        {
            prod = J[C * i + j];
            for (k = 0; k < p; k++) // loop over the sites in the interaction
                prod *= s[neigh[i][p * j + k]];
            sum += prod;
        }
        ind = sum - (1 + s[i]) / 2;
        // printf("%f\n", FRANDOM); to check if the generator s running correctly
        if (ind < 0 || FRANDOM < prob[ind])
        {
            s[i] = -s[i];
            mag += 2 * s[i];
        }
    }
}


#ifndef ANNEAL
#define simType "Quenching"
void coolingSimulation()
{
    fprintf(out, "#%s  C = %i p = %i  N = %i  Tp = %s  T = %f  H = %f seed = %u\n#mag ener time\n",
            simType, C, p, N, Tp_string, T, H, myrand);
    t = 0;
    fprintf(out, "%i %i 0\n", mag, ener() - ener0);

    for (; t < t_start;)
    {
        oneMCStep(t);
        t++;
        fprintf(out, "%i %i %lli\n", mag, ener() - ener0, t);
    }
    for (; t < t_end;)
    {
        for (int i = 1; i <= t_meas; i++, t++)
        {
            oneMCStep(t);
        }
        fprintf(out, "%i %i %lli\n", mag, ener() - ener0, t);
    }
}
#else
#define simType "Annealing"
int nanneal, t_end;
double deltaT, T_max;
void coolingSimulation()
{
    fprintf(out, "#%s  C = %i p = %i  N = %i  Tp = %s  T = %f  H = %f  deltaT= %f n_anneal=%d seed = %u\n#mag ener time\n",
            simType, C, p, N, Tp_string, T, H, deltaT, nanneal, myrand);

    T = T_max;
    initProb(1. / T, H);
    t = 0;

    fprintf(out, "%i %i 0\n", mag, ener() - ener0);

    for (; t < t_start;)
    {
        oneMCStep(t);
        t++;
        fprintf(out, "%i %i %lli\n", mag, ener() - ener0, t);
        if (!(t % nanneal))
        {
            T -= deltaT;
            initProb(1. / T, H);
        }
    }

    for (; t < t_end;) // the stop condition could be T>=0 and avoid computing t_end
    {
        for (int j = 0; j < t_meas; j++)
        {
            oneMCStep(t);
            t++;
        }
        fprintf(out, "%i %i %lli\n", mag, ener() - ener0, t);
        if (!(t % nanneal))
        {
            T -= deltaT;
            initProb(1. / T, H);
        }
    }
}
#endif



int main(int argc, char *argv[])
{
    int i, nSamples;
    double Tp;
    const char *thisRunDataPath = "..\\Data\\Epics\\ThisRun\\";
    char path[200] = "";
    char filename[200] = "";

    // this initializations works on Linux. I (RC) am working on Windows
    /*
    FILE *devran = fopen("/dev/random","r");
    //FILE *devran = fopen("/dev/urandom","r"); // lower quality
    fread(&myrand, 4, 1, devran);
    fclose(devran);
      */
    myrand = time(NULL); // my (RC) initialization, for Windows


#ifndef ANNEAL
    if (argc != 6)
    {
        fprintf(stderr, "usage: %s <N> <Tp> <T> <nSamples> <h>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    T = atof(argv[3]);
#else
    if (argc != 8)
    {
        fprintf(stderr, "usage: %s <N> <Tp> <T_max> <nSamples> <h> <deltaT(double)> <nAnneal (int)>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    T = atof(argv[3]);

    T_max = T;
    deltaT = atof(argv[6]);
    nanneal = atoi(argv[7]);
    t_end = nanneal * (int)((T / deltaT) + 1.1);
    if((nanneal%t_meas)){
        printf("%d", nanneal);
        error("n_anneal should be integers times t_meas.");
    }
#endif

    if((t_end%t_meas) || (t_start%t_meas)){
        error("t_end and t_start should be integers times t_meas.");
    }
    N = atoi(argv[1]);

    if (isdigit(*argv[2]))
    {
        Tp = atof(argv[2]);
    }
    else if (strcmp(argv[2], "inf") == 0)
    {
        Tp = -1; // so, in the rest of the code, if Tp is negative it means it is to be considered infinite
    }
    else
    {
        printf("Planting temperature must be a non-negative number or infinite (inf)\n");
        return EXIT_FAILURE;
    }

    strcpy(Tp_string, argv[2]);

    nSamples = atoi(argv[4]);
    H = atof(argv[5]);
    if (T <= 0.0)
        error("in T");
    if (C % 2)
    {
        if (H < -1.0 || H > 1.0)
            error("in h");
    }
    else
    {
        if (H < -2.0 || H > 0.0)
            error("in h");
    }

    n_int = N * C / p;

    if (Tp > 0.0)
        numPosJ = n_int * 0.5 * (1. + tanh(1. / Tp));
    else if (Tp == 0.0)
        numPosJ = n_int;
    else
    {
        numPosJ = n_int / 2;
    }

#ifdef ANNEAL
    printf("#%s  C = %i p = %i  N = %i  Tp = %s  T = %f  H = %f deltaT = %f n_anneal = %i seed = %u\n",
           simType, C, p, N, Tp_string, T, H, deltaT, nanneal, myrand);
#else
    printf("#%s  C = %i p = %i  N = %i  Tp = %s  T = %f  H = %f  seed = %u\n",
           simType, C, p, N, Tp_string, T, H, myrand);
#endif

    initRandom();
    allocateAll();
    initProb(1. / T, H);

#ifdef SINGLESTORY // if the program is compiled with the SINGLESTORY directive, it only generates one story (with # equal argument)
  is = nSamples; 
#endif
    do
    {
        initRRGraph();
        strcpy(path, "");
        sprintf(filename, "McStories\\Story_%d.txt", is);
        strcat(path, thisRunDataPath);
        strcat(path, filename);
        out = fopen(path, "w+");

        if (out == NULL)
        {
            printf("Error in the creation of the file %s\n\n", path);
            exit(EXIT_FAILURE);
        }

        mag = 0;
        for (i = 0; i < N; i++)
        {
            s[i] = (int)(FRANDOM > 0.5 ? 1 : -1); // different wrt to the planted state initial configuration case, where all s[i] are 1
            mag += s[i];
        }
        ener0 = ener();

        coolingSimulation();

        fclose(out);
        is++;
    } while (is < nSamples);

    return EXIT_SUCCESS;
}