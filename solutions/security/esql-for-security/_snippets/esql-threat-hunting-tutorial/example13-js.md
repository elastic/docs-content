```js
const response = await client.esql.query({
  format: "txt",
  query:
    '\nFROM network-logs\n| WHERE NOT CIDR_MATCH(destination.ip, "10.0.0.0/8", "192.168.0.0/16")\n| EVAL indicator.value = TO_STRING(destination.ip)\n| LOOKUP JOIN threat-intel ON indicator.value\n| LOOKUP JOIN asset-inventory ON host.name\n| WHERE threat.name IS NOT NULL\n| STATS total_bytes = SUM(network.bytes),\n        connection_count = COUNT(*),\n        time_span = DATE_DIFF("hour", MIN(@timestamp), MAX(@timestamp))\nBY host.name, destination.ip, threat.name, asset.criticality\n| EVAL mb_transferred = ROUND(total_bytes / 1048576, 2)\n| EVAL risk_score = CASE(\n    asset.criticality == "critical" AND mb_transferred > 100, 10,\n    asset.criticality == "high" AND mb_transferred > 100, 7,\n    mb_transferred > 50, 5,\n    3\n  )\n| WHERE total_bytes > 1000000\n| SORT risk_score DESC, total_bytes DESC\n| LIMIT 1000\n  ',
});
console.log(response);
```
