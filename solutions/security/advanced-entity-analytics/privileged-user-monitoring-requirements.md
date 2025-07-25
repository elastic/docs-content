---
applies_to:
  stack: preview 9.1
products:
  - id: security
  - id: cloud-serverless
---

# Privileged user monitoring requirements

This page covers the requirements for using the privileged user monitoring feature, as well as its known limitations.

* Privileged user monitoring feature requires the appropriate [subscription](https://www.elastic.co/pricing).

* To enable this feature, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#access-privileged-user-monitoring).

* To use these features , your role must have certain [privileges](#privmon_privs).

## Privileges [privmon_privs]

| Action | Index Privileges | Kibana Privileges |
| ------ | ---------------- | ----------------- |
| Enable the privileged user monitoring feature | N/A | **All** for the **Security** feature |
| View the Privileged user monitoring dashboard | `Read` for the following indices:<br> - `.entity_analytics.monitoring.users-<space-id>`<br> - `risk-score.risk-score-*`<br> - `.alerts-security.alerts-<space-id>`<br> -  `.ml-anomalies-shared`<br> - Security data view indices | **Read** for the **Security** feature |

## Known limitations

* Currently, none of the privileged user monitoring visualizations support [cross-cluster search](/solutions/search/cross-cluster-search.md) as part of the data that they query from. 

* You can define up to 10,000 privileged users per data source.

