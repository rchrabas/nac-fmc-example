"""
Policy object generators
"""

import random


# Valid base policies that exist in FMC (case sensitive)
INTRUSION_POLICIES_BASE_POLICIES = [
    "Balanced Security and Connectivity",
    "Security Over Connectivity"
]

# Valid access policy default actions
ACCESS_POLICY_DEFAULT_ACTIONS = [
    "BLOCK",
    "TRUST",
    "PERMIT",
    "NETWORK_DISCOVERY"
]

# Valid access rule actions
ACCESS_RULE_ACTIONS = [
    "ALLOW",
    "TRUST",
    "BLOCK",
    "MONITOR",
    "BLOCK_RESET",
    "BLOCK_INTERACTIVE"
]

# Valid category sections
CATEGORY_SECTIONS = ["mandatory", "default"]


def generate_intrusion_policies(intrusion_policies_number):
    """
    Generate intrusion policy objects with sequential names.
    Each policy references one of the valid base policies.
    """
    inspection_modes = ['DETECTION', 'PREVENTION']
    intrusion_policies = []

    for i in range(1, intrusion_policies_number + 1):
        # Select random inspection mode and base policy
        inspection_mode = random.choice(inspection_modes)
        base_policy = random.choice(INTRUSION_POLICIES_BASE_POLICIES)

        intrusion_policy = {
            'name': f'intrusion_policy_{i}',
            'inspection_mode': inspection_mode,
            'base_policy': base_policy
        }
        intrusion_policies.append(intrusion_policy)

    return intrusion_policies


def create_intrusion_policy_prerequisites():
    """
    Create the prerequisites structure for intrusion policies.
    This only needs to be generated once and defines the existing base policies.
    """
    return {
        'existing': {
            'fmc': {
                'domains': [
                    {
                        'name': 'Global',
                        'policies': {
                            'intrusion_policies': [
                                {'name': policy_name}
                                for policy_name in INTRUSION_POLICIES_BASE_POLICIES
                            ]
                        }
                    }
                ]
            }
        }
    }


