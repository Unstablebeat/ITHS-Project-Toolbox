"""
Importing python-nmap to use for scanning ports
"""
import nmap

def _scan_os(ip_list, save_settings):
    addresses = []
    options = "-O"

    save_file = save_settings

    for ip in ip_list:
        addresses.append(ip)

    if not addresses:
        ip = input("Enter an IP-Address to scan: ")
        addresses.append(ip)

    for host in addresses:
        nm = nmap.PortScanner()
        nm.scan(host, arguments=options)
        for host in nm.all_hosts():
            line = '----------------------------------'
            host_result = f"Host: {host}"
            state_result = f"State: {nm[host].state()}"
            os_result = f"OS: {nm[host]['osmatch'][0]['name']} Accuracy: {nm[host]['osmatch'][0]['accuracy']}"
            print(line + "\n" + host_result + "\n" + state_result + "\n" + os_result + "\n")
            if save_file:
                with open(save_file, 'a', encoding='UTF-8') as file:
                    file.write(line + "\n")
                    file.write(host_result + "\n")
                    file.write(state_result + "\n")
                    file.write(os_result + "\n")
    if save_file:
        print('----------------------------------')
        print(f"Result saved as: {save_file}")


def _scan(ip_list, save_settings, *args):
    addresses = []
    options = "-p 1-1000"

    save_file = save_settings

    if args:
        options = args[0]

    for ip in ip_list:
        addresses.append(ip)

    if not addresses:
        ip = input("Enter an IP-Address to scan: ")
        addresses.append(ip)

    for host in addresses:
        nm = nmap.PortScanner()
        nm.scan(host, arguments=options)

        for host in nm.all_hosts():
            line = '----------------------------------'
            host_result = f"Host: {host}"
            state_result = f"State: {nm[host].state()}"
            print(line + "\n" + host_result + "\n" + state_result)
            if save_file:
                with open(save_file, 'a', encoding='UTF-8') as file:
                    file.write(line + "\n")
                    file.write(host_result + "\n")
                    file.write(state_result + "\n")

            for proto in nm[host].all_protocols():
                proto_result = f"Protocol: {proto}"
                print(proto_result)
                if save_file:
                    with open(save_file, 'a', encoding='UTF-8') as file:
                        file.write(proto_result + "\n")
                ports = nm[host][proto].keys()
                for port in ports:
                    port_result = f"Port: {port}, State: {nm[host][proto][port]['state']}, Service: {nm[host][proto][port]['name']}"
                    print(port_result)
                    if save_file:
                        with open(save_file, 'a', encoding='UTF-8') as file:
                            file.write(port_result + "\n")
    if save_file:
        print('----------------------------------')
        print(f"Result saved as: {save_file}")
