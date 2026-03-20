sheet2docs - Google Sheets to CSV Sync
======================================

This automation syncs data from a Google Sheet to one or more CSV files in the
docs-content repository. It runs daily at 2 AM UTC and creates/updates a pull
request when the sheet data changes.


How it works
------------

1. GitHub Actions runs the sync workflow daily (or manually).
2. The Python script fetches data from the configured Google Sheet.
3. For each configured output, rows are filtered, sorted, column-selected,
   and written to a CSV file.
4. If any CSV has changed, a PR is created or updated on the
   `automated/sheets-sync` branch.
5. A team member reviews and merges the PR.
6. The updated CSV files are available in the repository.


Configuration formats
---------------------

The script supports two configuration formats in config.yml. Both formats
share the same `source` section.

### Legacy format (single output)

Uses top-level `columns` and `output` keys. This produces a single CSV file.

    source:
      sheet_url: "${GOOGLE_SHEET_URL}"
      tab_name: "Public Model List"

    columns:
      - source: "Author"
      - source: "Name"
      - source: "ID"

    output:
      filename: "models.csv"
      directory: "explore-analyze/elastic-inference"
      delimiter: ","

### Multi-output format

Uses a top-level `outputs` key with a list of output entries. Each entry
generates one CSV file. An optional `defaults` key provides shared values
that are inherited by all outputs (output-level values take precedence).

    source:
      sheet_url: "${GOOGLE_SHEET_URL}"
      tab_name: "Public Model List"

    defaults:
      directory: "explore-analyze/elastic-inference"
      delimiter: ","
      columns:
        - source: "Author"
        - source: "Name"
        - source: "ID"
        - source: "Model Card"

    outputs:
      - filename: "chat-models.csv"
        filter:
          column: "Type"
          values: ["LLM Chat"]
        sort:
          by: "Name"
          direction: "ascending"

      - filename: "embedding-models.csv"
        filter:
          column: "Type"
          values: ["Embedding - Sparse", "Embedding - Dense"]

      - filename: "all-models.csv"
        sort:
          by: "Author"
          direction: "ascending"


Backward compatibility
----------------------

If the config uses the legacy format (top-level `columns` + `output`), the
script behaves exactly as before: one CSV file is generated with no filtering
or sorting. No changes are needed to existing configs.

The two formats cannot be mixed. If both `output` and `outputs` are present,
the script exits with an error.


Configuration reference
-----------------------

### source (required)

    source:
      sheet_url: "..."     # Google Sheets URL or ID (supports ${ENV_VAR})
      tab_name: "..."      # Tab/sheet name within the spreadsheet

### defaults (optional, multi-output only)

Shared settings inherited by all outputs. Any key that is valid inside an
output entry can be placed here. Output-level values override defaults.

    defaults:
      directory: "path/to/output"
      delimiter: ","
      columns:
        - source: "Column Name"

### outputs (list, multi-output only)

Each entry generates one CSV file.

    outputs:
      - filename: "file.csv"           # Required: output filename
        directory: "path/to/output"    # Optional (default: ".")
        delimiter: ","                 # Optional (default: ",")

        columns:                       # Required (or inherited from defaults)
          - source: "Sheet Column"
          - source: "Old Name"
            target: "New Name"         # Optional: rename column in CSV

        filter:                        # Optional: select rows by column value
          column: "Type"               # Column to filter on
          values: ["Value1", "Value2"] # Rows matching any value are included

        sort:                          # Optional: order rows
          by: "Column Name"            # Column to sort by
          direction: "ascending"       # "ascending" (default) or "descending"


Column configuration
--------------------

Columns are defined as a list of dictionaries with `source` and optional
`target` keys:

    columns:
      - source: "Column Name"           # Keep original name
      - source: "Old Name"
        target: "New Name"              # Rename in CSV

Column order in the CSV follows the order in the configuration list, not the
spreadsheet column order.


Row filtering (splitting and grouping)
--------------------------------------

The `filter` option selects rows where a column matches one or more values.

Splitting: one value per output generates separate CSV files by category.

    filter:
      column: "Type"
      values: ["LLM Chat"]

Grouping: multiple values in one output combine categories into a single CSV.

    filter:
      column: "Type"
      values: ["Embedding - Sparse", "Embedding - Dense"]

Omitting `filter` includes all rows.


Row sorting
-----------

The `sort` option orders rows by a column value.

    sort:
      by: "Name"
      direction: "ascending"

- direction: "ascending" (default) or "descending"
- Uses stable sort: rows with equal sort keys preserve their original
  spreadsheet order.
- Sorting is case-insensitive.

Omitting `sort` preserves the original spreadsheet order.


Changing the output location
----------------------------

Edit the `directory` in the output or defaults section:

    defaults:
      directory: "path/to/output"

Note: The workflow automatically detects all generated CSV paths from the
script output. No manual workflow changes are needed when adding or moving
outputs.


Running manually
----------------

1. Go to the Actions tab in GitHub.
2. Select "Sync Google Sheets to CSV".
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

"Filter column 'X' not found in sheet"
  - The column name in filter.column must match a sheet header exactly.

"Sort column 'X' not found in sheet"
  - The column name in sort.by must match a sheet header exactly.

"Config cannot have both 'output'/'columns' and 'outputs'"
  - Use either the legacy format or multi-output format, not both.

"Google Sheets API has not been enabled"
  - Enable Google Sheets API and Drive API in the GCP project.

For detailed GCP setup, see SETUP-KEYLESS.md.
