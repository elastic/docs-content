---
applies_to:
  serverless:
    observability: preview
description: Find what needs attention in Elastic nightshift, start investigations, read their findings and proposed actions, ask follow-up questions, and use Slack to get results and ask questions.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigate and respond [nightshift-investigate-respond]

Use Elastic nightshift to work through a problem, from spotting it to acting on what the investigation finds. This page covers reviewing what needs attention, starting an investigation, reading its results, acting on proposed actions, asking follow-up questions, and using Slack. For how investigations work, refer to the [Investigation engine](./investigations.md).

How you can interact with investigations depends on your privileges. Refer to [Grant access to Elastic nightshift](./get-started/privileges.md).

## Review what needs attention [nightshift-investigations-attention]

The Elastic nightshift home page lists your investigations, grouped by severity to help decide what to look at first.

- **Severity tiles**: The tiles at the top show how many investigations are **Critical**, **High**, **Medium**, and **Low**.
- **Sections**: Select a tile to go directly to the related section. You can also see investigations that are **In progress**.
- **Search**: Use the **Search** field to find a specific investigation.
- **Cards**: Each investigation has a card with an {icon}`boxes_vertical` actions menu, a button to open the investigation in chat, and an assignee picker. To share an investigation, open the actions menu and select **Copy link**.

Select a card to open the investigation's details in a flyout.

