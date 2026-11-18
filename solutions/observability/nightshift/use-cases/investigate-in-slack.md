---
navigation_title: Investigate in Slack
applies_to:
  serverless:
    observability: preview
description: Bring Elastic nightshift into your Slack channels. Ask it questions in a thread, read investigation results where your team already talks, and follow up in the same thread.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigate in Slack [nightshift-investigate-in-slack]

Ask {{nightshift}} for help without leaving Slack. Mention `@Elastic` in a thread, and {{nightshift}} answers your question there. When an automation investigates an alert, the findings land in the channel, and anyone in the thread can ask follow-up questions.

## Before you begin [nightshift-uc-slack-before]

- An admin has [enabled {{nightshift}}](../get-started.md#nightshift-get-started-enable).
- An admin has connected your Slack workspace and the channel that you want to use. Refer to [Connect a Slack channel](#nightshift-uc-slack-connect).
- For automations, the channel is public. In a private channel, you can mention `@Elastic` and get answers, but messages there can't start automations. Private channels also need private channel access. Refer to [Private channels](../slack-app.md#nightshift-slack-app-private).

## Example: The on-call channel [nightshift-uc-slack-example]

Your team's alerts go to the `#ticketing-oncall` Slack channel, where an automation with the **New message in channel** trigger watches for messages from your alerting app. At 02:10 UTC, an alert says that `inventory-api` latency is above its threshold. Because the alert matches the automation's trigger, {{nightshift}} starts investigating a minute later, and a few minutes after that it replies in the alert's thread with the impact, the conclusion, and the hypotheses it tested. To set up an automation like this one, refer to [Investigate alerts from your other tools](./external-alerts.md#nightshift-uc-ext-slack).

The on-call engineer reads the reply and asks in the thread: "@Elastic is ticket-issuer affected too?" {{nightshift}} continues the same investigation and answers in the thread.

## Connect a Slack channel [nightshift-uc-slack-connect]

An admin connects the Slack workspace once, then each channel, on **Settings** → **General**. `@Elastic` answers only in connected channels. For the steps, refer to [Set up Slack](../investigation/set-up.md#nightshift-set-up-slack).

## Ask a question in a thread [nightshift-uc-slack-ask]

1. In a connected channel, start a thread, or open the thread that you want to ask about.
1. Mention `@Elastic` and ask your question. Be specific in your questions. Include the service, the symptom, and the time window. For example: "@Elastic why did checkout errors spike between 14:00 and 14:20 UTC?"

{{nightshift}} shows its progress in the thread and replies there with the answer, with a **View in {{kib}}** link to the conversation. A mention answers a question; it doesn't start an investigation. Investigations start from automations, or when you start one in {{kib}}. Refer to [Investigate anything](./investigate-anything.md).

A mention that opens a new conversation counts toward the **Manual investigations daily limit**, even though it doesn't start an investigation. Follow-up mentions in the same thread don't count. Refer to [Investigation limits](../investigation/limits.md).

## Get automation results in a thread [nightshift-uc-slack-results]

To get results in Slack automatically, set up an automation with a **Post in Slack** action. Refer to [Automatically investigate your alerts](./auto-investigate-alerts.md).

When the automation runs, {{nightshift}} posts a message when the investigation starts. When the investigation finishes or fails, it replies in the same thread. The reply shows:

- **Impact**: What the problem affects and how badly.
- **Conclusion**: The most likely cause and the evidence for it.
- **Hypotheses**: The explanations that {{nightshift}} tested, and which ones it confirmed or dismissed.

If your alerts already arrive in Slack from another app, an automation can watch for those messages and reply in the alert's thread instead.

## Discuss an investigation in its thread [nightshift-uc-slack-discuss]

You don't need to mention `@Elastic` for {{nightshift}} to use what your team says in an investigation's thread. When someone replies there without a mention, {{nightshift}} adds the reply to the investigation as context and runs the investigation again in the same conversation, one reply at a time. It doesn't answer the reply, but when the run finishes, it updates the investigation's status message in the thread with any new findings. To ask a question and get an answer, mention `@Elastic`.

This works in public channels only, because messages in private channels never reach your project unless they mention `@Elastic`. In {{kib}}, each reply appears in the investigation's chat, with its Slack author named in the message text.

## What you can do in Slack versus {{kib}} [nightshift-uc-slack-compare]

Use Slack to ask questions, follow up on investigations that automations post, and read the impact, conclusion, and hypotheses. To explore the hypothesis tree, mark proposed actions as applied or declined, or close, reopen, or assign an investigation, open it in {{kib}}. If a conversation started in Slack, ask follow-up questions in the thread, because its chat in {{kib}} is read-only. Refer to [Known issues](../known-issues.md#nightshift-known-issues-slack).

## Next steps [nightshift-uc-slack-next]

- [Automatically investigate your alerts](./auto-investigate-alerts.md): Post investigation results to this channel for every matching alert.
- [Investigate anything](./investigate-anything.md): Read the full results, check the hypothesis tree, and act on proposed actions in {{kib}}.
- [Connect your data and tools](../investigation/set-up.md#nightshift-set-up-slack): Manage the Slack workspace, channels, and other connectors.
