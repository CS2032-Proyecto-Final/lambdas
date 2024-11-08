import boto3
import json
from uuid import uuid4
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('t_books')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        tenant_id = body['tenant_id']
        isbn = body['isbn']
        title = body.get('title')
        author_name = body.get('author_name')
        author_lastname = body.get('author_lastname')
        quantity = body.get('quantity', 1)
        pages = body.get('pages')
        stock = body.get('stock', quantity)

        item = {
            'tenant_id': tenant_id,
            'isbn': isbn,
            'title': title,
            'author_name': author_name,
            'author_lastname': author_lastname,
            'quantity': quantity,
            'pages': pages,
            'stock': stock
        }
        
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Book created successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
