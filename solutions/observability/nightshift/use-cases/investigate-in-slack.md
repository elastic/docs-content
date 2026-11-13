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

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable).
- An admin has connected your Slack workspace and the channel that you want to use. Refer to [Connect a Slack channel](#nightshift-uc-slack-connect).
- The channel is public. Private channels aren't supported in Tech Preview.

## Example: the on-call channel [nightshift-uc-slack-example]

In this example scenario, assume your team's alerts go to the `#ticketing-oncall` Slack channel. At 02:10 UTC, an alert says that `inventory-api` latency is above its threshold. A minute later, {{nightshift}} has started investigating, and a few minutes later it replies in the alert's thread with the impact, the conclusion, and the hypotheses it tested.

The on-call engineer reads the reply and asks in the thread: "@Elastic is ticket-issuer affected too?" {{nightshift}} continues the same investigation and answers in the thread.

## Connect a Slack channel [nightshift-uc-slack-connect]

An admin connects the Slack workspace once, then each channel, on **Settings** → **General**. `@Elastic` answers only in connected channels. Refer to [Slack](../investigation/set-up.md#nightshift-set-up-slack).

## Ask a question in a thread [nightshift-uc-slack-ask]

1. In a connected channel, start a thread, or open the thread that you want to ask about.
1. Mention `@Elastic` and ask your question. Be specific in your questions. Include the service, the symptom, and the time window. For example: "@Elastic why did checkout errors spike between 14:00 and 14:20 UTC?"

{{nightshift}} starts an investigation, shows its progress in the thread, and replies there with the results. The investigation also appears on the {{nightshift}} home page, with its hypothesis tree and proposed actions.

A mention that starts an investigation counts toward the **Manual investigations daily limit**; replies in the same thread don't. Refer to [Investigation limits](../investigation/limits.md).

## Read investigation results in a thread [nightshift-uc-slack-results]

To get results in Slack without anyone asking, set up an automation with a **Post in Slack** action. Refer to [Automatically investigate your alerts](./auto-investigate-alerts.md).

When the automation runs, {{nightshift}} posts a message when the investigation starts. When the investigation finishes or fails, it replies in the same thread. The reply shows:

- **Impact**: What the problem affects and how badly.
- **Conclusion**: The most likely cause and the evidence for it.
- **Hypotheses**: The explanations that {{nightshift}} tested, and which ones it confirmed or dismissed.

If your alerts already arrive in Slack from another app, an automation can watch for those messages and reply in the alert's own thread instead.

To ask about the results, reply in the thread. {{nightshift}} continues the same investigation with your reply and answers in the thread. For the full investigation, with the hypothesis tree and proposed actions, open it in {{kib}}.

:::{note}
Every human reply in a results thread continues the investigation, not only replies that mention `@Elastic`. This works only in threads that `@Elastic` posted. Results posted through a custom Slack connector can't be continued from Slack.
:::

## What you can do in Slack and in {{kib}} [nightshift-uc-slack-compare]

Slack is for asking and reading. Managing an investigation happens in {{kib}}.

| Task | Slack | {{kib}} |
| --- | --- | --- |
| Start an investigation and ask follow-up questions | Yes | Yes |
| Read impact, conclusion, and hypotheses | Yes | Yes |
| Explore the hypothesis tree and its charts | No | Yes |
| Mark proposed actions as applied or declined | No | Yes |
| Close, reopen, or assign an investigation | No | Yes |

For an investigation that started in Slack, ask follow-up questions in the thread. Its chat in {{kib}} is read-only. Refer to [Known issues](../known-issues.md#nightshift-known-issues-slack).

To open {{nightshift}} in {{kib}}, select **Nightshift** in the navigation menu. Refer to [The home page](../homepage.md).

:::{tip}
**Use the channel where the alert lands.** Answers in the alert's thread keep the context in one place for the whole team.
:::

## Next steps [nightshift-uc-slack-next]

- [Automatically investigate your alerts](./auto-investigate-alerts.md): Post investigation results to this channel for every matching alert.
- [Investigate anything](./investigate-anything.md): Read the full results, check the hypothesis tree, and act on proposed actions in {{kib}}.
- [Connect your data and tools](../investigation/set-up.md#nightshift-set-up-slack): Manage the Slack workspace, channels, and other connectors.
