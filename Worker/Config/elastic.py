import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class ElasticsearchConnector:
    """
    Base class for Elasticsearch
    """

    def __init__(self):
        """
        Assign environment variables
        """
        self.host = os.getenv("ELASTICSEARCH_HOST")
        self.port = int(os.getenv("ELASTICSEARCH_PORT"))
        self.scheme = os.getenv("ELASTICSEARCH_SCHEME", "http")
        self.username = os.getenv("ELASTICSEARCH_USERNAME")
        self.password = os.getenv("ELASTICSEARCH_PASSWORD")

    def init_conn_str(self):
        """
        Connection string builder
        """
        if self.username and self.password:
            return f"{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.scheme}://{self.host}:{self.port}"

    def connect(self):
        """
        Establish Elasticsearch connection
        """
        return Elasticsearch([self.init_conn_str()])


class ElasticsearchContext:
    """
    Context Manager for ElasticSearch connection
    """

    def __enter__(self):
        """
        Open Elasticsearch connection at the start of the 'with' block
        :return: Elasticsearch connection
        """
        es_connector = ElasticsearchConnector()
        self.es_client = es_connector.connect()
        return self.es_client

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close Elasticsearch connection at the end of the 'with' block.
        :param exc_type: any
        :param exc_value: any
        :param traceback: any
        :return:
        """
        if self.es_client:
            self.es_client.close()
