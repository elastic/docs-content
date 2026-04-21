---
navigation_title: Action policy reference
applies_to:
  serverless: preview
products:
  - id: kibana
description: "API values, Dispatch per and Frequency UI mappings, dispatch outcomes, and workflow destination shape for {{alerting-v2}} action policies."
---

# Action policy reference [action-policy-reference-v2]

$$$action-policy-reference-v2$$$

Condensed tables for matchers, grouping, throttling, and dispatch outcomes. For step-by-step policy creation and narrative guidance, refer to [Create and configure an action policy](create-configure-action-policy-v2.md).

## Matcher fields (typical KQL) [matcher-fields-typical-kql]

| Field | Example use |
|---|---|
| episode_status | `"active"`, `"inactive"`, `"pending"`, `"recovering"` |
| data.* | Payload from the rule, for example `data.severity`, `data.env`, `data.host.name` |
| rule_id or rule.id | Rule identifier, for example `"rule-001"` |
| rule.name, rule.labels | Rule metadata for scoping |

## Notification grouping (API) [notification-grouping-api]

| Mode | When to use |
|---|---|
| per_episode (default) | Each episode is notified independently. |
| all | Batch **all** matching episodes into **one** notification for that policy evaluation. |
| per_field | Group by values of a `data.*` field so episodes sharing a key collapse into one notification per key. |

## Dispatch per (UI) mapping

| UI option | Maps to |
|---|---|
| **Episode** | per_episode |
| **Group** | per_field |
| **Digest** | all |

## Throttle strategies (API) [throttle-strategies-api]

| Strategy | Behavior |
|---|---|
| on_status_change | Notify when **episode status changes** (for example active → inactive). |
| per_status_interval | At most **once per interval** for each **episode status** value. |
| time_interval | At most **once per interval**, regardless of status changes. |
| every_time | Eligible to fire on **every dispatcher evaluation** for matching episodes (subject to other policy limits). |

## Frequency (UI) when Episode (per_episode) [frequency-ui-when-episode-per_episode]

| UI option | Typical API mapping |
|---|---|
| **On status change** | on_status_change |
| **On status change + repeat at interval** | per_status_interval (with **`interval`**) |
| **Every evaluation (no throttle)** | every_time |

## Frequency (UI) when Group (per_field)

| UI option | Typical API mapping |
|---|---|
| **At most once every…** | time_interval (with **`interval`**) |
| **Every evaluation (no throttle)** | every_time |

## Frequency (UI) when Digest (all)

| UI option | Typical API mapping |
|---|---|
| **Every evaluation (no throttle)** | every_time |

## Dispatch outcomes

| Outcome | Meaning |
|---|---|
| dispatched | Notifications were sent according to the policy. |
| throttled | Delivery was suppressed because throttling rules said to wait. |
| suppressed | The episode was suppressed before a notification went out, for example by an active suppression. |
| unmatched | No action policy matched this episode, so no workflow ran for it under these policies. |
| error | Processing failed. Check {{kib}} logs. |

## Workflow destination object (example)

| Property | Description |
|---|---|
| type | Destination type; `workflow` in the current UI. |
| id | Workflow identifier (exact property names follow the API and UI version). |
