from decimal import Decimal
import uuid
import datetime

from common.utils import build_response
from common.enums import HttpCodes
from common.exceptions.http_exception import HttpException

from repositories import OrderRepository
from dtos import CreateOrderDto

class OrderService:

    repository = OrderRepository()

    def get_all_orders(self):
        orders = self.repository.get_all_items()
        return build_response(HttpCodes.OK, orders)

    def get_order_by_id(self, order_id):
        response = self.repository.get_item_by_id(order_id)
        if not response:
            raise HttpException(
                message='Order not found',
                code=HttpCodes.NOT_FOUND
            )
            # return build_response(HttpCodes.NOT_FOUND, {'error': 'Order not found'})
        return build_response(HttpCodes.OK, response)
    
    def _create_order(self, order: CreateOrderDto):
        order_id = str(uuid.uuid4())
        result = self.repository.create_item({
            'id': order_id,
            'userId': order.userId,
            'items': order.items,
            'totalPrice': Decimal(str(order.totalPrice)),
            'createdAt': datetime.datetime.now().isoformat()
        })

        return result
    
    def catch_event_bus_events_and_handle(self, event):
        """
        This function is triggered by events from the EventBridge event bus.
        It handles the events and performs actions based on the event type.
        """
        event_type = event.get('source', '')
        
        # Handle different types of events
        if event_type == 'com.e_commerce.checkout_basket':
            # Handle checkout basket event
            event_detail = event.get('detail', {})
            self._create_order(CreateOrderDto(**event_detail))

        return build_response(
            status_code=200,
            body={
                "message": "Event handled successfully",
                "event": event,
            }
        )

    def catch_sqs_events_and_handle(self, event):
        """
        This function is triggered by events from the SQS queue.
        It handles the events and performs actions based on the event type.
        """
        event_records = event.get('Records')

        for record in event_records:
            record_data = record.get('body', {})
            if not record_data:
                continue
            self._create_order(CreateOrderDto(**record_data))

    def catch_api_events_and_handle(self, event):
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