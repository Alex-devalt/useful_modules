import locale
import platform
import socket
from subprocess import Popen, PIPE
from ipaddress import ip_address
from tabulate import tabulate

ENCODING = locale.getpreferredencoding()


def host_range_ping_tab(start_ip_address: str, number_of_ip_addresses: int) -> None:
    max_range = 256 - int(start_ip_address.split('.')[-1])
    number_of_ip_addresses = min(max_range, number_of_ip_addresses)

    ip_addresses_list = [str(ip_address(start_ip_address) + i) for i in range(number_of_ip_addresses)]
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args_list = [['ping', param, '5', ip_addr] for ip_addr in ip_addresses_list]
    processes = [Popen(args, stdout=PIPE, stderr=PIPE) for args in args_list]

    ip_list = [('ip address', 'availability')]

    for p in processes:
        code = p.wait()
        if code == 0:
            ip_list.append((p.args[-1], 'available'))
        else:
            ip_list.append((p.args[-1], 'not available'))

    print(tabulate(ip_list, headers='firstrow', tablefmt='grid'))


if __name__ == '__main__':
    my_local_ip = socket.gethostbyname(socket.gethostname())
    NUMBER_OF_IP_ADDRESSES = 10
    host_range_ping_tab(my_local_ip, NUMBER_OF_IP_ADDRESSES)
