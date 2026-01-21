sheet2docs - Google Sheets to CSV Sync
======================================

This automation syncs data from a Google Sheet to a CSV file in the docs-content
repository. It runs daily at 2 AM UTC and creates/updates a pull request when
the sheet data changes.


How it works
------------

1. GitHub Actions runs the sync workflow daily (or manually).
2. The Python script fetches data from the configured Google Sheet.
3. If the CSV has changed, a PR is created or updated on the `automated/sheets-sync` branch.
4. A team member reviews and merges the PR.
5. The updated CSV is available in the repository.


Configuration
-------------

Edit `scripts/sheet2docs/config.yml` to configure:

- source.sheet_url: The Google Sheet URL (uses GOOGLE_SHEET_URL secret)
- source.tab_name: The tab/sheet name within the spreadsheet
- columns: Which columns to include and optionally rename
- output.filename: The output CSV filename
- output.directory: Where to save the CSV (relative to repo root)


Adding or removing columns
--------------------------

Edit the `columns` section in config.yml:

    columns:
      - source: "Column Name"           # Keep original name
      - source: "Old Name"
        target: "New Name"              # Rename in CSV


Changing the output location
----------------------------

Edit the `output` section in config.yml:

    output:
      filename: "models.csv"
      directory: "path/to/output"

Note: You must also update the CSV_PATH in the workflow file
(.github/workflows/sync-sheets-keyless.yml) to match.


Running manually
----------------

1. Go to the Actions tab in GitHub.
2. Select "Sync Google Sheets to CSV (Keyless Auth)".
3. Click "Run workflow".
4. Optionally enable "Dry run" to test without creating a PR.


Required GitHub configuration
-----------------------------

Secrets:
- GOOGLE_SHEET_URL: Full URL of the Google Sheet

Variables:
- GCP_WORKLOAD_IDENTITY_PROVIDER: Workload Identity Provider resource name
- GCP_SERVICE_ACCOUNT_EMAIL: Service account email
- GCP_PROJECT_ID: GCP project ID


Google Sheet setup
------------------

The Google Sheet must be shared with the service account email
(Viewer permission). The service account email is the value of
GCP_SERVICE_ACCOUNT_EMAIL.


Troubleshooting
---------------

"Spreadsheet not found"
  - Ensure the sheet is shared with the service account email.
  - Check that GOOGLE_SHEET_URL secret is correct.

"Tab 'X' not found"
  - Verify the tab name matches exactly (case-sensitive).

"Column 'X' not found"
  - Column names must match the sheet headers exactly (case-sensitive).

"Google Sheets API has not been enabled"
  - Enable Google Sheets API and Drive API in the GCP project.

For detailed GCP setup, see SETUP-KEYLESS.md.
