---
applies_to:
  serverless:
    observability: preview
description: Learn how Elastic nightshift automations start investigations from alerts, schedules, and Slack messages, and post the results, for example to Slack.
products:
  - id: observability
  - id: cloud-serverless
---

# Automations [nightshift-automations]

An automation does work for you without a person starting it. An automation starts an investigation when something happens, and can then post the results, for example to Slack. Each automation is backed by a [workflow](/explore-analyze/workflows.md).

## What starts an automation [nightshift-automations-triggers]

An automation starts from one or more of these triggers:

- **An alert**: The automation starts an investigation when a matching alert becomes active. You can match alerts from specific rules, selected by name or tag. The alert can come from {{alerting-v1-system}} or {{alerting-v2-system}}, and must be in the same project as Elastic nightshift.
- **A schedule**: The automation starts an investigation at set times. You choose to run it every hour, every day at a set time, or on selected days of the week at a set time, in a time zone that you choose. An hourly schedule can run only during certain hours. An automation has one schedule, and custom cron schedules aren't supported.
- **A Slack message**: The automation starts an investigation from a Slack message.

A Slack trigger starts from a new message in the channels that you choose. You can narrow it to messages that contain certain text, messages from specific people, or messages that a specific app or bot posts.

If the alert or other subject is already part of an open investigation, the automation adds to that investigation instead of opening a second one. Every other matching alert starts its own investigation, even when it comes from the same rule, and each one counts against the daily limits.

## Instructions [nightshift-automations-instructions]

Instructions guide the investigation for each run. A scheduled automation requires instructions, which define the task for each run. Alert and Slack automations accept optional additional instructions. Instructions can be up to 5,000 characters. They're also the preferred way to give Elastic nightshift context about your systems. Refer to [Give Elastic nightshift context](../set-up-an-automation.md).

## What an automation does with the results [nightshift-automations-results]

An automation can post the results of an investigation to a Slack channel. The channel action uses the Elastic Slack app by default, and you can choose a saved Slack connector instead. Elastic nightshift posts a message when the investigation starts, then replies in the same thread when it finishes or fails. Refer to [Use investigations in Slack](../investigate-and-respond.md#nightshift-investigations-slack).

Direct-message actions aren't available yet.

## Who can manage automations [nightshift-automations-access]

Automations run as the `nightshift_automations` service account, so they keep working whoever created them. Creating, changing, turning on or off, and deleting an automation needs the **All** privilege for Elastic nightshift and the `manage_security` privilege, and the space must be enabled. Other users see the edit actions disabled, with a message that explains why. Refer to [Grant access to Elastic nightshift](../get-started/privileges.md).

You can cap how many investigations a trigger starts each day. Refer to [Settings and lifecycle](../manage/settings-and-lifecycle.md#nightshift-settings-lifecycle-investigations).

To create an automation, refer to [Set up an automation](../set-up-an-automation.md).

## Manage automations and check their runs [nightshift-automations-manage]

The **Automations** page lists the automations in the current space. An icon beside each name shows its trigger: an alert, a Slack message, or a schedule. For each automation, the list shows the **Author**, the number of **Successful**, **Failed**, and **Skipped** runs in the selected time range, **Today's usage** against its daily trigger limit, and an **Enabled** toggle. Use the toggle to turn an automation on or off without opening it. A turned-off automation starts nothing.

To narrow the list, search by name, or filter by **Status** (**Enabled** or **Paused**), **Tag**, **Author**, **Trigger**, or time range. The time range defaults to **Last 48 hours**. To copy or remove an automation, open its {icon}`boxes_vertical` menu and select **Clone** or **Delete**.

To see the details, select an automation's name. A flyout opens with an **Overview** tab, which shows the description, trigger, daily trigger limit, additional instructions, and actions, and a **Run history** tab. To change the automation, select **Edit**. To copy or remove it, open the **Actions** menu and select **Clone** or **Delete**. A change applies from the next trigger.

The **Run history** tab shows a chart of the runs over the selected time range, with status filters, such as **Succeeded** and **Skipped**, and a count for each. Below the chart, runs are grouped by day. Each run shows its status, how long ago it ran, and the investigation it started. A skipped run shows the source of the trigger and why it was skipped, for example "Deployment-wide investigation limit reached".

To see more about a run, select it. For a skipped run, the details show when it was triggered, its source, the message that triggered it, the reason, and the automation. A reason such as "The deployment-wide investigation limit was already reached, so this trigger did not start a run" means that a limit stopped the run. To raise a limit, refer to [Settings and lifecycle](../manage/settings-and-lifecycle.md#nightshift-settings-lifecycle-investigations).

The counts on the list come from the first page of runs, so they can be lower than the true total for a busy automation.

## Limitations in Tech Preview [nightshift-automations-limits]

- Slack is the only place an automation can post results.
- An automation starts only from alerts in the same project, schedules, and connected Slack channels.
- An automation can't group repeat firings of the same rule into one investigation.
- Schedules use hourly, daily, or weekly presets. Custom cron schedules aren't supported.
- Limits count investigations per day, not cost.
- Elastic nightshift creates a workflow for each automation. It has the same name as the automation and the `nightshift` and `automation` tags, and it appears on the **Workflows** page. Edit the automation, not its workflow.

## Learn more [nightshift-automations-nav]

- [How Elastic nightshift works](./index.md#nightshift-how-it-works): See where automations fit in
- [Investigation engine](../investigations.md): Learn how an investigation runs
