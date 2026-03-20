---
applies_to:
  stack: ga 9.3, preview 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Monitor privileged user activities

After you [set up privileged user monitoring](/solutions/security/advanced-entity-analytics/privileged-user-monitoring-setup.md), you can start monitoring your privileged users' activity using the different panels on the Privileged user monitoring dashboard.

To get started, find **Privileged user monitoring** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Risk levels of privileged users

When entity risk scoring is enabled, this panel shows the percentages and numbers of privileged users exhibiting risky behaviors that trigger alerts, grouped by their risk levels. This helps you assess how much risk administrative and other privileged users are contributing to your environment’s overall risk posture.

## Privileged users

This panel represents an inventory of privileged users, sourced from your provided [data sources](/solutions/security/advanced-entity-analytics/privileged-user-monitoring-setup.md#manage-data-sources). It gives a rich catalog of users that may be valuable to investigate, and provides additional information, including user risk scores and asset criticality assignment. This table also serves as a window into the users that are currently being monitored for their privileged status from the configured data sources.

## Top privileged access anomalies

The [Privileged Access Detection](integration-docs://reference/pad.md) package contains multiple {{ml}} jobs that can detect anomalous privileged user activity across various systems, such as Windows, Linux, and Okta system logs. You can install this package directly from the Privileged user monitoring dashboard and access the related {{ml}} jobs for any additional configuration.

Once you install the package, this panel displays a heatmap of the top privileged access anomalies performed by your defined privileged users. You can investigate these anomalies further by reviewing details for individual users or by navigating to the Anomaly Explorer.

## Privileged user activity

This panel contains the following tabs:

* **Granted rights**: Monitor when rights are granted. This helps you detect behavior such as over-provisioning or potential insider threats. It also highlights possible misuse of administrative privileges or violations of least-privilege policies.

* **Account switches**: Track when privileged users switch accounts. This can help you proactively identify potential lateral movement or unauthorized access.

* **Authentications**: Review authentication events for privileged users. Frequent authentication shows how actively these privileges are being used, while repeated failed authentication events can indicate attempted unauthorized access.
