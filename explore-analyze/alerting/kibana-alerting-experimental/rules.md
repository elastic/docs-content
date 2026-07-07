---
navigation_title: Rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rules in Kibana's experimental alerting system define what to detect using ES|QL. Evaluation runs on a schedule and alerts, action policies, and notifications flow from rule detections."
---

# Rules in the {{alerting-v2-system}}

A rule is where the {{alerting-v2-system}} starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. Alerts, action policies, and notifications all flow from what a rule detects. 

This page explains what rules do, what they don't control, and how to choose a creation path.

## What rules do [detection-and-notification]

On each run, a rule executes an {{esql}} query against your data. Matches are recorded as rule events (`rule_event`), and handled according to the rule's mode, which can be Signal mode or Alert mode. 

In Signal mode, each matching row is stored as a signal document with no alert lifecycle or notifications. In Alert mode, the rule creates and tracks an alert episode for each match. Episodes move through lifecycle states, appear on the Alerts UI, and can trigger notifications through action policies.

## What rules don't do 

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies, which are global objects scoped to your space that match alert episodes from any rule. A rule has no say in which policies pick it up.

This separation means you can build and test a rule without anyone getting paged, update notification routing without touching the rule, and have multiple action policies respond to the same rule independently.

## Next steps

- **[Create a rule](rules/create-a-rule.md):** Compare creation paths and choose the one that fits your workflow.
- **[Configure a rule](rules/configure-a-rule.md):** Set the schedule, grouping, activation thresholds, recovery conditions, and no-data behavior.
- **[View and manage rules](rules/view-manage-rules.md):** Enable, disable, clone, delete, and bulk-manage rules from the rules list.
- **[Review execution history](rules/review-execution-history.md):** Monitor rule and action policy execution outcomes across all rules in a space.
- **[ES|QL query patterns](rules/esql-query-patterns.md):** Browse query patterns ordered by complexity, from a basic event filter to SLO burn rate and persistent breach detection.