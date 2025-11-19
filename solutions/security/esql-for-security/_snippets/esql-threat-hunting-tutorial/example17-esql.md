```esql
FROM process-logs
| WHERE process.name == "schtasks.exe" AND process.command_line:"/create" <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| EVAL time_bucket = DATE_TRUNC(1 hour, @timestamp) <2>
| STATS task_creations = COUNT(*),
        creation_hours = COUNT_DISTINCT(time_bucket) <3>
BY user.name, host.name, asset.criticality
| WHERE task_creations > 0
| EVAL persistence_pattern = CASE(
    creation_hours > 1, "Multiple Hours",
    task_creations > 1, "Burst Creation",
    "Single Task"
  ) <4>
| SORT task_creations DESC
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) with [`:`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) match operator to detect scheduled task creation (a common persistence mechanism)
2. Uses [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) to group events into hourly time buckets for temporal analysis
3. Uses [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) with `time_bucket` to measure task creation velocity
4. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to classify suspicious patterns based on timing and frequency
