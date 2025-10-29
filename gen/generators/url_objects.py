"""
URL object generators: urls, url_groups
"""

import random


def generate_urls(urls_number):
    """
    Generate URL objects with sequential names and random subdomains of example.com.
    """
    subdomains = ['www', 'api', 'app', 'web', 'portal', 'admin', 'test', 'dev', 'staging', 'prod',
                  'mail', 'shop', 'store', 'blog', 'news', 'support', 'help', 'docs', 'wiki', 'cdn']
    urls = []

    for i in range(1, urls_number + 1):
        # Select random subdomain
        subdomain = random.choice(subdomains)

        url_obj = {
            'name': f'url_{i}',
            'url': f'https://{subdomain}.example.com'
        }
        urls.append(url_obj)

    return urls


def generate_url_groups(url_groups_number, available_url_objects):
    """
    Generate URL group objects with sequential names.
    Each URL group contains 2-4 URL references and 1-3 literal URLs.

    Args:
        url_groups_number: Number of URL groups to generate
        available_url_objects: List of URL object names that can be referenced
    """
    subdomains = ['www', 'api', 'app', 'web', 'portal', 'admin', 'test', 'dev', 'staging', 'prod',
                  'mail', 'shop', 'store', 'blog', 'news', 'support', 'help', 'docs', 'wiki', 'cdn']
    url_groups = []

    for i in range(1, url_groups_number + 1):
        url_group = {'name': f'url_group_{i}'}

        # Add URL object references (2-4 references)
        if len(available_url_objects) > 0:
            num_url_refs = random.randint(2, min(4, len(available_url_objects)))
            selected_urls = random.sample(available_url_objects, num_url_refs)
            url_group['urls'] = selected_urls

        # Add literal URLs (1-3 literals)
        # Use a set to ensure no duplicates
        num_literals = random.randint(1, 3)
        literals = set()
        while len(literals) < num_literals:
            subdomain = random.choice(subdomains)
            literals.add(f'https://{subdomain}.example.com')
        url_group['literals'] = list(literals)

        url_groups.append(url_group)

    return url_groups
