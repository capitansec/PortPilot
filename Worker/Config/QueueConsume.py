class RabbitMQCallbacks:
    @staticmethod
    def process_message(body):
        """
        Callback function to process received messages
        """
        print(f"Received message: {body}")
