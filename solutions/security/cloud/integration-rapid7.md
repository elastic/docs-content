---
applies_to:
  stack: all 
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---


# Rapid7
This page explains how to make data from the Rapid7 InsightVM integration (Rapid7) appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts** Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).

::::{NOTE}
Data from this integration does not appear on the [CNVM dashboard](/solutions/security/cloud/cnvm-dashboard.md).
::::

In order for Rapid7 data to appear in these workflows:

- Follow the steps to [set up the Rapid7 integration](https://www.elastic.co/docs/reference/integrations/tenable_io).
  - While configuring the integration, in the **Host detection data** section, under **Input parameters**, enter `host_metadata=all`. This enables the ingest of `cloud.*` fields.
- ({{stack}} users) Ensure you're on at least v9.1.
- Make sure the Rapid7 version is at least 2.0.0.

::::{NOTE}
You can ingest data from the Rapid7 integration for other purposes without following these steps.
::::
