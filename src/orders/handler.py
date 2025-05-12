import logging

from common.utils import build_response
from common.logger import config_logger
from common.enums import HttpCodes
from common.exceptions.http_exception import  HttpException

from services import OrderService

config_logger()
logger = logging.getLogger('microservice')

orders_service = OrderService()

@HttpException.throw_http_exception_decorator(logger)
def handle(event: dict, context):

    if event.get('detail-type', None) == 'checkout_basket':
        return orders_service.catch_event_bus_events_and_handle(event)

    method = event['httpMethod']
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    basket_id = path_params.get('id')
    order_id = query_params.get('orderId', None)
    if not order_id:
        raise HttpException(
            message='orderId is required',
            code=HttpCodes.BAD_REQUEST
        )

    method = event['httpMethod']
    path_params = event.get('pathParameters') or {}
    query_params = event.get('queryStringParameters') or {}
    product_id = path_params.get('id')

    if method == 'OPTIONS':
        return build_response(HttpCodes.OK, {}, cors=True)

    if method == 'GET':
        if basket_id:
            return orders_service.get_order_by_id(product_id)
        return orders_service.get_all_orders()

    else:
        raise HttpException(
            message='Method not allowed',
            code=HttpCodes.METHOD_NOT_ALLOWED
        )