import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('products')

def lambda_handler(event, context):
    method = event['httpMethod']
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    product_id = path_params.get('id')

    if method == 'OPTIONS':
        return build_response(200, {}, cors=True)

    if method == 'GET':
        if product_id:
            return get_product_by_id(product_id)
        return get_all_products()

    elif method == 'POST':
        body = loads_body(event)
        if not body:
            return build_response(400, {'error': 'Request body is required and seems to be empty'})
        return create_product(body)

    elif method == 'PUT':
        if not product_id:
            return build_response(400, {'error': 'Product ID is required in path'})
        body = loads_body(event)
        if not body:
            return build_response(400, {'error': 'Request body is required and seems to be empty'})
        return update_product(product_id, body)

    elif method == 'DELETE':
        if not product_id:
            return build_response(400, {'error': 'Product ID is required in path'})
        return delete_product(product_id)

    else:
        return build_response(405, {'error': 'Method not allowed'})

def get_all_products():
    response = table.scan()
    return build_response(200, response.get('Items', []))

def get_product_by_id(product_id):
    response = table.get_item(Key={'id': product_id})
    item = response.get('Item')
    if not item:
        return build_response(404, {'error': 'Product not found'})
    return build_response(200, item)

def create_product(data):
    product_id = str(uuid.uuid4())
    data['id'] = product_id
    table.put_item(Item=data)
    return build_response(201, {'message': 'Product created', 'id': product_id})

def update_product(product_id, data):
    data['id'] = product_id
    table.put_item(Item=data)
    return build_response(200, {'message': 'Product updated', 'id': product_id})

def delete_product(product_id):
    table.delete_item(Key={'id': product_id})
    return build_response(200, {'message': 'Product deleted'})

def build_response(status_code, body, cors=False):
    headers = {'Content-Type': 'application/json'}
    if cors:
        headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }

def loads_body(event):
    body = event.get('body')
    if body is None:
        return {}
    if isinstance(body, dict):
        return body
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}
    if isinstance(body, bytes):
        try:
            return json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return {}
