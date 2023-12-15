import socket
from Config.ElasticContext import ElasticsearchContext


def index_port(ip_address, ports):
    document = {
        "ip": str(ip_address),
        "ports": ports
    }
    with ElasticsearchContext() as es:
        es.index(body=document, index=str(ip_address), headers={'Content-Type': 'application/json'})
    print(ports, "indexed successfully")


def port_scan(host, mode):
    """"
    Scan ports of host
    :param host: strign, the host to scan
    :param mode: int, the mode to scan
    """
    mode += 1
    try:
        ports = []
        for port in range(1, 65535):
            sconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sconn.connect_ex((host, port))
            if result == 0:
                ports.append(port)
                print(f"Port {port} is open")  # Will be deleted
            sconn.close()
        index_port(host, ports)
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
