import json
from decimal import Decimal

# Custom JSON encoder to handle Decimal objects
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return float(o)
        return super(CustomEncoder, self).default(o)

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
        'body': json.dumps(body, cls=CustomEncoder)
    }

def loads_body(event: dict) -> dict:
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