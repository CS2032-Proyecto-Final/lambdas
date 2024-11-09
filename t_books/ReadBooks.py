import boto3
import os
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    tenant_id = event['queryStringParameters']['tenant_id']
    page = int(event['queryStringParameters'].get('page', 1))
    limit = 10  # Número de resultados por página
    
    # Obtener el nombre de la tabla desde la variable de entorno
    nombre_tabla = os.environ["TABLE_NAME"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)

    # Usar lastEvaluatedKey si se proporciona y no es la primera página
    start_key = None
    if page > 1 and 'lastEvaluatedKey' in event['queryStringParameters']:
        start_key = {
            'tenant_id': tenant_id,
            'isbn': event['queryStringParameters']['lastEvaluatedKey']
        }
    
    # Consulta con paginación
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
