---
navigation_title: Value report
applies_to:
  serverless:
    security: preview
---

# Value Report

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

To access the **Value report** page, you need the **SOC Management** Security sub-feature [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). 

:::{image} /solutions/images/security-value-report-rbac.png
:alt: value report RBAC setting
:screenshot:
:::