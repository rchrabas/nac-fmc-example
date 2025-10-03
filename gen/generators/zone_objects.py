"""
Security zone object generators
"""

import random


def generate_security_zones(security_zones_number):
    """
    Generate security zone objects with sequential names and random interface types.
    Interface types: ROUTED, ASA, INLINE, SWITCHED
    """
    interface_types = ['ROUTED', 'ASA', 'INLINE', 'SWITCHED']
    security_zones = []

    for i in range(1, security_zones_number + 1):
        # Select random interface type
        interface_type = random.choice(interface_types)

        security_zone = {
            'name': f'security_zone_{i}',
            'interface_type': interface_type
        }
        security_zones.append(security_zone)

    return security_zones
