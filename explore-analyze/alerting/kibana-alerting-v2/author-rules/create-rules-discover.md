---
navigation_title: Using Discover
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Convert an ES|QL query from Discover into a Kibana alerting v2 rule with the query pre-populated."
---

# Create Kibana alerting v2 rules in Discover [create-rules-discover-v2]

Create Kibana alerting v2 rules directly from Discover. When you build an ES|QL query in Discover that surfaces interesting patterns, you can convert it into a rule without rewriting the query.

## Create a rule from Discover

1. Open **Discover** and switch to ES|QL mode.
2. Write and run an ES|QL query that returns the data you want to monitor. For example:

   ```esql
   FROM logs-*
   | WHERE http.response.status_code >= 500
   | STATS error_count = COUNT(*) BY api.endpoint
   | WHERE error_count > 100
   ```

3. Review the results to confirm the query captures the pattern you want to alert on.
4. Click **Create rule** (or **Alerts > Create rule**) from the Discover toolbar.
5. The rule creation form opens with the ES|QL query pre-populated in the evaluation field.
6. Configure the remaining rule settings:
   - **Name** and **description**.
   - **Mode** (detect or alert).
   - **Schedule** (execution interval and lookback window).
   - **Grouping** fields if applicable.
   - **Alert delay**, **recovery**, and **no-data** settings for alert mode.
   - **Notification policies** to link.
7. Optionally preview the rule results.
8. Click **Save**.

## What gets pre-populated

When you create a rule from Discover:

- The full ES|QL query from your current Discover session is placed into the rule's base query field.
- The index pattern is inferred from the `FROM` command in your query.
- The time range is converted into the rule's lookback window.

You can modify any of these values in the rule form before saving.

## When to use Discover vs. the rule form

Use Discover when you want to:

- Explore data interactively before deciding on alert conditions.
- Build and test complex ES|QL queries with immediate feedback.
- Convert ad hoc analysis into persistent monitoring.

Use the rule form directly when you:

- Already know the query and settings you want.
- Want to start from a template or existing rule.
- Need to configure advanced settings like state transitions that are not surfaced in Discover.
