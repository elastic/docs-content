```esql
FROM windows-security-logs, process-logs, network-logs <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| WHERE user.name == "jsmith" OR user.name == "admin"
| EVAL event_type = CASE(
    event.code IS NOT NULL, "Authentication",
    process.name IS NOT NULL, "Process Execution",
    destination.ip IS NOT NULL, "Network Activity",
    "Unknown") <2>
| EVAL dest_ip = TO_STRING(destination.ip)
| EVAL attack_stage = CASE(
    process.parent.name LIKE "*word*", "Initial Compromise",
    process.name IN ("net.exe", "nltest.exe"), "Reconnaissance", 
    event.code == "4624" AND logon.type == "3", "Lateral Movement",
    process.name IN ("sqlcmd.exe", "ntdsutil.exe"), "Data Access",
    dest_ip NOT LIKE "10.*", "Exfiltration",
    "Other") <3>
| SORT @timestamp ASC <4>
| KEEP @timestamp, event_type, attack_stage, host.name, asset.criticality, user.name, process.name, destination.ip
| LIMIT 1000
```

1. Uses `FROM` with multiple indices for comprehensive correlation
2. Uses [`IS NOT NULL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#null-predicates) with [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to classify event types from different data sources
3. Uses complex [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) logic  to map events to MITRE ATT&CK stages
4. Uses [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) to build chronological attack timeline
