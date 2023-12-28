import psutil
import socket

def get_ipv4_address():
    interfaces = psutil.net_if_addrs()
    for interface_name, addresses in interfaces.items():
        for address in addresses:
            if address.family == socket.AF_INET and address.address.startswith('192.168.227'):
                return address.address
if __name__=="__main__":
    ipv4_address = get_ipv4_address()
    print(type(ipv4_address))

