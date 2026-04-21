---
navigation_title: Rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "What {{alerting-v2}} rules are, how evaluation works, and how rules connect to alerts and notifications."
---

# Rules

A rule is where {{alerting-v2}} starts. It points {{kib}} at the data you care about, describes what counts as a problem in {{esql}}, and says how often to check. Alerts, action policies, and notifications all flow from what a rule detects.

## What rules do [detection-and-notification-v2]

$$$detection-and-notification-v2$$$

On each run, a rule executes an {{esql}} query against your data. If the query finds a match. If the rule is in Detect mode, it writes a _signal_, a point-in-time record that the condition was met. In Alert mode, it also maintains an _alert episode_ for each matched series, tracking state from first breach through recovery.

When creating a rule, choose Detect mode to record and query results without alerting anyone, or Alert mode when you want to track issues and route notifications.

## What rules don't do 

Rules only define *what* to detect. They don't control notifications, who gets notified, or when. That's the job of action policies — global objects, scoped to your space, that match episodes from any rule. A rule has no say in which policies pick it up.

This separation means you can build and test a rule without anyone getting paged, update notification routing without touching the rule, and have multiple action policies respond to the same rule independently.

% ## How rule history works

% Rules never overwrite old data. Each evaluation appends rows to `.rule-events`, giving you a complete, queryable history of every time the condition was met, when it cleared, and what the data looked like.

% When a rule groups by fields (for example `BY host.name`), each unique combination is its own series, identified by `group_hash`. An episode spans one lifecycle arc on a series from first breach through recovery, identified by `episode_id`.

% You can query this history in Discover, build dashboards from it, or write follow-on rules that read `.rule-events` as a data source.

## What's next

- **[Author rules](rules/author-rules-v2.md):** Write the {{esql}} query, choose Detect or Alert mode, and structure your data sources and conditions.
- **[View and manage rules](rules/view-manage-rules-v2.md):** Enable, disable, clone, delete, and bulk-manage rules from the rules list.
