#!/usr/bin/env python3
"""
Kube-Stack Version Update Script

This script automatically updates the kube-stack version in the docset.yml file
by fetching the latest collector version from elastic-agent repository tags
and then retrieving the corresponding kube-stack version.

Usage:
    python update_kube_stack_version.py [--dry-run]

Options:
    --dry-run    Show what would be updated without making changes
"""

import urllib.request
import re
import sys
import argparse
import subprocess
import os
import datetime
from pathlib import Path


def fetch_url_content(url):
    """Fetch content from a URL"""
    try:
        print(f"Attempting to fetch: {url}")
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode('utf-8')
        return content
    except urllib.error.URLError as e:
        print(f"Failed to retrieve content: {e.reason}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching URL: {e}")
        return None


def get_latest_collector_version():
    """Get the latest semantic version from elastic-agent repository tags"""
    try:
        print("Fetching latest collector version from elastic-agent repository...")
        
        # Run git command to get the latest semantic version tag
        cmd = ['git', 'ls-remote', '--tags', 'https://github.com/elastic/elastic-agent.git']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
        
        if not result.stdout.strip():
            print("No output from git ls-remote command")
            return None
        
        # Extract version tags and find the latest semantic version
        tags = []
        for line in result.stdout.splitlines():
            if 'refs/tags/v' in line:
                tag = line.split('refs/tags/')[-1]
                # Match semantic version pattern (vX.Y.Z)
                if re.match(r'^v[0-9]+\.[0-9]+\.[0-9]+$', tag):
                    tags.append(tag)
        
        if not tags:
            print("No semantic version tags found")
            return None
            
        # Sort tags by version and get the latest
        def version_key(tag):
            # Remove 'v' prefix and split by dots
            version_parts = tag[1:].split('.')
            return tuple(int(part) for part in version_parts)
        
        latest_tag = max(tags, key=version_key)
        version = latest_tag[1:]  # Remove 'v' prefix
        
        print(f"Latest collector version: {version}")
        return version
        
    except subprocess.TimeoutExpired:
        print("Timeout while fetching tags from elastic-agent repository")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error fetching tags from elastic-agent repository: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return None
    except Exception as e:
        print(f"Error getting latest collector version: {e}")
        return None


def get_collector_version():
    """Get the latest collector version from elastic-agent repository tags"""
    return get_latest_collector_version()


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


def prepare_git_changes(version, dry_run=False):
    """Prepare git changes for PR creation (used by GitHub Actions)"""
    if dry_run:
        print(f"[DRY RUN] Would prepare git changes for kube-stack version {version}")
        return True
    
    try:
        # Add and commit changes
        subprocess.run(['git', 'add', 'docset.yml'], check=True)
        subprocess.run(['git', 'commit', '-m', f'chore: update kube-stack version to {version} [skip ci]'], check=True)
        
        print(f"Git changes prepared for kube-stack version {version}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error preparing git changes: {e}")
        return False
    except Exception as e:
        print(f"Error preparing git changes: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Update kube-stack version in docset.yml')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be updated without making changes')
    parser.add_argument('--prepare-git', action='store_true', default=False,
                       help='Prepare git changes for PR creation (used by GitHub Actions)')
    args = parser.parse_args()
    
    # Get the script directory and construct paths relative to it
    script_dir = Path(__file__).parent
    docset_path = script_dir.parent / 'docset.yml'
    
    print(f"Using docset.yml path: {docset_path}")
    
    # Get the latest collector version from elastic-agent repository
    col_version = get_collector_version()
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
        if args.prepare_git:
            # Prepare git changes for GitHub Actions PR creation
            git_success = prepare_git_changes(kube_stack_version, args.dry_run)
            if git_success:
                print("Kube-stack version update and git changes prepared successfully")
                sys.exit(0)
            else:
                print("Kube-stack version updated but git preparation failed")
                sys.exit(1)
        else:
            print("Kube-stack version update completed successfully")
            sys.exit(0)
    else:
        print("No update was needed - kube-stack version is already up to date")
        sys.exit(0)


if __name__ == '__main__':
    main()
