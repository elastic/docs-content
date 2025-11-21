% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```js
const response = await client.bulk({
  refresh: "wait_for",
  operations: [
    {
      index: {
        _index: "asset-inventory",
      },
    },
    {
      "host.name": "WS-001",
      "asset.criticality": "medium",
      "asset.owner": "IT",
      "asset.department": "finance",
    },
    {
      index: {
        _index: "asset-inventory",
      },
    },
    {
      "host.name": "SRV-001",
      "asset.criticality": "high",
      "asset.owner": "IT",
      "asset.department": "operations",
    },
    {
      index: {
        _index: "asset-inventory",
      },
    },
    {
      "host.name": "DB-001",
      "asset.criticality": "critical",
      "asset.owner": "DBA",
      "asset.department": "finance",
    },
    {
      index: {
        _index: "asset-inventory",
      },
    },
    {
      "host.name": "DC-001",
      "asset.criticality": "critical",
      "asset.owner": "IT",
      "asset.department": "infrastructure",
    },
    {
      index: {
        _index: "user-context",
      },
    },
    {
      "user.name": "jsmith",
      "user.role": "analyst",
      "user.department": "finance",
      "user.privileged": false,
    },
    {
      index: {
        _index: "user-context",
      },
    },
    {
      "user.name": "admin",
      "user.role": "administrator",
      "user.department": "IT",
      "user.privileged": true,
    },
    {
      index: {
        _index: "threat-intel",
      },
    },
    {
      "indicator.value": "185.220.101.45",
      "indicator.type": "ip",
      "threat.name": "APT-29",
      "threat.severity": "high",
    },
    {
      index: {
        _index: "threat-intel",
      },
    },
    {
      "indicator.value": "powershell.exe",
      "indicator.type": "process",
      "threat.name": "Living off the Land",
      "threat.severity": "medium",
    },
  ],
});
console.log(response);
```
