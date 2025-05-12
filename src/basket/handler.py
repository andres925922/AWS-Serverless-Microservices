import boto3

from common.utils import build_response, loads_body

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('basket')

def handle(event, context):
    method = event['httpMethod']
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    basket_id = path_params.get('id')

    return build_response(
        status_code=200,
        body={
            "message": "Basket handler",
            "method": method,
            "path_params": path_params,
            "query_params": query_params,
            "basket_id": basket_id,
            "body": loads_body(event),
        }
    )