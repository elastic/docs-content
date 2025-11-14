```esql
FROM network-logs
| WHERE NOT CIDR_MATCH(destination.ip, "10.0.0.0/8", "192.168.0.0/16") <1>
| EVAL indicator.value = TO_STRING(destination.ip) <2>
| LOOKUP JOIN threat-intel ON indicator.value
| LOOKUP JOIN asset-inventory ON host.name
| WHERE threat.name IS NOT NULL
| STATS total_bytes = SUM(network.bytes),
        connection_count = COUNT(*),
        time_span = DATE_DIFF("hour", MIN(@timestamp), MAX(@timestamp)) <3>
BY host.name, destination.ip, threat.name, asset.criticality
| EVAL mb_transferred = ROUND(total_bytes / 1048576, 2) <4>
| EVAL risk_score = CASE(
    asset.criticality == "critical" AND mb_transferred > 100, 10,
    asset.criticality == "high" AND mb_transferred > 100, 7,
    mb_transferred > 50, 5,
    3
  ) <5>
| WHERE total_bytes > 1000000
| SORT risk_score DESC, total_bytes DESC
| LIMIT 1000
```

1. Uses [`CIDR_MATCH`](elasticsearch://reference/query-languages/esql/functions-operators/ip-functions.md#esql-cidr_match) to filter internal IP ranges for external data transfer detection
2. Uses [`TO_STRING`](elasticsearch://reference/query-languages/esql/functions-operators/type-conversion-functions.md#esql-to_string) to standardize IP format for threat intel lookups
3. Uses [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) with `SUM` and `COUNT` to measure data transfer volume over time
4. Uses [`ROUND`](elasticsearch://reference/query-languages/esql/functions-operators/math-functions.md#esql-round) for human-readable values
5. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) for risk scoring based on asset criticality and size of data transferred
