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

# Ingest AWS Security Hub data

In order to enrich your {{elastic-sec}} workflows with third-party cloud security posture data collected by AWS Security Hub:

* Follow the steps to [set up the AWS Security Hub integration](https://docs.elastic.co/en/integrations/aws/securityhub).
* Make sure the integration version is at least 2.31.1.
* Ensure you have `read` privileges for the `security_solution-*.misconfiguration_latest` index.
* While configuring the AWS Security Hub integration, turn on **Collect AWS Security Hub Findings from AWS**. We recommend you also set the **Initial Interval** value to `2160h` (equivalent to 90 days) to ingest existing logs.

:::{image} /solutions/images/security-aws-config-finding-logs.png
:alt: AWS Security Hub integration settings showing the findings toggle
:::

After you’ve completed these steps, AWS Security Hub data will appear on the Misconfigurations tab of the [Findings](/solutions/security/cloud/findings-page.md) page.

Any available findings data will also appear in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) for related alerts. If alerts are present for a user or host that has findings data from AWS Security Hub, the findings will appear on the [entity details flyout](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-details-flyout).

