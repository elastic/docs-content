---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-aws-securityhub-data.html
  - https://www.elastic.co/guide/en/serverless/current/ingest-aws-securityhub-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# AWS Security Hub CSPM
This page explains how to make data from the AWS Security Hub CSPM integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Misconfigurations](/solutions/security/cloud/findings-page.md) tab.
- **Alert and Entity details flyouts**: Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).

In order for AWS Security Hub CSPM data to appear in these workflows:

* Follow the steps to [set up the AWS Security Hub CSPM integration](https://docs.elastic.co/en/integrations/aws/securityhub).
* Make sure the integration version is at least 2.31.1. 
* Ensure you have `read` privileges for the `security_solution-*.misconfiguration_latest` index.
* While configuring the AWS Security Hub CSPM integration, turn on **Collect AWS Security Hub CSPM Findings from AWS**. We recommend you also set the **Initial Interval** value to `2160h` (equivalent to 90 days) to ingest existing logs.

:::{image} /solutions/images/security-aws-config-finding-logs.png
:alt: AWS Security Hub CSPM integration settings showing the findings toggle
:::

::::{note}
You can ingest data from the AWS Security Hub CSPM integration for other purposes without following these steps.
::::
