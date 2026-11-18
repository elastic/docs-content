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

Ask {{nightshift}} for help without leaving Slack. Mention `@Elastic` in a thread, and {{nightshift}} starts an investigation and reports the results there. When an automation investigates an alert, the findings land in the channel, and anyone in the thread can ask follow-up questions.

## Before you begin [nightshift-uc-slack-before]

- An admin has [enabled {{nightshift}}](../get-started.md#nightshift-get-started-enable).
- An admin has connected your Slack workspace and the channel that you want to use. Refer to [Connect a Slack channel](#nightshift-uc-slack-connect).
- The channel is public. Private channels aren't supported in Tech Preview.

## Example: The on-call channel [nightshift-uc-slack-example]

Your team's alerts go to the `#ticketing-oncall` Slack channel. At 02:10 UTC, an alert says that `inventory-api` latency is above its threshold. A minute later, {{nightshift}} has started investigating, and a few minutes later it replies in the alert's thread with the impact, the conclusion, and the hypotheses it tested.

The on-call engineer reads the reply and asks in the thread: "@Elastic is ticket-issuer affected too?" {{nightshift}} continues the same investigation and answers in the thread.

## Connect a Slack channel [nightshift-uc-slack-connect]

An admin connects the Slack workspace once, then each public channel, on **Settings** → **General**. `@Elastic` answers only in connected channels. For the steps, refer to [Set up Slack](../investigation/set-up.md#nightshift-set-up-slack).

## Ask a question in a thread [nightshift-uc-slack-ask]

1. In a connected channel, start a thread, or open the thread that you want to ask about.
1. Mention `@Elastic` and ask your question. Be specific in your questions. Include the service, the symptom, and the time window. For example: "@Elastic why did checkout errors spike between 14:00 and 14:20 UTC?"

{{nightshift}} starts an investigation, shows its progress in the thread, and replies there with the results. The investigation also appears on the {{nightshift}} home page, with its hypothesis tree and proposed actions.

A mention that starts an investigation counts toward the **Manual investigations daily limit**; replies in the same thread don't. Refer to [Investigation limits](../investigation/limits.md).

## Get automation results in a thread [nightshift-uc-slack-results]

To get results in Slack automatically, set up an automation with a **Post in Slack** action. Refer to [Automatically investigate your alerts](./auto-investigate-alerts.md).

When the automation runs, {{nightshift}} posts a message when the investigation starts. When the investigation finishes or fails, it replies in the same thread. The reply shows:

- **Impact**: What the problem affects and how badly.
- **Conclusion**: The most likely cause and the evidence for it.
- **Hypotheses**: The explanations that {{nightshift}} tested, and which ones it confirmed or dismissed.

If your alerts already arrive in Slack from another app, an automation can watch for those messages and reply in the alert's thread instead.

## What you can do in Slack versus {{kib}} [nightshift-uc-slack-compare]

Use Slack to start investigations, ask follow-up questions, and read the impact, conclusion, and hypotheses. To explore the hypothesis tree, mark proposed actions as applied or declined, or close, reopen, or assign an investigation, open it in {{kib}}. If an investigation started in Slack, ask follow-up questions in the thread, because its chat in {{kib}} is read-only. Refer to [Limitations](../known-issues.md#nightshift-known-issues-slack).

## Next steps [nightshift-uc-slack-next]

- [Automatically investigate your alerts](./auto-investigate-alerts.md): Post investigation results to this channel for every matching alert.
- [Investigate anything](./investigate-anything.md): Read the full results, check the hypothesis tree, and act on proposed actions in {{kib}}.
- [Connect your data and tools](../investigation/set-up.md#nightshift-set-up-slack): Manage the Slack workspace, channels, and other connectors.
