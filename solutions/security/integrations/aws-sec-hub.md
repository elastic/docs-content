---
applies_to:
  stack: preview 9.3
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# AWS Security Hub
This integration uses the AWS Security Hub API to ingest vulnerability findings which appear in Elastic’s native vulnerability workflows. This page explains how to make data from the AWS Security Hub integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page.md) tab.
- **Alert and Entity details flyouts**: Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).

In order for AWS Security Hub data to appear in these workflows:

* Follow the steps to [set up the AWS Security Hub integration](https://docs.elastic.co/en/integrations/aws/securityhub link invalid).
* Ensure you have `read` privileges for the `security_solution-*.vulnerabilities_latest` index.
DRAFT? * While configuring the AWS Security Hub integration, turn on **Collect AWS Security Hub Findings from AWS**. We recommend you also set the **Initial Interval** value to `2160h` (equivalent to 90 days) to ingest existing logs.

::::{note}
You can ingest data from the AWS Security Hub integration for other purposes without following these steps.
::::
