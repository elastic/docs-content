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

The privileged user monitoring feature requires:
  * {applies_to}`stack: ` The appropriate [subscription](https://www.elastic.co/subscriptions)
  * {applies_to}`serverless: ` The appropriate [feature tier](https://www.elastic.co/pricing/serverless-security)

To enable this feature, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#access-privileged-user-monitoring).

To use this feature, you need:
  * {applies_to}`stack: ` A role with the appropriate [privileges](#privmon_privs)
  * {applies_to}`serverless: ` Either the appropriate [predefined Security user role](#privmon_roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with the right [privileges](#privmon_privs)

## Privileges [privmon_privs]

| Action | Index Privileges | Kibana Privileges |
| ------ | ---------------- | ----------------- |
| Enable the privileged user monitoring feature | N/A | **All** for the **Security** feature |
| View the Privileged user monitoring dashboard | `Read` for the following indices:<br> - `.entity_analytics.monitoring.users-<space-id>`<br> - `risk-score.risk-score-*`<br> - `.alerts-security.alerts-<space-id>`<br> -  `.ml-anomalies-shared`<br> - Security data view indices | **Read** for the **Security** feature |

## Predefined roles [privmon_roles]
```yaml {applies_to}
serverless: 
```

| Action | Predefined role |
| --- | --- |
| Enable privileged user monitoring | - Platform engineer<br>- Admin |
| View the Privileged user monitoring dashboard | - Tier 1 analyst<br>- Tier 2 analyst<br>- Tier 3 analyst<br>- Rule author<br>- SOC manager<br>- Platform engineer<br>- Detections admin<br>- Admin |

## Known limitations

* Currently, none of the privileged user monitoring visualizations support [cross-cluster search](/explore-analyze/cross-cluster-search.md) as part of the data that they query from. 

* You can define up to 10,000 privileged users per data source.

