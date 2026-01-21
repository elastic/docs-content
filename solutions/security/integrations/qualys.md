---
applies_to:
  stack: all 
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Qualys VMDR

This page explains how to make data from the Qualys Vulnerability Management, Detection and Response integration (Qualys VMDR) appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.

In order for Qualys VMDR data to appear in these workflows:

- Ensure you have read privileges for the following index: `security_solution-*.vulnerability_latest`.
- Follow the steps to [set up the Qualys VMDR integration](https://www.elastic.co/docs/reference/integrations/qualys_vmdr).
  - While configuring the integration, in the **Host detection data** section, under **Input parameters**, enter `host_metadata=all`. This enables the ingest of `cloud.*` fields.
- ({{stack}} users) Ensure you're on at least v8.16.
- Make sure the integration version is at least 6.0.0.

:::{note}
You can ingest data from the Qualys VMDR integration for other purposes without following these steps.
:::
