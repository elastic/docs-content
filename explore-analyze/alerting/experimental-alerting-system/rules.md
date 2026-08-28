---
navigation_title: Rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rules in the experimental alerting system define what to detect using ES|QL. Each match is written as a rule event. The rule's configuration determines whether those events are grouped into an alert episode."
---

# Rules in the {{alerting-v2-system}} [rules]

A rule is where the {{alerting-v2-system}} starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. On each scheduled run, {{kib}} writes each matching row as a [rule event](rules/rule-event-field-reference.md) to `.rule-events`. Those events are never overwritten. Alert episodes, action policies, and notifications all flow from those events.

## Rules don't control notifications [rules-dont-control-notifications]

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies, which are global objects scoped to your space that match alert episodes from any rule. 

This separation means you can update notification routing without touching a rule, and have multiple action policies respond to the same rule independently.

## Create, configure, and manage rules [rules-next-steps]

Use these pages to create a rule, change its settings, or review what it has detected.

- [Create a rule](rules/create-a-rule.md): Compare creation paths and choose the one that fits your workflow.
- [Configure a rule](rules/configure-a-rule.md): Set the schedule, grouping, alert delay, recovery condition, and no-data behavior.
- [Rule mode](rules/configure-rule-mode.md): Set whether matches are grouped into an alert episode or left as signals.
- [View and manage rules](rules/view-manage-rules.md): Enable, disable, clone, delete, and bulk-manage rules from the **Rules** page.
- [Review rule execution history](rules/review-rule-execution-history.md): Monitor rule execution outcomes across all rules in a space.
- [{{esql}} query patterns](rules/esql-query-patterns.md): Browse query patterns ordered by complexity, from a basic event filter to SLO burn rate and persistent breach detection.
- [Rule events](rules/rule-event-field-reference.md): Understand the documents {{kib}} writes to `.rule-events`, and how they relate to signals and alert episodes.
- [Query signals](alerts/query-signals.md): Query signals in Discover and use them as input to a rule that opens an episode.

:::{important} - How to use the {{alerting-v2-system}} documentation
Because the {{alerting-v2-system}} is still evolving, its UI can change before general availability. Rather than pointing to an exact button or menu, the documentation focuses on the underlying concepts and behavior. If something doesn't match what you see in the {{kib}} UI, look for the closest equivalent instead. The concepts and behaviors described in the documentation still apply.
:::