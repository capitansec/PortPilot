import socket

def port_scan(host, mode):
    # Ordinal attributes for scan mode -> 1: first 1024, 2: 65535
    # Scan types(TCP UDP etc.) not implemented yet.

    try:

        for port in range(1, 65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # returns an error indicator
            result = s.connect_ex((host, port))
            if result == 0:

                # Should index on elasticsearch
                print("Port {} is open".format(port))
            s.close()

    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")

