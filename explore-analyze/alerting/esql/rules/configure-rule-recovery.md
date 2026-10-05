---
navigation_title: Recovery condition
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to configure when and how an alert episode recovers: the recovery strategy and the delay before an alert episode closes."
---

# Recovery condition [recovery-condition]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

Recovery settings control how the rule decides an alert episode has resolved and how much confirmation it needs before closing the alert episode. When you set these correctly, alert episodes close when the underlying problem ends, rather than staying open indefinitely, closing for the wrong reason, or flapping between open and closed.

Signal rules don't use recovery settings. For alert rules:

* {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` You must set `recovery`.
* {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` You can omit `recovery_strategy`, but the rule then behaves as if it's set to **No recovery**.

## Recovery strategy [recovery-strategy-options]

Select one of the following options. If you're editing YAML directly, use the value for your version.

| Option | `recovery.strategy` value {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | `recovery_strategy` value {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | Description |
| --- | --- | --- | --- |
| **Default recovery** | `no_breach` | `no_breach` | Recovers the alert episode when its group no longer breaches. This covers most rules. |
| **Custom recovery** | `condition` | `query` | Recovers the alert episode when a separate recovery condition returns the group. Requires an alert condition. Without one, every row of the base query breaches, so the recovery condition never succeeds. |
| **No recovery** | `manual` | `none` | Doesn't recover automatically. The alert episode stays open until someone closes it. <br><br> No-data handling doesn't run either. {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` |

When a group has no data at all, [no-data handling](configure-no-data-handling.md) decides what happens to its alert episode.

{applies_to}`{ serverless: ga, stack: experimental 9.6+ }` To recover with a query that has its own `FROM` clause, set `recovery.strategy` to `query` and provide `recovery.query` in YAML. The rule form doesn't offer this option.

## When to change the recovery strategy [recovery-strategy-when-to-use]

Keep **Default recovery** when a group leaving the breach results reliably means the problem is over. This covers most rules.

Change the recovery strategy when:

* Leaving the breach results isn't enough to close an alert episode. For example, a value needs to drop to a safe margin under the breach threshold, not dip under it once. Use **Custom recovery** to define that condition.
* You want someone to close each alert episode deliberately. For example, a security investigation can continue after the query stops matching. Use **No recovery**.

## Recovery delay [recovery-delay]

Recovery delay controls how much confirmation the rule needs, once the recovery strategy's condition is met, before it actually closes the alert episode. This is separate from the recovery strategy: the strategy decides *what* counts as recovered, and the delay decides *how many times or for how long* that signal must hold before the alert episode closes. The same three modes available for [alert delay](configure-rule-alert-delay.md) apply:

| Mode | Behavior |
| --- | --- |
| Immediate | Closes the alert episode on the first evaluation that detects recovery. |
| Recoveries | Closes the alert episode after the rule detects recovery a set number of times in a row. |
| Duration | Closes the alert episode after recovery has held continuously for a set time. |

## When to configure recovery delay [recovery-delay-when-to-use]

Keep **Immediate** when a single non-breaching evaluation gives you enough confidence that the problem is over.

Add a recovery delay when:

* The rule alternates between breaching and recovering on consecutive evaluations, and you want to avoid a constant stream of open and closed notifications. Use **Recoveries**.
* The condition needs to stay resolved for a minimum stretch of time before you trust it, rather than for a number of evaluations. Use **Duration**.

## Recovery delay fields [recovery-delay-fields]

| Field | Type | Accepted values | Description |
| --- | --- | --- | --- |
| `recovering_count` | integer | 0–1000 | Number of consecutive non-breaching evaluations required before the alert episode closes. Set to `0` to skip the recovering phase and transition directly to inactive on recovery. |
| `recovering_timeframe` | duration | Any duration string | How long the condition must remain non-breaching before the alert episode closes. |
| `recovering_operator` | string | `and` or `or` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` <br><br> `AND` or `OR` {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | Whether the rule requires both `recovering_count` and `recovering_timeframe`, or only one, when you set both. |

Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

To combine Recoveries and Duration, set both `recovering_count` and `recovering_timeframe`, then use `recovering_operator` to decide whether the alert episode closes after both conditions hold or after either one does.

In the [YAML rule schema](yaml-rule-schema-reference.md#state-transition-fields), these fields live under `state_transition`:

- {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` Nested under `state_transition.recovering`. For example, `recovering_count` is `state_transition.recovering.count`. The `recovering` object must set `count` or `timeframe`, and you can't set it when `recovery.strategy` is `manual`.
- {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` Prefixed with `state_transition.`. For example, `recovering_count` is `state_transition.recovering_count`.

## Examples

### Recover only after a value returns to a safe margin, not just below the breach threshold

Create a rule that monitors CPU usage and opens an alert episode above 90%. Recovering as soon as usage dips to 89% would reopen and close the alert episode repeatedly during normal fluctuation. Set the recovery strategy to **Custom recovery** and define a recovery condition that only matches once CPU drops below 70%. The alert episode stays active through the fluctuation and recovers only when usage is solidly back in a safe range.

### Require a manual decision before closing an alert episode

Create a rule that detects a potential security incident. Even after the query stops matching, the investigation might still be ongoing. Set the recovery strategy to **No recovery**. The alert episode never closes on its own. Someone has to review and close it manually.

### Require consecutive recoveries before closing an alert episode

Create a rule that monitors database connection pool saturation. After the condition clears, set `recovering_count` to `3` to require 3 consecutive non-breaching evaluations before closing the alert episode. Without this, a rule that alternates between breaching and recovering on consecutive evaluations generates a constant stream of open and closed notifications.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Alert delay](configure-rule-alert-delay.md): The equivalent delay before an alert episode opens.
- [No-data handling](configure-no-data-handling.md): How the rule behaves when it can't confirm whether a group's absence is a genuine recovery.
