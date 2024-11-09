import boto3
import os
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Verificar que queryStringParameters exista y contenga los parámetros necesarios
    tenant_id = event.get('queryStringParameters', {}).get('tenant_id')
    page = int(event.get('queryStringParameters', {}).get('page', 1))
    
    if not tenant_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id is required'})
        }

    limit = 10  # Número de resultados por página
    nombre_tabla = os.environ["TABLE_NAME"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)

    start_key = None
    if page > 1 and event['queryStringParameters'].get('lastEvaluatedKey'):
        start_key = {
            'tenant_id': tenant_id,
            'isbn': event['queryStringParameters']['lastEvaluatedKey']
        }
    
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id),
        Limit=limit,
        ExclusiveStartKey=start_key
    )

    books = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey', None)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'books': books,
            'lastEvaluatedKey': last_evaluated_key
        })
    }
