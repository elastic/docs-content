---
navigation_title: Review execution history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use the Execution History page in Kibana's experimental alerting system to monitor rule and action policy execution outcomes across all rules in a space."
---

# Review execution history in the {{alerting-v2-system}} [review-rule-execution-history]

Execution history gives you a cross-rule, filterable log of every rule run and action policy dispatch across the space. Rule executions and action policy dispatcher decisions are shown separately, with different scopes.

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

## Action policy dispatcher decisions [policy-execution-records]

Action policy execution history shows one row per action policy dispatcher decision and covers the **last 24 hours** only. Use it to audit whether action policies are dispatching as expected. Results are paginated up to 100 per page.
