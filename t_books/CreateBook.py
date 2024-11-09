import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('t_books')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    item = {
        'tenant_id': data['tenant_id'],
        'isbn': data['isbn'],
        'title': data['title'],
        'author_name': data['author_name'],
        'author_lastname': data['author_lastname'],
        'quantity': data['quantity'],
        'pages': data['pages'],
        'stock': data['stock']
    }
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Book created successfully'})
    }
