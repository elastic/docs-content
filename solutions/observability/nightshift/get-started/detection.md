---
navigation_title: Set up detection
applies_to:
  serverless:
    observability: preview
description: Turn on Elastic nightshift detection so it learns how your system behaves and finds problems that none of your alerts catch.
products:
  - id: observability
  - id: cloud-serverless
---

# Set up detection [nightshift-get-started-detection]

Your alerts catch the problems you thought of in advance. Detection finds the rest. {{nightshift}} learns how your system normally behaves, watches for unusual changes, and groups related changes into a significant event, so you review one problem instead of a pile of small alerts.

Detection is separate from [investigations](./investigations.md). You can use investigations without it, and turn it on whenever you're ready.

## Before you begin [nightshift-get-started-detection-requirements]

Make sure you meet the following requirements:

- **{{nightshift}} is enabled for the space.** If it isn't, start with [Set up investigations](./investigations.md#nightshift-get-started-enable).
- **An admin to enable detection.** The predefined **Admin** role can do this. For other roles, refer to [Grant access to {{nightshift}}](privileges.md).
- **Your project has recent logs.** Detection watches logs in this project or in projects linked by [{{cps}}](/deploy-manage/cross-project-search-config.md). For other deployment types, refer to [Reference architecture](../reference-architecture.md).

## Choose your data and turn on detection [nightshift-get-started-detection-steps]

:::::{stepper}

::::{step} Choose what detection watches
:anchor: nightshift-get-started-detection-sources

1. On the {{nightshift}} home page, select **Detections**. If you aren't seeing it, make sure you've completed the **Get started** checklist. If you see **Detection setup requires manage and configure access**, ask an admin to enable it.
1. Under **Select data sources to analyze**, keep **All logs** (`FROM logs*`) selected. To watch only some of your data, select **Create new source**. Refer to [Choose what detection watches](../detection/sources.md).
::::

::::{step} Enable detection
:anchor: nightshift-get-started-detection-enable

Select **Enable detection**.

A badge by the **Detection engine** heading now shows **Monitoring**, with all counts at zero. Scheduled discovery is on by default, so there's nothing else to turn on.
::::

::::{step} Let detection learn your system
:anchor: nightshift-get-started-detection-learning

{{nightshift}} first reads your logs to learn which services and dependencies you have. It records them as [Knowledge Indicators](../context/knowledge-indicators.md), and then creates rules from them. The first KIs and rules appear within a few minutes. Expect the first signals 40 to 100 minutes after you enable detection.

While you wait, the counts at the top of the **Detections** page go up as {{nightshift}} learns. To review what it learned, refer to [How detection learns your system](../detection/learning.md).
::::

::::{step} Review your first significant events
:anchor: nightshift-get-started-detection-events

Significant events appear on the **Events** tab only when something unusual happens, so a quiet system can stay at zero for a while.

When an event appears, select it to read **What happened?** and the detections behind it. To find the likely cause, select **Investigate**. Refer to [Review significant events](../detection/significant-events.md).
::::

::::{step} Investigate new events automatically (optional)
:anchor: nightshift-get-started-detection-automate

A significant event is an alert, so an automation can investigate each new one for you and post the results to Slack. Create an automation with the **Alert triggered** trigger. Refer to [Automatically investigate your alerts](../use-cases/auto-investigate-alerts.md).
::::

:::::

## What's next [nightshift-get-started-detection-next]

- [Detect problems automatically](../use-cases/detect-problems.md): See what detection finds and how to act on it
- [How detection works](../detection/index.md): Learn how sources, Knowledge Indicators, rules, and signals fit together
- [Settings and limits](../settings.md): Pause detection and set its daily limits
