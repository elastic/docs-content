---
applies_to:
  stack: all 9.1
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---


# Tenable VM  
This page explains how to make data from the Tenable Vulnerability Management integration (Tenable VM) appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts** Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).

::::{NOTE}
Data from this integration does not appear on the [CNVM dashboard](/solutions/security/cloud/cnvm-dashboard.md).
::::

In order for Tenable VM data to appear in these workflows:

- Follow the steps to [set up the Tenable VM integration](https://www.elastic.co/docs/reference/integrations/tenable_io).
- ({{stack}} users) Ensure you're on at least v9.1.
- Make sure the Tenable VM version is at least 6.5.0.

::::{NOTE}
You can ingest data from the Tenable VM integration for other purposes without following these steps.
::::
