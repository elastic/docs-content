% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.esql.query(
    format="txt",
    query="
FROM network-logs
| WHERE NOT CIDR_MATCH(destination.ip, \"10.0.0.0/8\", \"192.168.0.0/16\")
| EVAL indicator.value = TO_STRING(destination.ip)
| LOOKUP JOIN threat-intel ON indicator.value
| LOOKUP JOIN asset-inventory ON host.name
| WHERE threat.name IS NOT NULL
| STATS total_bytes = SUM(network.bytes),
        connection_count = COUNT(*),
        time_span = DATE_DIFF(\"hour\", MIN(@timestamp), MAX(@timestamp))
BY host.name, destination.ip, threat.name, asset.criticality
| EVAL mb_transferred = ROUND(total_bytes / 1048576, 2)
| EVAL risk_score = CASE(
    asset.criticality == \"critical\" AND mb_transferred > 100, 10,
    asset.criticality == \"high\" AND mb_transferred > 100, 7,
    mb_transferred > 50, 5,
    3
  )
| WHERE total_bytes > 1000000
| SORT risk_score DESC, total_bytes DESC
| LIMIT 1000
  ",
)
print(resp)

```
