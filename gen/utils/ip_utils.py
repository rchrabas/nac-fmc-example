"""
IP address and subnet generation utilities
"""

import random


def generate_random_ip():
    """Generate a random private IP address from 10.0.0.0/8"""
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_random_subnet():
    """Generate a random subnet from 10.0.0.0/8 with mask between /16 and /28"""
    mask = random.randint(16, 28)

    # Generate random IP address
    octets = [10, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    # Calculate how many host bits to zero out
    host_bits = 32 - mask

    # Convert to 32-bit integer
    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

    # Create network mask and apply it to zero out host bits
    netmask = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF
    network_int = ip_int & netmask

    # Convert back to octets
    network_octets = [
        (network_int >> 24) & 0xFF,
        (network_int >> 16) & 0xFF,
        (network_int >> 8) & 0xFF,
        network_int & 0xFF
    ]

    return f"{network_octets[0]}.{network_octets[1]}.{network_octets[2]}.{network_octets[3]}/{mask}"
