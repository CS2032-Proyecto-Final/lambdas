import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('t_books')

def lambda_handler(event, context):
    try:
        tenant_id = event['queryStringParameters']['tenant_id']
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id)
        )
        books = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'body': json.dumps(books)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
