---
navigation_title: Recovery strategy
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to configure the recovery strategy for Alert-mode rules in the experimental alerting system. Controls whether an episode closes automatically, via a custom condition, or never."
---

# Recovery strategy in the {{alerting-v2-system}} [recovery-strategy]

Recovery strategy is an optional setting for Alert-mode rules in the {{alerting-v2-system}}. Use `recovery_strategy` to control how the rule decides an alert episode has resolved and can close automatically. Setting this correctly ensures episodes close when the underlying problem is actually fixed, rather than staying open indefinitely or closing for the wrong reason.

## Recovery strategy options [recovery-strategy-options]

Choose one of the following options. Each maps to a `recovery_strategy` value if you're editing YAML directly.

| Option | `recovery_strategy` value | Description |
| --- | --- | --- |
| Default | `no_breach` | Recovers an episode as soon as its active group no longer appears in the breach results. This is the default and covers most rules. |
| Custom recovery | `query` | Evaluates a separate recovery condition. The episode only recovers when this condition matches, independent of whether the breach condition still matches. |
| No recovery | `none` | Turns off automatic recovery entirely. Episodes stay open until closed manually. |

:::{note}
An unset `recovery_strategy` is treated differently from an explicit `none`: leaving it unset means no recovery events are emitted at all, while `none` is a deliberate choice to disable recovery. Both leave episodes open indefinitely, but only the second reflects an intentional decision.
:::

## When to change the recovery strategy [recovery-strategy-when-to-use]

Choose **Custom recovery** when:

* The condition that should close an episode isn't simply "no longer breaching." For example, a value needs to drop back to a safe margin below the original breach threshold, not just dip under it once. Define a separate recovery condition to require that.

Choose **No recovery** when:

* Episodes for this rule should never close automatically, because closing should always be a deliberate decision, such as for a security investigation that isn't necessarily resolved just because the query stopped matching.

Leave the recovery strategy set to **Default** when:

* The breach condition no longer matching is a reliable enough signal that the problem is resolved. This covers most rules.

## Examples

### Recover only after a value returns to a safe margin, not just below the breach threshold

This rule monitors CPU usage and opens an episode above 90%. Recovering as soon as usage dips to 89% would reopen and close the episode repeatedly during normal fluctuation. Set the recovery strategy to **Custom recovery** and define a recovery condition that only matches once CPU drops below 70%. The episode stays active through the fluctuation and recovers only when usage is solidly back in a safe range.

Use this when a value hovering near the breach threshold would otherwise cause the episode to flap between active and recovered.

### Require a manual decision before closing an episode

This rule detects a potential security incident. Even after the query stops matching, the investigation might still be ongoing. Set the recovery strategy to **No recovery**. The episode never closes on its own; someone has to review and close it directly.

Use this when treating "no longer matching" as "resolved" would be misleading or risky.
