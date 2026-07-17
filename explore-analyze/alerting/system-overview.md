---
navigation_title: Experimental alerting system
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: The experimental Kibana alerting system uses ES|QL rules to detect conditions, track problems as alert episodes, and route notifications through reusable action policies.
---

# {{alerting-v2-system-cap}} overview [system-overview]

The {{alerting-v2-system}} in {{kib}} watches your {{es}} data continuously, so your team doesn't have to. You define the conditions that matter, such as when to open an issue, who should know, and how often to notify them. The system handles the rest.

::::{note}
In the generally available {{kib}} alerting system, the term **alert** refers to a tracked occurrence of a rule condition. In the {{alerting-v2-system}}, the equivalent concept is called an **alert episode**. The two terms describe similar ideas in different systems and are not interchangeable.
::::

## The core idea [core-idea]

The {{alerting-v2-system}} separates *detecting* a problem from *acting* on it:

- **Detecting** - Rules focus purely on what to watch for in your data and on collecting breach and recovery events.
- **Acting** - Action policies handle who gets notified, when, and how, independently of any rule.

You can build and test detection logic before wiring up any notifications, and update notification routing across all rules in one place without editing the rules themselves.

## The four building blocks

The {{alerting-v2-system}} is built around four objects: rules, alert episodes, action policies, and workflows, each with a distinct role.

### Rules

A rule defines what to watch for in your data and how often to check, and runs in one of two modes: alert, which opens and tracks an alert episode until the condition clears, or signal, which records results over time without opening episodes or sending notifications.

Refer to [Rules](experimental-alerting-system/rules.md) to learn more.

### Alert episodes

In Alert mode, the rule opens one alert episode per problem and keeps it open until the condition clears. The alert episode moves through states (pending, active, recovering, inactive), giving you one lifecycle to triage rather than a separate item per rule check.

Refer to [Alert episodes](experimental-alerting-system/alerts.md) to learn more.

### Action policies

An action policy is the gating layer between an alert episode and a workflow. It decides whether and when to invoke a workflow by evaluating episode eligibility, match conditions, and frequency. Policy configuration determines the scope. A policy can apply to alert episodes from a specific rule, multiple rules, or all rules in the space.

Refer to [Notifications and actions](experimental-alerting-system/notifications-actions.md) to learn more.

### Workflows

A workflow is what actually sends the message or runs the automation, for example, posting to Slack, sending an email, calling a webhook. The {{alerting-v2-system}} invokes workflows in two ways: action policies that you configure to route alert episodes to a workflow based on match conditions and frequency, or alert episode lifecycle triggers that invoke a workflow immediately in response to a specific episode event, such as when it's activated or assigned.

Refer to [Connect workflows](experimental-alerting-system/workflows-alerting.md) to learn more.

## How the pieces fit together [how-pieces-fit-together]

At the simplest level:

1. A rule checks your data on a schedule.
2. The rule's query returns results when data matching its conditions is found.
3. The rule's mode determines what happens next:
   - Alert - The rule opens an alert episode to track the problem. An action policy can route it to a workflow to perform an action or send a notification.
   - Signal - Each result is recorded for querying later. Nothing else happens.

For a more detailed explanation of each stage, refer to [How the {{alerting-v2-system}} works](experimental-alerting-system/how-it-works.md).

## How to get started or go deeper [system-overview-next-steps]

- **New to the {{alerting-v2-system}}?** [Get started](experimental-alerting-system/get-started.md) walks you through enabling the system, setting up role access, and creating your first rule with a hands-on tutorial.
- **Wondering what you can detect?** [Rules](experimental-alerting-system/rules.md) shows you how to define what to watch for in {{esql}}, and how to choose and configure the right creation path for your use case.
- **Curious what happens when something breaks?** [Alerts](experimental-alerting-system/alerts.md) explains how alert episodes track a problem from first detection through recovery, and how to triage them as they come in.
- **Want the right people to know when it matters?** [Notifications and actions](experimental-alerting-system/notifications-actions.md) shows you how workflows and action policies decide who gets notified, and when.
