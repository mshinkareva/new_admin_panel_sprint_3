import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import backoff

from settings import es_settings


class ESWorker:
    def __init__(self):
        self.connect = Elasticsearch(es_settings.__str__())

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def create_index(self, index_name: str, schema_path: str) -> None:
        if not self.connect.indices.exists(index=index_name):
            with open(schema_path, 'r') as json_data:
                schema = json.load(json_data)
                self.connect.indices.create(index=index_name, body=schema)

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def load(self, index_name, data):
        actions = [
            {"_index": index_name, "_source": row, '_id': row['id']} for row in data
        ]
        bulk(self.connect, actions)