def generate_access_policies(
    policies_number,
    categories_per_policy,
    rules_per_policy,
    available_network_objects,
    available_port_objects,
    available_security_zones,
    available_intrusion_policies,
    available_url_objects
):
    """
    Generate access policy objects with sequential names.
    Each policy includes categories and access rules.

    Args:
        policies_number: Number of access policies to generate
        categories_per_policy: Number of categories per policy
        rules_per_policy: Number of rules per policy
        available_network_objects: List of network object names (hosts, networks, ranges, network_groups)
        available_port_objects: List of port object names (ports, icmpv4s, port_groups)
        available_security_zones: List of security zone names
        available_intrusion_policies: List of intrusion policy names
        available_url_objects: List of URL object names (urls, url_groups)
    """
    access_policies = []

    for policy_num in range(1, policies_number + 1):
        # Generate categories for this policy
        # Categories must be created in mandatory section first, then default section
        categories = []

        # Calculate how many categories per section (split evenly)
        mandatory_count = categories_per_policy // 2
        default_count = categories_per_policy - mandatory_count

        # Create mandatory categories first
        for cat_num in range(1, mandatory_count + 1):
            category = {
                'name': f'category_{policy_num}_{cat_num}',
                'section': 'mandatory'
            }
            categories.append(category)

        # Then create default categories
        for cat_num in range(mandatory_count + 1, categories_per_policy + 1):
            category = {
                'name': f'category_{policy_num}_{cat_num}',
                'section': 'default'
            }
            categories.append(category)

        # Separate categories by section (mandatory first, then default)
        mandatory_categories = [cat['name'] for cat in categories if cat['section'] == 'mandatory']
        default_categories = [cat['name'] for cat in categories if cat['section'] == 'default']

        # Create ordered list of all categories: mandatory first, then default
        ordered_category_names = mandatory_categories + default_categories

        # Calculate how many rules per category (distribute evenly)
        rules_per_category = rules_per_policy // len(ordered_category_names) if ordered_category_names else rules_per_policy

        # Generate access rules for this policy
        access_rules = []
        for rule_num in range(1, rules_per_policy + 1):
            rule = {
                'name': f'rule_{policy_num}_{rule_num}',
                'action': random.choice(ACCESS_RULE_ACTIONS)
            }

            # Assign a category to every rule (mandatory)
            # Rules use mandatory categories first, then default categories
            # Distribute evenly across categories within each section
            if ordered_category_names:
                category_index = (rule_num - 1) // rules_per_category
                # Handle case where we have leftover rules
                if category_index >= len(ordered_category_names):
                    category_index = len(ordered_category_names) - 1
                rule['category'] = ordered_category_names[category_index]

            # Add source zones (30% chance, 1-3 zones)
            if available_security_zones and random.random() > 0.7:
                num_zones = random.randint(1, min(3, len(available_security_zones)))
                rule['source_zones'] = random.sample(available_security_zones, num_zones)

            # Add destination zones (30% chance, 1-3 zones)
            if available_security_zones and random.random() > 0.7:
                num_zones = random.randint(1, min(3, len(available_security_zones)))
                rule['destination_zones'] = random.sample(available_security_zones, num_zones)

            # Add source network objects (50% chance, 1-5 objects)
            if available_network_objects and random.random() > 0.5:
                num_objects = random.randint(1, min(5, len(available_network_objects)))
                rule['source_network_objects'] = random.sample(available_network_objects, num_objects)

            # Add destination network objects (50% chance, 1-5 objects)
            if available_network_objects and random.random() > 0.5:
                num_objects = random.randint(1, min(5, len(available_network_objects)))
                rule['destination_network_objects'] = random.sample(available_network_objects, num_objects)

            # Add destination port objects (40% chance, 1-5 objects)
            if available_port_objects and random.random() > 0.6:
                num_objects = random.randint(1, min(5, len(available_port_objects)))
                rule['destination_port_objects'] = random.sample(available_port_objects, num_objects)

            # Add URL objects (40% chance, 1-3 objects)
            if available_url_objects and random.random() > 0.6:
                num_objects = random.randint(1, min(3, len(available_url_objects)))
                rule['url_objects'] = random.sample(available_url_objects, num_objects)

            # Add intrusion policy (30% chance)
            # Cannot be used with BLOCK, TRUST, BLOCK_RESET, or MONITOR actions
            if (available_intrusion_policies and
                rule['action'] not in ['BLOCK', 'TRUST', 'BLOCK_RESET', 'MONITOR'] and
                random.random() > 0.7):
                rule['intrusion_policy'] = random.choice(available_intrusion_policies)

            # Add logging options
            # send_events_to_fmc is always true
            rule['send_events_to_fmc'] = True

            # Apply action-specific logging rules
            if rule['action'] == 'MONITOR':
                # MONITOR requires specific logging settings
                rule['log_connection_begin'] = False
                rule['log_connection_end'] = True
            elif rule['action'] in ['BLOCK', 'BLOCK_RESET']:
                # BLOCK and BLOCK_RESET require log_connection_end = false
                rule['log_connection_end'] = False
                # Since send_events_to_fmc is true, at least one log must be true
                rule['log_connection_begin'] = True
            else:
                # For other actions, use random values but ensure at least one is true
                # (because send_events_to_fmc is true)
                log_begin = random.choice([True, False])
                log_end = random.choice([True, False])

                # If both are false, randomly make one true
                if not log_begin and not log_end:
                    if random.choice([True, False]):
                        log_begin = True
                    else:
                        log_end = True

                rule['log_connection_begin'] = log_begin
                rule['log_connection_end'] = log_end

            access_rules.append(rule)

        # Create the access policy
        access_policy = {
            'name': f'access_policy_{policy_num}',
            'default_action': random.choice(ACCESS_POLICY_DEFAULT_ACTIONS),
            'categories': categories,
            'access_rules': access_rules
        }

        access_policies.append(access_policy)

    return access_policies
