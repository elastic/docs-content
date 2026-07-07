---
navigation_title: Review execution history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use the Execution History page in Kibana's experimental alerting system to monitor rule and action policy execution outcomes across all rules in a space."
---

# Review execution history in the {{alerting-v2-system}} [review-execution-history]

Execution history gives you a cross-rule, filterable log of every rule run across all rules in the space. Use it to spot patterns that aren't visible when looking at individual rules, for example, a cluster of failures at the same timestamp that points to a shared dependency issue.

<!--
TODO: When PR #6525 (execution history page) is merged:
- Add a cross-reference here to the "Review execution history" page added in that PR.
- Add a link on that page pointing back to this page.
-->

## Rule execution records [rule-execution-records]

Rule execution records are displayed in a table with the following columns:

| Column | Description |
|---|---|
| **Timestamp** | When the rule execution ran. |
| **Rule** | The rule that ran. Selecting the rule name opens a summary so you can inspect the rule without leaving the page. |
| **Duration** | How long the execution took. |
| **Response** | The outcome of the run: `success` or `failure`. |
| **Message** | An optional message included with the execution result, typically an error description for failed runs. |

Use the outcome filter to view only successful or failed executions. Filtering is applied server-side. Results are limited to 10,000 records.
