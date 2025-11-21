```esql
FROM process-logs
| WHERE process.name IN ("powershell.exe", "cmd.exe", "net.exe", "sqlcmd.exe", "schtasks.exe", "sc.exe") <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| STATS executions = COUNT(*),
        unique_hosts = COUNT_DISTINCT(host.name),
        unique_commands = COUNT_DISTINCT(process.name) <3>
BY user.name, user.department
| WHERE executions > 1
| EVAL usage_pattern = CASE(
    executions > 5, "High Usage",
    executions > 3, "Moderate Usage", 
    "Low Usage"
  ) <4>
| SORT executions DESC
| LIMIT 1000
```

1. Uses `WHERE...IN` to monitor high-risk system tools
2. Uses [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) with `asset-inventory` and `user-context` indices to enrich events with context
3. Uses [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) to measure breadth of suspicious tool usage
4. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case)to classify usage patterns for anomaly detection
