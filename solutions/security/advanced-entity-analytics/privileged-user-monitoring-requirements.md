---
applies_to:
  stack: preview 9.1
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Privileged user monitoring requirements

This page covers the requirements for using the privileged user monitoring feature, as well as its known limitations.

* Privileged user monitoring feature requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.

* To enable this feature, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#access-privileged-user-monitoring).

* To use these features in {{stack}}, your role must have certain [privileges](#privmon_privs). In {{serverless-short}}, you need an appropriate [predefined user role](#privmon_roles) or a custom role with the right [privileges](#privmon_privs).

## Privileges [privmon_privs]

| Action | Index Privileges | Kibana Privileges |
| ------ | ---------------- | ----------------- |
| View the Privileged user monitoring dashboard | `Read` for the following indices:<br> - `.entity_analytics.monitoring.users-<space-id>`<br> - `risk-score.risk-score-*`<br> - `.alerts-security.alerts-<space-id>`<br> -  `.ml-anomalies-shared`<br> - security data view indices | **Read** for the **Security** feature |
| Enable the privileged user monitoring feature | TBD | **Read** for the **Security** feature |


## Predefined roles [privmon_roles]
```yaml {applies_to}
serverless: all
```

| Action | Predefined role |
| ------ | --------------- |
| TBD | TBD |
| TBD | TBD |


## Known limitations

* Currently, none of the privileged user monitoring visualizations support [cross-cluster search](/solutions/search/cross-cluster-search.md) as part of the data that they query from. 

* You can define up to 10,000 privileged users per data source.

