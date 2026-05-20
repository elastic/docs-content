---
applies_to:
  stack: ga 9.3+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# AWS Security Hub
This integration uses the AWS Security Hub API to ingest vulnerability findings which appear in Elastic’s native vulnerability workflows. This page explains how to make data from the AWS Security Hub integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab.
- **Alert and Entity details flyouts**: Data appears in the Insights section of the [Alert](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) and [Entity](/solutions/security/advanced-entity-analytics/view-entity-details.md#insights) details flyouts.

In order for AWS Security Hub data to appear in these workflows:

* Follow the steps to [set up the AWS Security Hub integration](https://www.elastic.co/docs/reference/integrations/aws_securityhub).
* Ensure you have `read` privileges for the `security_solution-*.vulnerability_latest` index.

::::{note}
You can ingest data from the AWS Security Hub integration for other purposes without following these steps.
::::
