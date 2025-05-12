import logging

from common.utils import build_response, loads_body
from common.logger import config_logger
from common.enums import HttpCodes
from common.exceptions.http_exception import HttpException

config_logger()
logger = logging.getLogger('microservice')

from services import ProductService

service = ProductService()

@HttpException.throw_http_exception_decorator(logger)
def handle(event, context):
    method = event['httpMethod']
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    product_id = path_params.get('id')

    if method == 'OPTIONS':
        return build_response(HttpCodes.OK, {}, cors=True)

    if method == 'GET':
        if product_id:
            return service.get_product_by_id(product_id)
        return service.get_all_products()

    elif method == 'POST':
        body = loads_body(event)
        if not body:
            raise HttpException(
                message='Request body is required and seems to be empty',
                code=HttpCodes.BAD_REQUEST
            )
        return service.create_product(body)

    elif method == 'PUT':
        if not product_id:
            raise HttpException(
                message='Product ID is required in path',
                code=HttpCodes.BAD_REQUEST
            )
        body = loads_body(event)
        if not body:
            raise HttpException(
                message='Request body is required and seems to be empty',
                code=HttpCodes.BAD_REQUEST
            )
        return service.update_product(product_id, body)

    elif method == 'DELETE':
        if not product_id:
            raise HttpException(
                message='Product ID is required in path',
                code=HttpCodes.BAD_REQUEST
            )
        return service.delete_product(product_id)

    else:
        raise HttpException(
            message='Method not allowed',
            code=HttpCodes.METHOD_NOT_ALLOWED
        )


