import socket
from datetime import datetime

from Config.ElasticContext import ElasticsearchContext


def index_ports(ip_address, ports, scan_id, scan_name, scan_owner):
    """
    :param ip_address: string, ip address to index
    :param ports: array, list of ports to index
    """
    document = {
        "scan_id": scan_id,
        "scan_name": scan_name,
        "scan_owner": scan_owner,
        "hosts": [
            {
                str(ip_address): ports
            }
        ],
        "@timestamp": datetime.utcnow().isoformat()
    }

    with ElasticsearchContext() as es:
        es.index(body=document, index="port-scan", headers={'Content-Type': 'application/json'})


def port_scan(host):
    """"
    Scan ports of host
    :param host: string, the host to scan
    """
    open_ports = []
    try:
        for port in range(1, 65535):
            sconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sconn.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port} is open")
            else:
                sconn.close()

        return open_ports

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
