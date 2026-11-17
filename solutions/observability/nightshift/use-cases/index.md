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

{{nightshift}} investigates problems in your system and reports the likely cause, provides evidence, and proposes actions you can take. You can ask it about a problem from the home page, call it into a Slack thread, point it at an alert, have it investigate your alerts automatically, or let it find problems that no alert catches. Find your use case in the following list.

## Before you begin [nightshift-use-cases-prereqs]

If you haven't set up {{nightshift}}, follow the [Get started](../get-started.md) checklist to enable {{nightshift}}, connect your data, and run your first investigation.

## Select a use case [nightshift-use-cases-goals]

Each guide walks you through a scenario from start to finish.

- [Investigate anything](./investigate-anything.md): Investigate a problem you describe, such as "Why is checkout latency up?", and receive a likely cause, evidence, and proposed actions.
- [Investigate in Slack](./investigate-in-slack.md): Connect and start investigations from Slack. Mention `@Elastic` in a channel, and receive the results in the thread where your team can read them.
- [Investigate your alerts](./investigate-alerts.md): Start an investigation from an alert, so {{nightshift}} has the service, the symptom, and the time window from the start.
- [Automatically investigate your alerts](./auto-investigate-alerts.md): Set up an automation that investigates each matching alert or significant event and posts the findings to Slack, without anyone starting it.
- [Investigate alerts from your other tools](./external-alerts.md): Set up an automation that investigates alerts from an external monitoring tool, an {{ech}} deployment, PagerDuty, or a script, when they arrive in Slack or by webhook.
- [Detect problems your alerts miss](./detect-problems.md): Use detection and significant events to find unusual changes in your logs and group them into one problem that you can review and investigate.

## Next steps [nightshift-use-cases-next]

- [The home page](../homepage.md): Get an overview of where your investigations are listed.
- [How {{nightshift}} builds context](../context/index.md): Learn how every investigation adds to the Wiki and Memory, so later investigations start with that context.
- [How investigations work](../investigation/index.md): Learn what an investigation does and how to judge its results.
