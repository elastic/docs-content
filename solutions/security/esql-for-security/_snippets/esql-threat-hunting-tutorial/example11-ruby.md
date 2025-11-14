```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "\nFROM process-logs\n| WHERE process.name == \"powershell.exe\" AND process.parent.name LIKE \"*word*\"\n| LOOKUP JOIN asset-inventory ON host.name\n| LOOKUP JOIN user-context ON user.name\n| EVAL encoded_command = CASE(process.command_line LIKE \"*-enc*\", true, false)\n| WHERE encoded_command == true\n| STATS count = COUNT(*) BY host.name, user.name, asset.criticality\n| LIMIT 1000\n  "
  }
)
print(resp)

```
