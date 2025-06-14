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

    if event.get('Records', None):
        return orders_service.catch_sqs_events_and_handle(event)            # Handle SQS event

    if event.get('detail-type', None) == 'checkout_basket':
        return orders_service.catch_event_bus_events_and_handle(event)      # Handle EventBridge event

    return orders_service.catch_api_events_and_handle(event)                # Handle API event
