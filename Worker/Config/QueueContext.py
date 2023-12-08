import os

import pika
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConnector:
    """
    Base class for RabbitMQ
    """

    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST")
        self.port = int(os.getenv("RABBITMQ_PORT"))
        self.username = os.getenv("RABBITMQ_USERNAME")
        self.password = os.getenv("RABBITMQ_PASSWORD")
        self.queue_name = os.getenv("RABBITMQ_QUEUE_NAME")

    def init_conn_params(self):
        """
        Connection parameters builder
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host,
                                               port=self.port,
                                               credentials=credentials)
        return parameters

    def connect(self):
        """
        Establish RabbitMQ connection
        """
        connection = pika.BlockingConnection(self.init_conn_params())
        return connection


class RabbitMQContext:
    """
    Context Manager for RabbitMQ connection
    """

    def __init__(self):
        self.rabbit_connector = RabbitMQConnector()
        self.connection = None

    def __enter__(self):
        """
        Open RabbitMQ connection at the start of the 'with' block
        :return: RabbitMQ connection and channel
        """
        self.connection = self.rabbit_connector.connect()
        self.channel = self.connection.channel()
        return self.connection, self.channel

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close RabbitMQ connection at the end of the 'with' block.
        :param exc_type: any
        :param exc_value: any
        :param traceback: any
        :return:
        """
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    # def send_message(self, queue_name, message):
    #     """
    #     Send a message to the specified queue in RabbitMQ
    #     :param queue_name: Name of the RabbitMQ queue
    #     :param message: The message to be sent
    #     """
    #     with self as (connection, channel):
    #         channel.queue_declare(queue=queue_name)
    #         channel.basic_publish(exchange='', routing_key=queue_name, body=message)
