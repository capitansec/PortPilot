import os

import pika


class RabbitMQPublisher:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST")
        self.port = os.getenv("RABBITMQ_PORT")
        self.username = os.getenv("RABBITMQ_USERNAME")
        self.password = os.getenv("RABBITMQ_PASSWORD")
        self.exchange_name = ''
        self.routing_key = os.getenv("RABBITMQ_QUEUE_NAME")

    def __enter__(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def publish_message(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent | 1 for transient
            )
        )
