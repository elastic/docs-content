---
navigation_title: Notification grouping
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Batch related Kibana alerting v2 alerts into fewer notifications using notification policy grouping by host, service, or custom fields."
---

# Kibana alerting v2 notification grouping [reduce-noise-grouping-v2]

Notification policy grouping batches related alerts into a single notification, reducing the number of messages sent without losing context.

## How grouping works

When a notification policy has `group_by` fields configured, the dispatcher groups matched episodes by those field values before dispatching. Instead of sending one notification per alert, it sends one notification per group containing all the alerts in that group.

For example, if you group by `host.name` and three rules are alerting for `host-a`, you receive one notification containing all three alerts instead of three separate notifications.

## Configuration

Grouping is configured on notification policies:

```yaml
group_by: [host.name]
```

For multi-field grouping:

```yaml
group_by: [host.name, severity]
```

## Grouping rules

- **Per-rule scope**: episodes from different rules are never grouped together, even if they share the same grouping field values.
- **Empty `group_by`**: if no grouping fields are set, each episode produces its own notification.
- **Missing fields**: if a grouping field is missing from an episode, it falls into a `null` bucket.

## Grouping vs. rule grouping

There are two types of grouping in Kibana alerting v2:

| Type | Where configured | What it does |
|---|---|---|
| **Rule grouping** | On the rule (`grouping.fields`) | Splits alert events into separate series per entity |
| **Notification policy grouping** | On the policy (`group_by`) | Batches alerts into fewer notifications |

Rule grouping determines *how many alert series exist*. Policy grouping determines *how many notifications are sent*. They work at different stages and can use different fields.

## When to use

- **Infrastructure monitoring**: group by `host.name` to get one notification per host with all its alerts.
- **Service monitoring**: group by `service.name` to batch all alerts for a service.
- **Severity-based routing**: group by `severity` to batch alerts of the same priority level.
