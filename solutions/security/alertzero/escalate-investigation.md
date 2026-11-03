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

Escalate an {{az-investigation}} when it needs a coordinated response from more than one person. An [{{az-escalation}}](glossary.md#alertzero-glossary-escalation) brings related {{az-investigations}} together with their attachments, a summary, and assignees, and you choose who can see it.

{{alertzero}} doesn't create {{az-escalations}} for you. You create each one yourself, and you become its owner. As the owner, you're the only person who can later change who can see it. Escalating doesn't close the {{az-investigation}} or change its status, assignees, or contents. Closing the {{az-escalation}} later closes the open {{az-investigations}} linked to it.

::::{admonition} Requirements
* You need the **Agentic Investigations**: **Manage escalations** sub-feature privilege to create an {{az-escalation}} or add an {{az-investigation}} to one. To learn more, refer to [](/solutions/security/alertzero/alertzero-privileges.md).
* You need the **Agent Builder: Read** or **Agent Builder: All** {{kib}} feature privilege to open an {{az-escalation}} and its linked {{az-investigations}}. To learn more, refer to [](/explore-analyze/ai-features/agent-builder/permissions.md).
::::

## Create an {{az-escalation}} [escalate-investigation-create]

1. Start from the {{az-investigation}} that you want to escalate:
   * On the **{{az-proposed-actions-cap}}** page, find the {{az-investigation}}, select the actions menu {icon}`boxes_vertical`, then select **Open an escalation**.
   * If you already have the {{az-investigation}} open, select **Open an escalation** at the bottom of its details flyout.
2. In the **Escalate investigation** window, keep **Create escalation** selected.
3. Optional: Edit the {{az-escalation}} title. It starts as the title of the {{az-investigation}}.
4. Choose who can see the {{az-escalation}}:
   * **Public**: Any user with the **Agent Builder: Read** or **Agent Builder: All** privilege can see it. This is the default. You're its only assignee until you add more.
   * **Private**: Only you and the people you add under **Who has access** can see it. You're listed as the owner and added as an assignee. Search for users and select any others you want to work with.
5. Select **Open escalation**.

## Add an {{az-investigation}} to an existing {{az-escalation}} [escalate-investigation-add]

Link an {{az-investigation}} to an {{az-escalation}} that already exists when it belongs to the same response. The {{az-escalation}} then covers both.

1. On the **{{az-proposed-actions-cap}}** page, find the {{az-investigation}}, select the actions menu {icon}`boxes_vertical`, then select **Attach to an escalation**.

   If you opened the {{az-investigation}} details flyout instead, select **Open an escalation** at the bottom of the flyout, and then select **Add to existing** in the **Escalate investigation** window.
2. Search for the {{az-escalation}}. The list shows open {{az-escalations}}, and each one shows how many {{az-investigations}} it links. An {{az-escalation}} is unavailable if the {{az-investigation}} is already linked to it, or if you don't own it and weren't added to it as a member of a private {{az-escalation}}. Hover over an unavailable {{az-escalation}} to see why.
3. Select the {{az-escalation}}, and then select **Add to escalation**.

## Next steps [escalate-investigation-next-steps]

* [Find the {{az-escalation}} and read its summary](manage-escalations.md).
* [Work on the {{az-escalation}} with your team](manage-escalations.md#manage-escalations-work).
* [Add or change assignees](manage-escalations.md#manage-escalations-assignees).
* [Close the {{az-escalation}}](manage-escalations.md#manage-escalations-close) when the response is complete.
