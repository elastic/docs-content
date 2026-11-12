---
navigation_title: Detect problems automatically
applies_to:
  serverless:
    observability: preview
description: Turn on Elastic nightshift detection to find problems in your logs that none of your alerts catch, review the significant events it raises, and investigate them.
products:
  - id: observability
  - id: cloud-serverless
---

# Detect problems automatically [nightshift-detect-problems]

Find the problems that none of your alerts catch. {{nightshift}} learns how your system normally behaves from your logs, watches for unusual changes, and groups related changes into one significant event. You review one problem with its evidence, instead of a pile of small alerts, and start an investigation from it in one step.

## Before you begin [nightshift-uc-detect-before]

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable).
- You have the privileges to turn on detection, or an admin has turned it on. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-admin).
- You have recent logs in your project. In Tech Preview, detection watches logs only, not metrics or traces.
- Detection runs all the time and uses tokens. Refer to [Cost and models](../cost-and-models.md).

## Example: statement timeouts nobody alerted on [nightshift-uc-detect-example]

Your alerts cover latency and error rates on `inventory-api`, but nothing watches the Postgres logs. One evening, Postgres starts to cancel `inventory-api` statements on the `encore` database because they hit the statement timeout. Users retry, so the error rate stays below your alert threshold.

Detection notices the timeout messages in the Postgres logs and raises a significant event: **Inventory API — PostgreSQL statement timeouts**, severity **High**, status **Active**. You open it, read what it found, and select **Investigate** to find out why.

## How detection finds problems [nightshift-uc-detect-how]

Detection learns your system from your logs, writes its own rules, and groups unusual changes into one significant event. Refer to [From your data to a significant event](../detection/index.md#nightshift-detection-flow).

## Find and investigate problems [nightshift-uc-detect-steps]

:::::{stepper}

::::{step} Turn on detection
:anchor: nightshift-uc-detect-enable

If the **Detection engine** on the **Detections** page doesn't show **Monitoring** yet, follow [Set up detection](../get-started/detection.md). The first KIs and rules appear within a few minutes, and the first signals 40 to 100 minutes later.
::::

::::{step} Review significant events
:anchor: nightshift-uc-detect-review

On the {{nightshift}} home page, select **Detections**. The **Events** tab lists the significant events of the **Last 24 hours**.

:::{image} ../../../images/nightshift-detections.png
:alt: The Detections page. The Detection engine shows Monitoring with counts of knowledge indicators, entities, rules, signals, and significant events. The Events tab lists significant events with their status, severity, and investigation
:screenshot:
:::

To filter events and read the statuses, refer to [Review significant events](../detection/significant-events.md).
::::

::::{step} Read an event
:anchor: nightshift-uc-detect-read

Select the event to read **What happened?** and the detections behind it. Treat a low confidence as a lead to check. Refer to [Read an event](../detection/significant-events.md#nightshift-detection-events-read).

:::{image} ../../../images/nightshift-significant-event-details.png
:alt: A significant event about Postgres client connection loss, with Medium severity, 24% confidence, and Active status. Next to it, one of its detections shows a trend chart and its ES|QL query
:screenshot:
:::

::::

::::{step} Investigate the event
:anchor: nightshift-uc-detect-investigate

The event tells you *what* changed. An investigation finds out *why*.

1. In the **Events** list, find an event whose **Investigation** column shows **Not started**.
1. In the **Actions** column, select **Investigate**. Or, in the event's details, select **Actions** > **Run investigation**.

The investigation runs like any other, and counts toward the **Manual investigations daily limit**. Refer to [Read an investigation](../investigation/index.md#nightshift-read-investigation). When it's done, the **Investigation** column shows **Completed**. For the other actions on an event, refer to [Act on an event](../detection/significant-events.md#nightshift-detection-events-act).
::::

:::::

## Investigate significant events automatically [nightshift-uc-detect-automate]

{{nightshift}} doesn't investigate significant events on its own. To have them investigated when they're raised, create an automation:

1. Follow [Create the automation](./auto-investigate-alerts.md#nightshift-uc-auto-create).
1. In the trigger, select **any source**, then **Only these sources** and **Significant events**.
1. Optionally, select a severity, such as **High** and **Critical**, so only the most serious events are investigated.
1. Add a **Post in Slack** action, so the findings go to your team's channel.

These investigations count toward the **Automatic investigations daily limit**. Refer to [Investigation limits](../investigation/limits.md).

## What to check [nightshift-uc-detect-check]

- **Give it time.** Detection starts with few rules, and some rules show zero matches at first. It improves as it learns more about your system.
- **Mark noise inactive.** If an event isn't a problem, select **Mark inactive**, so your team doesn't look at it again.
- **Check what it learned.** Detection is only as good as what {{nightshift}} learned about your system. Refer to [How detection learns your system](../detection/learning.md).
- **Pause it if you need to.** An admin can pause detection in Settings. Refer to [Pause or resume detection](../settings.md#nightshift-settings-pause).

## Next steps [nightshift-uc-detect-next]

- [How detection works](../detection/index.md): Learn how data becomes Knowledge Indicators, rules, signals, and significant events.
- [Review significant events](../detection/significant-events.md): Learn every filter, status, and action on the **Events** tab.
- [Choose what detection watches](../detection/sources.md): Add, edit, or pause sources.
- [Automatically investigate your alerts](./auto-investigate-alerts.md): Set up the automation that investigates significant events for you.
