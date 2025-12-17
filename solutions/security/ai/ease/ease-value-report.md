---
navigation_title: Value report
applies_to:
  serverless:
    security: preview
  stack: preview 9.3
---

# Value report

:::{include} /solutions/_snippets/value-report-intro.md
:::

## Requirements

```{applies_to}
serverless: preview
stack: preview 9.3
```

* To access the **Value report** page, your subscription must include AI-powered features. For {{sec-serverless}}, this means you need either the Elastic AI SOC Engine (EASE) or Security Analytics Complete [feature tier](https://www.elastic.co/pricing/serverless-security).

* To access the **Value report** page, you need the **SOC Management** Security sub-feature [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). 

![value report RBAC setting](/solutions/images/security-value-report-rbac.png "=50%")

::::{note}
The following default roles have the **SOC Management** privilege by default:
- EASE feature tier: ` _search_ai_lake_soc_manager`
- Security Analytics Complete: `admin` and `soc_manager`
::::