% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```ruby
response = client.esql.query(
  format: "txt",
  body: {
    "query": "
FROM windows-security-logs, process-logs, network-logs
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| WHERE user.name == \"jsmith\" OR user.name == \"admin\"
| EVAL event_type = CASE(
    event.code IS NOT NULL, \"Authentication\",
    process.name IS NOT NULL, \"Process Execution\",
    destination.ip IS NOT NULL, \"Network Activity\",
    \"Unknown\")
| EVAL dest_ip = TO_STRING(destination.ip)
| EVAL attack_stage = CASE(
    process.parent.name LIKE \"*word*\", \"Initial Compromise\",
    process.name IN (\"net.exe\", \"nltest.exe\"), \"Reconnaissance\", 
    event.code == \"4624\" AND logon.type == \"3\", \"Lateral Movement\",
    process.name IN (\"sqlcmd.exe\", \"ntdsutil.exe\"), \"Data Access\",
    dest_ip NOT LIKE \"10.*\", \"Exfiltration\",
    \"Other\")
| SORT @timestamp ASC
| KEEP @timestamp, event_type, attack_stage, host.name, asset.criticality, user.name, process.name, destination.ip
| LIMIT 1000
  "
  }
)
print(resp)

```
