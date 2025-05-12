from decimal import Decimal

from common.utils import build_response
from common.enums import HttpCodes

from repositories import ProductRepository

class ProductService:

    repository = ProductRepository()

    def get_all_products(self):
        products = self.repository.get_all_items()
        return build_response(HttpCodes.OK, products)

    def get_product_by_id(self, product_id):
        response = self.repository.get_item_by_id(product_id)
        if not response:
            return build_response(404, {'error': 'Product not found'})
        return build_response(HttpCodes.OK, response)

    def create_product(self, data):
        data['price'] = Decimal(str(data.get('price',0)))
        data['description'] = data.get('description', '')
        response = self.repository.create_item(data)
        return build_response(HttpCodes.CREATED, {'message': 'Product created', 'id': response['id']})

    def update_product(self, product_id, data):
        data['id'] = product_id
        response = self.repository.update_item(product_id, data)
        return build_response(HttpCodes.OK, {'message': 'Product updated', 'id': product_id})

    def delete_product(self, product_id):
        self.repository.delete_item(Key={'id': product_id})
        return build_response(HttpCodes.OK, {'message': 'Product deleted'})