import subprocess
import datetime
import socket
import sys

def get_git_commit():
    try:
        # Esegue il comando git per ottenere il codice identificativo dell'ultimo commit
        output = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
        git_hash = output.strip().decode('utf-8')
        return git_hash
    except (subprocess.CalledProcessError, OSError):
        # Gestisce eventuali errori in caso di fallimento del comando git
        return None

git_commit = get_git_commit()
current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
machine_id = socket.gethostname()


typeOfInfo = sys.argv[1]

# Crea il contenuto da scrivere nel file
content = f"{typeOfInfo} performed by machine: {machine_id}\nStarted at: {current_date}\nUsing git commit: {git_commit}\n\n"



if typeOfInfo=="Simulation":
    C=3
    p=3
    typeOfSimulation = sys.argv[3]
    print(typeOfSimulation)
    if typeOfSimulation == "anneal":
        simulation = "Annealing"
    if typeOfSimulation == "quench":
        simulation = "Quenching"
    nSamples = sys.argv[2]
    N = sys.argv[4]
    Tp = sys.argv[5]
    T = sys.argv[6]
    H = sys.argv[7]
    n_int = int(N) *C//int(p)
    c_eff = n_int*int(p)/int(N)
    content+= f'#{simulation} C = {C} p = {p}  N = {N}  Tp = {Tp}  T = {T}  H = {H}\nn_int = {n_int} c_eff = {c_eff} samples = {nSamples}\n'


# Scrivi il contenuto nel file
with open("..\Data\Epics\ThisRun\Info.txt", "w" if typeOfInfo=="Simulation" else "a") as file:
    file.write(content)


