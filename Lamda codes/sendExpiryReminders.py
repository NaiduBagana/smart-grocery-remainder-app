import boto3
import json
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
table = dynamodb.Table('GroceryItems')

def lambda_handler(event, context):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    response = table.scan()
    items = response.get('Items', [])

    reminders_sent = 0

    for item in items:
        expiry = item.get('expiryDate')
        email = item.get('userEmail')
        itemName = item.get('itemName')

        if expiry:
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
            if expiry_date == tomorrow:
                # Send email
                ses.send_email(
                    Source='chaitanyabagana143@gmail.com',
                    Destination={'ToAddresses': [email]},
                    Message={
                        'Subject': {'Data': f'Expiry Reminder: {itemName} expires tomorrow!'},
                        'Body': {
                            'Text': {
                                'Data': f'Hi,\n\nThis is a reminder that your item "{itemName}" is expiring on {expiry_date}.\n\n— Smart Grocery Reminder App'
                            }
                        }
                    }
                )
                reminders_sent += 1

    return {
        'statusCode': 200,
        'body': json.dumps(f"{reminders_sent} reminder(s) sent.")
    }
