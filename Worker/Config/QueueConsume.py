from Scanner.scan import port_scan, index_ports
import json


class RabbitMQCallbacks:
    @staticmethod
    def process_message(ch, method, properties, body):
        """
        Callback function to process received messages
        :param body: Received message as bytes
        """
        message_dump = json.loads(body.decode('utf-8'))
        target = message_dump['target']
        scan_id = message_dump['scan_id']
        scan_name = message_dump['scan_name']
        scan_owner = message_dump['scan_owner']

        open_ports = port_scan(target)
        index_ports(target, open_ports, scan_id, scan_name, scan_owner)





