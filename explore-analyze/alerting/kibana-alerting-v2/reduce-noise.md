---
navigation_title: Reduce noise and false positives
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Select the right Kibana alerting v2 feature to reduce noise: thresholds, no-data handling, notification policies, throttling, snooze, rules on alerts, and more."
---

# Reduce {{kib}} alerting v2 noise and false positives [reduce-noise-v2]

{{kib}} alerting v2 offers many ways to reduce noise, each applied at a different stage—from the {{esql}} query and lifecycle thresholds through notification policies, throttling, and manual controls. Selecting the wrong lever wastes effort and can hide real problems. This page helps you **match a situation to a mechanism** and explains **how mechanisms fit in the pipeline** so you can combine them deliberately.

If multiple rows in the table apply, see [Using them together](#using-them-together).

## Select the right approach

| Your situation | Use this | What it does |
|---|---|---|
| The {{esql}} query matches too much normal traffic (too many breaching rows) | [Author and tune the rule](author-rules.md) | Narrows the query, `WHERE` clause, schedule, or lookback so evaluations only surface what matters |
| Short spikes or flapping metrics open alerts before they should | [Activation thresholds](reduce-noise/activation-thresholds.md) | Requires consecutive breaches or a minimum duration before an episode becomes **active** |
| The alert recovers and reopens too often (flapping) | [Recovery thresholds](reduce-noise/recovery-thresholds.md) | Requires sustained clear conditions before an episode leaves **recovering** |
| The query returns no rows and **no_data** or recovery behavior is misleading | [No-data handling](reduce-noise/no-data-handling.md) | Configures how empty results are interpreted so gaps do not look like false recoveries or false alerts |
| Notifications repeat for the same group on every evaluation | [Throttling](reduce-noise/throttle.md) | Enforces a minimum interval between notifications **per notification group** |
| Recipients get too many separate messages for related episodes | [Notification grouping](reduce-noise/grouping.md) | Batches related alerts into fewer notifications |
| Notifications should only go out for certain episodes (severity, labels, payload fields) | [Matchers](reduce-noise/matcher.md) | Applies notification policy **rule_labels** scoping and **KQL** episode matching so only matching episodes route to workflows |
| Planned maintenance: evaluations should continue but on-call should not be paged | [Maintenance windows](reduce-noise/maintenance-windows.md) | Pauses notifications for a scheduled window |
| A temporary quiet period is needed for a series or episode without changing the rule | [Snooze or silence](reduce-noise/snooze-or-silence.md) | Snoozes or silences notifications; **acknowledge** can also quiet an episode while work proceeds |
| Many low-level alerts should roll up into one higher-level signal | [Rules on alerts](reduce-noise/rules-on-alerts.md) | Runs follow-on rules on **`.rule-events`** (or related data) to correlate and notify once |
| One **alert episode** should stop notifying and leave the triage queue while the rule keeps running | [Deactivate alerts](reduce-noise/deactivate-alerts.md) | **Deactivates** that episode; the rule still evaluates and can detect new episodes for other **series** |

## How each mechanism works

Mechanisms are listed in **rough pipeline order**: from what happens during rule evaluation and lifecycle, through notification policy processing, to operator controls.

### Author and tune the rule

Acts on: **the {{esql}} query and rule schedule, before interpretation as breach or no_data**

**Problem:** The detector fires on the wrong things.

Refine the base query, alert `WHERE` clause, schedule, and lookback. This is the only option that improves the underlying signal. Other tools filter or route what the rule already emits. See [Author rules](author-rules.md).

### Activation and recovery thresholds

Acts on: **episode lifecycle transitions** (pending → active, recovering → inactive)

**Problem:** Conditions flicker, or recovery should hold steady before closing.

[Activation thresholds](reduce-noise/activation-thresholds.md) delay promotion to **active**. [Recovery thresholds](reduce-noise/recovery-thresholds.md) delay return to **inactive**. Both reduce flip-flopping without hiding rows in the source data.

### No-data handling

Acts on: **evaluations that return zero rows**

**Problem:** Data stopped arriving, or empty results should not imply recovery or a **no_data** storm.

Configure how the rule treats empty results. See [No-data handling](reduce-noise/no-data-handling.md) and [No-data handling (rule settings)](author-rules/rule-settings/no-data-handling.md).

### Notification matchers and grouping

Acts on: **which episodes a notification policy considers and how they are batched**

**Problem:** Only some episodes should page the team, or messages should batch by service or host.

[Matchers](reduce-noise/matcher.md) scope policies (labels + KQL). [Grouping](reduce-noise/grouping.md) combines related episodes into fewer notifications.

### Throttling

Acts on: **notification send rate for a group**

**Problem:** The same notification repeats on every run.

[Throttling](reduce-noise/throttle.md) limits how often a policy may notify for the same group. Detection and episode state are unchanged; only dispatch spacing changes.

### Maintenance windows

Acts on: **notification dispatch during a window**

**Problem:** Maintenance is scheduled; events should still be recorded without paging.

[Maintenance windows](reduce-noise/maintenance-windows.md) pause notifications for planned work. Evaluations continue unless the rule is no longer enabled in the {{rules-ui}}.

### Snooze, silence, and acknowledgment

Acts on: **notifications for a scope (series, attributes, episode)**

**Problem:** Quiet a series for a time, or mark ownership of an episode.

[Snooze or silence](reduce-noise/snooze-or-silence.md) covers temporary suppression and acknowledgment-driven quieting.

### Rules on alerts

Acts on: **downstream correlation and routing**

**Problem:** One summary notification is enough when the pattern is severe, not one per underlying row.

[Rules on alerts](reduce-noise/rules-on-alerts.md) uses alert event data as input to another rule so operations can escalate or summarize.

### Deactivate alerts

Acts on: **a single alert episode** (lifecycle processing and notifications)

**Problem:** One **alert episode** should drop out of triage while other **series** keep running.

[Deactivate alerts](reduce-noise/deactivate-alerts.md) **deactivates** that episode: lifecycle processing and notifications stop for it, while the rule continues to evaluate and can open new episodes for other **group_hash** values.

## Key distinctions

|  | Tune rule / schedule | Activation / recovery thresholds | No-data handling | Matchers / grouping / throttle | {{maint-windows-cap}} / snooze / silence | Rules on alerts | **Deactivate alerts** |
|---|---|---|---|---|---|---|---|
| **Rule still evaluates** | Yes | Yes | Yes | Yes | Yes | Yes (source rules) | Yes |
| **Changes breach detection logic** | Yes | No (delays state) | Yes (empty-result policy) | No | No | N/A | No |
| **Reduces notifications** | If fewer breaches | Indirectly | Indirectly | Yes | Yes | Yes | Yes |
| **Typical time scope** | Until next edit | Consecutive runs / duration | Per evaluation | Policy config | Window or until cleared | N/A | Until episode handled |

## Using them together [using-them-together]

These options stack. A common pattern is: **tune the query** for precision, add **activation** thresholds to ignore spikes, use **matchers and throttling** so notification policies only fire for the right episodes at a sustainable rate, and use **{{maint-windows-cap}}** or **snooze** during known change windows.

**Example: Noisy CPU rule**

| Situation | Action | Mechanism |
|---|---|---|
| The {{esql}} query flags any host over 70% | Tighten the query or add a stricter `WHERE` | Author and tune the rule |
| Legitimate bursts open alerts for 1-minute spikes | Require 3 consecutive breaches before **active** | Activation thresholds |
| The same host pages every run for an hour | Add **throttle** and **grouping** on the notification policy | Throttle, grouping |
| Only production hosts should page on-call | Add **rule_labels** and **KQL** on the policy | Matchers |
| Database change window this evening | Open a {{maint-windows-cap}} or **snooze** the series | {{maint-windows-cap}}, snooze |

::::{note}
**Order of application matters.** Thresholds and no-data behavior affect **lifecycle state** before notification policies run. Matchers and throttling apply when the **dispatcher** processes episodes. Snooze and {{maint-windows-cap}} affect **whether notifications send**, not whether `.rule-events` documents are written—check Discover if raw history is needed.
::::
