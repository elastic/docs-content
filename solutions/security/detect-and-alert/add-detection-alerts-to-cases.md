---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/signals-to-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-signals-to-cases.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Add detection alerts to cases [security-signals-to-cases]

From the Alerts table, you can attach one or more alerts to a [new case](/solutions/security/detect-and-alert/add-detection-alerts-to-cases.md#signals-to-new-cases) or [an existing one](/solutions/security/detect-and-alert/add-detection-alerts-to-cases.md#signals-to-existing-cases). Alerts from any rule type can be added to a case.

::::{note}
* After you add an alert to a case, you can remove it from the case activity under the alert summary or by using the [cases API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-cases).
* Each case can have a maximum of 1,000 alerts.

::::


:::{image} /solutions/images/security-add-alert-to-case.gif
:alt: add alert to case
:screenshot:
:::


## Add alerts to a new case [signals-to-new-cases]

To add alerts to a new case:

1. Do one of the following:

    * To add a single alert to a case, select the **More actions** menu (**…**) in the Alerts table or **Take action** in the alert details flyout, then select **Add to a new case**.
    * To add multiple alerts, select the alerts, then select **Add to a new case** from the **Bulk actions** menu.

2. Give the case a name, assign a severity level, and provide a description. You can use [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) syntax in the case description.

    ::::{note}
    If you do not assign your case a severity level, it will be assigned **Low** by default.
    ::::

3. Optionally, add a category, assignees and relevant tags. You can add users only if they meet the necessary [prerequisites](/explore-analyze/cases/configure-case-access.md).
4. Specify whether you want to sync the status of associated alerts. It is enabled by default; however, you can toggle this setting on or off at any time. If it remains enabled, the alert’s status updates whenever the case’s status is modified.
5. Select a connector. If you’ve previously added one, that connector displays as the default selection. Otherwise, the default setting is `No connector selected`.
6. Click **Create case** after you’ve completed all of the required fields. A confirmation message is displayed with an option to view the new case. Click the link in the notification or go to the Cases page to view the case.

:::{image} /solutions/images/security-add-alert-to-new-case.png
:alt: add alert to new case
:screenshot:
:::


## Add alerts to an existing case [signals-to-existing-cases]

To add alerts to an existing case:

1. Do one of the following:

    * To add a single alert to a case, select the **More actions** menu (**…**) in the Alerts table or **Take action** in the alert details flyout, then select **Add to existing case**.
    * To add multiple alerts, select the alerts, then select **Add to an existing case** from the **Bulk actions** menu.

2. From the **Select case** dialog box, select the case to which you want to attach the alert. A confirmation message is displayed with an option to view the updated case. Click the link in the notification or go to the Cases page to view the case’s details.

    ::::{note}
    If you attach the alert to a case that has been configured to sync its status with associated alerts, the alert’s status updates any time the case’s status is modified.
    ::::


:::{image} /solutions/images/security-add-alert-to-existing-case.png
:alt: Select case dialog listing existing cases
:screenshot:
:::
