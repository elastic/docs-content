#!/usr/bin/env python3
"""
Google Sheets to CSV Sync Script

Fetches data from a Google Sheet, filters columns based on configuration,
and generates a CSV file.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
import gspread
import yaml


# Exit codes
EXIT_SUCCESS = 0
EXIT_CONFIG_ERROR = 1
EXIT_AUTH_ERROR = 2
EXIT_SHEET_ERROR = 3
EXIT_DATA_ERROR = 4
EXIT_FILE_ERROR = 5


def substitute_env_vars(obj: Any) -> Any:
    """
    Recursively substitute environment variables in a configuration object.

    Replaces ${VAR_NAME} with the value of the VAR_NAME environment variable.

    Args:
        obj: Configuration object (dict, list, or string)

    Returns:
        Object with environment variables substituted
    """
    if isinstance(obj, dict):
        return {key: substitute_env_vars(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [substitute_env_vars(item) for item in obj]
    elif isinstance(obj, str):
        # Find all ${VAR_NAME} patterns and substitute
        pattern = r'\$\{([^}]+)\}'
        matches = re.findall(pattern, obj)
        result = obj
        for var_name in matches:
            env_value = os.environ.get(var_name)
            if env_value is None:
                print(f"Warning: Environment variable '{var_name}' not set", file=sys.stderr)
                continue
            result = result.replace(f'${{{var_name}}}', env_value)
        return result
    else:
        return obj


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and parse YAML configuration file.

    Supports environment variable substitution for sensitive values.
    Use ${VAR_NAME} in config.yml to reference environment variables.

    Args:
        config_path: Path to YAML config file

    Returns:
        Dictionary containing configuration

    Raises:
        SystemExit: If config file is invalid or missing required fields
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Validate required fields
        if not config:
            print(f"Error: Config file is empty: {config_path}", file=sys.stderr)
            sys.exit(EXIT_CONFIG_ERROR)

        required_fields = ['source', 'columns', 'output']
        for field in required_fields:
            if field not in config:
                print(f"Error: Missing required field '{field}' in config", file=sys.stderr)
                sys.exit(EXIT_CONFIG_ERROR)

        # Substitute environment variables in config
        config = substitute_env_vars(config)

        # Validate source fields
        if 'sheet_url' not in config['source']:
            print("Error: Missing 'sheet_url' in source config", file=sys.stderr)
            sys.exit(EXIT_CONFIG_ERROR)

        if 'tab_name' not in config['source']:
            print("Error: Missing 'tab_name' in source config", file=sys.stderr)
            sys.exit(EXIT_CONFIG_ERROR)

        # Validate columns
        if not isinstance(config['columns'], list) or len(config['columns']) == 0:
            print("Error: 'columns' must be a non-empty list", file=sys.stderr)
            sys.exit(EXIT_CONFIG_ERROR)

        for i, col in enumerate(config['columns']):
            if not isinstance(col, dict):
                print(f"Error: Column {i} must be a dictionary", file=sys.stderr)
                sys.exit(EXIT_CONFIG_ERROR)
            if 'source' not in col:
                print(f"Error: Column {i} missing 'source' field", file=sys.stderr)
                sys.exit(EXIT_CONFIG_ERROR)

        # Validate output
        if 'filename' not in config['output']:
            print("Error: Missing 'filename' in output config", file=sys.stderr)
            sys.exit(EXIT_CONFIG_ERROR)

        print(f"✓ Loaded config from {config_path}")
        return config

    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(EXIT_CONFIG_ERROR)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in config file: {e}", file=sys.stderr)
        sys.exit(EXIT_CONFIG_ERROR)


def authenticate_google_sheets(credentials_path: Optional[str] = None) -> gspread.Client:
    """
    Authenticate with Google Sheets API.

    Supports multiple authentication methods:
    - Explicit service account JSON file (via --credentials flag)
    - Workload Identity Federation (via GOOGLE_APPLICATION_CREDENTIALS)
    - Application Default Credentials (gcloud auth)

    Args:
        credentials_path: Path to service account JSON file, or None to use
                         Application Default Credentials

    Returns:
        Authenticated gspread client

    Raises:
        SystemExit: If authentication fails
    """
    try:
        # Define required scopes
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]

        if credentials_path:
            # Explicit service account JSON file provided
            creds = ServiceAccountCredentials.from_service_account_file(
                credentials_path, scopes=scopes
            )
            client = gspread.authorize(creds)
        else:
            # Check for GOOGLE_APPLICATION_CREDENTIALS
            creds_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if not creds_file:
                print("Error: No credentials provided. Set GOOGLE_APPLICATION_CREDENTIALS "
                      "or use --credentials flag", file=sys.stderr)
                sys.exit(EXIT_AUTH_ERROR)

            # Load credentials file to check its type
            with open(creds_file, 'r') as f:
                creds_data = json.load(f)

            # Check if it's a service account or other type (WIF, ADC, etc.)
            creds_type = creds_data.get('type', '')

            if creds_type == 'service_account':
                # Standard service account JSON
                creds = ServiceAccountCredentials.from_service_account_file(
                    creds_file, scopes=scopes
                )
                client = gspread.authorize(creds)

            else:
                # For external_account (WIF) and other types, use google.auth.default()
                # which properly handles service account impersonation
                from google.auth.transport.requests import AuthorizedSession
                print(f"  Credential type in file: {creds_type}")
                creds, project = google.auth.default(scopes=scopes)
                print(f"  Loaded credential class: {type(creds).__name__}")
                creds.refresh(Request())
                print(f"  Token after refresh: {creds.token[:20] if creds.token else 'NO TOKEN'}...")
                client = gspread.Client(auth=creds)
                client.session = AuthorizedSession(creds)

        print("✓ Authenticated with Google Sheets API")
        return client

    except FileNotFoundError as e:
        print(f"Error: Credentials file not found: {e}", file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in credentials file: {e}", file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)
    except Exception as e:
        print(f"Error: Authentication failed: {e}", file=sys.stderr)
        sys.exit(EXIT_AUTH_ERROR)


def column_index_to_letter(col_idx: int) -> str:
    """
    Convert 1-based column index to A1 notation (A, B, C, ..., Z, AA, AB, etc.).
    
    Args:
        col_idx: 1-based column index (1 = A, 2 = B, etc.)
        
    Returns:
        Column letter(s) in A1 notation
    """
    col_letter = ''
    temp_col = col_idx
    while temp_col > 0:
        temp_col -= 1
        col_letter = chr(65 + (temp_col % 26)) + col_letter
        temp_col //= 26
    return col_letter


def extract_sheet_id(sheet_url: str) -> str:
    """
    Extract spreadsheet ID from Google Sheets URL or return as-is if already an ID.

    Args:
        sheet_url: Google Sheets URL or spreadsheet ID

    Returns:
        Spreadsheet ID
    """
    # If it's already just an ID (no slashes or dots), return it
    if '/' not in sheet_url and '.' not in sheet_url:
        return sheet_url

    # Extract ID from URL
    # Format: https://docs.google.com/spreadsheets/d/{ID}/edit...
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
    if match:
        return match.group(1)

    # If no match, assume it's already an ID
    return sheet_url


def get_hyperlinks_from_sheets_api(
    credentials: Any,
    sheet_id: str,
    tab_name: str
) -> Dict[str, str]:
    """
    Fetch hyperlink metadata from Google Sheets API v4.
    
    Args:
        credentials: Google credentials object
        sheet_id: Spreadsheet ID
        tab_name: Name of the worksheet/tab
        
    Returns:
        Dictionary mapping cell addresses (A1 notation) to hyperlink URLs
    """
    try:
        # Build the Sheets API service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get all cells with hyperlinks using includeGridData
        result = service.spreadsheets().get(
            spreadsheetId=sheet_id,
            ranges=[f"{tab_name}!A:ZZ"],  # Get all columns
            includeGridData=True
        ).execute()
        
        hyperlinks = {}
        
        # Find the correct sheet in the result
        for sheet_data in result.get('sheets', []):
            sheet_props = sheet_data.get('properties', {})
            if sheet_props.get('title') == tab_name:
                # Get the grid data
                grid_data = sheet_data.get('data', [])
                if not grid_data:
                    continue
                
                row_data_list = grid_data[0].get('rowData', [])
                
                for row_idx, row_data in enumerate(row_data_list, start=1):
                    cell_values = row_data.get('values', [])
                    
                    for col_idx, cell in enumerate(cell_values, start=1):
                        # Convert column index to letter (A, B, C, etc.)
                        col_letter = column_index_to_letter(col_idx)
                        cell_address = f"{col_letter}{row_idx}"
                        
                        url = None
                        
                        # Check for hyperlink at cell level (most common for formatted links)
                        if 'hyperlink' in cell:
                            url = cell['hyperlink']
                        
                        # Check in textFormatRuns (rich text with links)
                        if not url:
                            text_format_runs = cell.get('textFormatRuns', [])
                            for run in text_format_runs:
                                link = run.get('format', {}).get('link', {})
                                if 'uri' in link:
                                    url = link['uri']
                                    break
                        
                        # Check in effectiveFormat.textFormat.link
                        if not url:
                            effective_format = cell.get('effectiveFormat', {})
                            text_format = effective_format.get('textFormat', {})
                            link = text_format.get('link', {})
                            if 'uri' in link:
                                url = link['uri']
                        
                        # Check in userEnteredFormat.textFormat.link
                        if not url:
                            user_format = cell.get('userEnteredFormat', {})
                            text_format = user_format.get('textFormat', {})
                            link = text_format.get('link', {})
                            if 'uri' in link:
                                url = link['uri']
                        
                        if url:
                            hyperlinks[cell_address] = url
        
        return hyperlinks
        
    except Exception as e:
        print(f"Warning: Could not fetch hyperlinks: {e}", file=sys.stderr)
        return {}


def format_cell_with_hyperlink(
    cell_value: str,
    cell_address: str,
    hyperlinks: Dict[str, str]
) -> str:
    """
    Format a cell value as Markdown link if it has a hyperlink.
    
    Args:
        cell_value: The text value of the cell
        cell_address: Cell address in A1 notation (e.g., "A1")
        hyperlinks: Dictionary mapping cell addresses to URLs
        
    Returns:
        Formatted string: Markdown link if hyperlink exists, otherwise plain text
    """
    if cell_address in hyperlinks and hyperlinks[cell_address]:
        url = hyperlinks[cell_address]
        # Escape brackets in text to avoid breaking Markdown
        text = cell_value.replace('[', '\\[').replace(']', '\\]')
        return f"[{text}]({url})"
    return cell_value


def fetch_sheet_data(
    client: gspread.Client,
    sheet_url: str,
    tab_name: str
) -> List[Dict[str, Any]]:
    """
    Fetch all data from specified Google Sheet tab, preserving hyperlinks as Markdown.

    Args:
        client: Authenticated gspread client
        sheet_url: Google Sheets URL or spreadsheet ID
        tab_name: Name of the tab/sheet within the spreadsheet

    Returns:
        List of dictionaries, where each dict represents a row with column headers as keys.
        Cells with hyperlinks are formatted as Markdown links [text](url).

    Raises:
        SystemExit: If sheet cannot be accessed or tab not found
    """
    try:
        # Extract sheet ID from URL
        sheet_id = extract_sheet_id(sheet_url)

        # Open spreadsheet
        spreadsheet = client.open_by_key(sheet_id)
        print(f"✓ Opened spreadsheet: {spreadsheet.title}")

        # Get specific worksheet/tab
        try:
            worksheet = spreadsheet.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            available_sheets = [ws.title for ws in spreadsheet.worksheets()]
            print(f"Error: Tab '{tab_name}' not found in spreadsheet", file=sys.stderr)
            print(f"Available tabs: {', '.join(available_sheets)}", file=sys.stderr)
            sys.exit(EXIT_SHEET_ERROR)

        print(f"✓ Found tab: {tab_name}")

        # Get credentials from the client for API access
        credentials = None
        try:
            # Try to get credentials from the client's session
            if hasattr(client, 'session') and hasattr(client.session, 'credentials'):
                credentials = client.session.credentials
            elif hasattr(client, 'auth'):
                credentials = client.auth
            else:
                # Fall back to default credentials
                credentials, _ = google.auth.default()
        except Exception as e:
            print(f"Warning: Could not get credentials for hyperlink extraction: {e}", file=sys.stderr)
            credentials = None

        # Fetch hyperlinks if credentials are available
        hyperlinks = {}
        if credentials:
            print("✓ Fetching hyperlink metadata...")
            hyperlinks = get_hyperlinks_from_sheets_api(credentials, sheet_id, tab_name)
            if hyperlinks:
                print(f"✓ Found {len(hyperlinks)} cells with hyperlinks")
            else:
                print("  No hyperlinks found in sheet")
        else:
            print("⚠ Continuing without hyperlink extraction (links will be plain text)")

        # Get all records (returns list of dicts with headers as keys)
        data = worksheet.get_all_records()
        print(f"✓ Fetched {len(data)} rows")

        if len(data) == 0:
            print("Warning: Sheet has no data rows (may only have headers)", file=sys.stderr)
            return []

        # Get the range to map cell addresses
        all_values = worksheet.get_all_values()
        headers = all_values[0] if all_values else []
        
        # Process each row and format cells with hyperlinks
        formatted_data = []
        for row_idx, row_data in enumerate(data, start=2):  # Start at 2 (row 1 is headers)
            formatted_row = {}
            for col_idx, header in enumerate(headers, start=1):
                # Convert column index to letter (A, B, C, etc.)
                col_letter = column_index_to_letter(col_idx)
                cell_address = f"{col_letter}{row_idx}"
                
                # Get cell value
                cell_value = row_data.get(header, '')
                
                # Format with hyperlink if available
                formatted_value = format_cell_with_hyperlink(cell_value, cell_address, hyperlinks)
                formatted_row[header] = formatted_value
            
            formatted_data.append(formatted_row)

        return formatted_data

    except gspread.SpreadsheetNotFound:
        print(f"Error: Spreadsheet not found: {sheet_url}", file=sys.stderr)
        print("Make sure the sheet is shared with the service account email", file=sys.stderr)
        sys.exit(EXIT_SHEET_ERROR)
    except gspread.exceptions.APIError as e:
        print(f"Error: Google Sheets API error: {e}", file=sys.stderr)
        sys.exit(EXIT_SHEET_ERROR)
    except Exception as e:
        import traceback
        print(f"Error: Failed to fetch sheet data: {type(e).__name__}: {e}", file=sys.stderr)
        print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)
        sys.exit(EXIT_SHEET_ERROR)


def filter_columns(
    data: List[Dict[str, Any]],
    column_config: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """
    Filter data to only include configured columns and apply renaming.

    Args:
        data: List of row dictionaries from Google Sheets
        column_config: List of column configurations with 'source' and optional 'target'

    Returns:
        List of row dictionaries with only configured columns

    Raises:
        SystemExit: If a configured column doesn't exist in the data
    """
    if not data:
        return []

    # Check that all configured columns exist
    available_columns = set(data[0].keys()) if data else set()
    for col_conf in column_config:
        source_col = col_conf['source']
        if source_col not in available_columns:
            print(f"Error: Column '{source_col}' not found in sheet", file=sys.stderr)
            print(f"Available columns: {', '.join(sorted(available_columns))}", file=sys.stderr)
            sys.exit(EXIT_DATA_ERROR)

    # Build mapping of source -> target column names
    column_mapping = {}
    for col_conf in column_config:
        source = col_conf['source']
        target = col_conf.get('target', source)  # Use source as target if not specified
        column_mapping[source] = target

    # Filter and rename columns
    filtered_data = []
    for row in data:
        filtered_row = {}
        for source, target in column_mapping.items():
            filtered_row[target] = row[source]
        filtered_data.append(filtered_row)

    print(f"✓ Filtered to {len(column_mapping)} columns")
    return filtered_data


def write_csv(
    data: List[Dict[str, Any]],
    output_path: str,
    delimiter: str = ','
) -> None:
    """
    Write data to CSV file.

    Args:
        data: List of row dictionaries
        output_path: Path where CSV should be written
        delimiter: CSV delimiter character (default: comma)

    Raises:
        SystemExit: If file cannot be written
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Write CSV
        if not data:
            print("Warning: No data to write to CSV", file=sys.stderr)
            # Write empty file with just headers
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write('')
            return

        # Get field names from first row
        fieldnames = list(data[0].keys())

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)

        # Get file size
        file_size = os.path.getsize(output_path)
        file_size_kb = file_size / 1024

        print(f"✓ Wrote CSV to {output_path} ({file_size_kb:.1f} KB)")

    except PermissionError:
        print(f"Error: Permission denied writing to {output_path}", file=sys.stderr)
        sys.exit(EXIT_FILE_ERROR)
    except Exception as e:
        print(f"Error: Failed to write CSV: {e}", file=sys.stderr)
        sys.exit(EXIT_FILE_ERROR)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Sync Google Sheets data to CSV file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using environment variable for credentials
  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
  python sync_sheet.py --config config.yml

  # Using credentials flag
  python sync_sheet.py --config config.yml --credentials /path/to/credentials.json
        """
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--credentials',
        help='Path to Google service account credentials JSON file '
             '(defaults to GOOGLE_APPLICATION_CREDENTIALS env var)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Authenticate
    client = authenticate_google_sheets(args.credentials)

    # Fetch data
    data = fetch_sheet_data(
        client,
        config['source']['sheet_url'],
        config['source']['tab_name']
    )

    # Filter columns
    filtered_data = filter_columns(data, config['columns'])

    # Prepare output path
    output_dir = config['output'].get('directory', '.')
    output_filename = config['output']['filename']
    output_path = os.path.join(output_dir, output_filename)

    # Get delimiter
    delimiter = config['output'].get('delimiter', ',')

    # Write CSV
    write_csv(filtered_data, output_path, delimiter)

    print("✓ CSV file generated successfully")
    sys.exit(EXIT_SUCCESS)


if __name__ == '__main__':
    main()
