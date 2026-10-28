---
navigation_title: No-data handling
applies_to:
  stack: ga 9.6+
  serverless: ga
products:
  - id: kibana
description: "How to configure the no-data strategy for rules: hold the last known alert state, trigger recovery, or ignore an empty query result."
---

# No-data handling in {{alerting-v2-system}} [no-data-handling]

No-data handling is an optional setting for {{alerting-v2-system}} rules that group matches into an alert. It controls what the rule does when it can't tell whether an alert has genuinely recovered or the data just stopped showing up. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting. In the rule form, the setting is **No data behavior**.

In YAML, set no-data handling with the `no_data` object.

## How no-data handling fits into recovery [no-data-and-recovery]

When a breached group stops matching, the rule runs a presence query to check whether the group still has data. By default, the presence query is the [base query](configure-rule-query.md#query-base). To use a different query, set `no_data.query`.

* **Group still has data**: The group isn't missing, so the rule treats this as a genuine [recovery](configure-rule-recovery.md) rather than a data gap. With **Custom recovery**, the alert recovers when the recovery condition matches. If the group has data but the condition doesn't match, the alert stays open.
* **Group has no data**: The rule can't tell whether the problem cleared up or the data source stopped reporting. What happens next depends on **No data behavior**.

This check runs for each group separately. If one host goes quiet while others keep reporting, the rule applies **No data behavior** to the alert for that host.

If **No data behavior** is **Do nothing**, the rule skips the presence query. With **Default recovery**, every group that stops matching then recovers.

**No data behavior** applies with any recovery option. With **No recovery**, the rule never recovers an alert on its own, but **Recover immediately** can still close an alert when its group has no data.

To use **Keep last known status** or **Recover immediately**, the rule needs an alert condition or a no-data query. Without one, a group that stops breaching looks the same as a group that has no data.

## No-data strategy options [no-data-strategy-options]

Choose one of the following options in the **No data behavior** field. Each maps to a strategy value if you're editing YAML directly.

| Option | `no_data.strategy` value | Description |
| --- | --- | --- |
| Keep last known status | `keep_last` | Hold the last known lifecycle state. An active breach stays active and a recovered alert stays recovered. |
| Recover immediately | `resolve` | Close the alert the first time the rule finds no data for the group. |
| Do nothing | `ignore` | Skip the no-data check. With **Default recovery**, a group that stops matching recovers, but the rule doesn't confirm that the data pipeline is actually working. This is the default. |

## When to configure no-data handling [no-data-when-to-use]

Configure no-data handling when:

* The data source your rule monitors can go silent. Examples include a metrics agent that stops reporting, a pipeline that breaks, or a service that stops generating events.
* A false recovery caused by an empty query result would be more harmful than holding the current alert state.
* Absence of data is itself a signal worth surfacing, such as missing heartbeat events from a critical service.

Leave no-data handling off, or set it to **Do nothing**, when:

* Your data source reliably produces output on every evaluation and a gap in data would indicate a genuine recovery. 
* You are still tuning the rule and don't yet know how it behaves when data is absent.

## Examples

### Maintain alert state during a metrics collection outage

Create a rule that monitors infrastructure CPU. Set **No data behavior** to **Keep last known status** so that if the metrics collection agent ever stops sending data, an active CPU breach doesn't auto-recover just because the query returned nothing. Instead, the rule holds the alert in its current state until data resumes.

### Close the alert when a queue empties out

Create a rule that monitors how many jobs are waiting in a queue and opens an alert when the backlog gets too large. To close the alert once the queue is empty and the query has nothing to return, set **No data behavior** to **Recover immediately** (`resolve`).

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md): How no-data handling fits into the recovery process.
- [No-data detection](esql-no-data-detection.md): An {{esql}} pattern for detecting one specific silent source, rather than an empty base query result.
