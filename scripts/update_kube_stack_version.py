#!/usr/bin/env python3
"""
Script to update the kube-stack-version and helm-version in docset.yml based on
versions from the Kibana and Elastic Agent repositories.

This script:
1. Retrieves the latest semver from the Kibana repository
2. Reads the constants.ts file from that Kibana version
3. Extracts the OTEL_KUBE_STACK_VERSION value
4. Fetches the go.mod file from the Elastic Agent repository
5. Extracts the Helm version from go.mod
6. Updates both kube-stack-version and helm-version in docset.yml
"""

import re
import sys
import requests
import time
from pathlib import Path


def get_latest_kibana_version() -> str:
    """
    Retrieve the latest semantic version from the Kibana repository by fetching all tags
    and finding the highest version with retry logic.
    
    Returns:
        str: The latest version tag (e.g., 'v9.2.0')
        
    Raises:
        Exception: If unable to fetch version information after retries
    """
    url = "https://api.github.com/repos/elastic/kibana/tags"
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching Kibana tags (attempt {attempt + 1}/{max_retries})")
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
            
            print(f"Latest Kibana version: {latest_version}")
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


def fetch_constants_ts_content(version: str) -> str:
    """
    Fetch the content of the constants.ts file from the Kibana repository with retry logic.
    
    Args:
        version (str): The version tag to fetch (e.g., 'v9.2.0')
    
    Returns:
        str: The content of the constants.ts file
        
    Raises:
        Exception: If unable to fetch the file content after retries
    """
    url = f"https://raw.githubusercontent.com/elastic/kibana/{version}/x-pack/solutions/observability/plugins/observability_onboarding/public/application/quickstart_flows/otel_kubernetes/constants.ts"
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching constants.ts from Kibana {version} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            print(f"Successfully fetched constants.ts from Kibana {version}")
            return response.text
            
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Failed to fetch constants.ts file after {max_retries} attempts: {e}")


def extract_kube_stack_version(content: str) -> str:
    """
    Extract the OTEL_KUBE_STACK_VERSION from the constants.ts file content.
    
    Args:
        content (str): The content of the constants.ts file
        
    Returns:
        str: The OTEL_KUBE_STACK_VERSION value
        
    Raises:
        Exception: If the version pattern is not found
    """
    # Pattern to match OTEL_KUBE_STACK_VERSION = 'version' or "version"
    pattern = r'OTEL_KUBE_STACK_VERSION\s*=\s*[\'"]([^\'"]+)[\'"]'
    
    match = re.search(pattern, content)
    if not match:
        raise Exception("OTEL_KUBE_STACK_VERSION pattern not found in constants.ts file")
    
    version = match.group(1)
    print(f"Extracted OTEL_KUBE_STACK_VERSION: {version}")
    return version


def fetch_elastic_agent_gomod() -> str:
    """
    Fetch the content of the go.mod file from the Elastic Agent repository with retry logic.
    
    Returns:
        str: The content of the go.mod file
        
    Raises:
        Exception: If unable to fetch the file content after retries
    """
    url = "https://raw.githubusercontent.com/elastic/elastic-agent/refs/heads/main/go.mod"
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching go.mod from Elastic Agent repository (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            print("Successfully fetched go.mod from Elastic Agent repository")
            return response.text
            
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Failed to fetch go.mod file after {max_retries} attempts: {e}")


def extract_helm_version(content: str) -> str:
    """
    Extract the Helm version from the go.mod file content.
    
    Args:
        content (str): The content of the go.mod file
        
    Returns:
        str: The Helm version (e.g., '3.15.4')
        
    Raises:
        Exception: If the Helm version pattern is not found
    """
    # Pattern to match helm.sh/helm/v3 vX.Y.Z
    pattern = r'helm\.sh/helm/v3\s+v([\d.]+)'
    
    match = re.search(pattern, content)
    if not match:
        raise Exception("Helm version pattern not found in go.mod file")
    
    version = match.group(1)
    print(f"Extracted Helm version: {version}")
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


def update_helm_version(helm_version: str, docset_path: Path) -> None:
    """
    Update the helm-version in the docset.yml file.
    
    Args:
        helm_version (str): The new version to set
        docset_path (Path): Path to the docset.yml file
        
    Raises:
        Exception: If unable to update the file
    """
    try:
        # Read the current docset.yml content
        with open(docset_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern to match helm-version: <value> (with 2 spaces at the beginning)
        pattern = r'(  helm-version:\s*)([^\s\n]+)'
        
        # Replace the version
        new_content = re.sub(pattern, rf'\g<1>{helm_version}', content)
        
        if new_content == content:
            # Check if the version is already correct
            current_match = re.search(pattern, content)
            if current_match and current_match.group(2) == helm_version:
                print(f"helm-version is already set to {helm_version}")
                return
            else:
                raise Exception("helm-version pattern not found in docset.yml")
        
        # Write the updated content back to the file
        with open(docset_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Successfully updated helm-version to {helm_version} in docset.yml")
        
    except Exception as e:
        raise Exception(f"Failed to update docset.yml: {e}")


def main():
    """Main function to orchestrate the update process."""
    try:
        print("Starting version update process...")
        
        # Get the script directory and project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        docset_path = project_root / "docset.yml"
        
        # Verify docset.yml exists
        if not docset_path.exists():
            raise Exception(f"docset.yml not found at {docset_path}")
        
        # Step 1: Get latest Kibana version
        print("\n1. Retrieving latest Kibana version...")
        latest_version = get_latest_kibana_version()
        
        # Step 2: Fetch constants.ts content
        print("\n2. Fetching constants.ts file content from Kibana repository...")
        constants_content = fetch_constants_ts_content(latest_version)
        
        # Step 3: Extract OTEL_KUBE_STACK_VERSION
        print("\n3. Extracting OTEL_KUBE_STACK_VERSION...")
        kube_stack_version = extract_kube_stack_version(constants_content)
        
        # Step 4: Fetch go.mod content from Elastic Agent repository
        print("\n4. Fetching go.mod file content from Elastic Agent repository...")
        gomod_content = fetch_elastic_agent_gomod()
        
        # Step 5: Extract Helm version
        print("\n5. Extracting Helm version...")
        helm_version = extract_helm_version(gomod_content)
        
        # Step 6: Update docset.yml with kube-stack-version
        print("\n6. Updating kube-stack-version in docset.yml...")
        update_docset_yml(kube_stack_version, docset_path)
        
        # Step 7: Update docset.yml with helm-version
        print("\n7. Updating helm-version in docset.yml...")
        update_helm_version(helm_version, docset_path)
        
        print(f"\n✅ Successfully updated:")
        print(f"   - kube-stack-version to {kube_stack_version}")
        print(f"   - helm-version to {helm_version}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()