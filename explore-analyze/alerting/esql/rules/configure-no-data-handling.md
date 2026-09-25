---
navigation_title: No-data handling
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to configure the no-data strategy for rules: hold the last known alert state, trigger recovery, or ignore an empty query result."
---

# No-data handling [no-data-handling]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

No-data handling controls what the rule does when it can't tell whether an alert episode has genuinely recovered or the data just stopped showing up. Setting this correctly prevents false recoveries and misleading `no_data` events when data sources stop reporting.

::::{applies-switch}

:::{applies-item} stack: experimental =9.5

No-data handling is optional for rules that group matches into an alert episode. The YAML field is `no_data_strategy`.

:::

:::{applies-item} { stack: experimental 9.6+, serverless: ga }

Alert rules must set `no_data`. Signal rules must omit it. Omitting `no_data` on an alert rule fails validation.

:::

::::

## How no-data handling fits into recovery [no-data-and-recovery]

:::::{applies-switch}

::::{applies-item} stack: experimental =9.5

When a breached group stops matching, the rule re-runs the [base query](configure-rule-query.md#query-base) to confirm the group is actually gone before recovering the alert episode:

* **Group still there** - The base query still returns the group, confirming this is a genuine [recovery](configure-rule-recovery.md) rather than a data gap.
* **Group missing too** - The base query returns nothing for the group either, so the rule can't tell whether the problem actually cleared up or the data source just stopped reporting. What happens next depends on how you've configured `no_data_strategy`.

The check described above is part of the recovery process, so it only runs when `recovery_strategy` is **Default** or **Custom recovery**.

If `recovery_strategy` is **No recovery** instead, alert episodes stay open until someone closes them manually, the base-query check above doesn't run, and `no_data_strategy` has no effect.

::::

::::{applies-item} { stack: experimental 9.6+, serverless: ga }

For any strategy other than **Do nothing**, the rule needs a presence query so it can tell a group that stopped breaching from a group that has no data. Set `no_data.query`, or omit it and set `query.breach`. If you omit `no_data.query`, the rule uses `query.base` as the presence query.

* **Group still there.** The presence query still returns the group, so this is a [recovery](configure-rule-recovery.md) rather than a data gap.
* **Group missing too.** The presence query does not return the group. What happens next depends on `no_data.strategy`.

**Do nothing** (`ignore`) skips this check. Missing groups do not produce `no_data` events.

::::

:::::

## No-data strategy options [no-data-strategy-options]

:::::{applies-switch}

::::{applies-item} stack: experimental =9.5

Choose one of the following options. Each maps to a `no_data_strategy` value if you're editing YAML directly.

| Option | `no_data_strategy` value | Description |
| --- | --- | --- |
| Keep last status | `last_known_status` | Hold the last known lifecycle state. An active breach stays active and a recovered alert episode stays recovered. |
| Recover | `recover` | Treat absence as recovery. |
| Do nothing | `none` | Skip the no-data check. An empty result is treated the same as **Recover**, but the rule doesn't confirm that the data pipeline is actually working. |

:::{note}
`no_data_strategy` only triggers when the base query returns **zero rows**. If one host or data source goes quiet but others keep reporting, the query still returns rows for the ones still reporting, so `no_data_strategy` won't trigger. To catch a single silent source in that situation, use the {{esql}} pattern in [No-data detection](esql-no-data-detection.md), which turns a silent source into its own alert row.
:::

::::

::::{applies-item} { stack: experimental 9.6+, serverless: ga }

Choose one of the following options. Each maps to a `no_data.strategy` value if you're editing YAML directly.

| Option | `no_data.strategy` | Description |
| --- | --- | --- |
| **Keep last known status** | `keep_last` | Hold the alert episode's current status when the rule finds no data for the group. |
| **Recover immediately** | `resolve` | Close the alert episode the first time the rule finds no data for the group. |
| **Do nothing** | `ignore` | Do not check whether a group still has data. |

`no_data.strategy: alert` is a stored value that marks an existing alert episode active when the rule finds no data. Create and update requests reject it, and the rule form does not offer it.

To check presence with a query other than `query.base`, set `no_data.query`. Do not set `no_data.query` when the strategy is `ignore`.

:::{note}
If one host or data source goes quiet but others keep reporting, the presence query can still return rows for the ones that report. To catch a single silent source, use the {{esql}} pattern in [No-data detection](esql-no-data-detection.md), which turns a silent source into its own alert row.
:::

::::

:::::

## When to configure no-data handling [no-data-when-to-use]

Configure no-data handling when:

* The data source your rule monitors can go silent. Examples include a metrics agent that stops reporting, a pipeline that breaks, or a service that stops generating events.
* A false recovery caused by missing data would be more harmful than holding the current alert state.
* Absence of data is itself a signal worth surfacing, such as missing heartbeat events from a critical service.

::::{applies-switch}

:::{applies-item} stack: experimental =9.5

Do not configure `no_data_strategy`, or set it to **Do nothing**, when:

* Your data source reliably produces output on every evaluation and a gap in data would indicate a genuine recovery.
* You are still tuning the rule and don't yet know how it behaves when data is absent.

:::

:::{applies-item} { stack: experimental 9.6+, serverless: ga }

Set `no_data.strategy` to `ignore` (**Do nothing**) when:

* Your data source reliably produces output on every evaluation and a gap in data would indicate a genuine recovery.
* You are still tuning the rule and don't yet know how it behaves when data is absent.

:::

::::

## Examples

### Maintain alert state during a metrics collection outage

Create a rule that monitors infrastructure CPU. Configure the no-data strategy as **Keep last known status** so that if the metrics collection agent stops sending data, an active CPU breach doesn't recover just because the query returned nothing. The rule holds the alert episode in its current state until data resumes.

::::{applies-switch}

:::{applies-item} stack: experimental =9.5

In YAML, set `no_data_strategy` to `last_known_status`. The rule form calls this option **Keep last status**.

:::

:::{applies-item} { stack: experimental 9.6+, serverless: ga }

In YAML, set `no_data.strategy` to `keep_last`.

:::

::::

### Close the alert episode when a queue empties out

Create a rule that monitors how many jobs are waiting in a queue and opens an alert episode when the backlog gets too large. Configure the no-data strategy so that once the queue is empty and the query has nothing to return, the alert episode closes.

::::{applies-switch}

:::{applies-item} stack: experimental =9.5

In YAML, set `no_data_strategy` to `recover`. The rule form calls this option **Recover**.

:::

:::{applies-item} { stack: experimental 9.6+, serverless: ga }

In YAML, set `no_data.strategy` to `resolve`. The rule form calls this option **Recover immediately**.

:::

::::

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Recovery condition](configure-rule-recovery.md): How no-data handling fits into the recovery process.
- [No-data detection](esql-no-data-detection.md): An {{esql}} pattern for detecting one specific silent source, rather than an empty base query result.
