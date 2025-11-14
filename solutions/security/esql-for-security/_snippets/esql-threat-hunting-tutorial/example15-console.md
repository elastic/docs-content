```console
POST /_query?format=txt
{
  "query": """
FROM process-logs
| WHERE process.name IN ("powershell.exe", "cmd.exe", "net.exe", "sqlcmd.exe", "schtasks.exe", "sc.exe")
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| STATS executions = COUNT(*),
        unique_hosts = COUNT_DISTINCT(host.name),
        unique_commands = COUNT_DISTINCT(process.name)
BY user.name, user.department
| WHERE executions > 1
| EVAL usage_pattern = CASE(
    executions > 5, "High Usage",
    executions > 3, "Moderate Usage", 
    "Low Usage"
  )
| SORT executions DESC
| LIMIT 1000
  """
}
```
