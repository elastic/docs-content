---
navigation_title: Rule mode
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How rule mode determines whether Kibana opens an alert episode or keeps matching rows available for later analysis, and when to use each."
---

# Rule mode in the {{alerting-v2-system}} [rule-mode]

Rule mode decides what happens when a rule finds a match. The match can raise an alert episode that your team triages and gets notified about, or it can become a record that you query later. Use this page to see what each mode does, when to use it, and how to set it.

## What each rule mode does [rule-mode-options]

Every rule runs in one of these modes:

| Mode | What it does |
| --- | --- |
| **Detect and respond** (**Alert** in earlier {{stack}} versions) | Opens a tracked [alert episode](../alerts.md) that {{kib}} follows as the condition persists and recovers. Alert episodes appear on the **Alerts** page for triage, and action policies can route them to workflows that notify your team. |
| **Collect evidence** (**Signal** in earlier {{stack}} versions) | Records each match as a [rule event](rule-event-field-reference.md) that you can [query in Discover](../alerts/query-signals.md), chart on a dashboard, or feed into a later rule. Matches never appear on the **Alerts** page and never notify anyone. |

## When to use each [rule-mode-when-to-use]

Select **Detect and respond** when:

* The query is ready for production, and you want each breach tracked as a distinct alert episode that opens, escalates, and closes when the condition clears.
* Your team triages, acknowledges, or escalates what the rule finds.
* You want action policies to invoke workflows when alert episodes open, escalate, or recover.
* You need to know how long a condition has been active or how it changes state. Matches recorded by **Collect evidence** carry no lifecycle.

Select **Collect evidence** when:

* You're still tuning the query and want to see what it catches without paging your on-call team. Preview the query in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox), then create the rule when the query is ready.
* You want to build detection history that you can query later, without adding alert noise.
* Nobody needs a notification when the condition fires. These matches reach no action policy.

## Set the rule mode [rule-mode-set]

Set either mode when you create the rule, using the rule form or YAML editor. In YAML, the mode is set in the `kind` field. To learn more, refer to the [YAML rule schema reference](yaml-rule-schema-reference.md).

:::{note}
You can't change the mode after you save the rule. To use the other mode, create a new rule, or create a copy of an existing rule and set the mode before you save it.
:::

## Examples

### Build detection history before opening alert episodes

You're writing a new detection query and want to verify it produces the results you expect before anyone gets paged. Preview the query in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox) or in Discover, then create the rule in the mode you want to keep.

To record matches without opening alert episodes or triggering notifications, create a rule that records rule events. If you later want those matches tracked as alert episodes, create a separate rule that opens an alert episode. You can reuse the same query, or write a follow-on query that reads those events from `.rule-events`. For the follow-on pattern, refer to [Correlate events in a follow-on rule](../alerts/query-signals.md#correlate-signals-alert-rule).

### Route critical alert episodes to an on-call workflow

You have a checkout service error rate rule and want on-call engineers notified when it fires. Create the rule so each breach opens a tracked alert episode that action policies can route to a workflow. The rule's alert episodes appear on the **Alerts** page and are visible to any action policy whose KQL matcher matches the alert episode fields.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Query rule events](../alerts/query-signals.md): Query events with `type: signal` in Discover, build dashboards, and use them as input to a rule that opens an alert episode.
- [Rule events](rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how `type` relates to rule `kind`.
