from Scanner.scan import port_scan


class RabbitMQCallbacks:
    @staticmethod
    def process_message(ch, method, properties, body):
        """
        Callback function to process received messages
        """
        port_scan(body, mode=1)
        print(f"{body} is scanning")
