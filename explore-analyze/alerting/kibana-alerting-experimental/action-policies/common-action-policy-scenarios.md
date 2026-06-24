---
navigation_title: Common scenarios
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Common action policy scenarios for the experimental alerting system, including routing by severity, handling severity escalation, and controlling re-notification."
---

# Common action policy scenarios [common-action-policy-scenarios]

Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page covers common situations you're likely to encounter when setting up action policies, and explains how to configure them to get the behavior you expect.

## Route alert episodes to different workflows by severity [routing-by-severity]

When your rules produce alert episodes at different severity levels, you'll often want to route them to different workflows. For example, you might page an on-call team for critical episodes while sending lower-severity episodes to a Slack channel for async review.

To do this, create separate policies scoped to specific severity values using match conditions:

| Field | Policy A | Policy B |
|---|---|---|
| **Policy type** | Global | Global |
| **Match conditions** | `severity: "critical"` | `severity: "low" OR severity: "medium" OR severity: "high"` |
| **Notify per** | Episode | Episode |
| **Frequency** | On status change | On status change |
| **Destinations** | PagerDuty workflow | Slack workflow |

Each policy evaluates alert episodes independently:

- An episode with `severity: "critical"` matches Policy A but not Policy B.
- An episode with `severity: "high"` matches Policy B but not Policy A.
- If an episode's severity changes mid-lifecycle, the policies that match it change accordingly. For example, if an episode escalates from `high` to `critical`, Policy A starts matching and Policy B stops matching. Policy A fires because it has no prior notification record for that episode.

## Manage notifications across severity changes [severity-escalation]

To manage notifications effectively when episode severity changes, you need to understand how policies match and re-match episodes as severity shifts. Whether a severity change fires a notification depends on whether the policy has matched the episode before and what frequency option is set.

### Notify when an episode escalates into a new severity threshold

Scope a policy to the severity level you want to be notified about. When an episode escalates into that severity level for the first time, the policy fires because it has no prior notification record for the episode.

**Example:** Policy B is scoped to `severity: "critical"`. An episode starts at `low` severity, so Policy B does not match. When the episode escalates to `critical`, Policy B now matches and fires (regardless of the frequency setting) because it has never notified for this episode before.

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

### Prevent duplicate notifications when severity changes within an existing match

If a policy already matched an episode at a lower severity and the episode escalates, the policy does not automatically re-notify. With `On status change` frequency, a severity change alone does not count as a status change.

**Example:** Policy A matches all episodes regardless of severity. It notified when the episode was `low`. The episode escalates to `critical`, but Policy A still matches and the status has not changed, only the severity has. The throttle blocks re-notification. To re-notify on escalation, use a time-based throttle or create separate policies per severity level as described in [Route alert episodes to different workflows by severity](#routing-by-severity).

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | (None, matches all episodes) |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | Slack workflow |

### Stop notifications when an episode de-escalates below a policy's threshold

If an episode drops below a policy's severity threshold, the policy stops matching and sends no further notifications. If the episode later escalates back above the threshold, the policy fires again as if it were the first match.

**Example:** Policy B is scoped to `severity: "critical"`. An episode de-escalates from `critical` to `high`. Policy B no longer matches and stops sending notifications. If the episode later escalates back to `critical`, Policy B fires again.

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | On status change |
| **Destinations** | PagerDuty workflow |

## Re-notify for persistently active episodes [controlling-re-notification]

The `On status change` frequency option notifies once per status transition (for example, when an episode activates or resolves). This is efficient for reducing noise, but it means that a persistently active episode that only changes in severity won't re-trigger a notification.

If you want re-notification for episodes that stay active without a status change, use a time-based throttle instead:

- **`At most once every…`:** Re-notifies after the configured interval regardless of whether severity or status changed. For example, `1h` sends a follow-up notification every hour while the episode remains active and matched.
- **`On status change + repeat at interval`:** Notifies on status change and then repeats at the configured interval while the episode stays in the same status.

**Example:** You want to be re-paged if a critical episode stays open for more than an hour. Set the policy frequency to `At most once every 1h`. The policy fires when the episode first matches and then again each hour until the episode resolves or no longer matches.

| Field | Value |
|---|---|
| **Policy type** | Global |
| **Match conditions** | `severity: "critical"` |
| **Notify per** | Episode |
| **Frequency** | At most once every 1 hour |
| **Destinations** | PagerDuty workflow |

## Related pages

- [Action policy reference](action-policy-reference.md) - Find descriptions of match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md) - Understand how action policies evaluate and gate alert episodes.
- [Create and configure an action policy](create-configure-action-policy.md) - Learn how to set up policy type, match conditions, grouping, frequency, and workflow destinations.
