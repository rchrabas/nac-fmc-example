"""
Service object generators: ports, icmpv4s, port_groups
"""

import random


def generate_ports(ports_number):
    """
    Generate port objects with sequential names and random ports/protocols.
    Mix of single ports and port ranges with TCP, UDP, or ESP protocols.
    """
    ports = []
    protocols = ['TCP', 'UDP', 'ESP']

    for i in range(1, ports_number + 1):
        # Randomly decide if this is a single port or range
        is_range = random.choice([True, False])

        # Select random protocol
        protocol = random.choice(protocols)

        port_obj = {
            'name': f'port_{i}',
            'protocol': protocol
        }

        # ESP typically doesn't have port numbers, so only add port for TCP/UDP
        if protocol in ['TCP', 'UDP']:
            if is_range:
                # Generate port range (e.g., "8000-8010")
                start_port = random.randint(1024, 60000)
                end_port = start_port + random.randint(1, 100)
                if end_port > 65535:
                    end_port = 65535
                port_obj['port'] = f"{start_port}-{end_port}"
            else:
                # Generate single port
                port_obj['port'] = random.randint(1024, 65535)

        ports.append(port_obj)

    return ports


def generate_icmpv4s(icmpv4s_number):
    """
    Generate ICMPv4 objects with sequential names and valid ICMP type/code combinations.
    Uses IANA-compliant ICMP type and code mappings.
    """
    # Valid ICMP type and code combinations based on IANA specifications
    valid_combinations = {
        0: [0],                    # Echo Reply
        3: [0, 1, 2, 3, 4, 5],     # Destination Unreachable
        5: [0, 1, 2, 3],           # Redirect
        8: [0],                    # Echo Request
        11: [0, 1],                # Time Exceeded
        12: [0, 1, 2],             # Parameter Problem
        40: [0, 1, 2, 3, 4, 5]     # Photuris
    }

    icmpv4s = []

    for i in range(1, icmpv4s_number + 1):
        # Select a random valid ICMP type
        icmp_type = random.choice(list(valid_combinations.keys()))

        # Select a valid code for this type
        valid_codes = valid_combinations[icmp_type]
        code = random.choice(valid_codes)

        icmpv4_obj = {
            'name': f'icmpv4_{i}',
            'icmp_type': icmp_type,
            'code': code
        }

        icmpv4s.append(icmpv4_obj)

    return icmpv4s


def generate_port_groups(port_groups_number, available_port_objects):
    """
    Generate port group objects with sequential names and random port/icmpv4 references.
    Each port group contains 2-6 objects from the available port objects list.

    Args:
        port_groups_number: Number of port groups to generate
        available_port_objects: List of object names that can be referenced (ports and icmpv4s only)
    """
    port_groups = []

    for i in range(1, port_groups_number + 1):
        # Determine how many objects this group should have (2-6)
        num_objects = random.randint(2, 6)

        # Select random objects from available port objects
        if len(available_port_objects) < num_objects:
            # If we don't have enough objects, use what we have
            selected_objects = available_port_objects.copy()
        else:
            selected_objects = random.sample(available_port_objects, num_objects)

        port_group = {
            'name': f'port_group_{i}',
            'objects': selected_objects
        }
        port_groups.append(port_group)

    return port_groups
