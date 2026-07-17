---
navigation_title: Recovery condition
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to configure when and how an Alert-mode rule recovers in the experimental alerting system: the recovery strategy and the delay before an episode closes."
---

# Recovery condition in the {{alerting-v2-system}} [recovery-condition]

Recovery condition settings are optional for Alert-mode rules in the {{alerting-v2-system}}. They control how the rule decides an alert episode has resolved and how much confirmation it needs before closing the episode. Setting these correctly ensures episodes close when the underlying problem is actually fixed, rather than staying open indefinitely, closing for the wrong reason, or flapping between open and closed.

## Recovery strategy [recovery-strategy-options]

Choose one of the following options. Each maps to a `recovery_strategy` value if you're editing YAML directly.

| Option | `recovery_strategy` value | Description |
| --- | --- | --- |
| Default | `no_breach` | Recovers an episode once its group stops breaching but still shows up in the base query (checked without the alert condition applied). That second check confirms the group is actually healthy, not just missing from the data. This is the default and covers most rules. |
| Custom recovery | `query` | Evaluates a separate recovery condition. A match recovers the episode. No match falls back to the same base-query check as **Default**. |
| No recovery | `none` | Turns off automatic recovery entirely. Episodes stay open until closed manually. Because recovery is never evaluated, no-data handling never runs either. |

:::{note}
An unset `recovery_strategy` behaves the same as **No recovery**, but unset usually means the setting was overlooked rather than a deliberate choice.
:::

An empty base query result triggers [no-data handling](configure-no-data-handling.md) for rules using **Default** or **Custom recovery**.

### When to change the recovery strategy [recovery-strategy-when-to-use]

Choose **Custom recovery** when:

* The condition that should close an episode isn't simply "no longer breaching." For example, a value needs to drop back to a safe margin below the original breach threshold, not just dip under it once. Define a separate recovery condition to require that.

Choose **No recovery** when:

* Episodes for this rule should never close automatically, because closing should always be a deliberate decision, such as for a security investigation that isn't necessarily resolved just because the query stopped matching.

Leave the recovery strategy set to **Default** when:

* The breach condition no longer matching is a reliable enough signal that the problem is resolved. This covers most rules.

## Recovery delay [recovery-delay]

Recovery delay controls how much confirmation the rule needs, once the recovery strategy's condition is met, before it actually closes the episode. This is separate from the recovery strategy: the strategy decides *what* counts as recovered, and the delay decides *how many times or for how long* that signal must hold before the episode closes. The same three modes available for [alert delay](configure-rule-alert-delay.md) apply:

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Closes the episode as soon as recovery is detected on the first evaluation. | Use when a single non-breaching evaluation is enough confidence that the problem is resolved. |
| Recoveries | Closes the episode after recovery is detected a set number of times in a row. | Use when a rule alternates between breaching and recovering on consecutive evaluations, and you want to avoid a constant stream of open and closed notifications. |
| Duration | Closes the episode after recovery has held continuously for a set time. | Use when you need the condition to stay resolved for a minimum stretch of time before you trust it, rather than just counting evaluations. |

### Recovery delay fields

| Field | Type | Accepted values | Description |
| --- | --- | --- | --- |
| `recovering_count` | integer | 0–1000 | Number of consecutive non-breaching evaluations required before the alert episode closes. Set to `0` to skip the recovering phase and transition directly to inactive on recovery. |
| `recovering_timeframe` | duration | Any duration string | How long the condition must remain non-breaching before the alert episode closes. |
| `recovering_operator` | string | `AND` or `OR` | When both `recovering_count` and `recovering_timeframe` are set, controls whether both must be satisfied (`AND`) or either one is enough (`OR`). |

Timeframe fields accept duration strings between `5s` and `365d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

:::{note}
In the YAML rule schema, these fields are prefixed with `state_transition.`. For example, `recovering_count` here is `state_transition.recovering_count` in the [YAML rule schema reference](yaml-rule-schema-reference.md#state-transition-fields). They are the same fields.
:::

You can combine Recoveries and Duration by setting both `recovering_count` and `recovering_timeframe`. Use `recovering_operator: AND` to require both conditions before the episode closes, or `recovering_operator: OR` if either condition alone is enough.

## Examples

### Recover only after a value returns to a safe margin, not just below the breach threshold

Create a rule that monitors CPU usage and opens an episode above 90%. Recovering as soon as usage dips to 89% would reopen and close the episode repeatedly during normal fluctuation. Set the recovery strategy to **Custom recovery** and define a recovery condition that only matches once CPU drops below 70%. The episode stays active through the fluctuation and recovers only when usage is solidly back in a safe range.

### Require a manual decision before closing an episode

Create a rule that detects a potential security incident. Even after the query stops matching, the investigation might still be ongoing. Set the recovery strategy to **No recovery**. The episode never closes on its own. Someone has to review and close it manually.

### Require consecutive recoveries before closing an episode

Create a rule that monitors database connection pool saturation. After the condition clears, set `recovering_count` to `3` to require 3 consecutive non-breaching evaluations before closing the episode. Without this, a rule that alternates between breaching and recovering on consecutive evaluations generates a constant stream of open and closed notifications.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [Alert delay](configure-rule-alert-delay.md): The equivalent delay before an episode opens.
- [No-data handling](configure-no-data-handling.md): How the rule behaves when it can't confirm whether a group's absence is a genuine recovery.
