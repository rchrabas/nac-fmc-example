# Cisco FMC YAML Configuration Generator

Python CLI application that generates YAML configuration files for the Network As Code for Cisco Secure Firewall Management Center (nac-fmc) Terraform module.

Generated configuration is fully random and is used only to demonstrate capabilities of the solution.

## About nac-fmc

The [nac-fmc Terraform module](https://registry.terraform.io/modules/netascode/nac-fmc/fmc/latest) provides a Network-as-Code (NaC) solution for managing Cisco Secure Firewall Manager (FMC) configurations. It enables infrastructure-as-code practices by allowing you to define FMC objects, policies, and configurations in YAML files, which are then applied using Terraform.

This generator creates sample YAML configurations that can be used as input for the nac-fmc module, making it easy to test and develop FMC configurations at scale.

## Requirements

- Python 3.10+
- PyYAML

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit the configuration file at `gen/cfg.yaml`:

```yaml
settings:
  - hosts_number: 10                      # Number of host objects to generate
  - networks_number: 10                   # Number of network objects to generate
  - ranges_number: 10                     # Number of range objects to generate
  - ports_number: 10                      # Number of port objects to generate
  - icmpv4s_number: 10                    # Number of ICMPv4 objects to generate
  - security_zones_number: 10             # Number of security zone objects to generate
  - port_groups_number: 5                 # Number of port group objects to generate
  - network_groups_number: 5              # Number of network group objects to generate
  - urls_number: 10                       # Number of URL objects to generate
  - url_groups_number: 5                  # Number of URL group objects to generate
  - intrusion_policies_number: 3          # Number of intrusion policies to generate
  - access_control_policies_number: 2     # Number of access control policies to generate
  - access_control_categories_number: 4   # Number of categories per access control policy
  - access_control_rules_number: 20       # Number of rules per access control policy
```

## Usage

Run the generator (no command-line arguments needed):

```bash
# With activated venv
python gen/gen.py

# Or without activating venv
./venv/bin/python gen/gen.py
```

The application will:
1. Clear the `data/` folder
2. Generate the specified number of objects for each type
3. Create separate YAML files for each object type in `data/` folder

## Supported Objects

The generator supports the following FMC object types:

### Network Objects
- **Hosts** - Individual IP addresses
- **Networks** - IP subnets with CIDR notation
- **Ranges** - IP address ranges
- **Network Groups** - Collections of hosts, networks, ranges, and other network groups

### Service Objects
- **Ports** - TCP/UDP/ESP port definitions
- **ICMPv4** - ICMP type and code specifications
- **Port Groups** - Collections of ports and ICMP objects

### URL Objects
- **URLs** - Individual URL definitions
- **URL Groups** - Collections of URL objects and literal URL values

### Zone Objects
- **Security Zones** - Interface groupings with zone types

### Policy Objects
- **Intrusion Policies** - IPS policies that inherit from base policies
- **Access Control Policies** - Firewall access policies with categories and rules

## Object Generation Rules

- **Domain**: All objects are created under the Global domain
- **Naming**: Sequential names (host_1, host_2, network_1, network_2, etc.)
- **IP Addresses**: Random values from 10.0.0.0/8 subnet (duplicates allowed)
- **Subnets**: Random values from 10.0.0.0/8 with network masks between /16 and /28, properly aligned to network boundaries
- **IP Ranges**: Random start and end IPs from 10.0.0.0/8 (start < end)
- **Ports**: Random protocols (TCP/UDP/ESP), random ports (1024-65535) or port ranges, ESP protocol without port numbers
- **ICMPv4**: Valid ICMP type/code combinations following IANA specifications (types: 0, 3, 5, 8, 11, 12, 40)
- **Security Zones**: Random interface types (ROUTED, ASA, INLINE, SWITCHED)
- **URLs**: Random subdomains from a predefined list of example.com domain
- **Port Groups**: Each group contains 2-6 randomly selected objects (ports and icmpv4s only)
- **Network Groups**: Each group contains 3-5 randomly selected objects (hosts, networks, ranges, or other network groups)
- **URL Groups**: Each group contains 2-4 references to existing URL objects and 1-3 literal URL values using random subdomains of example.com
- **Intrusion Policies**: Generated policies inherit from base policies defined in prerequisites file
- **Access Control Policies**: Each policy contains specified number of categories and rules that reference generated network, service, URL, security zone, and intrusion policy objects

## Applying Configuration to FMC

After generating the YAML configuration files, you need to apply them to your Cisco Secure Firewall Manager using Terraform:

1. **Update FMC credentials** in `main.tf`:
   ```hcl
   provider "fmc" {
     username = "your-fmc-username"
     password = "your-fmc-password"
     url      = "https://your-fmc-address"
   }
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Apply the configuration**:
   ```bash
   terraform apply
   ```

For more information on configuring and using the nac-fmc module, refer to the [module documentation](https://registry.terraform.io/modules/netascode/nac-fmc/fmc/latest).

## Data Model Documentation

### Network Objects
- [Host objects](https://netascode.cisco.com/docs/data_models/fmc/objects/host/)
- [Network objects](https://netascode.cisco.com/docs/data_models/fmc/objects/network/)
- [Range objects](https://netascode.cisco.com/docs/data_models/fmc/objects/range/)
- [Network Group objects](https://netascode.cisco.com/docs/data_models/fmc/objects/network_group/)

### Service Objects
- [Port objects](https://netascode.cisco.com/docs/data_models/fmc/objects/port/)
- [ICMPv4 objects](https://netascode.cisco.com/docs/data_models/fmc/objects/icmpv4/)
- [Port Group objects](https://netascode.cisco.com/docs/data_models/fmc/objects/port_group/)

### URL Objects
- [URL objects](https://netascode.cisco.com/docs/data_models/fmc/objects/url/)
- [URL Group objects](https://netascode.cisco.com/docs/data_models/fmc/objects/url_group/)

### Zone Objects
- [Security Zone objects](https://netascode.cisco.com/docs/data_models/fmc/objects/security_zone/)

### Policy Objects
- [Intrusion Policy objects](https://netascode.cisco.com/docs/data_models/fmc/policies/intrusion_policy/)
- [Access Control Policy objects](https://netascode.cisco.com/docs/data_models/fmc/policies/access_policy/)