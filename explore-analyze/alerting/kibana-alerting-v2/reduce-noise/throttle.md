---
navigation_title: Throttling
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Limit Kibana alerting v2 notification frequency by setting a minimum interval between notifications for the same group."
---

# Kibana alerting v2 throttle [throttle-v2]

Throttling sets a minimum interval between notifications for the same notification group. It reduces notification volume without affecting alert detection or lifecycle tracking.

## How throttling works

1. When the dispatcher processes a notification group for the first time, it always fires — the first occurrence is never throttled.
2. The dispatcher records a `notified` action with the current timestamp.
3. On subsequent runs, the dispatcher checks whether the time elapsed since the last `notified` action is less than the throttle interval.
4. If the interval has not passed, the notification is suppressed with outcome `suppress` and reason `throttled`.
5. Once the interval expires, the next occurrence fires and the window resets.

The throttle window resets from the timestamp of the last dispatched notification, not from the first occurrence.

## Configuration

Throttling is configured on notification policies:

```yaml
throttle:
  interval: 15m
```

This means at most one notification per 15 minutes for each notification group.

## Throttle scope

Throttling is applied per `(rule_id, policy_id, group_key)`. This means:

- Different rules are throttled independently, even through the same policy.
- Different grouping key values are throttled independently (for example, `host-a` and `host-b` each have their own throttle window).
- Different policies are throttled independently, even for the same rule.

## When to use

- **Warning-level alerts** where immediate notification is not critical but periodic awareness is useful.
- **High-volume rules** that produce many alerts per evaluation cycle.
- **Summary notifications** where you want a periodic digest rather than per-alert notifications.

## Relationship to other mechanisms

- **Grouping** reduces the number of notifications by batching alerts. **Throttling** reduces the frequency of those batched notifications.
- **Snooze** suppresses all notifications for a fixed duration. **Throttling** allows periodic notifications at a controlled rate.
