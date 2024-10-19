import smtplib
import os

class Notificador:

    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')  
        self.smtp_port = os.getenv('SMTP_PORT', 587)
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')

    def send_email(self, to_email: str, subject: str, message_body: str) -> dict:
        try:
            text = f"Subject: {subject}\n\n{message_body}"

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Segurança

                # Login no servidor SMTP
                server.login(self.email, self.password)

                # Envio do e-mail
                server.sendmail(self.email, to_email, text)

            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro: {str(e)}")

