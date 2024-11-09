import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('t_books')

def lambda_handler(event, context):
    tenant_id = event['queryStringParameters']['tenant_id']
    page = int(event['queryStringParameters'].get('page', 1))
    limit = 10  # Número de resultados por página

    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id),
        Limit=limit,
        ExclusiveStartKey={'tenant_id': tenant_id, 'isbn': response['LastEvaluatedKey']['isbn']} if page > 1 else None
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
