---
applies_to:
  stack: all 9.1
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---


# Ingest Qualys VMDR data

The integration now support enumeration in the native vulnerability findings workflow and provide out-of-the-box contextualization as Insights within alert and entity flyouts.

You can enrich your {{elastic-sec}} workflows with third-party vulnerability findings from the Qualys Vulnerability Management, Detection and Response (VMDR) integration. To get set up:

* Follow the steps to [set up the Qualys VMDR integration](https://www.elastic.co/docs/reference/integrations/qualys_vmdr).
* Make sure the integration version is at least 6.5.0

After you’ve completed these steps, Qualys VMDR data will appear on the [Vulnerabilities](/solutions/security/cloud/findings-page-3.md) tab of the Findings page and on the [Vulnerability Management dashboard](/solutions/security/cloud/cnvm-dashboard.md). This data will also appear in the [Insights section](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section) for related alerts.


