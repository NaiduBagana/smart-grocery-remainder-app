import json
import boto3

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')  # Add SES client
table = dynamodb.Table('GroceryItems')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        itemName = body['itemName']
        expiryDate = body['expiryDate']
        email = body['email']

        # Save item to DynamoDB
        table.put_item(
            Item={
                'userEmail': email,
                'itemName': itemName,
                'expiryDate': expiryDate
            }
        )

        # Send email using Amazon SES
        response = ses.send_email(
            Source='chaitanyabagana143@gmail.com',  # Relace with your verified SES email
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': f'Reminder: {itemName} expires on {expiryDate}'
                },
                'Body': {
                    'Text': {
                        'Data': f'Hello,\n\nYou added "{itemName}" to your grocery list, which expires on {expiryDate}.\n\n- Smart Grocery Reminder App'
                    }
                }
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps("Item saved and email sent successfully!")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
