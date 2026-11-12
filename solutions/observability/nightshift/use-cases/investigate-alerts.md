---
navigation_title: Investigate your alerts
applies_to:
  serverless:
    observability: preview
description: Start an Elastic nightshift investigation from an alert or an alert episode, and find out why it fired and what to do about it.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigate your alerts [nightshift-investigate-alerts]

When an alert fires, select **Investigate**, and {{nightshift}} finds out why. The alert already tells it the rule, the service, the threshold, and when the problem started, so you don't have to describe anything. You get the likely cause, the impact, and actions that you can take.

## Before you begin [nightshift-uc-alerts-before]

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable). Until then, alerts don't show the **Investigate** action.
- You have the privileges to start investigations. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-analyst).
- The alert is in the same project as {{nightshift}}. It can come from the {{alerting-v1-system}} or the {{alerting-v2-system}}.
- Each investigation that you start with **Investigate** counts toward the **Manual investigations daily limit**. Refer to [Investigation limits](../investigation/limits.md).

## Example: a latency alert on inventory-api [nightshift-uc-alerts-example]

At 11:05 UTC, an APM latency threshold rule fires: average latency of GET /tickets on `inventory-api` is above 1.5 seconds. You open the alert and select **Investigate**.

A few minutes later, {{nightshift}} reports that latency stayed above the threshold for about an hour, that ticket lookups often failed, and that a slow query on the `encore` database is the likely cause. It proposes that you inspect the query plan and add a missing index.

## Start an investigation from an alert [nightshift-uc-alerts-start]

You can start from the alerts table or from the alert details page. Both start the same investigation.

**From the alerts table:**

1. Find **Alerts** in the navigation menu or with the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Find the alert, open its {icon}`boxes_vertical` **More actions** menu, and select **Investigate**.

% SCREENSHOT: Observability Alerts table with the More actions menu of a Latency threshold alert on inventory-api open, showing the Investigate item.

**From the alert details page:**

1. Open the alert's details page, for example from the link in an alert notification.
1. Select **Investigate** at the top of the page.

% SCREENSHOT: Alert details page for the inventory-api Latency threshold alert, with the Investigate button highlighted in the page header.

The button shows **Investigating…** while {{nightshift}} starts. Then an **Investigation started** message appears. Select **View investigation** to open it on the {{nightshift}} home page.

## Start an investigation from an alert episode [nightshift-uc-alerts-episode]

Alert episodes come from the [{{alerting-v2-system-short}}](/explore-analyze/alerting/esql/system-overview.md).

- In the episodes table, open the episode's row actions menu and select **Investigate**.
- On the episode details page, open the menu at the top of the page and select **Investigate**.

You can investigate one episode at a time.

## Read the investigation [nightshift-uc-alerts-read]

An alert investigation looks like any other investigation. In **What's happened**, the trigger card shows the alert. Select **View alert** to go back to it.

:::{image} ../../../images/nightshift-investigation-chat-action.png
:alt: An investigation of a latency threshold alert on inventory-api, with the alert as its trigger and a latency chart under Impact. In the chat next to it, a proposed action to inspect and fix a query plan shows Decline and Mark as applied
:screenshot:
:::

Read the results, check the hypothesis tree, and act on the proposed actions the same way as for a question. Refer to [Read an investigation](../investigation/index.md#nightshift-read-investigation).

## When an alert already has an investigation [nightshift-uc-alerts-existing]

{{nightshift}} doesn't open a second investigation for the same problem.

| Situation | What happens |
| --- | --- |
| The alert already has an investigation | The action reads **View investigation**. Select it to open the investigation. |
| You want fresh results, for example after you applied a fix | Select **Re-investigate**. On the alert details page, find it in the **Actions** menu. |

**Re-investigate** appears after someone has opened the earlier investigation.

An alert or significant event that's already part of an open investigation joins it. A new alert from the same rule starts its own investigation, and automations can't group repeat firings into one. Refer to [One problem, one investigation](../investigation/index.md#nightshift-investigations-dedup).

## What to check [nightshift-uc-alerts-check]

- **Check the time window.** The investigation starts from when the alert fired. If the problem started earlier, say so in chat: "The latency started climbing at 09:00 UTC, before the alert fired."
- **Don't assume the alert is right.** {{nightshift}} can find that an alert fired on a short burst, or for a reason other than the one the rule name suggests. Read **Impact** before you escalate.
- **Investigating the same rule often?** Let an automation do it. Refer to [Automatically investigate your alerts](./auto-investigate-alerts.md).

## Next steps [nightshift-uc-alerts-next]

- [Automatically investigate your alerts](./auto-investigate-alerts.md): Have every matching alert investigated and the results posted to Slack.
- [Investigate anything](./investigate-anything.md): Learn how to read results, check the hypothesis tree, and ask follow-up questions.
- [How investigations work](../investigation/index.md): Learn how far to trust a conclusion.
