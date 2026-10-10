---
navigation_title: Route by severity
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to route alerts to different workflows based on severity level."
---

# Route alerts by severity [route-by-severity]

To send critical and non-critical alerts to different workflows in {{alerting-v2-system}}, scope one action policy per severity.

For example, you might page an on-call team for critical alerts while sending lower-severity alerts to a Slack channel for async review.

| Field | Action Policy A | Action Policy B |
|---|---|---|
| **Match conditions** | `severity: "critical"` | `severity: "low" OR severity: "medium" OR severity: "high"` |
| **Notify per** | Alert | Alert |
| **Frequency** | On status change | On status change |
| **Destinations** | PagerDuty workflow | Slack workflow |

Each action policy evaluates alerts independently.

- An alert with `severity: "critical"` matches Action Policy A but not Action Policy B.
- An alert with `severity: "high"` matches Action Policy B but not Action Policy A.
- If an alert's severity changes mid-lifecycle, the action policies that match it change accordingly. For example, if an alert escalates from `high` to `critical`, Action Policy A starts matching and Action Policy B stops matching. Action Policy A fires because it has no prior notification record for that alert.

## Related pages

- [Manage severity escalation notifications](severity-escalation.md): Understand what happens when an alert that has already matched an action policy changes severity.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [Create and configure an action policy](create-configure-action-policy.md): Set up an action policy with match conditions.
