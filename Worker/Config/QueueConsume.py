from Scanner.scan import port_scan


class RabbitMQCallbacks:
    @staticmethod
    def process_message(ch, method, properties, body):
        """
        Callback function to process received messages
        """
        print(f"{body.decode()} is scanning")
        port_scan(body, mode=1)

