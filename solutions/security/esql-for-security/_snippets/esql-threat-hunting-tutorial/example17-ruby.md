% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "\nFROM process-logs\n| WHERE process.name == \"schtasks.exe\" AND process.command_line:\"/create\"\n| LOOKUP JOIN asset-inventory ON host.name\n| LOOKUP JOIN user-context ON user.name\n| EVAL time_bucket = DATE_TRUNC(1 hour, @timestamp)\n| STATS task_creations = COUNT(*),\n        creation_hours = COUNT_DISTINCT(time_bucket)\nBY user.name, host.name, asset.criticality\n| WHERE task_creations > 0\n| EVAL persistence_pattern = CASE(\n    creation_hours > 1, \"Multiple Hours\",\n    task_creations > 1, \"Burst Creation\",\n    \"Single Task\"\n  )\n| SORT task_creations DESC\n| LIMIT 1000\n  "
  }
)
print(resp)

```
