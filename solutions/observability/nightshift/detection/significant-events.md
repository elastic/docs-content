---
navigation_title: Review significant events
applies_to:
  serverless:
    observability: preview
description: Review the significant events that detection raises, check why each one was raised, investigate it, and route significant events to your team like any other alert.
products:
  - id: observability
  - id: cloud-serverless
---

# Review significant events [nightshift-detection-events]

A significant event is a problem that detection found in your logs: one event for related changes, with a summary of what happened and the signals behind it. Review the list to find what needs attention, check why each event was raised, and start an investigation to find the likely cause.

For the privileges to view events and start investigations, refer to [Grant access](../get-started/privileges.md#nightshift-privileges-analyst).

## Find an event [nightshift-detection-events-find]

On the {{nightshift}} home page, select **Detections**. The **Events** tab lists your significant events, the most recently updated first.

Each row shows the event's title and summary, when it was **Updated at** and **Created at**, its **Status**, its **Severity**, and its **Investigation** state: **Not started**, **In progress**, or **Completed**.

To narrow the list:

- Search the events, or change the time range. The default is **Last 24 hours**.
- Filter by **Severity**, **Status**, or **Investigation**.
- In the **Entities** list on the left, select the services or databases that you care about. The number next to each one is its count of events.

## Review an event [nightshift-detection-events-read]

Select an event to open its details.

The header shows the title, when the event was raised, and three badges: severity, confidence, and status. The **Overview** tab has these sections:

- **What happened?**: A summary of the problem and the evidence that discovery grouped into the event. Select **Show more** to read all of it.
- **Investigation**: The investigation of the event and its state, if there is one.
- **Detections**: The signals behind the event, each with the rule that found it and the kind of change, such as **Non-stationary**. Select one to open its trend, its {{esql}} query, and how discovery judged it. Refer to [Check the signals behind an event](./rules-and-signals.md#nightshift-detection-signals-event).

The **Timeline** tab shows how the event developed, in time order: each signal that fed it, when {{nightshift}} raised it with an explanation of its severity and confidence, and every later update or status change.

### Severity and confidence [nightshift-detection-events-severity]

- **Severity** is how serious the problem is likely to be for your system: **Low**, **Medium**, **High**, or **Critical**.
- **Confidence** reflects how strong and consistent the evidence for the event is.

An event with low confidence can still be worth a look, but check its signals first. For example, an event with **Confidence 24%** may rest on a single rule, or on signals that discovery refuted.

### Status [nightshift-detection-events-status]

| Status | What it means | What to do |
| --- | --- | --- |
| **Active** | A current failure is confirmed, or is plausible and not yet ruled out. | Review it and investigate. |
| **Recovering** | Every rule behind the event looks healthy again. If any of them breaches again, the event returns to **Active**. | Keep an eye on it. No action is needed yet. |
| **Inactive** | Every signal that confirmed the event was checked again and cleared, or someone marked the event inactive. | Nothing. Inactive events are resolved. |

An event doesn't become inactive only because a rule goes quiet. It stays **Active** or **Recovering** until its signals are checked again and cleared.

## Act on an event [nightshift-detection-events-act]

To find the likely cause, select **Investigate** in the event's row, or open the event and select **Actions** → **Run investigation**. These investigations count toward the **Manual investigations daily limit**. Refer to [Investigation limits](../investigation/limits.md). When the investigation is done, the row shows **View investigation**. To learn how to read the result, refer to [How investigations work](../investigation/index.md).

The **Actions** menu in the event's details also has:

- **Run follow-up**: Queue another investigation, while one is still running. It starts when the first one finishes.
- **Open investigation in chat**: Continue a completed investigation with your own questions.
- **New chat about this event**: Ask questions about the event without starting an investigation, for example "Which services does this affect?".
- **Mark inactive**: Close an event that no longer needs attention. Optionally, add an **Assessment note** with your reason.

## Route significant events and investigate them automatically [nightshift-detection-events-route]

A significant event is an alert in the {{alerting-v2-system}}. You can use it like any other alert:

- **Investigate every event automatically.** Create an automation with the **Alert triggered** trigger and the **Significant events** source. Refer to [Investigate significant events automatically](../use-cases/detect-problems.md#nightshift-uc-detect-automate).
- **Notify your team.** Create an action policy that routes significant events to a workflow, which sends the notification to Slack, PagerDuty, email, or a webhook. Refer to [Notifications and actions](/explore-analyze/alerting/esql/notifications-actions.md) and [Create an action policy](/explore-analyze/alerting/esql/action-policies/create-configure-action-policy.md).

## Next steps [nightshift-detection-events-next]

- [How investigations work](../investigation/index.md): Read an investigation and check its reasoning.
- [Automatically investigate your alerts](../use-cases/auto-investigate-alerts.md): Investigate significant events as soon as they're raised.
- [Rules and signals](./rules-and-signals.md): Remove rules that raise noisy events.
