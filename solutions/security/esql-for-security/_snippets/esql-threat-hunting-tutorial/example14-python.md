```python
resp = client.esql.query(
    format="txt",
    query="\nFROM windows-security-logs, process-logs, network-logs\n| LOOKUP JOIN asset-inventory ON host.name\n| LOOKUP JOIN user-context ON user.name\n| WHERE user.name == \"jsmith\" OR user.name == \"admin\"\n| EVAL event_type = CASE(\n    event.code IS NOT NULL, \"Authentication\",\n    process.name IS NOT NULL, \"Process Execution\",\n    destination.ip IS NOT NULL, \"Network Activity\",\n    \"Unknown\")\n| EVAL dest_ip = TO_STRING(destination.ip)\n| EVAL attack_stage = CASE(\n    process.parent.name LIKE \"*word*\", \"Initial Compromise\",\n    process.name IN (\"net.exe\", \"nltest.exe\"), \"Reconnaissance\", \n    event.code == \"4624\" AND logon.type == \"3\", \"Lateral Movement\",\n    process.name IN (\"sqlcmd.exe\", \"ntdsutil.exe\"), \"Data Access\",\n    dest_ip NOT LIKE \"10.*\", \"Exfiltration\",\n    \"Other\")\n| SORT @timestamp ASC\n| KEEP @timestamp, event_type, attack_stage, host.name, asset.criticality, user.name, process.name, destination.ip\n| LIMIT 1000\n  ",
)
print(resp)

```
