import smtplib
import email.message
import constants


class Mail:
    def __init__(self, car, value):
        # Constants objects
        self.receiver = constants.receivers
        self.sender = constants.sender
        self.password = constants.password
        self.car = car
        self.value = value

    def send(self):
        email_body = "Carro alugado:       " + str(self.car) + str(self.value)
        msg = email.message.Message()
        msg['Subject'] = "CARRO ALUGADO"
        msg['From'] = self.receiver
        msg['To'] = self.receiver
        password = self.password
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_body)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Success email sent')
