---
navigation_title: Using Discover
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Convert an ES|QL query from Discover into a Kibana alerting v2 rule with the query pre-populated."
---

# Create Kibana alerting v2 rules in Discover [create-rules-discover-v2]

Create Kibana alerting v2 rules directly from Discover. When you build an ES|QL query in Discover that surfaces interesting patterns, you can convert it into a rule without rewriting the query.

While you prototype in Discover, each row in the result table is one document in {{es}}. After you save a rule, each evaluation run writes documents to `.rule-events`. The mode you select for the rule (Detect or Alert) determines whether those events are stored as `signal` or `alert` documents and whether `episode.*` fields exist. For how that maps to rows in Discover and how the stream is structured, refer to [Explore {{kib}} alerting v2 alerts and signals in Discover](../manage-alerts/explore-alerts-discover.md) and [Rule event and action field reference](../alert-event-field-reference.md).

## Create a rule from Discover

1. Open Discover and switch to ES|QL mode.
2. Write and run an ES|QL query that returns the data you want to monitor.
3. Review the results to confirm the query captures the pattern you want to alert on.
4. Open the Rules menu on the Discover toolbar and choose Create v2 ES|QL rule (wording may vary slightly by release). Legacy rule types from solutions or plugins appear under Create v1 rules when your deployment exposes them.
5. The rule creation form opens with the ES|QL query pre-populated in the evaluation field.
6. Configure the remaining rule settings:
   - Name and description.
   - Mode (detect or alert).
   - Schedule (execution interval and lookback window).
   - Grouping fields if applicable.
   - Alert delay, recovery, and no-data settings for alert mode.
   - Notification policies to link.
7. Optionally preview the rule results.
8. Click Save.

## What gets pre-populated

When you create a rule from Discover:

- The full ES|QL query from your current Discover session is placed into the rule's base query field.
- The index pattern is inferred from the `FROM` command in your query.
- The time range is converted into the rule's lookback window.

You can modify any of these values in the rule form before saving.
