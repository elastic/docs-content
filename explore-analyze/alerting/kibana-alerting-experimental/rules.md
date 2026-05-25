---
navigation_title: Rules
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "What rules are in the {{alerting-v2}}, how evaluation works, and how rules connect to alerts and notifications."
---

# Rules in {{alerting-v2}}

Rules are part of the {{alerting-v2}} in {{kib}}. For rules in the existing Kibana alerting system, see [Rules in Kibana alerting](../alerts/create-manage-rules.md).

A rule is where the {{alerting-v2}} start. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. Alerts, action policies, and notifications all flow from what a rule detects.

## What rules do [detection-and-notification]


On each run, a rule executes an {{esql}} query against your data. If the query finds a match and the rule is in Detect mode, it writes a _signal_, a point-in-time record that the condition was met. In Alert mode, it also maintains an _alert episode_ for each matched series, tracking state from first breach through recovery.

When creating a rule, choose Detect mode to record and query results without alerting anyone, or Alert mode when you want to track issues and route notifications.

## What rules don't do 

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies — global objects, scoped to your space, that match episodes from any rule. A rule has no say in which policies pick it up.

This separation means you can build and test a rule without anyone getting paged, update notification routing without touching the rule, and have multiple action policies respond to the same rule independently.

% ## How rule history works

% Rules never overwrite old data. Each evaluation appends rows to `.rule-events`, giving you a complete, queryable history of every time the condition was met, when it cleared, and what the data looked like.

% When a rule groups by fields (for example `BY host.name`), each unique combination is its own series, identified by `group_hash`. An episode spans one lifecycle arc on a series from first breach through recovery, identified by `episode_id`.

% You can query this history in Discover, build dashboards from it, or write follow-on rules that read `.rule-events` as a data source.

## Create a rule [create-a-rule]

Rules in the {{alerting-v2}} are always created and edited through a flyout. Three starting points are available:

- **From scratch**: Build the rule query and settings directly in the rule form. The form and the YAML editor are both available inside the same flyout; you can switch between them at any point without losing your work. Start here when you know what you want to detect. See [Create rules using the rule builder](rules/create-rule-from-rule-builder.md).
- **From Discover**: Start from an {{esql}} query you've already written and validated in Discover. The rule creation flyout opens pre-populated with the current query, so you can verify how the data groups before committing to a schedule. See [Create rules from Discover](rules/create-rule-from-discover.md).
- **With the AI agent**: Describe what you want to detect in plain language. Agent Builder generates a rule definition and walks you through reviewing and saving it. Use this when you know the problem but aren't sure how to express it as an {{esql}} query.

## Next steps

- **[Author rules](rules/author-rules.md):** Write the {{esql}} query, choose Detect or Alert mode, and structure your data sources and conditions.
- **[Configure a rule](rules/configure-a-rule.md):** Set the schedule, grouping, activation thresholds, recovery conditions, and no-data behavior.
- **[View and manage rules](rules/view-manage-rules.md):** Enable, disable, clone, delete, and bulk-manage rules from the rules list.