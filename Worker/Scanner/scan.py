import socket


def port_scan(host, mode):
    """"
    Scan ports of host
    :param host: strign, the host to scan
    :param mode: int, the mode to scan
    """
    mode += 1
    try:
        for port in range(1, 65535):
            sconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sconn.connect_ex((host, port))
            if result == 0:
                # Should index on elasticsearch
                print(f"Port {port} is open")  # Will be deleted
            sconn.close()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
