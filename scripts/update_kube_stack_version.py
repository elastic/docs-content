#!/usr/bin/env python3
"""
Kube-Stack Version Update Script

This script automatically updates the kube-stack version in the docset.yml file
by fetching the latest version from the elastic-agent repository.

Usage:
    python update_kube_stack_version.py [--dry-run]

Options:
    --dry-run    Show what would be updated without making changes
"""

import urllib.request
import re
import sys
import argparse
from pathlib import Path


def fetch_url_content(url):
    """Fetch content from a URL"""
    try:
        print(f"Attempting to fetch: {url}")
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
        return content
    except urllib.error.URLError as e:
        print(f"Failed to retrieve content: {e.reason}")
        return None


def get_collector_version(file_path):
    """Extract the collector version from docset.yml"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        lines = content.splitlines()
        for line in lines:
            if line.strip().startswith('edot-collector-version:'):
                return line.split(':', 1)[1].strip()
        
        # If no specific version is found, use a default version that we know works
        return '9.1.2'
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def get_kube_stack_version(version='main'):
    """Extract KubeStackChartVersion from elastic-agent repository"""
    # Try different URL formats for the k8s.go file
    # First try with the version as-is (in case it already has 'v' prefix)
    url = f'https://raw.githubusercontent.com/elastic/elastic-agent/{version}/testing/integration/k8s/k8s.go'
    print(f"Trying k8s.go URL: {url}")
    content = fetch_url_content(url)
    
    # If first attempt fails and version doesn't start with 'v', try with 'v' prefix
    if content is None and not version.startswith('v') and version != 'main':
        url = f'https://raw.githubusercontent.com/elastic/elastic-agent/v{version}/testing/integration/k8s/k8s.go'
        print(f"Retrying k8s.go with URL: {url}")
        content = fetch_url_content(url)
    
    # If that fails too, try with main branch
    if content is None:
        url = 'https://raw.githubusercontent.com/elastic/elastic-agent/main/testing/integration/k8s/k8s.go'
        print(f"Falling back to main branch for k8s.go: {url}")
        content = fetch_url_content(url)
    
    if content is None:
        print(f"Could not fetch k8s.go from any URL")
        return None
        
    # Look for the KubeStackChartVersion line
    lines = content.splitlines()
    for line in lines:
        if 'KubeStackChartVersion' in line and '=' in line:
            # Extract the version from the line like: KubeStackChartVersion = "0.6.3"
            match = re.search(r'KubeStackChartVersion\s*=\s*"([^"]+)"', line)
            if match:
                return match.group(1)
    
    print("Could not find KubeStackChartVersion in k8s.go")
    return None


def update_docset_kube_stack_version(version, docset_path, dry_run=False):
    """Update the kube-stack-version substitution in docset.yml"""
    try:
        with open(docset_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the kube-stack-version line
        pattern = r'(kube-stack-version:\s*)[0-9]+\.[0-9]+\.[0-9]+'
        replacement = f'\\g<1>{version}'
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            if dry_run:
                print(f"[DRY RUN] Would update kube-stack-version to {version} in {docset_path}")
                return True
            else:
                with open(docset_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated kube-stack-version to {version} in {docset_path}")
                return True
        else:
            print(f"kube-stack-version already up to date: {version}")
            return False
            
    except Exception as e:
        print(f"Error updating {docset_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Update kube-stack version in docset.yml')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be updated without making changes')
    args = parser.parse_args()
    
    # Get the script directory and construct paths relative to it
    script_dir = Path(__file__).parent
    docset_path = script_dir.parent / 'docset.yml'
    
    print(f"Using docset.yml path: {docset_path}")
    
    # Get the current collector version from docset.yml
    col_version = get_collector_version(docset_path)
    if col_version is None:
        print("Error: Could not determine collector version")
        sys.exit(1)
    
    print(f"Collector version: {col_version}")
    
    # Get the kube-stack version from elastic-agent repository
    kube_stack_version = get_kube_stack_version(col_version)
    if kube_stack_version is None:
        print("Error: Could not fetch kube-stack version")
        sys.exit(1)
    
    print(f"Found kube-stack version: {kube_stack_version}")
    
    # Update the docset.yml file
    success = update_docset_kube_stack_version(kube_stack_version, docset_path, args.dry_run)
    
    if success:
        print("Kube-stack version update completed successfully")
        sys.exit(0)
    else:
        print("No update was needed or update failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
