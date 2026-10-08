---
navigation_title: "{{alerting-v2-system-cap}}"
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Kibana Universal Alerting writes each match as a rule event, then either groups those events into an alert with notifications or keeps them available for later analysis.
---

# Overview [system-overview]

{{alerting-v2-system-cap}} runs rules against your {{es}} data on a schedule and writes each match as a rule event. Depending on the rule's configuration, {{kib}} either groups those events into an alert that can notify you through a workflow, or keeps them available for later analysis.

This page introduces the five objects in the system and how they connect. Use it to decide where to go next. For a step-by-step walkthrough after a rule runs, refer to [How it works](get-started/how-it-works.md).

:::{note}
Looking for {{alerting-v1-system}}? Refer to the [{{alerting-v1-system-cap}} overview](/explore-analyze/alerting/alerts.md). Both systems use the term **alert**, but they create and track alerts differently, so the APIs and instructions for one system don't apply to the other.

{applies_to}`stack: experimental =9.5` In {{stack}} 9.5, the {{alerting-v2-system}} UI calls an alert an **alert episode**. For example, the **Notify per** option for one notification per alert is **Episode** instead of **Alert**.
:::

## The core idea [core-idea]

{{alerting-v2-system-cap}} starts with a rule evaluating your data on a schedule. When the rule detects a match, {{kib}} writes a rule event to `.rule-events`. The rule's configuration determines whether those events are grouped into an [alert](alerts.md) and can notify. Events that aren't part of an alert remain available for later analysis.

## The building blocks

You create and configure three of the five building blocks: rules, action policies, and workflows. {{kib}} generates the other two, rule events and alerts, from your rules' matches.

### Rules

A rule defines what to watch for in your data and how often to check. On each run, {{kib}} writes matches as [rule events](rules/rule-event-field-reference.md).

Refer to [Rules](rules.md) to learn more.

### Rule events

A rule event is the document {{kib}} writes to `.rule-events` for each match.

Refer to [Rule events](rules/rule-event-field-reference.md) to learn more.

### Alerts

An [alert](alerts.md) tracks one problem from first detection through recovery, so you triage one lifecycle per problem.

Refer to [Alerts](alerts.md) to learn more.

### Action policies

An action policy decides whether and when to invoke a workflow for an alert. You configure that on the policy, not on the rule, so you can change routing without editing each rule. The workflow sends the notification.

Refer to [Notifications and actions](notifications-actions.md) to learn more.

### Workflows

A workflow sends the notification or runs the automation, for example posting to Slack, sending an email, or calling a webhook.

Refer to [Connect workflows](workflows-alerting.md) to learn more.

## How the pieces fit together [how-pieces-fit-together]

Every match becomes a rule event. From there, the rule's configuration determines the next step:

* **Alert** - {{kib}} groups the event into an [alert](alerts.md). An action policy evaluates the alert and can invoke a workflow, which sends the notification or runs the automation.

* **No alert** - The event stays in `.rule-events` for later analysis. You can [query it in Discover](alerts/query-signals.md), build dashboards, or feed it into another rule. Rule events that aren't part of an alert (`type: signal`) don't appear on **Alerts** and aren't evaluated by action policies or lifecycle triggers.

## Get started or go deeper [system-overview-next-steps]

- [Get started](get-started.md): Learn how the system works and its key terms, then create your first rule in a hands-on tutorial.
- [Set up {{alerting-v2-system}}](setup.md): Check the requirements, then turn the system on or off.
- [Manage](manage.md): Give your team the role privileges it needs, and manage the API keys that authorize rules, action policies, and workflows.
- [Rules](rules.md): Define what to watch for in {{esql}}, and decide which creation path fits your use case.
- [Alerts](alerts.md): Learn how alerts track a problem from first detection through recovery, and how to triage them.
- [Notifications and actions](notifications-actions.md): Learn how action policies decide when to invoke a workflow, and how workflows send the notification.
