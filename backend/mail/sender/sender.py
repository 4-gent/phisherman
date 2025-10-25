from mailjet_rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['MAILJET_API_KEY']
api_secret = os.environ['MAILJET_SECRET_KEY']

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def email_send():
    print('made it to email send')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "marlonrburog@gmail.com",
                    "Name": "Mailjet API"
                },
                "To": [
                    {
                        "Email": "marlon.burog@sjsu.edu",
                        "Name": "Marlon Burog"
                    }
                ],
                "Subject": "First email send - mailjet",
                "TextPart": "Test",
                "HTMLPart":"<h3>Testing, including link <a>https://google.com</a></h3>"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print("Email result: ", result.json())