---
description: "Find the AlertZero proposed actions that need a decision, filter them by impacted entity, and assign, close, or escalate investigations in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Use {{alertzero}} [alertzero-use]

Your work in {{alertzero}} starts on the **{{az-proposed-actions-cap}}** page. It shows the {{az-proposed-actions}} waiting for your decision and the ones that closed recently. Use it to find what needs you, focus on one host, user, or service, and assign, close, or escalate {{az-investigations}}.

To open the page, select **{{alertzero}}** in the navigation menu. If no {{az-worker}} is on and no {{az-investigation}} exists yet, {{alertzero}} shows the [setup steps](set-up-alertzero.md) instead.

To view the page and open {{az-investigation}} details, you need the privileges to use {{alertzero}}. Refer to [](alertzero-privileges.md).

## Find what needs a decision [alertzero-use-sections]

The page header shows how many actions need you. Each card shows one {{az-investigation}} and its {{az-proposed-actions}}. {{alertzero}} sorts open {{az-proposed-actions}} into the **Respond**, **Investigate**, and **Configure** sections by the kind of action. Each section lists the newest first, along with approved {{az-proposed-actions}} that are still running.

To review and decide {{az-proposed-actions}}, select a card. Refer to [](decide-proposed-action.md).

The **Closed Actions** section lists {{az-proposed-actions}} that closed in the last 72 hours. Refer to [](review-closed-proposed-actions.md).

If any {{az-worker}} runs failed in the past 24 hours, a callout lists the affected {{az-workers}}, with links to their failed runs in Workflows. Refer to [](view-execution-history.md).

## Focus on one host, user, or service [alertzero-use-filter]

In the **Impact** filter, select the entity. Every section, including **Closed Actions**, then shows only the {{az-investigations}} that affect it. To clear the filter, select the entity again.

If the message "Impacted entities are unavailable" appears, you don't have the privileges to see impacted entities. Refer to [](alertzero-privileges.md).

## Assign, close, or escalate {{az-investigations}} [alertzero-use-investigation]

| To | Do this |
| --- | --- |
| Review the evidence and decide its {{az-proposed-actions}} | Select the card. The {{az-investigation}}'s details open in a flyout. |
| Ask follow-up questions | Select **Open in chat**. |
| Assign it to someone | Select {icon}`plus_circle` **Add or change assignees**. |
| Share it | From the actions menu, select **Copy link**. |
| Close it | From the actions menu, select **Close investigation**, then give a reason. Closing it also declines its pending {{az-proposed-actions}}. |
| Reopen it | From the actions menu, select **Open investigation**. |
| Escalate it | From the actions menu, select **Open an escalation** or **Attach to an escalation**. Refer to [](escalate-investigation.md). |

Some of these actions need more privileges than viewing the page. Refer to [](alertzero-privileges.md).

## Next steps [alertzero-use-next]

- [](decide-proposed-action.md): Approve or decline {{az-proposed-actions}}.
- [](review-closed-proposed-actions.md): Check what happened to recent {{az-proposed-actions}}.
- [](decide-detection-change.md), [](respond-to-attack.md), and [](act-on-hunt-finding.md): Decide the {{az-proposed-actions}} that each {{az-watch}} brings you.
