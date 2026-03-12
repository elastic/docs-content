---
navigation_title: Before you begin
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Prerequisites and setup steps to review before creating Kibana alerting v2 rules."
---

# Before you begin with Kibana alerting v2 [alerting-before-you-begin-v2]

Before creating Kibana alerting v2 rules, review the following prerequisites and setup steps.

## Prerequisites

To use Kibana alerting v2, you need:

- **{{stack}} 9.4 or later.**
- **ES|QL knowledge.** Kibana alerting v2 rules are defined using ES|QL queries. Familiarity with ES|QL syntax, aggregations, and the `STATS`, `WHERE`, `EVAL`, and `KEEP` commands is essential. Refer to the [ES|QL reference](/explore-analyze/query-filter/languages/esql.md) for details.
- **Data indexed in {{es}}.** Your source data (logs, metrics, traces, or alert events from other rules) must be indexed and accessible from the cluster where you create rules.
- **Appropriate privileges.** You need Kibana privileges to create and manage rules, notification policies, and workflows. Refer to [Alerting privileges](before-you-begin/alerting-privileges.md) for details.

## Key differences from Kibana alerting v1

If you are coming from Kibana alerting v1, note these differences:

- **You write the query.** Instead of selecting a rule type and filling in parameters, you write an ES|QL query that defines exactly what to look for and what data to include in each alert event.
- **Alerts are immutable.** Each rule evaluation appends new event documents rather than updating existing ones. This gives you a full history of every evaluation.
- **Notifications are separate from rules.** Instead of configuring actions on each rule, you create notification policies that match alerts and route them to workflow destinations. One policy can serve many rules.
- **Snooze is per series, not per rule.** You can snooze notifications for a specific host or service without silencing the entire rule.
- **Alert data is queryable.** Alert events are stored in standard {{es}} indices and can be queried with ES|QL in Discover, used in dashboards, or fed to other rules.

## Coexistence with Kibana alerting v1

Kibana alerting v2 runs alongside Kibana alerting v1. Both systems are fully operational:

- You access Kibana alerting v2 rules and Kibana alerting v1 rules from the same **Rules** navigation entry, in separate tabs.
- Each system writes to its own indices. Kibana alerting v2 alert events go to `.alerts-events-*`; Kibana alerting v1 alerts go to `.alerts-*`.
- There is no automatic migration. You can copy rules from Kibana alerting v1 to Kibana alerting v2 manually when you are ready.
- You can create rules on alerts that correlate across both systems by querying both alert indices.
