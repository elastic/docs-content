---
navigation_title: Rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rules in the experimental alerting system define what to detect using ES|QL. Each match is written as a rule event, then handled as a signal or as part of an alert episode."
---

# Rules in the {{alerting-v2-system}} [rules]

A rule is where the {{alerting-v2-system}} starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. Alert episodes, signals, action policies, and notifications all flow from what a rule detects. 

This page explains what rules do, what they don't control, and how to choose a creation path.

## What rules do [detection-and-notification]

On each scheduled run, a rule executes an {{esql}} query against your data. {{kib}} records matches as [rule events](rules/rule-event-field-reference.md): one event per matching row, per run, written to `.rule-events`. {{kib}} never overwrites those events. The rule's mode, Signal or Alert, is the configuration that determines whether {{kib}} records those events as signals or tracks them as an alert episode.

In Signal mode, each event is a signal (`type: signal`) with no alert lifecycle or notifications. In Alert mode, each event is `type: alert` and carries `episode.*` fields. Events that share an `episode.id` form an alert episode. Episodes move through lifecycle states. An action policy can evaluate an episode and invoke a workflow to send a notification. Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts** to view them.

## What rules don't do 

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies, which are global objects scoped to your space that match alert episodes from any rule. A rule has no say in which action policies pick it up.

This separation means you can update notification routing without touching a rule, and have multiple action policies respond to the same rule independently.

## What to do next with rules [rules-next-steps]

From here, you can create, configure, and manage rules, and review what they've detected.

- [Create a rule](rules/create-a-rule.md): Compare creation paths and choose the one that fits your workflow.
- [Configure a rule](rules/configure-a-rule.md): Set the schedule, grouping, alert delay, recovery condition, and no-data behavior.
- [View and manage rules](rules/view-manage-rules.md): Enable, disable, clone, delete, and bulk-manage rules from the **Rules** page.
- [Review rule execution history](rules/review-rule-execution-history.md): Monitor rule execution outcomes across all rules in a space.
- [{{esql}} query patterns](rules/esql-query-patterns.md): Browse query patterns ordered by complexity, from a basic event filter to SLO burn rate and persistent breach detection.
- [Rule events](rules/rule-event-field-reference.md): Understand the documents {{kib}} writes to `.rule-events`, and how they relate to signals and alert episodes.
- [Query signals](alerts/query-signals.md): Query Signal mode output in Discover and correlate signals with Alert mode rules.

:::{important} - How to use the {{alerting-v2-system}} documentation
Because the {{alerting-v2-system}} is still evolving, its UI can change before general availability. Rather than pointing to an exact button or menu, the documentation focuses on the underlying concepts and behavior. If something doesn't match what you see in the {{kib}} UI, look for the closest equivalent instead. The concepts and behaviors described in the documentation still apply.
:::