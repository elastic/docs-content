---
navigation_title: Rules
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Rules define what to detect using ES|QL. Each match is written as a rule event. The rule's configuration determines whether those events are grouped into an alert."
---

# Rules [rules]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

In {{alerting-v2-system}}, a rule is where detection starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. On each scheduled run, {{kib}} writes each matching row as a [rule event](rules/rule-event-field-reference.md) to `.rule-events`. Those events are never overwritten.

## Workflows on action policies send notifications [rules-dont-control-notifications]

A rule doesn't send notifications. [Action policies](action-policies/about-action-policies.md) match alerts from any rule and invoke a workflow, which sends the notification. Because routing lives on the policy, you can change it without editing a rule, and several policies can respond to the same alert independently.

## Create, configure, and manage rules [rules-next-steps]

- [Create a rule](rules/create-a-rule.md): Compare creation paths and select the one that fits your workflow.
- [Configure a rule](rules/configure-a-rule.md): Set the schedule, grouping, alert delay, recovery condition, and no-data behavior.
- [Rule mode](rules/configure-rule-mode.md): Set whether matches are grouped into an alert or remain available for later analysis.
- [View and manage rules](rules/view-manage-rules.md): Enable, disable, clone, delete, and bulk-manage rules from the **Rules** page.
