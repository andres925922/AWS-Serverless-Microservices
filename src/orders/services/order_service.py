from decimal import Decimal
import uuid
import datetime

from common.utils import build_response
from common.enums import HttpCodes
from common.exceptions.http_exception import HttpException

from repositories import OrderRepository

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
    
    def _create_order(self, event:dict):
        event_detail = event.get('detail', {})
        order_id = str(uuid.uuid4())
        user_id = event_detail.get('userId')
        items = event_detail.get('items', [])
        total_price = event_detail.get('totalPrice')

        result = self.repository.create_item({
            'id': order_id,
            'userId': user_id,
            'items': items,
            'totalPrice': Decimal(str(total_price)),
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
            self._create_order(event)

        return build_response(
            status_code=200,
            body={
                "message": "Event handled successfully",
                "event": event,
            }
        )