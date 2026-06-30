---
navigation_title: Rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rules in Kibana's experimental alerting system define what to detect using ES|QL. Evaluation runs on a schedule; alerts, action policies, and notifications flow from rule detections."
---

# Rules in the {{alerting-v2-system}}

Rules are part of the {{alerting-v2-system}} in {{kib}}. For rules in the existing Kibana alerting system, see [Rules in Kibana alerting](../alerts/create-manage-rules.md).

A rule is where the {{alerting-v2-system}} starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. Alerts, action policies, and notifications all flow from what a rule detects. 

This page explains what rules do, what they don't control, and how to choose a creation path.

## What rules do [detection-and-notification]


On each run, a rule executes an {{esql}} query against your data. If the query finds a match and the rule is in Signal mode, it writes a _signal_, a point-in-time record that the condition was met. In Alert mode, it also maintains an _alert episode_ for each matched series, tracking state from first breach through recovery.

When creating a rule, choose Signal mode to record and query results without alerting anyone, or Alert mode when you want to track issues and route notifications.

## What rules don't do 

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies, which are global objects scoped to your space that match alert episodes from any rule. A rule has no say in which policies pick it up.

This separation means you can build and test a rule without anyone getting paged, update notification routing without touching the rule, and have multiple action policies respond to the same rule independently.

% ## How rule history works

% Rules never overwrite old data. Each evaluation appends rows to `.rule-events`, giving you a complete, queryable history of every time the condition was met, when it cleared, and what the data looked like.

% When a rule groups by fields (for example `BY host.name`), each unique combination is its own series, identified by `group_hash`. An alert episode spans one lifecycle arc on a series from first breach through recovery, identified by `episode_id`.

% You can query this history in Discover, build dashboards from it, or write follow-on rules that read `.rule-events` as a data source.

## Create a rule [create-a-rule]

Three creation options are available:

- **[Create ES|QL rule](rules/create-esql-rule.md)**: Write the detection query as {{esql}} directly, with a live preview of results and a YAML editor also available. Use this when you want full control over the query.
- **[Create with AI Agent](rules/create-rule-ai-agent.md)**: Describe what you want to detect in plain language. The AI agent generates a rule definition and walks you through reviewing and saving it. Use this when you know the problem but aren't sure how to write the {{esql}}.
- **[Start from a rule builder](rules/use-rule-builder.md)**: Choose a structured rule type and fill in a guided form. The builder generates the {{esql}} query automatically. Use this when you want to create a standard metric-threshold rule without writing {{esql}} by hand.

If you already have an {{esql}} query working in Discover, you can also [create a rule directly from there](rules/create-rule-from-discover.md) to skip re-entering the query.

## Next steps

- **[Author rules](rules/author-rules.md):** Write the {{esql}} query, choose Signal or Alert mode, and structure your data sources and conditions.
- **[Configure a rule](rules/configure-a-rule.md):** Set the schedule, grouping, activation thresholds, recovery conditions, and no-data behavior.
- **[View and manage rules](rules/view-manage-rules.md):** Enable, disable, clone, delete, and bulk-manage rules from the rules list.
- **Rule Doctor:** Analyze your rules for duplicates, stale conditions, threshold tuning opportunities, and coverage gaps. Rule Doctor surfaces findings with impact and confidence ratings and tracks each insight through an open → applied or dismissed lifecycle. Access it from the {{alerting-v2-system}} navigation.

<!-- TODO: Update this description and link to the Rule Doctor dedicated page once it is published. The page should cover the insight types, the open/applied/dismissed lifecycle, impact and confidence ratings, continuous analysis scheduling, and required privileges (read-alerting-v2-rule-doctor / write-alerting-v2-rule-doctor). -->