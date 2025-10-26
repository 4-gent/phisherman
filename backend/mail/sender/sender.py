from mailjet_rest import Client
import os
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from connect import db

load_dotenv()

api_key = os.environ.get('MAILJET_API_KEY')
api_secret = os.environ.get('MAILJET_SECRET_KEY')

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def email_send(email_html_body, email_subject_line, email_preheader, company):
    """
    Sends an email campaign via Mailjet using their built-in open/click tracking.
    Recipients are automatically pulled from the 'users' collection by company.
    """

    users_col = db.get_collection('users')
    campaigns_col = db.get_collection('campaigns')

    # Fetch all users from the same company
    recipients = []
    try:
        cursor = users_col.find({'company': company})
        for u in cursor:
            email = u.get('email')
            name = u.get('username') or ''
            if email:
                recipients.append({'Email': email, 'Name': name})
    except Exception as e:
        print(f"Error fetching users for company '{company}':", e)

    if not recipients:
        print(f"No recipients found for company '{company}'")
        return {'success': False, 'message': f'No users found for {company}'}

    # Create a campaign record
    campaign_id = str(ObjectId())
    sent_at = datetime.now()

    campaign_doc = {
        '_id': campaign_id,
        'company': company,
        'subject': email_subject_line,
        'preheader': email_preheader,
        'created_at': sent_at,
        'sent_count': len(recipients),
        'opens': 0,
        'clicks': 0,
        'recipients': recipients,
        'mailjet_tracking': True
    }
    campaigns_col.insert_one(campaign_doc)

    # Send via Mailjet
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "marlonrburog@gmail.com",
                    "Name": company or "Phisherman"
                },
                "To": recipients,
                "Subject": email_subject_line,
                "TextPart": email_preheader,
                "HTMLPart": email_html_body,
                "TrackOpens": "enabled",
                "TrackClicks": "enabled",
                "CustomCampaign": campaign_id  # helps identify this batch later
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        print("Mailjet send result:", result.status_code)
        print(result.json())

        # Save Mailjet Message IDs for later tracking
        mailjet_data = result.json()
        if mailjet_data and 'Messages' in mailjet_data:
            for msg in mailjet_data['Messages']:
                campaigns_col.update_one(
                    {'_id': campaign_id},
                    {'$set': {'mailjet_data': msg}}
                )

        return {'campaign_id': campaign_id, 'result': result.json()}
    except Exception as e:
        print("Error sending campaign via Mailjet:", e)
        return {'success': False, 'message': str(e)}
