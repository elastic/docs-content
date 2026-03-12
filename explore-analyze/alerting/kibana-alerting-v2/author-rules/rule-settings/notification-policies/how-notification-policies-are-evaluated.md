---
navigation_title: How notification policies are evaluated
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "How the Kibana alerting v2 dispatcher processes alert episodes through a 10-step pipeline: suppressions, matchers, grouping, throttling, and dispatch."
---

# How Kibana alerting v2 notification policies are evaluated [how-notification-policies-evaluated-v2]

The dispatcher is the asynchronous component that bridges rule execution and notification delivery. It polls for new alert episodes and processes them through a 10-step pipeline that applies suppressions, evaluates matchers, groups alerts, applies throttling, and dispatches to workflow destinations.

The dispatcher runs every 10 seconds and processes up to 10,000 episodes per run.

## The 10-step pipeline

### Step 1: Fetch alert episodes

The dispatcher queries the `.alerts-events-*` data stream for alert episodes with new events since the last run. Each episode is identified by its `episode_id` and includes the `last_event_timestamp`, `rule_id`, `group_hash`, and `episode_status`.

### Step 2: Fetch suppressions

Two queries against `.alerts-actions` determine the suppression state of each episode:

- **Per-episode suppressions**: acknowledgement (`ack`) and deactivation (`deactivate`) status.
- **Per-series suppressions**: snooze status for the episode's `group_hash`.

### Step 3: Apply suppressions

Suppressed episodes are filtered out. An episode is suppressed if:

- It has been **acknowledged** (`last_ack_action == "ack"`).
- It has been **deactivated** (`last_deactivate_action == "deactivate"`).
- Its series has been **snoozed** and the snooze expiry is after the episode's last event timestamp.

Suppressed episodes are recorded with outcome `suppress` and the corresponding reason (`ack`, `deactivate`, or `snooze`).

### Step 4: Fetch rules

Load the rule definitions for all remaining (non-suppressed) episodes by `rule_id`.

### Step 5: Fetch notification policies

Load the notification policies referenced by each rule's `notification_policies` array.

### Step 6: Evaluate matchers

Each episode is tested against the matcher of every relevant notification policy. The matcher is a KQL expression evaluated in-process (no {{es}} query). The matcher can access:

- `data.*` — the alert event payload
- `rule_id`, `group_hash`, `episode_id`
- `episode_status` (`inactive`, `pending`, `active`, `recovering`)
- `last_event_timestamp`

An empty matcher (empty string) is a catch-all that matches every episode.

### Step 7: Build notification groups

Matched episodes are grouped into notification groups by `(rule_id, policy_id, group_key)`. The `group_key` is computed from the policy's `groupBy` fields.

- If `groupBy` is empty, each episode becomes its own notification group.
- If a `groupBy` field is missing from an episode, the episode falls into a `null` bucket.
- Episodes from different rules are never grouped together.

### Step 8: Apply throttling

For each notification group, the dispatcher checks whether a `notified` action was recorded within the policy's `throttle.interval`. If so, the group is throttled — no notification is sent. The first occurrence in a group always fires.

The throttle window resets from the timestamp of the last dispatched notification for that group.

### Step 9: Dispatch to workflows

Non-throttled notification groups are dispatched to the workflow destinations configured in the notification policy. Dispatch is fire-and-forget. The dispatcher uses the API key stored on the notification policy for authentication.

### Step 10: Record outcomes

The dispatcher records an action document for each processed episode:

| Outcome | Meaning |
|---|---|
| `fire` | Episode was dispatched to a workflow |
| `suppress` | Episode was suppressed, with a reason: `ack`, `deactivate`, `snooze`, or `throttled` |
| `notified` | Recorded per notification group for throttle tracking |

## Delivery guarantees

The dispatcher provides at-least-once delivery. If the dispatcher crashes mid-run, it re-processes episodes from the last known checkpoint. Workflow destinations should be designed to handle duplicate notifications gracefully.

## Batch limits and ordering

The dispatcher processes up to 10,000 episodes per run, ordered by oldest first. If more than 10,000 episodes are pending, the oldest are processed first, and the remainder are picked up in subsequent runs.
