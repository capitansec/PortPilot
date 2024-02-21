from Scanner.scan import port_scan
import json


class RabbitMQCallbacks:
    @staticmethod
    def process_message(ch, method, properties, body):
        """
        Callback function to process received messages
        :param body: Received message as bytes
        """


        print("Received message:", (body.decode('utf-8')))



