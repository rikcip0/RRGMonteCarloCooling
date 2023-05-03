import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


# Aggiunta dell'allegato
FOLDER_PATH = 'C:\\Users\\Riccardo\\Desktop\\Codici\\PhD\\diluted_pSpin\\Quenching\\Data\\LastRun'

# Parametri per l'invio dell'email
mittente = 'riccardo.cipolloni@gmail.com'
destinatario = 'riccardo.cipolloni@gmail.com'
password = 'draeuqsahbvwdgrf'
oggetto = 'Quenching results!'
testo = 'The results for your quenching simulation with parameters'
testo += '100\n\n'

with open(FOLDER_PATH+'\\Results.txt', 'r') as file:
    testo+= file.read()

# Creazione del messaggio email
msg = MIMEMultipart()
msg['From'] = mittente
msg['To'] = destinatario
msg['Subject'] = oggetto

# Aggiunta del testo dell'email
msg.attach(MIMEText(testo))


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
    server.login(mittente, password)
    server.sendmail(mittente, destinatario, msg.as_string())
    server.quit()

print('\nEmail inviata con successo!\n')
