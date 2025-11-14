```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "\nFROM windows-security-logs\n| WHERE event.code == \"4624\" AND logon.type == \"3\"\n| LOOKUP JOIN asset-inventory ON host.name\n| EVAL time_bucket = DATE_TRUNC(30 minute, @timestamp)\n| STATS unique_hosts = COUNT_DISTINCT(host.name),\n        criticality_levels = COUNT_DISTINCT(asset.criticality),\n        active_periods = COUNT_DISTINCT(time_bucket),\n        first_login = MIN(@timestamp),\n        last_login = MAX(@timestamp) \nBY user.name\n| WHERE unique_hosts > 2\n| EVAL time_span_hours = DATE_DIFF(\"hour\", first_login, last_login)\n| EVAL movement_velocity = ROUND(unique_hosts / (time_span_hours + 1), 2)\n| EVAL lateral_movement_score = unique_hosts * criticality_levels\n| SORT lateral_movement_score DESC \n| LIMIT 1000\n  "
  }
)
print(resp)

```
