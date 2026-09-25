---
navigation_title: Experimental alerting system
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: The experimental Kibana alerting system writes each match as a rule event, then either groups those events into an alert episode with notifications or keeps them available for later analysis.
---

# {{alerting-v2-system-cap}} overview [system-overview]

The {{alerting-v2-system}} in {{kib}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, and the system handles detection, tracking, and notification from there.

This page introduces the five objects in the system and how they connect. Use it to decide where to go next. For a step-by-step walkthrough after a rule runs, refer to [How it works](how-it-works.md).

::::{note}
In the generally available {{kib}} alerting system, the term **alert** refers to a tracked occurrence of a rule condition. In the {{alerting-v2-system}}, the equivalent concept is called an **alert episode**. Each system's APIs, UI, and instructions apply only to that system's concepts.
::::

## The core idea [core-idea]

The {{alerting-v2-system}} starts with a rule evaluating your data on a schedule. When the rule detects a match, {{kib}} writes a rule event to `.rule-events`. The rule's configuration determines whether those events are grouped into an [alert episode](alerts.md) and can notify. Events that aren't part of an alert episode remain available for later analysis.

## The building blocks

You create and configure three of the five building blocks: rules, action policies, and workflows. {{kib}} generates the other two, rule events and alert episodes, from your rules' matches.

### Rules

A rule defines what to watch for in your data and how often to check. On each run, {{kib}} writes matches as [rule events](rules/rule-event-field-reference.md).

Refer to [Rules](rules.md) to learn more.

### Rule events

A rule event is the document {{kib}} writes to `.rule-events` for each match.

Refer to [Rule events](rules/rule-event-field-reference.md) to learn more.

### Alert episodes

An [alert episode](alerts.md) tracks one problem from first detection through recovery, so you triage one lifecycle per problem.

Refer to [Alerts](alerts.md) to learn more.

### Action policies

An action policy decides whether and when to invoke a workflow for an alert episode. You configure that on the policy, not on the rule, so you can change routing without editing each rule. The workflow sends the notification.

Refer to [Notifications and actions](notifications-actions.md) to learn more.

### Workflows

A workflow sends the notification or runs the automation, for example posting to Slack, sending an email, or calling a webhook.

Refer to [Connect workflows](workflows-alerting.md) to learn more.

## How the pieces fit together [how-pieces-fit-together]

Every match becomes a rule event. From there, the rule's configuration determines the next step:

* **Alert episode** - {{kib}} groups the event into an [alert episode](alerts.md). An action policy evaluates the alert episode and can invoke a workflow, which sends the notification or runs the automation.

* **No episode** - The event stays in `.rule-events` for later analysis. You can [query it in Discover](alerts/query-signals.md), build dashboards, or feed it into another rule. Rule events that aren't part of an alert episode (`type: signal`) don't appear on **Alerts** and aren't evaluated by action policies or lifecycle triggers.

## Get started or go deeper [system-overview-next-steps]

- **New to the {{alerting-v2-system}}?** [Get started](get-started.md) walks you through enabling the system, setting up role access, and creating your first rule with a hands-on tutorial.
- **Wondering what you can detect?** [Rules](rules.md) shows you how to define what to watch for in {{esql}}, and how to choose and configure the right creation path for your use case.
- **Curious what happens when something breaks?** [Alerts](alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- **Want the right people to know when it matters?** [Notifications and actions](notifications-actions.md) shows you how action policies decide when to invoke a workflow, and how workflows send the notification.
