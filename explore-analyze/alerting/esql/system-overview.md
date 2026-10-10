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

Use {{alerting-v2-system}} to detect conditions in your {{es}} data with {{esql}} rules. You can track each problem as an alert from first detection through recovery and route its notifications through reusable action policies, or record matches for later analysis without sending notifications.

:::{note}
Looking for {{alerting-v1-system}}? Refer to the [{{alerting-v1-system-cap}} overview](/explore-analyze/alerting/alerts.md). Both systems use the term **alert**, but they create and track alerts differently, so the APIs and instructions for one system don't apply to the other.

{applies_to}`stack: experimental =9.5` In {{stack}} 9.5, the {{alerting-v2-system}} pages, such as **Rules**, **Alerts**, and **Action Policies**, are under **Alerting V2 Preview** in **Stack Management** instead of under **Alerting** in the Observability navigation menu. The UI also calls an alert an **alert episode**. For example, the **Notify per** option for one notification per alert is **Episode** instead of **Alert**.
:::

## The building blocks

You create and configure rules, action policies, and workflows. {{kib}} generates the other two building blocks, rule events and alerts, from your rules' matches.

- [Rules](rules.md): Define what to watch for in your data and how often to check.
- [Rule events](rules/rule-event-field-reference.md): Record each match as a document in `.rule-events`.
- [Alerts](alerts.md): Track one problem from first detection through recovery, so you triage one lifecycle per problem.
- [Action policies](notifications-actions.md): Decide whether and when to invoke a workflow for an alert. You configure this on the policy, not on the rule, so you can change routing without editing each rule.
- [Workflows](workflows-alerting.md): Send the notification or run the automation, for example posting to Slack, sending an email, or calling a webhook.

## How the pieces fit together [how-pieces-fit-together]

$$$core-idea$$$

A rule evaluates your data on a schedule, and {{kib}} writes each match as a rule event. The rule's configuration determines the next step:

- **Alert**: {{kib}} groups the event into an alert. An action policy evaluates the alert and can invoke a workflow, which sends the notification or runs the automation.
- **No alert**: The event stays in `.rule-events` for later analysis. You can [query it in Discover](alerts/query-signals.md), build dashboards, or feed it into another rule. These events (`type: signal`) don't appear on the **Alerts** page and aren't evaluated by action policies or lifecycle triggers.

For a step-by-step walkthrough of what happens after a rule runs, refer to [How it works](get-started/how-it-works.md).

## Get started or go deeper [system-overview-next-steps]

- [Get started](get-started.md): Learn how the system works and its key terms, then create your first rule in a hands-on tutorial.
- [Set up {{alerting-v2-system}}](setup.md): Check the requirements, then turn the system on or off.
- [Manage](manage.md): Give your team the role privileges it needs, and manage the API keys that authorize rules, action policies, and workflows.
- [Rules](rules.md): Define what to watch for in {{esql}}, and decide which creation path fits your use case.
- [Alerts](alerts.md): Learn how alerts track a problem from first detection through recovery, and how to triage them.
- [Notifications and actions](notifications-actions.md): Learn how action policies decide when to invoke a workflow, and how workflows send the notification.
