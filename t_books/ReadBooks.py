import boto3
import os
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Extraer los parámetros directamente de 'query'
    tenant_id = event['query']['tenant_id']
    page = int(event['query']['page'])

    limit = 10  # Número de resultados por página
    nombre_tabla = os.environ["TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)

    # Configurar la clave de inicio para paginación, si corresponde
    start_key = None
    if page > 1 and 'lastEvaluatedKey' in event['query']:
        start_key = {
            'tenant_id': tenant_id,
            'isbn': event['query']['lastEvaluatedKey']
        }
    
    # Realizar la consulta en DynamoDB
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id),
        Limit=limit,
        ExclusiveStartKey=start_key
    )

    books = response['Items']
    last_evaluated_key = response.get('LastEvaluatedKey', None)

    # Retornar la lista de libros y la clave de paginación
    return {
        'statusCode': 200,
        'body': json.dumps({
            'books': books,
            'lastEvaluatedKey': last_evaluated_key
        })
    }
