---
applies_to:
  stack: ga 9.3
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Prisma Cloud

This page explains how to make data from the Prisma Cloud integration appear in the following places within {{elastic-sec}}:

- **Findings page**: Data appears on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab and the [Misconfiguations](/solutions/security/cloud/findings-page.md) tab.
- **Alert and Entity details flyouts**: Applicable data appears in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section).


In order for Prisma Cloud data to appear in these workflows:

* Follow the steps to [set up the Prisma Cloud integration](https://docs.elastic.co/en/integrations/prisma_cloud).
* Make sure the integration version is at least 4.0.0.
* Ensure you have `read` privileges for the following indices: `security_solution-*.misconfiguration_latest`, `security_solution-*.vulnerability_latest`.



