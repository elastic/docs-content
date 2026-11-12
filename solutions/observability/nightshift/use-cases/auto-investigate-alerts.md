---
navigation_title: Automatically investigate your alerts
applies_to:
  serverless:
    observability: preview
description: Create an Elastic nightshift automation that investigates each matching alert when it fires and posts the findings to a Slack channel.
products:
  - id: observability
  - id: cloud-serverless
---

# Automatically investigate your alerts [nightshift-auto-investigate-alerts]

Have every important alert investigated before anyone opens it. An automation starts a {{nightshift}} investigation when a matching alert fires and posts the findings in a Slack thread, so the likely cause and proposed actions are waiting for the on-call engineer.

## Before you begin [nightshift-uc-auto-before]

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable).
- You have the privileges to create automations. Without them, you can only view automations. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-admin).
- The alert rules that you want to cover are in the same project as {{nightshift}}. For alerts from other tools, refer to [Investigate alerts from your other tools](./external-alerts.md).
- To post to Slack, an admin has connected the channel. Refer to [Slack](../investigation/set-up.md#nightshift-set-up-slack).

New to investigations? Start a few yourself first, so you know what the results look like. Refer to [Investigate your alerts](./investigate-alerts.md).

## Example: critical checkout alerts [nightshift-uc-auto-example]

Your checkout alert rules have the tag `checkout`. You want every **Critical** alert from them investigated, with the findings posted to `#checkout-oncall`.

1. A rule tagged `checkout` fires an alert with severity **Critical**.
1. The automation checks that the alert matches and that no daily limit is reached.
1. If it does, {{nightshift}} starts an investigation and posts a message in `#checkout-oncall`.
1. When the investigation finishes, {{nightshift}} replies in that message's thread with the impact, the conclusion, and the hypotheses.
1. If it doesn't, the automation skips the alert and records why in its **Run history**.

## Create the automation [nightshift-uc-auto-create]

1. On the {{nightshift}} home page, select **Automations**, then select **Create automation**.
1. Enter a **Name**, for example `Investigate critical checkout alerts`. Optionally, add a **Description** and **Tags**.
1. Under **Trigger**, select **Add trigger**, then **Alert triggered**. The trigger reads as a sentence: **When an alert** from **Any rule** from **any source** changes to **Active** with severity **Any severity**.

   :::{image} ../../../images/nightshift-automation-create-trigger.png
   :alt: The Create automation flyout with Name, Description, and Tags, and the Add trigger menu open with Alert triggered under Elastic, New message in channel under Slack, and Every… under Scheduled
   :screenshot:
   :::

1. Select **Any rule** and choose what to match:
   - Select a tag, such as `checkout`. A tag selects every rule with it, including rules that you add later.
   - Or select individual rules by name.
1. Optionally, select **any source** to limit where alerts come from: **Classic** rules, **Universal rules**, **Significant events**, or **External sources**.
1. Select **Any severity** and select **Critical**. Only the severities that the selected rules support are available. {{nightshift}} checks the severity once, when the alert becomes active; later changes don't start an investigation.
1. Set the **Daily trigger limit**. Refer to [Daily trigger limit](../investigation/automations.md#nightshift-automations-daily-limit).
1. In **Additional Instructions**, tell {{nightshift}} about these services. Refer to [Point {{nightshift}} to your runbooks and code](#nightshift-uc-auto-instructions).
1. Under **Actions**, select **Add action**, then **Post in Slack**. Search for `#checkout-oncall` and select it. If no channels are listed, select **Connect channels in Settings**.
1. Select **Save and enable**. To save it turned off instead, select **Save**.

The automation now appears on the **Automations** page with **Enabled** on. To pause it, turn off **Enabled**.

## Check the deployment-wide limits [nightshift-uc-auto-limits]

Deployment-wide limits apply on top of the automation's own limit, and the lowest limit wins. Refer to [How a start is checked](../investigation/limits.md#nightshift-limits-check).

## Point {{nightshift}} to your runbooks and code [nightshift-uc-auto-instructions]

Each investigation that the automation starts reads its **Additional Instructions**, up to 5,000 characters. Include:

- **Where things live**: the GitHub repositories for the services and their deployment configuration.
- **Runbooks**: links to the runbooks for these alerts, and the checks your team does first.
- **Ownership**: who owns each service and its dependencies.
- **What's normal**: known noisy periods, planned jobs, or dependencies that often cause trouble.

For the checkout alerts in the example:

```text
Checkout runs on the web service and calls inventory-api, which uses the
Postgres encore database. Code: github.com/example/web and
github.com/example/inventory-api. Helm charts are in deploy/helm.
Runbook: https://wiki.example.com/runbooks/checkout.
The payments team owns web; the inventory team owns inventory-api.
A reconcile-batch job runs every hour on the hour and can hold row locks.
```

## Check what the automation did [nightshift-uc-auto-runs]

On the **Automations** page, select the automation, then **Run history**. A skipped run shows why. Refer to [Check what an automation did](../investigation/automations.md#nightshift-automations-run-history).

:::{image} ../../../images/nightshift-automations-list.png
:alt: The Automations page listing automations with their Successful, Failed, and Skipped run counts, a Today's usage bar against each daily trigger limit, and an Enabled switch
:screenshot:
:::

% SCREENSHOT: Automation details flyout, Run history tab, with the runs chart, the status filters, and a day with one succeeded run and one skipped run showing "Daily trigger limit of 20 reached".

## Other triggers [nightshift-uc-auto-variants]

To start from a schedule or a Slack message instead, refer to [Triggers](../investigation/automations.md#nightshift-automations-triggers). For alerts that another tool posts in Slack, refer to [Investigate alerts from your other tools](./external-alerts.md).

:::{image} ../../../images/nightshift-automation-details.png
:alt: The details of an automation with a New message in channel trigger for one alerting app. It shows the Enabled switch, Today's usage of 1 of 10, a daily trigger limit of 10 per day that resets at 12:00 AM UTC, Additional Instructions, and a Post in Slack action that replies in the thread of the triggering message
:screenshot:
:::

## Tips [nightshift-uc-auto-tips]

- **Start narrow.** Begin with a few rules that fire a few times a day and matter to someone. Widen it when the results are useful.
- **Read the first results.** Check the hypothesis tree of the first investigations, and improve the instructions where {{nightshift}} looked in the wrong place.
- **Expect one investigation per alert.** A new alert from the same rule starts its own investigation, and automations can't group repeat firings into one. Refer to [One problem, one investigation](../investigation/index.md#nightshift-investigations-dedup).
- **Edit the automation, not its workflow.** Changes apply from the next trigger. Refer to [The workflow behind an automation](../investigation/automations.md#nightshift-automations-workflow).

## Next steps [nightshift-uc-auto-next]

- [Investigate in Slack](./investigate-in-slack.md): Ask follow-up questions in the results thread.
- [Detect problems automatically](./detect-problems.md): Find problems that no alert catches, and investigate them with an automation too.
- [Automations](../investigation/automations.md): Manage, clone, and delete automations, and read every setting.
- [Investigation limits](../investigation/limits.md): Set the daily limits for your deployment.
