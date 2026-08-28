---
navigation_title: Experimental alerting system
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: The experimental Kibana alerting system writes each match as a rule event, then either groups those events into an alert episode with notifications or leaves them available for later analysis.
---

# {{alerting-v2-system-cap}} overview [system-overview]

The {{alerting-v2-system}} in {{kib}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, and the system handles detection, tracking, and notification from there.

::::{note}
In the generally available {{kib}} alerting system, the term **alert** refers to a tracked occurrence of a rule condition. In the {{alerting-v2-system}}, the equivalent concept is called an **alert episode**. Each system's APIs, UI, and instructions apply only to that system's concepts.
::::

## The core idea [core-idea]

The {{alerting-v2-system}} starts with a rule evaluating your data on a schedule. When the rule detects a match, {{kib}} writes a rule event to `.rule-events`. The rule's configuration determines whether those events are grouped into an alert episode. Events that aren't part of an episode remain available for later analysis as signals. 

You can change your rule's configuration as your needs change, including whether matches become alert episodes.

:::{image} /explore-analyze/images/basic-system-flow.png
:alt: Flowchart showing a rule detecting a match, Kibana writing a rule event, then either grouping that event into an alert episode or leaving it with no episode for later analysis
:::

## The building blocks

The {{alerting-v2-system}} is built around five objects: rules, rule events, alert episodes, action policies, and workflows, each with a distinct role.

### Rules

A rule defines what to watch for in your data and how often to check. On each run, {{kib}} writes matches as [rule events](experimental-alerting-system/rules/rule-event-field-reference.md).

Refer to [Rules](experimental-alerting-system/rules.md) to learn more.

### Rule events

A rule event is the document {{kib}} writes to `.rule-events` for each match. The rule's configuration determines whether those events are grouped into an alert episode.

Refer to [Rule events](experimental-alerting-system/rules/rule-event-field-reference.md) and [Query signals](experimental-alerting-system/alerts/query-signals.md) to learn more.

### Alert episodes

An alert episode tracks one problem from first detection through recovery, so you triage one lifecycle per problem.

Refer to [Alert episodes](experimental-alerting-system/alerts.md) to learn more.

### Action policies

An action policy decides whether and when to invoke a workflow for an alert episode. Notifications are configured on the policy, not on the rule, so you can update where they're sent without editing each rule.

Refer to [Notifications and actions](experimental-alerting-system/notifications-actions.md) to learn more.

### Workflows

A workflow sends the notification or runs the automation, for example posting to Slack, sending an email, or calling a webhook.

Refer to [Connect workflows](experimental-alerting-system/workflows-alerting.md) to learn more.

## How the pieces fit together [how-pieces-fit-together]

Together, these building blocks form two main paths, which diverge based on the rule's configuration:

1. A rule evaluates your data on a schedule and detects a match.
2. {{kib}} writes the match as a rule event to `.rule-events`.
3. The rule's configuration determines the next step:

   * **Alert episode** - {{kib}} groups the event into an episode. An action policy evaluates the episode and can invoke a workflow, which sends the notification or runs the automation.

   * **No episode** - The event remains available for later analysis as a signal. You can query it, build dashboards, or feed it into another rule. Action policies evaluate alert episodes only, so this event never reaches a policy or a workflow.

:::{image} /explore-analyze/images/detailed-system-flow.png
:alt: Flowchart showing a rule detecting a match, Kibana writing a rule event, then either grouping the event into an alert episode that an action policy can route to a workflow, or leaving the event with no episode for later analysis
:::

## Get started or go deeper [system-overview-next-steps]

- **New to the {{alerting-v2-system}}?** [Get started](experimental-alerting-system/get-started.md) walks you through enabling the system, setting up role access, and creating your first rule with a hands-on tutorial.
- **Wondering what you can detect?** [Rules](experimental-alerting-system/rules.md) shows you how to define what to watch for in {{esql}}, and how to choose and configure the right creation path for your use case.
- **Curious what happens when something breaks?** [Alerts](experimental-alerting-system/alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- **Want the right people to know when it matters?** [Notifications and actions](experimental-alerting-system/notifications-actions.md) shows you how workflows and action policies decide who gets notified, and when.
