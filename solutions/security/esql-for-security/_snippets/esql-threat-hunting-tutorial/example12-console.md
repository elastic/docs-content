```console
POST /_query?format=txt
{
  "query": """
FROM windows-security-logs
| WHERE event.code == "4624" AND logon.type == "3"
| LOOKUP JOIN asset-inventory ON host.name
| EVAL time_bucket = DATE_TRUNC(30 minute, @timestamp)
| STATS unique_hosts = COUNT_DISTINCT(host.name),
        criticality_levels = COUNT_DISTINCT(asset.criticality),
        active_periods = COUNT_DISTINCT(time_bucket),
        first_login = MIN(@timestamp),
        last_login = MAX(@timestamp) 
BY user.name
| WHERE unique_hosts > 2
| EVAL time_span_hours = DATE_DIFF("hour", first_login, last_login)
| EVAL movement_velocity = ROUND(unique_hosts / (time_span_hours + 1), 2)
| EVAL lateral_movement_score = unique_hosts * criticality_levels
| SORT lateral_movement_score DESC 
| LIMIT 1000
  """
}
```
