import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notificador:
    def init(self):
        self.email_user = "taskmanagerfiap@gmail.com"
        self.email_pass = "qefjfollbqfwugxo"

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
        except Exception as e:
            print(f"Erro: {str(e)}")
        finally:
            server.quit()