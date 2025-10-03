"""
Configuration loading and parsing utilities
"""

import yaml
import sys
from pathlib import Path


def load_config():
    """Load configuration from gen/cfg.yaml"""
    config_path = Path(__file__).parent.parent / 'cfg.yaml'

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(1)


def parse_config(config):
    """Parse configuration and extract settings"""
    settings = {}

    if 'settings' not in config:
        print("Error: 'settings' section not found in config", file=sys.stderr)
        sys.exit(1)

    # Parse settings list
    for item in config['settings']:
        if isinstance(item, dict):
            settings.update(item)

    return settings