To review the significant events that Elastic nightshift detected, select **Detections**. Refer to [Review significant events](./audit-and-manage-detections.md#nightshift-detections-review-events).

## Start an investigation [nightshift-investigations-start]

Use Elastic nightshift to investigate a problem, ask questions about what it found, check how it reached its conclusion, and resolve the problem. Start an investigation from one of the following places:

- [**From the Elastic nightshift home page**](#nightshift-investigations-start-describe)
- [**From a {{alerting-v1-system}} alert**](#nightshift-investigations-start-alert)
- [**From a {{alerting-v2-system}} alert episode**](#nightshift-investigations-start-episode)
- [**From a significant event**](#nightshift-investigations-start-event)

If the alert or significant event you start from is already part of an open investigation, Elastic nightshift adds to that investigation instead of opening a second one. A new alert from the same rule starts its own investigation. A closed investigation is never continued.

### Investigate a problem you describe [nightshift-investigations-start-describe]

When you notice an issue in your system that's not covered by an alert, use the home page to describe the problem in your own words.

1. From the Elastic nightshift home page, select **Investigate**.
1. Describe the problem. The more context you provide about your system, the better the investigation. For example, ask "Why is checkout latency up?" or "What caused last night's error spike?"
1. Select **Investigate**.

The investigation appears in the **In progress** section of the home page.

### Investigate an alert [nightshift-investigations-start-alert]

Start an investigation from a {{alerting-v1-system-short}} alert to find out what happened and how to fix it. You can do this from the alerts table or from the alert details page.

To start from the alerts table:

1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Find the alert that you want to investigate, open its {icon}`boxes_vertical` **More actions** menu, and select **Investigate**.
1. In the **Investigation started** message, select **View investigation**.

To start from the alert details page:

1. Open the alert's details page in {{kib}}, for example from an alert notification.
1. Select **Investigate** at the top of the page.
1. In the **Investigation started** message, select **View investigation**.

If the alert already has an investigation, the button reads **View investigation** instead. To investigate the alert again, open the **Actions** menu and select **Re-investigate**.

### Investigate an alert episode [nightshift-investigations-start-episode]

Alert episodes come from the [{{alerting-v2-system-short}}](/explore-analyze/alerting/esql/system-overview.md). To investigate one, select **Investigate** from its row actions menu in the episodes table, or from the menu at the top of the episode details page. If the episode already has an investigation, the action reads **View investigation**.

### Investigate a significant event [nightshift-investigations-start-event]

Significant events are alerts that Elastic nightshift creates when related signals add up to something meaningful. To investigate one:

1. From the Elastic nightshift home page, select **Detections**.
1. Make sure the **Events** tab is selected.
1. The **Investigation** column shows if the significant event has a **Completed** investigation or if an investigation has **Not started**.
1. From a significant event that hasn't been investigated, select {icon}`inspect` **Investigate** from the **Actions** column.

## Read the investigation results [nightshift-investigations-results]

When an investigation finishes, Elastic nightshift reports what happened, what it affects, and what most likely caused it. From the home page, select an investigation. A flyout opens with the investigation's status, **Open** or **Closed**, and its severity: **Low**, **Medium**, **High**, or **Critical**. While the investigation runs, the flyout shows **Investigating…**.

Agent Builder titles the investigation when its first round ends. Until then, the investigation is named for its first subject, such as the rule name of the alert that triggered it, or shows **New investigation**.

The flyout has the following sections:

- **What's happened**: A short summary of what the investigation observed. The card in this section shows what triggered the investigation, such as the alert.
- **Impact**: What the problem affects, with a chart of the affected activity, so you can prioritize it and involve the right teams.
- **Conclusion**: The best-supported explanation of why the problem occurred. Select **View hypothesis tree** to see how Elastic nightshift reached it.
- **Proposed actions**: The changes that Elastic nightshift suggests. Refer to [Review proposed actions](#nightshift-investigations-actions).

### Review how Elastic nightshift reached its conclusion [nightshift-investigations-hypotheses]

To validate the reasoning, review the hypotheses that Elastic nightshift considered.

1. In the investigation flyout, select **View hypothesis tree**.
1. Read the tree from top to bottom:

   - **Trigger**: What started the investigation.
   - **Hypothesis**: Each hypothesis that Elastic nightshift tested, with its status and confidence. The status is **Investigating**, **Confirmed**, or **Dismissed**, and the confidence appears as a percentage. A hypothesis that was still being investigated when the investigation stopped shows **Unresolved**.
   - **Conclusion**: The conclusion, connected to the hypothesis that was confirmed.
   - **Proposed action**: The actions that follow from the conclusion, each with a **High confidence**, **Medium confidence**, or **Low confidence** label.

   The tree also shows how many hypotheses were analyzed and how many were confirmed or dismissed.

1. To read a hypothesis in full, select its card.

Use **Fit to view** to fit the whole tree on screen, and **Close details** to close the panel.

## Review proposed actions [nightshift-investigations-actions]

An investigation ends with proposed actions, changes that Elastic nightshift suggests to mitigate or fix the problem. A proposed action might be a command to run, a configuration change, a code fix, or a rollback. You make the change yourself, then record in the investigation that you did. You need write access to Elastic nightshift to mark proposed actions as **applied** or **declined**.

1. From the Elastic nightshift home page, open the investigation.
1. In the **Proposed actions** section, select an action. Each action shows a title, a note such as **Apply manually**, and a status badge. Actions that you haven't reviewed show **Needs review**.
1. Read the explanation of why Elastic nightshift suggests the action and what it involves.
1. Make the change in your environment.
1. Select **Mark as applied**.

Marking an action as applied lets Elastic nightshift and your teammates know that you applied it. To undo your confirmation, open the action and select **Mark as not applied**.

If an action doesn't make sense for your system, open it, select **Decline**, and optionally enter a reason why you declined it.

## Ask follow-up questions in chat [nightshift-investigations-chat]

Chat with Elastic nightshift to ask questions about an investigation, such as how it reached a conclusion, or to ask it to check something else. The conversation continues the investigation, so Elastic nightshift keeps its findings in context. You need access to Agent Builder, which hosts the chat.

1. From the Elastic nightshift home page, open the investigation.
1. Select **Open chat**. The conversation opens in Agent Builder.
1. Ask your question. For example:

   - "How did you arrive at this conclusion?"
   - "What else changed in the checkout service around the same time?"

You can also select the {icon}`product_agent` **Open in chat** button on an investigation card on the home page.

### Add or challenge a hypothesis [nightshift-investigations-chat-hypothesis]

If Elastic nightshift missed a hypothesis, or you think it tested one incorrectly, for example because it didn't find the right data, ask it to add or challenge a hypothesis.

1. Open the investigation and select **Open chat**.
1. Ask Elastic nightshift to add or challenge a hypothesis. For example:

   - "Add and test a hypothesis that the checkout service failures were caused by a GCP outage."
   - "I don't think the database caused this. Challenge that hypothesis."

Elastic nightshift runs the hypothesis again and updates the hypothesis tree with the result, marked **Confirmed** or **Dismissed** with a confidence percentage.

### Check whether symptoms have returned to normal [nightshift-investigations-chat-symptoms]

After you apply a mitigation, ask Elastic nightshift whether the symptoms have returned to normal.

1. Open the investigation and select **Open chat**.
1. Ask whether the problem is resolved. For example, "Have the checkout errors returned to normal since I applied the rollback?"

## Check what Elastic nightshift has learned [nightshift-investigations-learned]

Elastic nightshift saves what it learns from investigations to the Wiki and Memory, and reuses it in later investigations. To see what it has learned, select {icon}`boxes_vertical` → **Knowledge** on the home page and open the **Wiki** tab. You can archive Wiki pages that aren't useful and restore them later. Refer to [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md).

## Use investigations in Slack [nightshift-investigations-slack]

Use Slack to talk to Elastic nightshift where your team already works, and to receive the results of investigations. An admin must have [connected the Slack channel](./get-started/connect-your-data-and-tools.md#nightshift-connect-slack) in {{kib}}.

- **Chat in a channel.** In a connected channel, mention `@elastic` in a thread and ask your question. Elastic nightshift streams its responses into the thread. A mention starts a conversation. To start an investigation, use an automation or start one in {{kib}}.
- **Receive results.** An automation with a Slack action posts the results of its investigations to the channel. Elastic nightshift posts a message when the investigation starts, then replies in the same thread when it finishes or fails. Refer to [Set up an automation](./set-up-an-automation.md).
- **Ask questions in the results thread.** When an automation posts the results of an investigation to a channel, you can ask questions about that investigation in the same thread. Mention or reply in the thread, and Elastic nightshift answers from the investigation. This applies to results that the Elastic Slack app posted, not to messages posted through a custom Slack connector.

Chat in Slack can't close, reopen, or reassign investigations. Do that in {{kib}}.

## Learn more [nightshift-investigations-nav]

- [Investigation engine](./investigations.md): Learn how investigations work
- [Set up an automation](./set-up-an-automation.md): Run investigations when an alert fires or on a schedule
- [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md): Review what Elastic nightshift has learned
- [Get started with Elastic nightshift](./get-started.md): Check the requirements, enable Elastic nightshift, and run your first investigation