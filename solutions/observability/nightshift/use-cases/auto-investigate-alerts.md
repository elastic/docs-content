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

{{nightshift}} can automatically investigate your alerts using automations. An automation starts a investigation when an alert matches the conditions you set up, and posts the findings in a Slack thread, giving the on-call engineer a head start on fixing the problem.

## Before you begin [nightshift-uc-auto-before]

Make sure you meet the following requirements:

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable).
- You have the privileges to create automations. Without them, you can only view automations. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-admin).
- The alert rules that you want to investigate are in the same project as {{nightshift}}. For alerts from other tools, refer to [Investigate alerts from your other tools](./external-alerts.md).
- An admin has connected the Slack channel you want to send investigation results to. Refer to [Set up Slack](../investigation/set-up.md#nightshift-set-up-slack).

Before setting up automations, run some investigations to familiarize yourself with the process and the results. Refer to [Investigate your alerts](./investigate-alerts.md).

## Example: critical checkout alerts [nightshift-uc-auto-example]

In this example scenario, assume your checkout alert rules have the tag `checkout`. You want every **Critical** alert from them investigated, with the findings posted to `#checkout-oncall`.

The process looks something like this:

1. A rule tagged `checkout` fires an alert with severity **Critical**.
1. The automation checks that the alert matches and that no daily limit is reached.
1. {{nightshift}} starts an investigation and posts a message in `#checkout-oncall`.
1. When the investigation finishes, {{nightshift}} replies in that message's thread with the impact, the conclusion, and the hypotheses.

## Create the automation [nightshift-uc-auto-create]

For this process to work, you need to first creating the automation that fires under this scenario:

1. On the {{nightshift}} home page, select **Automations** → **Create custom automation**.
1. Enter a **Name**, for example `Investigate critical checkout alerts`. Optionally, add a **Description** and **Tags**.
1. Under **Trigger**, select **Add trigger** → **Alert triggered**. The trigger reads as a sentence: **When an alert** from **Any rule** from **any source** changes to **Active** with severity **Any severity**.
1. Select **Any rule**, select one of the following:
   - Select a tag, such as `checkout`. Every rule with that tag is selected, including rules that you add later.
   - Select individual rules by name.
1. Optionally, select **any source** to limit where alerts come from: **Classic** rules, **Universal rules**, **Significant events**, or **External sources**.
1. Select **Any severity** and select the alert severity that you want to trigger an investigation. Only the severities that the selected rules support are available. {{nightshift}} checks the severity once, when the alert becomes active; later changes don't start an investigation.
1. Set the **Daily trigger limit**. Refer to [Daily trigger limit](../investigation/automations.md#nightshift-automations-daily-limit).
1. Optionally, in **Additional Instructions**, tell {{nightshift}} about these services. Refer to [Point {{nightshift}} to your runbooks and code](#nightshift-uc-auto-instructions).
1. Under **Actions**, select **Add action** → **Post in Slack**. Search for and select the Slack channel you want to send investigation results to. If no channels are listed, select **Connect channels in Settings**.
1. Select **Save and enable**. To save an automation, but leave it turned off, select **Save**.

The automation now appears on the **Automations** page with **Enabled** on. To pause it, turn off **Enabled**.

## Check the deployment-wide limits [nightshift-uc-auto-limits]

Deployment-wide limits apply on top of the automation's own limit, and the lowest limit wins. Refer to [How a start is checked](../investigation/limits.md#nightshift-limits-check).

## Point {{nightshift}} to your runbooks and code [nightshift-uc-auto-instructions]

Each investigation that the automation starts reads its **Additional Instructions**, up to 5,000 characters. Include information like:

- **Where things live**: the GitHub repositories for the services and their deployment configuration.
- **Runbooks**: links to the runbooks for these alerts, and the checks your team does first.
- **Ownership**: who owns each service and its dependencies.
- **What's normal**: known noisy periods, planned jobs, or dependencies that often cause trouble.

For the checkout alerts in the example scenario, you might add something like:

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

% SCREENSHOT: Automation details flyout, Run history tab, with the runs chart, the status filters, and a day with one succeeded run and one skipped run showing "Daily trigger limit of 20 reached".

## Other triggers [nightshift-uc-auto-variants]

To start from a schedule or a Slack message instead, refer to [Triggers](../investigation/automations.md#nightshift-automations-triggers). For alerts that another tool posts in Slack, refer to [Investigate alerts from your other tools](./external-alerts.md).

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
