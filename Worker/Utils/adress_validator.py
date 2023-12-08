import ipaddress


def validate_address(address):
    """
    Validate an ip address or subnet
    :param address: string, ip or subnet
    :return: boolean, True if valid, False otherwise
    """
    try:
        ipaddress.ip_network(address, strict=False)
        return True
    except ValueError:
        return False
