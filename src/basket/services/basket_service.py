from decimal import Decimal

from common.utils import build_response
from common.enums import HttpCodes
from common.exceptions.http_exception import HttpException

from repositories import BasketRepository

class BasketService:

    repository = BasketRepository()

    def get_all_basket(self):
        baskets = self.repository.get_all_items()
        return build_response(HttpCodes.OK, baskets)

    def get_basket_by_id(self, user_id):
        response = self.repository.get_item_by_id(user_id)
        if not response:
            raise HttpException(
                message='Basket not found',
                code=HttpCodes.NOT_FOUND
            )
        return build_response(HttpCodes.OK, response)

    def create_basket(self, data):
        basket_id = data.get('user_id')
        response = self.repository.create_item(data, key="basket_id", id_=basket_id)
        return build_response(HttpCodes.CREATED, {'message': 'Basket created', 'id': response['id']})

    def update_basket(self, user_id, data):
        data['user_id'] = user_id
        response = self.repository.update_item(data['user_id'], data, key="basket_id")
        return build_response(HttpCodes.OK, {'message': 'Product updated', 'id': data['user_id']})

    def delete_basket(self, user_id):
        self.repository.delete_item(user_id, key='basket_id')
        return build_response(HttpCodes.OK, {'message': 'Product deleted'})