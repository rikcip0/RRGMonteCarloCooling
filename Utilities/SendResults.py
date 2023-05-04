import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


# Aggiunta dell'allegato
FOLDER_PATH = os.path.abspath('..\\Data\\LastRun')

# Parametri per l'invio dell'email
sender = 'riccardo.sender@gmail.com'
receiver = 'cipolloni.1714653@studenti.uniroma1.it'
password = 'jdbhfoxtsogsptql'
object = 'Quenching results!'
body = 'The results for your simulation with inputs\n'

with open(FOLDER_PATH+'\\Results.txt', 'r') as file:
    body+= file.read()

# Creazione del messaggio email
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = object

# Aggiunta del body dell'email
msg.attach(MIMEText(body))


# Ottieni la lista di tutti i file nella cartella
file_list = os.listdir(FOLDER_PATH)
# Filtra la lista di file escludendo quelli con estensione .txt
file_list = [f for f in file_list if not f.endswith('.txt')]

# Aggiungi tutti i file come allegati al messaggio email
for file in file_list:
    file_path = os.path.join(FOLDER_PATH, file)
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

body = 'Inviata email con allegati:\n'
for file in file_list:
    body += (file +'\n')
print(body)
