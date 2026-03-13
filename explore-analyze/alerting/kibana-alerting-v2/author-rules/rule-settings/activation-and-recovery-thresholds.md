---
navigation_title: Activation and recovery thresholds
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Control when Kibana alerting v2 alerts transition between lifecycle states using consecutive-breach and duration-based thresholds."
---

# Kibana alerting v2 activation and recovery thresholds [activation-recovery-thresholds-v2]

Activation and recovery thresholds control when alerts transition between lifecycle states. They prevent transient spikes from creating actionable alerts and prevent rapid toggling between active and recovered.

These settings are only available for alert-mode rules (`kind: alert`).

## Alert lifecycle states

An alert transitions through these states:

```
inactive → pending → active → recovering → inactive
```

- **Inactive** — the condition is not met.
- **Pending** — the condition is met, but activation thresholds have not been satisfied yet.
- **Active** — the condition is met and activation thresholds are satisfied. The alert is actionable.
- **Recovering** — the condition is no longer met, but recovery thresholds have not been satisfied yet.

## Activation thresholds

Activation thresholds prevent the `pending` → `active` transition until the condition has persisted. This filters out transient spikes.

Configure activation using count, timeframe, or both:

| Field | Description | Example |
|---|---|---|
| `pending_count` | Consecutive breaches required | `3` — condition must be met 3 times in a row |
| `pending_timeframe` | Minimum duration the condition must persist | `5m` — condition must hold for 5 minutes |
| `pending_operator` | How to combine count and timeframe | `AND` (both required) or `OR` (either sufficient) |

### Examples

**Count only**: Alert activates after 3 consecutive breaches.

```yaml
state_transition:
  pending_count: 3
```

**Timeframe only**: Alert activates after the condition persists for 5 minutes.

```yaml
state_transition:
  pending_timeframe: 5m
```

**Count AND timeframe**: Alert activates after 3 consecutive breaches within a 5-minute window.

```yaml
state_transition:
  pending_operator: AND
  pending_count: 3
  pending_timeframe: 5m
```

**Count OR timeframe**: Alert activates after either 3 consecutive breaches or 5 minutes of persistence, whichever happens first.

```yaml
state_transition:
  pending_operator: OR
  pending_count: 3
  pending_timeframe: 5m
```

### Skipping pending

If no activation threshold is set (the default), the alert transitions directly from `inactive` to `active` on the first breach. The `pending` state is skipped entirely.

## Recovery thresholds

Recovery thresholds prevent the `recovering` → `inactive` transition until the condition has been absent long enough. This prevents alerts from flapping between active and recovered.

| Field | Description | Example |
|---|---|---|
| `recovering_count` | Consecutive recoveries required | `2` — condition must be absent 2 times in a row |
| `recovering_timeframe` | Minimum duration for recovery | `10m` — condition must be absent for 10 minutes |
| `recovering_operator` | How to combine count and timeframe | `AND` or `OR` |

### Example

```yaml
state_transition:
  recovering_operator: AND
  recovering_count: 2
  recovering_timeframe: 10m
```

This means the alert stays in `recovering` until the condition is absent for at least 2 consecutive evaluations **and** at least 10 minutes have passed.

## Choosing thresholds

- **High-frequency metrics** (1-minute intervals): use count-based thresholds (for example, `pending_count: 3`) to filter out single-evaluation spikes.
- **Low-frequency checks** (15-minute or longer intervals): use timeframe-based thresholds (for example, `pending_timeframe: 30m`) since count-based thresholds would cause long delays.
- **Noisy environments**: combine count and timeframe with `AND` for stricter activation.
- **Critical conditions**: use low thresholds or skip them entirely to ensure fast detection.
