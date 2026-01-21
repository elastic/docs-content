# sheet2docs

Automated Google Sheets to CSV synchronization for Elastic documentation.

## Overview

This tool syncs data from a Google Sheet and generates a CSV file that can be included in documentation. The system runs daily through GitHub Actions and creates pull requests when the data changes, allowing for review before the changes go live.

## Quick start

### Accessing the CSV

The generated CSV file is available at:

```
https://raw.githubusercontent.com/elastic/docs-content/main/explore-analyze/ai-features/agent-builder/models.csv
```

### Using in documentation

Include the CSV in Markdown files using the `csv-table` directive:

```markdown
:::{csv-table}
:file: models.csv
:header-rows: 1
:::
```

## How it works

```
Google Sheets (source of truth)
         ↓
[Python script syncs data daily]
         ↓
      CSV file
         ↓
[Pull request created if changed]
         ↓
[Review and merge]
         ↓
[Public CSV via raw.githubusercontent.com]
```

## Features

- **Automated sync**: Runs daily at 2 AM UTC.
- **Pull request workflow**: Changes are reviewed before going live.
- **Column filtering**: Only include specific columns from the sheet.
- **Column renaming**: Transform column names for documentation.
- **Manual trigger**: Run sync on-demand via GitHub Actions UI.
- **Keyless auth**: Uses Workload Identity Federation (no stored credentials).

## File structure

```
scripts/sheet2docs/
├── config.yml          # Column mappings and output settings
├── sync_sheet.py       # Python sync script
├── requirements.txt    # Python dependencies
├── SETUP-KEYLESS.md    # GCP authentication setup guide
└── readme.md           # This file

.github/workflows/
└── sync-sheets-keyless.yml   # GitHub Actions workflow
```

## Configuration

The sync behavior is controlled by `config.yml`:

```yaml
source:
  sheet_url: "${GOOGLE_SHEET_URL}"  # From GitHub secret
  tab_name: "Models"

columns:
  - source: "Type"
  - source: "Author"
  - source: "Name"
  - source: "ID"

output:
  filename: "models.csv"
  directory: "explore-analyze/ai-features/agent-builder"
```

### Adding or changing columns

1. Edit `config.yml` to add/remove columns.
2. Column names must match the Google Sheet header exactly (case-sensitive).
3. Optionally rename columns with `target`:

```yaml
columns:
  - source: "Original Name"
    target: "New Name"
```

## Authentication

This tool uses **Workload Identity Federation** (keyless auth) for secure, credential-free authentication to Google Cloud.

### Required GitHub configuration

| Type | Name | Description |
|------|------|-------------|
| Secret | `GOOGLE_SHEET_URL` | Full URL of the Google Sheet |
| Variable | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider resource name |
| Variable | `GCP_SERVICE_ACCOUNT` | Service account email |

For detailed GCP setup, see [SETUP-KEYLESS.md](SETUP-KEYLESS.md).

### Google Sheet access

The Google Sheet must be shared with the service account email (Viewer permission).

## Workflow

### Scheduled sync

The workflow runs automatically daily at 2 AM UTC:

1. Fetches latest data from Google Sheet.
2. Generates CSV file.
3. If changes detected:
   - Creates new branch.
   - Commits CSV changes.
   - Opens pull request.
4. Team reviews and merges PR.
5. Updated CSV is publicly available.

### Manual sync

Trigger a sync manually through GitHub Actions:

1. Go to **Actions** tab in GitHub.
2. Select **Sync Google Sheets to CSV (Keyless Auth)** workflow.
3. Click **Run workflow**.
4. Optionally enable **Dry run** to test without creating a PR.

### Example output

```
✓ Loaded config from config.yml
✓ Authenticated with Google Sheets API
✓ Opened spreadsheet: Your Spreadsheet
✓ Found tab: Models
✓ Fetched 42 rows
✓ Filtered to 4 columns
✓ Wrote CSV to explore-analyze/ai-features/agent-builder/models.csv
✓ CSV file generated successfully
```
