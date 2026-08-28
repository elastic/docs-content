---
navigation_title: Experimental alerting system
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: The experimental Kibana alerting system writes each match as a rule event, then either tracks those events as an alert episode with notifications or records them as signals for later analysis.
---

# {{alerting-v2-system-cap}} overview [system-overview]

The {{alerting-v2-system}} in {{kib}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, and the system handles detection, tracking, and notification from there.

::::{note}
In the generally available {{kib}} alerting system, the term **alert** refers to a tracked occurrence of a rule condition. In the {{alerting-v2-system}}, the equivalent concept is called an **alert episode**. Each system's APIs, UI, and instructions apply only to that system's concepts.
::::

## The core idea [core-idea]

The {{alerting-v2-system}} starts with a rule evaluating your data on a schedule. When the rule detects a match, {{kib}} writes a rule event. The rule's configuration determines whether those events become a tracked alert episode or are recorded as signals for later analysis.

:::{image} /explore-analyze/images/basic-system-flow.png
:alt: Flowchart showing that after a rule detects a match, it either creates an alert episode or records a signal
:::

Because acting and recording are independent, you can change that configuration as your needs change. For example, you can record matches as signals first, then switch to alert episodes when you're ready to notify. Notifications are handled separately by action policies, so you can update where notifications are sent for multiple rules without editing each rule individually.

## The building blocks

The {{alerting-v2-system}} is built around five objects: rules, alert episodes, signals, action policies, and workflows, each with a distinct role.

### Rules

A rule defines what to watch for in your data and how often to check. On each run, {{kib}} writes matches as [rule events](experimental-alerting-system/rules/rule-event-field-reference.md). The rule's configuration determines whether those events become a tracked alert episode or are recorded as signals.

Refer to [Rules](experimental-alerting-system/rules.md) to learn more.

### Alert episodes

An alert episode tracks one problem and moves through states (pending, active, recovering, inactive), giving you one lifecycle to triage rather than a separate item per rule check. Alert episodes are passed to action policies for evaluation.

Refer to [Alert episodes](experimental-alerting-system/alerts.md) to learn more.

### Signals

A signal is a rule event that skips action policy evaluation entirely. As signals accumulate, you can query them in Discover, build dashboards from them, or feed them into another rule that correlates activity across sources, feeding back into the start of the flow.

Refer to [Query signals](experimental-alerting-system/alerts/query-signals.md) to learn more.

### Action policies

An action policy is the gating layer between an alert episode and a workflow. It decides whether and when to invoke a workflow by evaluating episode eligibility, match conditions, and frequency. A policy's configuration determines its scope, so one policy can cover alert episodes from a specific rule, multiple rules, or all rules in the space. This means you can change notification routing without touching any rule.

Refer to [Notifications and actions](experimental-alerting-system/notifications-actions.md) to learn more.

### Workflows

A workflow is what actually sends the notification or runs the automation, for example, posting to Slack, sending an email, calling a webhook. An action policy can invoke it, or a lifecycle trigger can invoke it immediately when the episode is activated or assigned.

Refer to [Connect workflows](experimental-alerting-system/workflows-alerting.md) to learn more.

## How the pieces fit together [how-pieces-fit-together]

Together, these building blocks form two main paths, which diverge based on the rule's configuration:

1. A rule evaluates your data on a schedule and detects a match.
2. {{kib}} writes the match as a rule event.
3. Based on the rule's configuration, {{kib}} either tracks the event as an alert episode or records it as a signal:

   * **Alert episode** - An action policy evaluates the episode and decides whether and when to invoke a workflow. The workflow sends the notification or runs the automation.

   * **Signal** - The event is recorded for later analysis and skips action policy evaluation and workflow invocation. You can query signals, build dashboards from them, or feed them into another rule.

:::{image} /explore-analyze/images/detailed-system-flow.png
:alt: Flowchart showing that after a rule finds a match, it either acts by creating an alert episode that an action policy evaluates and routes to trigger notifications or actions or records a signal that doesn't trigger notifications or actions
:::

## Get started or go deeper [system-overview-next-steps]

- **New to the {{alerting-v2-system}}?** [Get started](experimental-alerting-system/get-started.md) walks you through enabling the system, setting up role access, and creating your first rule with a hands-on tutorial.
- **Wondering what you can detect?** [Rules](experimental-alerting-system/rules.md) shows you how to define what to watch for in {{esql}}, and how to choose and configure the right creation path for your use case.
- **Curious what happens when something breaks?** [Alerts](experimental-alerting-system/alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- **Want the right people to know when it matters?** [Notifications and actions](experimental-alerting-system/notifications-actions.md) shows you how workflows and action policies decide who gets notified, and when.
