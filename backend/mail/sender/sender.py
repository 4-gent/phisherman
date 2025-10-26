from mailjet_rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['MAILJET_API_KEY']
api_secret = os.environ['MAILJET_SECRET_KEY']

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def email_send(email_html_body, email_subject_line, email_preheader, company):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "marlonrburog@gmail.com",
                    "Name": company
                },
                "To": [
                    {
                        "Email": "marlon.burog@sjsu.edu",
                        "Name": "Marlon Burog"
                    }
                ],
                "Subject": email_subject_line,
                "TextPart": email_preheader,
                "HTMLPart": email_html_body
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)