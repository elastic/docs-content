---
applies_to:
  stack: ga 9.2
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# AWS Config

This page explains how to make data from the AWS Config integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Misconfigurations](/solutions/security/cloud/findings-page.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.


In order for AWS Config data to appear in these workflows:

* Follow the steps to [set up the AWS Config integration](https://docs.elastic.co/en/integrations/aws/config).
* Make sure the integration version is at least 4.0.0.
* Ensure you have `read` privileges for the following index: `security_solution-*.misconfiguration_latest`.