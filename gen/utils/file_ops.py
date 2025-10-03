"""
File operation utilities for YAML generation
"""

import yaml
from pathlib import Path


def create_fmc_structure(object_type, objects):
    """Create the FMC YAML structure for a specific object type"""
    return {
        'fmc': {
            'domains': [
                {
                    'name': 'Global',
                    'objects': {
                        object_type: objects
                    }
                }
            ]
        }
    }


def create_fmc_policy_structure(policy_type, policies):
    """Create the FMC YAML structure for a specific policy type"""
    return {
        'fmc': {
            'domains': [
                {
                    'name': 'Global',
                    'policies': {
                        policy_type: policies
                    }
                }
            ]
        }
    }


def clear_data_folder():
    """Clear the data folder before generation"""
    data_path = Path(__file__).parent.parent.parent / 'data'

    if data_path.exists():
        # Remove all files in data folder
        for file in data_path.glob('*.yaml'):
            file.unlink()
        print(f"Cleared data folder")
    else:
        # Create data folder if it doesn't exist
        data_path.mkdir(parents=True, exist_ok=True)
        print(f"Created data folder")


def write_output(data, filename):
    """Write generated data to YAML file in data folder"""
    output_path = Path(__file__).parent.parent.parent / 'data' / filename

    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"Generated {filename}")
