```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "\nFROM process-logs\n| WHERE process.name IN (\"powershell.exe\", \"cmd.exe\", \"net.exe\", \"sqlcmd.exe\", \"schtasks.exe\", \"sc.exe\")\n| LOOKUP JOIN asset-inventory ON host.name\n| LOOKUP JOIN user-context ON user.name\n| STATS executions = COUNT(*),\n        unique_hosts = COUNT_DISTINCT(host.name),\n        unique_commands = COUNT_DISTINCT(process.name)\nBY user.name, user.department\n| WHERE executions > 1\n| EVAL usage_pattern = CASE(\n    executions > 5, \"High Usage\",\n    executions > 3, \"Moderate Usage\", \n    \"Low Usage\"\n  )\n| SORT executions DESC\n| LIMIT 1000\n  "
  }
)
print(resp)

```
