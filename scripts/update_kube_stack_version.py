#!/usr/bin/env python3
"""
Script to update the kube-stack-version in docset.yml based on the latest version
from the elastic-agent repository.

This script:
1. Retrieves the latest semver from the elastic-agent repository
2. Reads the k8s.go file from the elastic-agent repository
3. Extracts the KubeStackChartVersion value
4. Updates the kube-stack-version in docset.yml
"""

import re
import sys
import requests
import time
from pathlib import Path
from typing import Optional


def get_latest_elastic_agent_version() -> str:
    """
    Retrieve the latest semantic version from the elastic-agent repository by fetching all tags
    and finding the highest version with retry logic.
    
    Returns:
        str: The latest version tag (e.g., 'v8.12.0')
        
    Raises:
        Exception: If unable to fetch version information after retries
    """
    url = "https://api.github.com/repos/elastic/elastic-agent/tags"
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching elastic-agent tags (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            tags_data = response.json()
            if not tags_data:
                raise Exception("No tags found in repository")
            
            # Extract version tags matching pattern vX.Y.Z
            version_pattern = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
            versions = []
            
            for tag in tags_data:
                tag_name = tag.get('name', '')
                if version_pattern.match(tag_name):
                    # Extract version components for sorting
                    match = version_pattern.match(tag_name)
                    major, minor, patch = map(int, match.groups())
                    versions.append((major, minor, patch, tag_name))
            
            if not versions:
                raise Exception("No valid version tags found")
            
            # Sort by version components and get the latest
            versions.sort(key=lambda x: (x[0], x[1], x[2]))
            latest_version = versions[-1][3]
            
            print(f"Latest elastic-agent version: {latest_version}")
            return latest_version
            
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Failed to fetch tags after {max_retries} attempts: {e}")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Error retrieving version after {max_retries} attempts: {e}")


def fetch_k8s_go_content(version: str) -> str:
    """
    Fetch the content of the k8s.go file from the elastic-agent repository with retry logic.
    
    Args:
        version (str): The version tag to fetch
        
    Returns:
        str: The content of the k8s.go file
        
    Raises:
        Exception: If unable to fetch the file content after retries
    """
    url = f"https://raw.githubusercontent.com/elastic/elastic-agent/{version}/testing/integration/k8s/k8s.go"
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching k8s.go from version {version} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            print(f"Successfully fetched k8s.go from version {version}")
            return response.text
            
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Failed to fetch k8s.go file after {max_retries} attempts: {e}")


def extract_kube_stack_version(content: str) -> str:
    """
    Extract the KubeStackChartVersion from the k8s.go file content.
    
    Args:
        content (str): The content of the k8s.go file
        
    Returns:
        str: The KubeStackChartVersion value
        
    Raises:
        Exception: If the version pattern is not found
    """
    # Pattern to match KubeStackChartVersion = "version"
    pattern = r'KubeStackChartVersion\s*=\s*"([^"]+)"'
    
    match = re.search(pattern, content)
    if not match:
        raise Exception("KubeStackChartVersion pattern not found in k8s.go file")
    
    version = match.group(1)
    print(f"Extracted KubeStackChartVersion: {version}")
    return version


def update_docset_yml(kube_stack_version: str, docset_path: Path) -> None:
    """
    Update the kube-stack-version in the docset.yml file.
    
    Args:
        kube_stack_version (str): The new version to set
        docset_path (Path): Path to the docset.yml file
        
    Raises:
        Exception: If unable to update the file
    """
    try:
        # Read the current docset.yml content
        with open(docset_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern to match kube-stack-version: <value> (with 2 spaces at the beginning)
        pattern = r'(  kube-stack-version:\s*)([^\s\n]+)'
        
        # Replace the version
        new_content = re.sub(pattern, rf'\g<1>{kube_stack_version}', content)
        
        if new_content == content:
            # Check if the version is already correct
            current_match = re.search(pattern, content)
            if current_match and current_match.group(2) == kube_stack_version:
                print(f"kube-stack-version is already set to {kube_stack_version}")
                return
            else:
                raise Exception("kube-stack-version pattern not found in docset.yml")
        
        # Write the updated content back to the file
        with open(docset_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Successfully updated kube-stack-version to {kube_stack_version} in docset.yml")
        
    except Exception as e:
        raise Exception(f"Failed to update docset.yml: {e}")


def main():
    """Main function to orchestrate the update process."""
    try:
        print("Starting kube-stack-version update process...")
        
        # Get the script directory and project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        docset_path = project_root / "docset.yml"
        
        # Verify docset.yml exists
        if not docset_path.exists():
            raise Exception(f"docset.yml not found at {docset_path}")
        
        # Step 1: Get latest elastic-agent version
        print("\n1. Retrieving latest elastic-agent version...")
        latest_version = get_latest_elastic_agent_version()
        
        # Step 2: Fetch k8s.go content
        print("\n2. Fetching k8s.go file content...")
        k8s_content = fetch_k8s_go_content(latest_version)
        
        # Step 3: Extract KubeStackChartVersion
        print("\n3. Extracting KubeStackChartVersion...")
        kube_stack_version = extract_kube_stack_version(k8s_content)
        
        # Step 4: Update docset.yml
        print("\n4. Updating docset.yml...")
        update_docset_yml(kube_stack_version, docset_path)
        
        print(f"\n✅ Successfully updated kube-stack-version to {kube_stack_version}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()