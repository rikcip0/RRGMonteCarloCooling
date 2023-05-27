import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


# Aggiunta dell'allegato
FOLDER_PATH = os.path.abspath('..\\Data\\ThisRun')

# Parametri per l'invio dell'email
sender = 'riccardo.sender@gmail.com'
receiver = 'cipolloni.1714653@studenti.uniroma1.it'
password = 'jdbhfoxtsogsptql'
object = 'Results for '
body = ""

with open(os.path.join(FOLDER_PATH, "Info.txt"), 'r') as file:
    body+= file.read()


# Trova l'indice del carattere '#'
hashPosition = body.find("#")

# Verifica se il carattere '#' è presente nel file
if hashPosition!= -1:
    # Trova l'indice del primo spazio dopo il carattere '#'
    nextSpacePosition = body.find(" ", hashPosition)

    # Estrai la parola successiva al carattere '#'
    symType = body[hashPosition + 1:nextSpacePosition]
else:
    print("No simulation type specified by '#' has been found.")

object += (symType + "!")

# Creazione del messaggio email
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = object

# Aggiunta del body dell'email
msg.attach(MIMEText(body))


# Ottieni la lista di tutti i file nella cartella
file_list = os.listdir(os.path.join(FOLDER_PATH, "Plots"))
# Filtra la lista di file escludendo quelli con estensione .txt
file_list = [f for f in file_list if not f.endswith('.txt')]

# Aggiungi tutti i file come allegati al messaggio email
for file in file_list:
    file_path = os.path.join(FOLDER_PATH, "Plots", file)
    attachment = MIMEBase('application', "octet-stream")
    attachment.set_payload(open(file_path, "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(attachment)

# Connessione al server SMTP e invio dell'email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

body = 'Sent an email with attachments:\n'
for file in file_list:
    body += (file +'\n')
print(body)
