---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/building-block-rule.html
  - https://www.elastic.co/guide/en/serverless/current/security-building-block-rules.html
---

# About building block rules

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/building-block-rule.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-building-block-rules.md

Create building block rules when you do not want to see their generated alerts in the UI. This is useful when you want:

* A record of low-risk alerts without producing noise in the Alerts table.
* Rules that execute on the alert indices (`.alerts-security.alerts-<kibana space>`). You can then use building block rules to create hidden alerts that act as a basis for an *ordinary* rule to generate visible alerts.


## Set up rules that run on alert indices [_set_up_rules_that_run_on_alert_indices]

To create a rule that searches alert indices, select **Index Patterns** as the rule’s **Source** and enter the index pattern for alert indices (`.alerts-security.alerts-*`):

:::{image} ../../../images/security-alert-indices-ui.png
:alt: alert indices ui
:class: screenshot
:::


## View building block alerts in the UI [_view_building_block_alerts_in_the_ui]

By default, building block alerts are excluded from the Overview and Alerts pages. You can choose to include building block alerts on the Alerts page, which expands the number of alerts.

1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Alerts table, select **Additional filters** → **Include building block alerts**, located on the far-right.

::::{note}
On a building block rule details page, the rule’s alerts are displayed (by default, **Include building block alerts** is selected).
::::
