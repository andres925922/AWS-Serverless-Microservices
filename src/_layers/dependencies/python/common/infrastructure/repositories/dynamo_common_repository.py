

import boto3
from mypy_boto3_dynamodb.service_resource import Table
import uuid
import datetime
import typing

sortKey = typing.TypeVar('sortKey', bound=typing.Dict[str, str])

class DynamoCommonRepository:

    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table: Table = self.dynamodb.Table(table_name)

    def get_all_items(self):
        response = self.table.scan()
        return response.get('Items', [])

    def get_item_by_id(
            self, 
            item_id, *, 
            key: str = 'id', 
            sort_key: sortKey = None):
        if sort_key:
            response = self.table.get_item(Key={key: item_id, 'sortKey': sort_key})
        else:
            response = self.table.get_item(Key={key: item_id})
        return response.get('Item')

    def create_item(self, data: dict, *, key: str = 'id', id_: str = None):
        if id_:
            item_id = id_
        else:
            item_id = str(uuid.uuid4())
        data[key] = item_id
        data['created_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.table.put_item(Item=data)
        return data

    def update_item(self, item_id, data, *, key: str = 'id'):
        data['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in data.keys())
        expression_attribute_values = {f":{k}": v for k, v in data.items()}
        self.table.update_item(
            Key={key: item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return self.get_item_by_id(item_id)

    def delete_item(self, item_id, *, key: str = 'id'):
        self.table.delete_item(Key={key: item_id})