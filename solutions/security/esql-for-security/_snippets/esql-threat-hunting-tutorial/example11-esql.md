```esql
FROM process-logs
| WHERE process.name == "powershell.exe" AND process.parent.name LIKE "*word*" <1>
| LOOKUP JOIN asset-inventory ON host.name <2>
| LOOKUP JOIN user-context ON user.name <3>
| EVAL encoded_command = CASE(process.command_line LIKE "*-enc*", true, false) <4>
| WHERE encoded_command == true <5>
| STATS count = COUNT(*) BY host.name, user.name, asset.criticality <6>
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) with [`==`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-equals) and [`LIKE`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-like) operators to detect PowerShell processes 
2. Enriches using [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) with asset inventory
3. Enriches with user context using `LOOKUP JOIN`
4. Uses [`EVAL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-eval) and [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to detect encoded commands
5. Additional filtering with [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) 
6. Aggregates results with [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) and [`COUNT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count) grouped by multiple fields
