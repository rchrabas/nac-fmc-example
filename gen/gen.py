#!/usr/bin/env python3
"""
FMC YAML Configuration Generator
Generates YAML files for nac-fmc Terraform module
"""

from utils.config import load_config, parse_config
from utils.file_ops import clear_data_folder, write_output, create_fmc_structure, create_fmc_policy_structure
from generators.network_objects import generate_hosts, generate_networks, generate_ranges
from generators.service_objects import generate_ports, generate_icmpv4s, generate_port_groups
from generators.url_objects import generate_urls, generate_url_groups
from generators.zone_objects import generate_security_zones
from generators.group_objects import generate_network_groups
from generators.policy_objects import (
    generate_intrusion_policies,
    create_intrusion_policy_prerequisites,
    generate_access_policies
)


def main():
    print("FMC YAML Configuration Generator")
    print("=" * 50)

    # Load configuration
    config = load_config()
    settings = parse_config(config)

    # Clear data folder
    clear_data_folder()

    # Track all available object names for network groups
    available_objects = []

    # Track available port/icmpv4 object names for port groups
    available_port_objects = []

    # Track available URL object names for URL groups
    available_url_objects = []

    # Track available security zone names for access policies
    available_security_zones = []

    # Track available intrusion policy names for access policies
    available_intrusion_policies = []

    # Generate hosts
    if 'hosts_number' in settings:
        hosts_number = settings['hosts_number']
        if hosts_number > 0:
            print(f"Generating {hosts_number} host(s)...")
            hosts = generate_hosts(hosts_number)
            fmc_data = create_fmc_structure('hosts', hosts)
            write_output(fmc_data, 'hosts.nac.yaml')
            # Add host names to available objects
            available_objects.extend([h['name'] for h in hosts])

    # Generate networks
    if 'networks_number' in settings:
        networks_number = settings['networks_number']
        if networks_number > 0:
            print(f"Generating {networks_number} network(s)...")
            networks = generate_networks(networks_number)
            fmc_data = create_fmc_structure('networks', networks)
            write_output(fmc_data, 'networks.nac.yaml')
            # Add network names to available objects
            available_objects.extend([n['name'] for n in networks])

    # Generate ranges
    if 'ranges_number' in settings:
        ranges_number = settings['ranges_number']
        if ranges_number > 0:
            print(f"Generating {ranges_number} range(s)...")
            ranges = generate_ranges(ranges_number)
            fmc_data = create_fmc_structure('ranges', ranges)
            write_output(fmc_data, 'ranges.nac.yaml')
            # Add range names to available objects
            available_objects.extend([r['name'] for r in ranges])

    # Generate ports
    if 'ports_number' in settings:
        ports_number = settings['ports_number']
        if ports_number > 0:
            print(f"Generating {ports_number} port(s)...")
            ports = generate_ports(ports_number)
            fmc_data = create_fmc_structure('ports', ports)
            write_output(fmc_data, 'ports.nac.yaml')
            # Add port names to available port objects
            available_port_objects.extend([p['name'] for p in ports])

    # Generate ICMPv4 objects
    if 'icmpv4s_number' in settings:
        icmpv4s_number = settings['icmpv4s_number']
        if icmpv4s_number > 0:
            print(f"Generating {icmpv4s_number} ICMPv4 object(s)...")
            icmpv4s = generate_icmpv4s(icmpv4s_number)
            fmc_data = create_fmc_structure('icmpv4s', icmpv4s)
            write_output(fmc_data, 'icmpv4s.nac.yaml')
            # Add icmpv4 names to available port objects
            available_port_objects.extend([i['name'] for i in icmpv4s])

    # Generate security zones
    if 'security_zones_number' in settings:
        security_zones_number = settings['security_zones_number']
        if security_zones_number > 0:
            print(f"Generating {security_zones_number} security zone(s)...")
            security_zones = generate_security_zones(security_zones_number)
            fmc_data = create_fmc_structure('security_zones', security_zones)
            write_output(fmc_data, 'security_zones.nac.yaml')
            # Add security zone names to available security zones
            available_security_zones.extend([sz['name'] for sz in security_zones])

    # Generate URLs
    if 'urls_number' in settings:
        urls_number = settings['urls_number']
        if urls_number > 0:
            print(f"Generating {urls_number} URL(s)...")
            urls = generate_urls(urls_number)
            fmc_data = create_fmc_structure('urls', urls)
            write_output(fmc_data, 'urls.nac.yaml')
            # Add URL names to available URL objects
            available_url_objects.extend([u['name'] for u in urls])

    # Generate port groups (must be after ports and icmpv4s)
    if 'port_groups_number' in settings and len(available_port_objects) > 0:
        port_groups_number = settings['port_groups_number']
        if port_groups_number > 0:
            print(f"Generating {port_groups_number} port group(s)...")
            port_groups = generate_port_groups(port_groups_number, available_port_objects)
            fmc_data = create_fmc_structure('port_groups', port_groups)
            write_output(fmc_data, 'port_groups.nac.yaml')
            # Add port group names to available port objects
            available_port_objects.extend([pg['name'] for pg in port_groups])

    # Generate network groups (must be after all other objects)
    if 'network_groups_number' in settings and len(available_objects) > 0:
        network_groups_number = settings['network_groups_number']
        if network_groups_number > 0:
            print(f"Generating {network_groups_number} network group(s)...")
            network_groups = generate_network_groups(network_groups_number, available_objects)
            fmc_data = create_fmc_structure('network_groups', network_groups)
            write_output(fmc_data, 'network_groups.nac.yaml')
            # Add network group names to available objects
            available_objects.extend([ng['name'] for ng in network_groups])

    # Generate URL groups (must be after URLs)
    if 'url_groups_number' in settings and len(available_url_objects) > 0:
        url_groups_number = settings['url_groups_number']
        if url_groups_number > 0:
            print(f"Generating {url_groups_number} URL group(s)...")
            url_groups = generate_url_groups(url_groups_number, available_url_objects)
            fmc_data = create_fmc_structure('url_groups', url_groups)
            write_output(fmc_data, 'url_groups.nac.yaml')
            # Add URL group names to available URL objects
            available_url_objects.extend([ug['name'] for ug in url_groups])

    # Generate intrusion policies
    if 'intrusion_policies_number' in settings:
        intrusion_policies_number = settings['intrusion_policies_number']
        if intrusion_policies_number > 0:
            # First, generate prerequisites file (only once)
            print("Generating intrusion policy prerequisites...")
            prerequisites = create_intrusion_policy_prerequisites()
            write_output(prerequisites, 'intrusion_policies_existing.nac.yaml')

            # Then generate the intrusion policies
            print(f"Generating {intrusion_policies_number} intrusion polic(ies)...")
            intrusion_policies = generate_intrusion_policies(intrusion_policies_number)
            fmc_data = create_fmc_policy_structure('intrusion_policies', intrusion_policies)
            write_output(fmc_data, 'intrusion_policies.nac.yaml')
            # Add intrusion policy names to available intrusion policies
            available_intrusion_policies.extend([ip['name'] for ip in intrusion_policies])

    # Generate access policies (must be after all objects and policies)
    if 'access_control_policies_number' in settings:
        policies_number = settings['access_control_policies_number']
        categories_number = settings.get('access_control_categories_number', 0)
        rules_number = settings.get('access_control_rules_number', 0)

        if policies_number > 0 and (categories_number > 0 or rules_number > 0):
            # Generate the access policies
            print(f"Generating {policies_number} access polic(ies) with {categories_number} categories and {rules_number} rules each...")
            access_policies = generate_access_policies(
                policies_number,
                categories_number,
                rules_number,
                available_objects,
                available_port_objects,
                available_security_zones,
                available_intrusion_policies,
                available_url_objects
            )

            # Write each policy to a separate file
            for policy in access_policies:
                policy_name = policy['name']
                fmc_data = create_fmc_policy_structure('access_policies', [policy])
                write_output(fmc_data, f'access_policies_{policy_name}.nac.yaml')

    print("=" * 50)
    print("Generation completed successfully!")


if __name__ == '__main__':
    main()
