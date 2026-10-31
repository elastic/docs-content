---
description: "Find the AlertZero proposed actions that need a decision, filter them by impacted entity, and assign, close, or escalate investigations in Elastic Security."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Use {{alertzero}} [alertzero-use]

Every decision in {{alertzero}} starts on the **{{az-proposed-actions-cap}}** page. It lists the {{az-proposed-actions}} that are waiting for you, sorted by the kind of action, and the ones that closed recently.

To open it, select **{{alertzero}}** in the navigation menu. Once at least one {{az-worker}} is on or an {{az-investigation}} exists, {{alertzero}} opens on this page. Until then, it shows the setup steps in [](set-up-alertzero.md).

To view the page, you need the **Proposed Actions** privilege set to **Read**. Refer to [](alertzero-privileges.md).

## Find what needs a decision [alertzero-use-sections]

The page header shows how many actions need you. {{alertzero}} sorts open {{az-proposed-actions}} into the **Respond**, **Investigate**, and **Configure** sections, based on the kind of action each one proposes. Each section lists the newest first and also shows approved {{az-proposed-actions}} that are still running.

To decide one, select its card. Refer to [](decide-proposed-action.md).

The **Closed Actions** section lists {{az-proposed-actions}} that closed in the last 72 hours. Refer to [](review-closed-proposed-actions.md).

## Filter by impacted entity [alertzero-use-filter]

To focus on one host, user, or service, select its entity in the **Impact** filter. Every section, including **Closed Actions**, then shows only the {{az-investigations}} that affect that entity. To clear the filter, select the entity again.

If the page shows **Impacted entities are unavailable**, you need the **Agentic Investigations** privilege set to **Read**.

## Work with {{az-investigations}} [alertzero-use-investigation]

Each card on the page belongs to one {{az-investigation}}. From the card, you can:

| To | Do this |
| --- | --- |
| Review the evidence and decide its {{az-proposed-actions}} | Select the card. The {{az-investigation}}'s details open in a flyout. Refer to [](decide-proposed-action.md). |
| Ask follow-up questions about it | Select **Open in chat**. |
| Assign it to someone | Select **Add or change assignees**. |
| Share it | Open the actions menu and select **Copy link**. |
| Close it | Open the actions menu and select **Close investigation**. Closing it also declines its pending {{az-proposed-actions}}, and you give a reason. |
| Reopen it | Open the actions menu and select **Open investigation**. |
| Escalate it | Open the actions menu and select **Open an escalation** or **Attach to an escalation**. Refer to [](escalate-investigation.md). |

Some of these need more privileges than viewing the page. Refer to [](alertzero-privileges.md).

## When nothing needs you [alertzero-use-idle]

When no {{az-proposed-actions}} are open or recently closed, the page shows **No actions need you**, with how many {{az-watches}} and {{az-workers}} are running.

The page lists {{az-investigations}} only when they have {{az-proposed-actions}}. If any {{az-worker}} run failed in the past 24 hours, a callout lists the {{az-workers}} that reported problems, and each one links to its failed runs in Workflows. Refer to [](view-execution-history.md).

## Next steps [alertzero-use-next]

- [](decide-proposed-action.md): Approve or decline {{az-proposed-actions}}.
- [](review-closed-proposed-actions.md): Check what happened to recent {{az-proposed-actions}}.
- [](escalate-investigation.md): Turn {{az-investigations}} into coordinated responses.
