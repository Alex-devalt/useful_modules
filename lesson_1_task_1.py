import locale
import platform
from subprocess import Popen, PIPE
from ipaddress import ip_address

ENCODING = locale.getpreferredencoding()


def host_range_ping_tab(ip_addresses: list) -> None:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args_list = [['ping', param, '4', ip_addr] for ip_addr in ip_addresses]
    processes = [Popen(args, stdout=PIPE, stderr=PIPE) for args in args_list]

    for p in processes:
        code = p.wait()
        if code == 0:
            print(p.args[-1], ' available')
        else:
            print(p.args[-1], ' not available')


if __name__ == '__main__':
    NUMBER_OF_IP_ADDRESSES = 10
    ip_addresses_list = [str(ip_address('8.8.8.8') + i) for i in range(NUMBER_OF_IP_ADDRESSES)]
    host_range_ping_tab(ip_addresses_list)
