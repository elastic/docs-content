---
description: "Find the AlertZero proposed actions that are waiting for you in Elastic Security, see which ones fit your role, and follow up on an investigation."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Work through {{az-proposed-actions}} [alertzero-use]

{{az-workers}} do the analysis, and you decide what they bring you, such as which alerts to close, how to contain an attack, and which detection rules to change. Everything waiting for you is on the {{alertzero}} home page, the **{{az-proposed-actions-cap}}** page. To open it, select **{{alertzero}}** in the navigation menu.

Each card on the page is one {{az-proposed-action}}. Select a card to see the {{az-investigation}} behind it: the evidence the {{az-worker}} gathered and what it concluded.

## Find the work for your role [alertzero-use-sections]

The page groups {{az-proposed-actions}} by the kind of decision they need. If you cover more than one role, work through more than one section.

| Section | What you decide | Usually decided by |
| --- | --- | --- |
| **Respond** | Response actions, such as isolating a host. Refer to [](respond-to-attack.md) and [](act-on-hunt-finding.md). | Incident responders and threat hunters |
| **Investigate** | Whether to close false-positive alerts, and whether to send an attack for forensics. Refer to [](decide-proposed-action.md) and [](respond-to-attack.md). | Triage analysts |
| **Configure** | Changes to detection rules. Refer to [](decide-detection-change.md). | Detection engineers |

To see only the work that involves one host, user, or service, select it under **Impact**. This helps when the same host turns up in several {{az-investigations}} and you want to handle them together.

## Follow up on an {{az-investigation}} [alertzero-use-follow-up]

Besides approving or declining, you can:

- **Ask about the evidence:** Select **Open in chat** to ask the AI follow-up questions about the {{az-investigation}}, such as why the {{az-worker}} judged an alert a false positive.
- **Hand it off:** Assign the {{az-investigation}} to a teammate, or [escalate it](escalate-investigation.md) to work on it with others.
- **Dismiss everything at once:** Close the {{az-investigation}} to decline all its pending {{az-proposed-actions}} in one step.

## Next steps [alertzero-use-next]

- [](decide-proposed-action.md): Judge a {{az-proposed-action}}, approve or decline it, and check recent decisions.
- [](respond-to-attack.md): Take an attack from verdict to containment.
- [](decide-detection-change.md): Review a change to a detection rule.
