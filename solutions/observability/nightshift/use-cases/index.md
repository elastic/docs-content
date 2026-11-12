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

{{nightshift}} investigates problems in your system and reports the likely cause, the evidence, and actions you can take. You can ask it about one problem yourself, call it into a Slack thread, point it at an alert, have it investigate your alerts automatically, or let it find problems that no alert catches. Each page in this section walks you through one of these, with a real example.

## Your goal [nightshift-use-cases-goals]

| Your goal | Start here | What you get |
| --- | --- | --- |
| Ask about a problem in your own words | [Investigate anything](./investigate-anything.md) | An investigation of the problem you describe, such as "Why is checkout latency up?", with a likely cause, evidence, and proposed actions. |
| Get help where your team already talks | [Investigate in Slack](./investigate-in-slack.md) | An investigation that starts when you mention `@Elastic` in a channel, with the results in the thread for everyone to read. |
| Find out why an alert fired | [Investigate your alerts](./investigate-alerts.md) | An investigation that starts from the alert, so it has the service, the symptom, and the time window from the start. |
| Have alerts investigated before you look at them | [Automatically investigate your alerts](./auto-investigate-alerts.md) | An automation that investigates each matching alert or significant event and posts the findings to Slack, without anyone starting it. |
| Investigate alerts that fire in your other tools | [Investigate alerts from your other tools](./external-alerts.md) | An automation that investigates alerts from another monitoring tool, an {{ech}} deployment, PagerDuty, or a script, when they arrive in Slack or by webhook. |
| Find problems that none of your alerts catch | [Detect problems automatically](./detect-problems.md) | Significant events: related unusual changes in your logs, grouped into one problem that you can review and investigate. |

Haven't set up {{nightshift}} yet? Do the [Get started](../get-started.md) checklist first. It enables {{nightshift}}, connects your data, and runs your first investigation.

## How the use cases build on each other [nightshift-use-cases-map]

You don't have to do these in order, but most teams move from left to right: they start investigations themselves, then let {{nightshift}} start them.

1. **Investigate anything.** You describe a problem on the {{nightshift}} home page, read the result, and check the reasoning. This is where you learn how investigations work.
1. **Investigate in Slack** and **Investigate your alerts.** You start the same kind of investigation from where you already are: a Slack thread or an alert.
1. **Automatically investigate your alerts.** An automation starts an investigation for each matching alert and posts the results in Slack. Nobody has to start it.
1. **Detect problems automatically.** Detection finds problems that you don't have alerts for. Add its significant events to an automation, and those are investigated too.

Every investigation adds to the wiki and memory that {{nightshift}} keeps about your system, so later investigations start from that context. Refer to [How {{nightshift}} builds context](../context/index.md).

## Next steps [nightshift-use-cases-next]

- [Investigate anything](./investigate-anything.md): Start here if you haven't run an investigation yet.
- [How investigations work](../investigation/index.md): Learn what an investigation does and how to judge its results.
- [The home page](../homepage.md): Find your way around the place where all investigations are listed.
