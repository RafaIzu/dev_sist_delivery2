import os
from twilio.rest import Client

class Sms:
    def __credencials(self):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        return client


    def send_sms(self, msg, tel):
        tel = "+55" + tel
        client = self.__credencials()
        print(">>> I recived this: ", tel)
        client.messages.create(from_=os.environ['TWILIO_PHONE_NUMBER'],
                               to=tel, body=msg)

