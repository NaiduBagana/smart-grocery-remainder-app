import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GroceryItems') 

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
