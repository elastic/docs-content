---
navigation_title: Route by severity
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to route alert episodes to different workflows based on severity level in the experimental alerting system."
---

# Route alert episodes by severity in the {{alerting-v2-system}} [routing-by-severity]

When your rules in the {{alerting-v2-system}} produce alert episodes at different severity levels, you can route them to different workflows by creating separate action policies that are scoped to specific severity values using match conditions.

For example, you might page an on-call team for critical episodes while sending lower-severity episodes to a Slack channel for async review.

| Field | Policy A | Policy B |
|---|---|---|
| **Policy type** | Global | Global |
| **Match conditions** | `severity: "critical"` | `severity: "low" OR severity: "medium" OR severity: "high"` |
| **Notify per** | Episode | Episode |
| **Frequency** | On status change | On status change |
| **Destinations** | PagerDuty workflow | Slack workflow |

Each policy evaluates alert episodes independently.

- An episode with `severity: "critical"` matches Policy A but not Policy B.
- An episode with `severity: "high"` matches Policy B but not Policy A.
- If an episode's severity changes mid-lifecycle, the policies that match it change accordingly. For example, if an episode escalates from `high` to `critical`, Policy A starts matching and Policy B stops matching. Policy A fires because it has no prior notification record for that episode.

## Related pages

- [Manage severity escalation notifications](severity-escalation.md) explains what happens when an episode that has already matched a policy changes severity.
- [Action policy reference](action-policy-reference.md) for match condition fields, grouping modes, and frequency options.
- [Create and configure an action policy](create-configure-action-policy.md) to set up a policy with match conditions.
