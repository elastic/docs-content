---
navigation_title: Rule mode
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How rule mode determines whether Kibana groups matching rows into an alert episode or keeps them available for later analysis, and when to use each."
---

# Rule mode in the {{alerting-v2-system}} [rule-mode]

Rule mode is a required setting for rules in the {{alerting-v2-system}}. It determines whether {{kib}} groups each [rule event](rule-event-field-reference.md) into an alert episode or keeps it available for later analysis. It's set by the rule creation method. Some [creation paths](create-a-rule.md) only support one mode.

| Mode | `kind` value | Behavior |
| --- | --- | --- |
| Signal | `signal` | {{kib}} writes a rule event with `type: signal` for each matching row. No alert episodes, no notifications. |
| Alert | `alert` | {{kib}} writes a rule event with `type: alert` and `episode.*` fields for each matching row. Events that share an `episode.id` form an alert episode. Episodes are tracked through lifecycle states, appear on the **Alerts** page, and can be routed to workflows by action policies. |

Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts** to view and triage alert episodes.

In YAML, this setting is the `kind` field on the rule. `kind` configures the rule. `type` on each rule event records what {{kib}} wrote for that run. Set `kind` when you create the rule. You can't change it later in the UI or in YAML. If you need the other mode, create another rule.

## When to use each [rule-mode-when-to-use]

Record matches without grouping them into an episode when:

* You're writing a new detection query and want to record matches without notifying anyone.
* You need to build detection history in `.rule-events` without generating alert noise or triggering notifications.

Recording matches without grouping them into an episode is **not** the right fit when:

* You need to track how long a condition has been active or how it transitions between states. Those events don't create episodes or lifecycle state.
* You need notifications when a condition fires. Create a rule that groups matches into an alert episode and attach an action policy.

Group matches into alert episodes when:

* The rule is production-ready and each breach should be tracked as a distinct alert episode that opens, can escalate, and closes when the condition clears.
* Alert episodes from the rule should be available for triage, acknowledgment, or escalation.
* You want to attach action policies to invoke workflows when alert episodes open, escalate, or recover.

Grouping matches into episodes is **not** the right fit when:

* You're still tuning the rule's query, and generating alert episodes creates noise for on-call teams. Preview the query in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox), then create it when the query is ready. To keep recording matches without episodes, create a separate rule that records rule events only.

## Examples

### Build detection history before enabling alert episodes

You're writing a new detection query and want to verify it produces the results you expect before anyone gets paged. Preview the query in the [query sandbox](create-esql-rule.md#rule-builder-query-sandbox) or in Discover, then create the rule in the mode you want to keep.

To record matches without opening episodes or triggering notifications, create a rule that records rule events. If you later want those matches tracked as episodes, create a separate rule that groups them into an episode. You can reuse the same query, or write a follow-on query that reads those events from `.rule-events`. For the follow-on pattern, refer to [Correlate events in a follow-on rule](../alerts/query-signals.md#correlate-signals-alert-rule).

### Route critical episodes to an on-call workflow

You have a checkout service error rate rule and want on-call engineers notified when it fires. Create the rule so each breach opens a tracked episode that action policies can route to a workflow. The rule's episodes appear on the **Alerts** page and are visible to any action policy whose KQL matcher matches the episode fields.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Create a rule](create-a-rule.md): Compare rule creation paths and choose the one that fits your workflow.
- [Query signals](../alerts/query-signals.md): Query events with `type: signal` in Discover, build dashboards, and use them as input to a rule that opens an episode.
- [Rule events](rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how `type` relates to rule `kind`.
- [Rule event data model](../alerts/rule-event-data-model.md): Shared `.rule-events` schema for `signal` and `alert` events.
