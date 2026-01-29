```esql
FROM windows-security-logs
| WHERE event.code == "4624" AND logon.type == "3" <1>
| LOOKUP JOIN asset-inventory ON host.name
| EVAL time_bucket = DATE_TRUNC(30 minute, @timestamp) <2>
| STATS unique_hosts = COUNT_DISTINCT(host.name),
        criticality_levels = COUNT_DISTINCT(asset.criticality),
        active_periods = COUNT_DISTINCT(time_bucket),
        first_login = MIN(@timestamp),
        last_login = MAX(@timestamp) 
BY user.name <3>
| WHERE unique_hosts > 2
| EVAL time_span_hours = DATE_DIFF("hour", first_login, last_login) <4>
| EVAL movement_velocity = ROUND(unique_hosts / (time_span_hours + 1), 2)
| EVAL lateral_movement_score = unique_hosts * criticality_levels <5>
| SORT lateral_movement_score DESC 
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) for basic authentication filtering
2. Creates time buckets with [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) for temporal analysis
3. Uses [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) with [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) for comprehensive access metrics
4. Uses [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) for duration calculations
5. Uses [`EVAL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-eval) with [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case)for risk scoring
