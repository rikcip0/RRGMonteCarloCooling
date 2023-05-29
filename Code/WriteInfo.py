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
content = f"{typeOfInfo} performed by machine: {machine_id}\nStarted at: {current_date}\nUsing git commit: {git_commit}\n"



if typeOfInfo=="Simulation":
    nStories = sys.argv[2]
    if len(sys.argv) > 1:
        content+= f'\nprojectedStories = {nStories}\n'


# Scrivi il contenuto nel file
with open("..\Data\ThisRun\Info.txt", "w" if typeOfInfo=="Simulation" else "a") as file:
    file.write(content)


