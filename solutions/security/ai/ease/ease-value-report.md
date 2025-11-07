---
navigation_title: Value report
applies_to:
  serverless:
    security: preview
  stack: preview 9.3
---

# Value report

The **Value report** page estimates your savings from using Elastic's AI SOC features for alert triage, in terms of **Analyst time saved** and **Cost Savings**. The message at the top of the page explains how those numbers were determined, and how many alerts were **Escalated** and **Filtered** by AI. 

You can interact with the page in the following ways:

- **Update the time range:** Use the time selector in the upper right corner to select the time range for which to show value metrics.
- **Export report:** Select **Export report** in the upper right corner to download a sharable PDF of the value report.


:::{image} /solutions/images/security-ease-value-report.png
:alt: The Value Report in an EASE project
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