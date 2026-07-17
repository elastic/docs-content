---
navigation_title: Review rule execution history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use the Execution History page in Kibana's experimental alerting system to monitor rule execution outcomes across all rules in a space."
---

# Review rule execution history in the {{alerting-v2-system}} [review-rule-execution-history]

Rule execution history gives you a cross-rule, filterable log of every rule run in the space.

## Rule executions [rule-execution-records]

Rule execution history shows one row per rule evaluation across all rules in the space. Use it to spot patterns that aren't visible when looking at individual rules, for example, a cluster of failures at the same timestamp that points to a shared dependency issue.

| Column | Description |
|---|---|
| **Timestamp** | When the rule execution ran. |
| **Rule** | The rule that ran. Selecting the rule name opens a summary so you can inspect the rule without leaving the page. |
| **Duration** | How long the execution took. |
| **Response** | The outcome of the run: `success` or `failure`. |
| **Message** | An optional message included with the execution result, typically an error description for failed runs. |

Use the outcome filter to view only successful or failed executions. Filtering is applied server-side. Results are paginated up to 100 per page. You can page through up to 10,000 records — this is a pagination ceiling, not a retention limit. Deeper history exists in the event log but is not reachable by paging further.

## Related pages

- [Review action policy execution history](../action-policies/review-action-policy-execution-history.md): Monitor dispatcher outcomes for the notifications a rule's alert episodes trigger.
- [View and manage rules](view-manage-rules.md): Find the rule behind a specific execution and inspect or edit it.