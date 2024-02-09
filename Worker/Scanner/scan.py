import socket
from datetime import datetime

from Config.ElasticContext import ElasticsearchContext


def index_ports(ip_address, ports):
    """
    :param ip_address: string, ip address to index
    :param ports: array, list of ports to index
    """
    for port in ports:
        document = {
            "ip": str(ip_address.decode()),
            "port": port,
            "state": "open",
            "@timestamp": datetime.utcnow().isoformat()
        }
        with ElasticsearchContext() as es:
            es.index(body=document, index="port-scan", headers={'Content-Type': 'application/json'})


def port_scan(host, mode):
    """"
    Scan ports of host
    :param host: string, the host to scan
    :param mode: int, the mode to scan
    """
    mode += 1
    try:
        open_ports = []
        for port in range(1, 65535):
            sconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sconn.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port} is open")

            else:
                print(f"port is closed")
            sconn.close()

        index_ports(host, open_ports)

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
