---
navigation_title: Reduce noise and false positives
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Reduce Kibana alerting v2 alert noise and false positives using activation thresholds, notification policy controls, rules on alerts, and manual suppression."
---

# Reduce Kibana alerting v2 noise and false positives [reduce-noise-v2]

Kibana alerting v2 provides multiple mechanisms to reduce alert noise and prevent false positives. Each mechanism operates at a different stage of the alerting pipeline, from rule evaluation to notification delivery. Use them in combination for layered noise reduction.

## Noise reduction at a glance

| Mechanism | Stage | Scope | What it does |
|---|---|---|---|
| [Activation thresholds](reduce-noise/activation-thresholds.md) | Rule evaluation | Per series | Require consecutive breaches or duration before activating |
| [Recovery thresholds](reduce-noise/recovery-thresholds.md) | Rule evaluation | Per series | Require consecutive recoveries or duration before deactivating |
| [No-data handling](reduce-noise/no-data-handling.md) | Rule evaluation | Per series | Prevent false recoveries when data stops |
| [Grouping](reduce-noise/grouping.md) | Notification policy | Per notification | Batch related alerts into fewer notifications |
| [Throttle](reduce-noise/throttle.md) | Notification policy | Per group | Limit notification frequency |
| [Matcher](reduce-noise/matcher.md) | Notification policy | Per policy | Route only matching alerts to destinations |
| [Snooze or silence](reduce-noise/snooze-or-silence.md) | Alert action | Per series or attribute | Temporarily suppress notifications |
| [Maintenance windows](reduce-noise/maintenance-windows.md) | Notification policy | Scheduled | Pause notifications during planned work |
| [Rules on alerts](reduce-noise/rules-on-alerts.md) | Rule evaluation | Cross-rule | Replace many alerts with one meaningful one |
| [Deactivate alerts](reduce-noise/deactivate-alerts.md) | Alert action | Per episode | Stop processing for resolved-but-not-recovered episodes |

## Choosing the right approach

**Preventing alerts from activating too quickly**
:   Use [activation thresholds](reduce-noise/activation-thresholds.md) to filter transient spikes.

**Preventing alerts from toggling between active and recovered**
:   Use [recovery thresholds](reduce-noise/recovery-thresholds.md) to require sustained recovery.

**Reducing the number of notifications without reducing detection**
:   Use [grouping](reduce-noise/grouping.md) to batch alerts, [throttle](reduce-noise/throttle.md) to limit frequency, or [matchers](reduce-noise/matcher.md) to route only the most important alerts.

**Suppressing notifications during known events**
:   Use [maintenance windows](reduce-noise/maintenance-windows.md) for scheduled deployments, or [snooze](reduce-noise/snooze-or-silence.md) for ad hoc suppression.

**Replacing many low-level alerts with fewer high-level ones**
:   Use [rules on alerts](reduce-noise/rules-on-alerts.md) to create correlation and escalation patterns.

**Stopping notifications for alerts you've already seen**
:   Use [acknowledge](reduce-noise/snooze-or-silence.md) to suppress per episode, or [deactivate](reduce-noise/deactivate-alerts.md) to fully stop processing.

## Progressive noise reduction

A recommended approach for new deployments:

1. **Start with detect mode** — run rules in detect mode to produce signals without noise. Review signal volume in Discover.
2. **Enable alert mode selectively** — switch rules to alert mode one at a time. Tune activation thresholds to filter transient conditions.
3. **Add notification policies** — create policies with matchers and throttling to control which alerts generate notifications and how often.
4. **Create rules on alerts** — for services with many rules, create higher-order rules that correlate across alerts and notify only on significant patterns.
