"""
Network object generators: hosts, networks, ranges
"""

import random
from utils.ip_utils import generate_random_ip, generate_random_subnet


def generate_hosts(hosts_number):
    """Generate host objects with sequential names and random IPs"""
    hosts = []
    for i in range(1, hosts_number + 1):
        host = {
            'name': f'host_{i}',
            'ip': generate_random_ip()
        }
        hosts.append(host)
    return hosts


def generate_networks(networks_number):
    """Generate network objects with sequential names and random subnets"""
    networks = []
    for i in range(1, networks_number + 1):
        network = {
            'name': f'network_{i}',
            'prefix': generate_random_subnet()
        }
        networks.append(network)
    return networks


def generate_ranges(ranges_number):
    """Generate range objects with sequential names and random IP ranges"""
    ranges = []
    for i in range(1, ranges_number + 1):
        # Generate two IPs for the range
        ip1 = generate_random_ip()
        ip2 = generate_random_ip()

        # Ensure proper order (start < end)
        parts1 = [int(x) for x in ip1.split('.')]
        parts2 = [int(x) for x in ip2.split('.')]

        if parts1 > parts2:
            ip1, ip2 = ip2, ip1

        range_obj = {
            'name': f'range_{i}',
            'ip_range': f'{ip1}-{ip2}'
        }
        ranges.append(range_obj)
    return ranges
