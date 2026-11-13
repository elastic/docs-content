---
navigation_title: What you can do
applies_to:
  serverless:
    observability: preview
description: Find the Elastic nightshift use case that fits your goal, from asking about one problem to having every alert investigated before you look at it.
products:
  - id: observability
  - id: cloud-serverless
---

# What you can do with {{nightshift}} [nightshift-use-cases]

{{nightshift}} investigates problems in your system and reports the likely cause, provides evidence, and proposes actions you can take. You can ask it about a problem from the home page, call it into a Slack thread, point it at an alert, have it investigate your alerts automatically, or let it find problems that no alert catches. Find your use case in the following table.

## Before you begin [nightshift-use-cases-prereqs]

If you haven't set up {{nightshift}}, follow the [Get started](../get-started.md) checklist to enable {{nightshift}}, connect your data, and run your first investigation.

## Select a use case [nightshift-use-cases-goals]

Each guide walks you through one scenario from start to finish.

| Use case | Guide | Description |
| --- | --- | --- |
| Ask about a problem in your own words | [Investigate anything](./investigate-anything.md) | Investigate a problem you describe, such as "Why is checkout latency up?", and receive a likely cause, evidence, and proposed actions. |
| Get help where your team already works | [Investigate in Slack](./investigate-in-slack.md) | Connect and start investigations from Slack. Mention `@Elastic` in a channel, and receive the results in the thread where your team can read them. |
| Find out why an alert fired | [Investigate your alerts](./investigate-alerts.md) | Start an investigation from an alert, so {{nightshift}} has the service, the symptom, and the time window from the start. |
| Have {{nightshift}} automatically investigate alerts | [Automatically investigate your alerts](./auto-investigate-alerts.md) | Set up an automation that investigates each matching alert or significant event and posts the findings to Slack, without anyone starting it. |
| Investigate alerts from your other tools | [Investigate alerts from your other tools](./external-alerts.md) | Set up an automation that investigates alerts from another monitoring tool, an {{ech}} deployment, PagerDuty, or a script, when they arrive in Slack or by webhook. |
| Find problems outside your alerts | [Detect problems automatically](./detect-problems.md) | Use significant events to find unusual changes in your logs and group them into one problem that you can review and investigate. |

## How the use cases work together [nightshift-use-cases-map]

The following is a typical flow your team might follow:

1. **Investigate anything.** Describe a problem on the {{nightshift}} home page, read the result, and check the reasoning to learn how investigations work.
1. **Investigate in Slack** and **Investigate your alerts.** Start an investigation from where you already work, like a Slack thread or an alert.
1. **Automatically investigate your alerts.** Create an automation that starts an investigation for each matching alert and posts the results in Slack.
1. **Detect problems automatically.** Use detections to find problems that you don't have alerts for. Add its significant events to an automation, and {{nightshift}} investigates those too.

Every investigation adds information about your system to the {{nightshift}} Wiki and Memory, so later investigations start with that context. Refer to [How {{nightshift}} builds context](../context/index.md).

## Next steps [nightshift-use-cases-next]

- [Investigate anything](./investigate-anything.md): Start here if you haven't run an investigation yet.
- [How investigations work](../investigation/index.md): Learn what an investigation does and how to judge its results.
- [The home page](../homepage.md): Get an overview of where your investigations are listed.
