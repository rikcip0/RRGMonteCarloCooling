/* by FRT */
// C-XORSAT on C-RRG
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <time.h> //L'ho aggiunto io (RC) per inizializzare il generatore

#define C 3
#define p 3               // to be implemented, for the moment it is not used and assumed p=C
#define nDisorderCopies 1 // number of instances for each disorder configuration
#define t_end 10e3        // numero di MC steps

#define FNORM (2.3283064365e-10)
#define RANDOM ((_ira[_ip++] = _ira[_ip1++] + _ira[_ip2++]) ^ _ira[_ip3++])
#define FRANDOM (FNORM * RANDOM)
#define pm1 ((FRANDOM > 0.5) ? 1 : -1)

/* variabili globali per il generatore random */
unsigned int myrand, _ira[256];
unsigned char _ip, _ip1, _ip2, _ip3;

int N, numPosJ, *graph, *deg, *J, **neigh, *s;
int ener0, mag, nextMeasMag;
double prob[C + 1];

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

void allocateAll(void)
{
  deg = (int *)calloc(N, sizeof(int));
  graph = (int *)calloc(C * N, sizeof(int));
  J = (int *)calloc(C * N, sizeof(int));
  neigh = (int **)calloc(N, sizeof(int *));
  neigh[0] = (int *)calloc(N * C * C, sizeof(int));
  for (int i = 1; i < N; i++)
    neigh[i] = neigh[0] + i * C * C;
  s = (int *)calloc(N, sizeof(int));
}

int *whereEqual(int *a) // returns the first element of the a-array which is equal to another element of a (if not present: NULL)
{
  int i, j;

  for (i = 0; i < C - 1; i++)
    for (j = i + 1; j < C; j++)
      if (a[i] == a[j])
        return a + j;
  return NULL;
}

void initRRGraph(void)
{
  int i, j, k, changes, tmp, site, *pointer;

  for (i = 0; i < N; i++)
    for (j = 0; j < C; j++)
      graph[C * i + j] = i;   // avrò (per c=3) graph = [0 0 0 1 1 1 2 2 2 ... N N N ]
  for (i = 0; i < C * N; i++) // scorro tutto l'array e faccio switch casuali (uno per ogni posizione)
  {
    j = (int)(FRANDOM * C * N);
    tmp = graph[j];
    graph[j] = graph[i];
    graph[i] = tmp;
  } // alla fine avrò tipo [3 4 5  1 4 6  3 3 5 ...]
  do
  {
    changes = 0;
    for (i = 0; i < N; i++)
    {
      pointer = whereEqual(graph + i * C); // vedo se ho mai un'interazione in cui appare almeno 2 volte la stessa variabile
      if (pointer != NULL)                 // e in caso prendo la prima occorrenza della variabile e la switcho con una in un'entrata random
      {
        j = (int)(FRANDOM * C * N);
        tmp = graph[j];
        graph[j] = *pointer;
        *pointer = tmp;
        changes++;
      }
    }
  } while (changes); // continuo finchè non serve più fare switch (cioè nessuna variabile interagisce con se stessa)

  for (i = 0; i < N; i++)
    deg[i] = 0;

  for (i = 0; i < numPosJ; i++) // associo le prime numPosJ c-plette di graph alle interazioni con J=1
  {
    for (j = 0; j < C; j++) // Per ogni sito nella c-pletta
    {
      site = graph[i * C + j];
      for (k = 0; k < C; k++)
        neigh[site][C * deg[site] + k] = graph[i * C + k]; // per ogni site, nell'array neigh[site] avrò le c-plette di interazione cui partecipa
      J[C * site + deg[site]] = 1;                         // nella posizione C s + d dell'array metto l'accoppiamento della d-esima interazione dello spin s
      deg[site]++;
    }
  }
  for (; i < N; i++)
  {
    for (j = 0; j < C; j++)
    {
      site = graph[i * C + j];
      for (k = 0; k < C; k++)
        neigh[site][C * deg[site] + k] = graph[i * C + k];
      J[C * site + deg[site]] = -1;
      deg[site]++;
    }
  }
  for (i = 0; i < N; i++)
    if (deg[i] != C)
      error("nei gradi");
}

void initProb(double beta, double field)
{
  int i;

  i = C;
  while (i >= 0)
  {
    prob[i] = exp(-2. * beta * (i + field));
    i -= 2;
  }
  i = C - 1;
  while (i >= 0)
  {
    prob[i] = exp(-2. * beta * (i + 1 - field));
    i -= 2;
  }
}

