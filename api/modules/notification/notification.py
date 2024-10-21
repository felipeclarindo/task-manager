import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Notificador:
    def __init__(self):
        self.email_user = os.getenv("EMAIL")
        self.email_pass = os.getenv("EMAIL_PASSWORD")

    def send_email(self, to_email: str, subject: str, message_body: str) -> None:
        try:
            # Criação da mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject

            # Adicionando o corpo da mensagem
            msg.attach(MIMEText(message_body, 'plain', 'utf-8'))

            # Configuração do servidor SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls() 
            server.login(self.email_user, self.email_pass) 
            server.sendmail(msg['From'], to_email, msg.as_string())

            print("Email enviado com sucesso!")
            server.quit()
        except Exception as e:
            print(f"Erro: {str(e)}")