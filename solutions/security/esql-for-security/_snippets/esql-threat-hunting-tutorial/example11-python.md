% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.esql.query(
    format="txt",
    query="
FROM process-logs
| WHERE process.name == \"powershell.exe\" AND process.parent.name LIKE \"*word*\"
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| EVAL encoded_command = CASE(process.command_line LIKE \"*-enc*\", true, false)
| WHERE encoded_command == true
| STATS count = COUNT(*) BY host.name, user.name, asset.criticality
| LIMIT 1000
  ",
)
print(resp)

```
