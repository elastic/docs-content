---
description: "Find AlertZero escalations, read their summaries, work on them with your team, change who is assigned and who can see them, and close them."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Manage {{az-escalations}}

Use the **{{az-escalations-cap}}** page to see which {{az-escalations}} are open, who is assigned to each, and where each one stands. You see every {{az-escalation}} that you have access to in one place, and each one shows its assignees.

::::{admonition} Requirements
To see, assign, or close an {{az-escalation}}, your role needs specific privileges. Refer to [](alertzero-privileges.md).
::::

## Find your {{az-escalations}} [manage-escalations-find]

1. Open the **{{az-escalations-cap}}** page from the navigation menu, or search for it with the global search field.
2. Check each open {{az-escalation}}. It shows the title, when it was opened and last updated, and who it's assigned to.
3. Optional: To see only the {{az-escalations}} that involve a specific host, user, or other entity, select it under **Impacted entities**. The filter applies to both the open and closed lists.

You see {{az-escalations}} that are public, and private ones that you own or were given access to.

## Read an {{az-escalation}}'s summary [manage-escalations-summary]

Select an {{az-escalation}} to open it as a chat in {{agent-builder}}, with its details flyout. The flyout shows:

* A summary that {{alertzero}} writes from the messages, notes, and attachments in the {{az-escalation}}. It refreshes shortly after new messages, notes, or attachments are added to the {{az-escalation}}. Closing a linked {{az-investigation}} doesn't refresh it.
* The attachments collected from the linked {{az-investigations}}.
* Linked {{az-investigations}}, each with an **Open** or **Closed** badge. An open {{az-investigation}} with {{az-proposed-actions}} that nobody has decided yet shows **Action required**.
* The entities that the linked {{az-investigations}} affect.

The flyout header shows the {{az-escalation}} title, status, and assignees, and when it was created.

## Work on an {{az-escalation}} [manage-escalations-work]

The {{az-escalation}} is where you and your team coordinate the response. Everyone who can see it can read the full conversation and send messages in it. You decide on {{az-proposed-actions}} in the linked {{az-investigations}}.

1. In the details flyout, under **Linked investigations**, select each {{az-investigation}} marked **Action required**, and decide on its {{az-proposed-actions}}. To learn how, refer to [](work-in-alertzero.md).
2. To talk to your team, send a message in the chat. To post a message for the other people without asking the agent to respond, select **Include agent**, and then select **Skip agent**. To learn more, refer to [](/explore-analyze/ai-features/agent-builder/chat.md#post-without-running-the-agent).

## Change who is assigned [manage-escalations-assignees]

1. On the **{{az-escalations-cap}}** page, select **Add or change assignees** {icon}`plus_circle` next to the {{az-escalation}}.
2. Search for users, then select or clear them.

On a private {{az-escalation}}, adding an assignee also gives that person access to it, and removing an assignee removes their access.

## Change who can see an {{az-escalation}} [manage-escalations-visibility]

Only the owner of an {{az-escalation}} can change who can see it. Open the {{az-escalation}} and use the sharing button in the chat header, as described in [](/explore-analyze/ai-features/agent-builder/chat.md#share-a-conversation).

Changing who can see an {{az-escalation}} doesn't change who is assigned to it.

## Close an {{az-escalation}} [manage-escalations-close]

Close an {{az-escalation}} when the response is complete.

1. Open the {{az-escalation}}, and then select its status in the flyout header.
2. Select **Closed**.
3. In the **Close this escalation?** window, review the linked {{az-investigations}} that will be closed and the number of pending {{az-proposed-actions}} that will be declined.
4. If there are pending {{az-proposed-actions}}, select a reason for declining them. You can also add an optional note. Your reason and notes apply to all the declined {{az-proposed-actions}}.
5. Select **Close escalation**.

:::{warning}
Closing an {{az-escalation}} also closes its open linked {{az-investigations}} and their chats, and declines their pending {{az-proposed-actions}}.
:::

If a linked {{az-investigation}} has been deleted or isn't accessible to you, you can't close the {{az-escalation}} until you resolve the problem. If a linked {{az-investigation}} can't be closed, for example because a pending {{az-proposed-action}} can't be declined, the {{az-escalation}} stays open. Check that you have the required privileges, and then try again.
