% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "
FROM process-logs
| WHERE process.name == \"schtasks.exe\" AND process.command_line:\"/create\"
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| EVAL time_bucket = DATE_TRUNC(1 hour, @timestamp)
| STATS task_creations = COUNT(*),
        creation_hours = COUNT_DISTINCT(time_bucket)
BY user.name, host.name, asset.criticality
| WHERE task_creations > 0
| EVAL persistence_pattern = CASE(
    creation_hours > 1, \"Multiple Hours\",
    task_creations > 1, \"Burst Creation\",
    \"Single Task\"
  )
| SORT task_creations DESC
| LIMIT 1000
  "
  }
)
print(resp)

```
