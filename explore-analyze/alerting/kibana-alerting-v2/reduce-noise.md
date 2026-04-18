---
navigation_title: Reduce noise and false positives
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Match each {{alerting-v2}} situation to a control: rule settings, notification policies, or alert episode actions."
---

# Reduce {{alerting-v2}} noise and false positives [reduce-noise-v2]

{{alerting-v2}} offers many ways to reduce noise. Controls live in three places:

- **[Rule settings](author-rules/rule-settings.md)**: Thresholds, no-data handling, rule-level grouping, {{maint-windows-cap}}, and related evaluation settings.
- **[Send notifications](send-notifications.md)**: Action policies: matchers, Dispatch per, Frequency, destinations, and dispatcher behavior.
- **[View and manage alert episodes](manage-alerts.md)**: Snooze, acknowledge, deactivate, tags, and anything persisted in **`.alert-actions`**.

This page is a **decision table** so you can match a situation to the right mechanism. Deep content lives on the pages above.

If multiple rows in the table apply, refer to [Using them together](#using-them-together).

## Select the right approach

| Your situation | Use this | What it does |
|---|---|---|
| The {{esql}} query matches too much normal traffic with too many breaching rows | [Author and tune the rule](author-rules.md) | Narrows the query, `WHERE` clause, schedule, or lookback so evaluations only surface what matters |
| Short spikes or flapping metrics open alerts before they should | [Activation and recovery thresholds](author-rules/rule-settings.md#activation-recovery-thresholds-v2) | Requires consecutive breaches or a minimum duration before an episode becomes active |
| The alert recovers and reopens too often, flapping | [Activation and recovery thresholds](author-rules/rule-settings.md#activation-recovery-thresholds-v2) | Requires sustained clear conditions before an episode leaves recovering |
| The query returns no rows and no_data or recovery behavior is misleading | [No-data handling](author-rules/rule-settings.md#no-data-handling-v2) | Configures how empty results are interpreted so gaps do not look like false recoveries or false alerts |
| Notifications repeat for the same group on every evaluation | [Throttling on action policies](send-notifications.md#throttle-v2) | Enforces a minimum interval between notifications per notification group |
| Recipients get too many separate messages for related episodes | [Notification grouping on action policies](send-notifications.md#reduce-noise-grouping-v2) | Batches related alerts into fewer notifications |
| Notifications should only go out for certain episodes by severity, labels, or payload fields | [Matchers](send-notifications.md#matcher-v2) | Uses KQL on the action policy over episode and rule context (for example `rule.labels` and payload fields) so only matching episodes route to workflows |
| Planned maintenance: evaluations should continue but on-call should not be paged | [{{maint-windows-cap}}](author-rules/rule-settings.md#maintenance-windows-v2) | Pauses notifications for a scheduled window |
| A temporary quiet period is needed for a series or episode without changing the rule | [Investigate and respond](manage-alerts/investigate-respond.md#alert-actions-v2) (snooze, silence, acknowledge) | Snoozes or silences notifications. Acknowledge can also quiet an episode while work proceeds |
| Many low-level alerts should roll up into one higher-level signal | [Author rules](author-rules.md) ({{esql}} over `.rule-events`) | Runs follow-on rules on `.rule-events` or related data to correlate and notify once |
| One alert episode should stop notifying and leave the triage queue while the rule keeps running | [Investigate and respond](manage-alerts/investigate-respond.md#alert-actions-v2) (deactivate / resolve) | Deactivates that episode. The rule still evaluates and can detect new episodes for other series |

Use the links in the table for procedures and reference detail on each control.

## Key distinctions

|  | Tune rule / schedule | Activation / recovery thresholds | No-data handling | Matchers / grouping / throttle | {{maint-windows-cap}} / snooze / silence | Rules on alerts | Deactivate / resolve |
|---|---|---|---|---|---|---|---|
| Rule still evaluates | Yes | Yes | Yes | Yes | Yes | Yes, source rules | Yes |
| Changes breach detection logic | Yes | No, delays state only | Yes, empty-result policy | No | No | N/A | No |
| Reduces notifications | If fewer breaches | Indirectly | Indirectly | Yes | Yes | Yes | Yes |
| Typical time scope | Until next edit | Consecutive runs / duration | Per evaluation | Policy config | Window or until cleared | N/A | Until episode handled |

## Using them together [using-them-together]

These options stack. A common pattern is: tune the query for precision, add activation thresholds to ignore spikes, use matchers and throttling so action policies only fire for the right episodes at a sustainable rate, and use {{maint-windows-cap}} or snooze during known change windows.

Example: Noisy CPU rule

| Situation | Action | Mechanism |
|---|---|---|
| The {{esql}} query flags any host over 70% | Tighten the query or add a stricter `WHERE` | Author and tune the rule |
| Legitimate bursts open alerts for 1-minute spikes | Require 3 consecutive breaches before active | Activation thresholds |
| The same host pages every run for an hour | Add throttle and grouping on the action policy | Throttle, grouping |
| Only production hosts should page on-call | Add KQL on the policy matcher (for example on host or `rule.labels`) | Matchers |
| Database change window this evening | Open a {{maint-windows-cap}} or snooze the series | {{maint-windows-cap}}, snooze |

::::{note}
Order of application matters. Thresholds and no-data behavior affect lifecycle state before action policies run. Matchers and throttling apply when action policies are evaluated for each episode. Snooze and {{maint-windows-cap}} affect whether notifications send, not whether `.rule-events` documents are written. Check Discover if raw history is needed.
::::
