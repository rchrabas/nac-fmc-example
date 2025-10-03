"""
Network group object generators
"""

import random


def generate_network_groups(network_groups_number, available_objects):
    """
    Generate network group objects with sequential names and random object references.
    Each network group contains 3-5 objects from the available objects list.

    Args:
        network_groups_number: Number of network groups to generate
        available_objects: List of object names that can be referenced (hosts, networks, ranges, network_groups)
    """
    network_groups = []

    for i in range(1, network_groups_number + 1):
        # Determine how many objects this group should have (3-5)
        num_objects = random.randint(3, 5)

        # Select random objects from available objects
        if len(available_objects) < num_objects:
            # If we don't have enough objects, use what we have
            selected_objects = available_objects.copy()
        else:
            selected_objects = random.sample(available_objects, num_objects)

        network_group = {
            'name': f'network_group_{i}',
            'objects': selected_objects
        }
        network_groups.append(network_group)

        # Add this network group to available objects for future groups
        available_objects.append(f'network_group_{i}')

    return network_groups
