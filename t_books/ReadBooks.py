import boto3
import os
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Verificar que queryStringParameters exista y contenga los parámetros necesarios
    query_params = event.get('queryStringParameters') or {}
    tenant_id = query_params.get('tenant_id')
    page = int(query_params.get('page', 1))
    
    if not tenant_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id is required'})
        }

    limit = 10  # Número de resultados por página
    nombre_tabla = os.environ["TABLE_NAME"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)

    # Preparar la clave de inicio para paginación
    start_key = None
    if page > 1 and query_params.get('lastEvaluatedKey'):
        start_key = {
            'tenant_id': tenant_id,
            'isbn': query_params['lastEvaluatedKey']
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
