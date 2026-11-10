---
description: "Turn an AlertZero investigation into a coordinated response."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Escalate an {{az-investigation}}

Escalate an {{az-investigation}} when you need to work on it with other people, whether to coordinate a broader response or to collaborate privately with a smaller group. An {{az-escalation}} brings related {{az-investigations}} together with their attachments, a summary, and assignees, and you choose who can see it.

You create each {{az-escalation}} yourself; {{alertzero}} doesn't create them for you. When you create one, you become its owner, and only the owner can change its visibility later. Escalating an {{az-investigation}} doesn't close it or change its status, assignees, or contents. When you close the {{az-escalation}}, its linked open {{az-investigations}} close too.

::::{admonition} Requirements
To create an {{az-escalation}} or add an {{az-investigation}} to one, your role needs specific privileges. Refer to [](alertzero-privileges.md).
::::

## Create an {{az-escalation}} [escalate-investigation-create]

To escalate an {{az-investigation}}, select **Open an escalation** from its actions menu {icon}`boxes_vertical` on the **{{az-proposed-actions-cap}}** page, or from its details flyout. You can change the {{az-escalation}}'s title and choose whether it's visible to anyone with the [appropriate privileges](alertzero-privileges.md), or restricted to specific people. If you restrict access, add the people who should work on it. You become its owner and an assignee, and you can [change assignees](manage-escalations.md#manage-escalations-assignees) later.

## Add an {{az-investigation}} to an existing {{az-escalation}} [escalate-investigation-add]

If an {{az-investigation}} belongs to a response that's already escalated, add it to that {{az-escalation}} instead of creating a new one.

Start from the {{az-investigation}} and choose to attach it to an existing {{az-escalation}}. Search the open {{az-escalations}} and select the one for the same response. Each shows how many {{az-investigations}} it already links. Some {{az-escalations}} are unavailable, such as one that already links the {{az-investigation}}. Hover over an unavailable {{az-escalation}} to find out why.

You can add an {{az-investigation}} to a restricted {{az-escalation}} only if you own it or have been given access to it.

## Next steps [escalate-investigation-next-steps]

* [Find the {{az-escalation}} and read its summary](manage-escalations.md).
* [Work on the {{az-escalation}} with your team](manage-escalations.md#manage-escalations-work).
* [Add or change assignees](manage-escalations.md#manage-escalations-assignees).
* [Close the {{az-escalation}}](manage-escalations.md#manage-escalations-close) when the response is complete.