int ener(void)
{
  int i, j, prod, res = 0;

  for (i = 0; i < numPosJ; i++)
  {
    prod = 1;
    for (j = 0; j < C; j++)
      prod *= s[graph[C * i + j]];
    res += prod;
  }
  for (; i < N; i++)
  {
    prod = -1;
    for (j = 0; j < C; j++)
      prod *= s[graph[C * i + j]];
    res += prod;
  }
  return -res;
}

void oneMCStep(long long int t, FILE *out, int is)
{
  int i, j, k, ind, prod, sum;

  for (i = 0; i < N; i++)
  {

    sum = 0;
    for (j = 0; j < C; j++)
    {
      prod = J[C * i + j];
      for (k = 0; k < C; k++)
        prod *= s[neigh[i][C * j + k]];
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
  fprintf(out, "%i %i %lli %d\n", mag, ener() - ener0, t, is);
}

int main(int argc, char *argv[])
{
  int i, is, nSamples;
  long long unsigned int t;
  double Tp, T, H;
  char Tp_string[7];
  char mcStoriesFile[80];

  // questa inizializzazione funziona su LINUX
  /*
  FILE *devran = fopen("/dev/random","r");
  //FILE *devran = fopen("/dev/urandom","r"); // lower quality
  fread(&myrand, 4, 1, devran);
  fclose(devran);
    */

  myrand = time(NULL); // mia inizializzazione, che ho Windows
  if (argc != 6)
  {
    fprintf(stderr, "usage: %s <N> <Tp> <T> <nSamples> <h>\n", argv[0]);
    exit(EXIT_FAILURE);
  }
  N = atoi(argv[1]);

  if (isdigit(*argv[2]))
  {
    Tp = atof(argv[2]);
  }
  else if (strcmp(argv[2], "inf") == 0)
  {
    Tp = -1;
  }
  else
  {
    printf("Planting temperature must be a non-negative number or infinite (inf)\n");
    return EXIT_FAILURE;
  }

  strcpy(Tp_string, argv[2]);

  T = atof(argv[3]);
  nSamples = atoi(argv[4]);
  H = atof(argv[5]);
  if (T <= 0.0)
    error("in T");
  if (H < 0.0 || H > 1.0)
    error("in H");

  sprintf(mcStoriesFile,
          "../Data/Archive/QuenchingResults/McStories_N%d_Tp%s_T%f_h%f_S%d.txt",
          N, Tp_string, T, H, nSamples);

  FILE *out = fopen(mcStoriesFile, "w+");

  if (out == NULL)
  {
    printf("Error in the creation of the file %s", mcStoriesFile);
    exit(EXIT_FAILURE);
  }

  printf("#Quenching  C = %i  N = %i  Tp = %s  T = %f  H = %f  seed = %u\n",
         C, N, Tp_string, T, H, myrand);
  initRandom();
  allocateAll();

  if (Tp > 0.0)
    numPosJ = N * 0.5 * (1. + tanh(1. / Tp));
  else if (Tp == 0.0)
    numPosJ = N;
  else
  {
    numPosJ = N / 2;
  }

  initProb(1. / T, H);
  for (is = 0; is < nSamples * nDisorderCopies; is++)
  {
    if (!(is % nDisorderCopies))
    {
      initRRGraph();
    }
    for (i = 0; i < N; i++)
    {
      s[i] = (int)(FRANDOM > 0.5 ? 1 : 0); // different wrt the planted case, where all s[i] are 1
    }
    mag = N;
    ener0 = ener();
    nextMeasMag = mag - 2;
    for (t = 1; t < t_end; t++)
    {
      oneMCStep(t, out, is);
    }
  }

  // Da qui in poi faccio solo una copia dei dati delle simulazioni
  rewind(out);
  char ch;
  FILE *target;
  char target_file[200] = "C:\\Users\\Riccardo\\Desktop\\Codici\\PhD\\diluted_pSpin\\Quenching\\Data\\LastRun\\McStories.txt";

  target = fopen(target_file, "w");
  if (target == NULL)
  {
    fclose(out);
    printf("Press any key to exit...");
    exit(EXIT_FAILURE);
  }
  while ((ch = fgetc(out)) != EOF)
    fputc(ch, target);
  printf("\nMonte Carlo stories file copied successfully.\n");
  fclose(target);
  fclose(out);

  return EXIT_SUCCESS;
}