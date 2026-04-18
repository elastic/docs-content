---
navigation_title: Send notifications
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Route {{alerting-v2}} alert episodes to workflows using action policies: matchers, Dispatch per, Frequency, and dispatcher behavior."
---

# Send {{alerting-v2}} notifications [send-notifications-v2]

$$$send-notifications-v2$$$

Action policies are **global** in each space: they define matchers, grouping, throttling, and **workflow** destinations for episodes. For how policies relate to rules and the dispatcher, see [Action policies](#action-policies-v2) and [Core {{alerting-v2}} concepts](core-v2-alerting-concepts.md#detection-and-notification-v2). [Workflows](../../workflows.md) are documented separately. For rule evaluation settings (schedule, thresholds, no-data, grouping, {{maint-windows-cap}}), see [Rule settings](author-rules/rule-settings.md).

## Action policies [action-policies-v2]

$$$action-policies-v2$$$

An action policy defines how and when alerts reach people and systems. In Kibana alerting v2, action policies are **global** saved objects within a space: they are not attached to individual rules. Which rules and episodes a policy applies to is determined by an optional **KQL matcher** over episode and rule fields (for example `rule.labels` and `rule.name`), not by references from the rule.

### Compare Kibana alerting v1 and v2 action policies

| | Kibana alerting v1 | Kibana alerting v2 |
|---|---|---|
| **Scope** | Per-rule connectors and actions on the rule | **Global** action policies per space. Rules do not reference specific policies |
| **Matching** | Rule execution drives connector runs | Optional **KQL matcher** on the policy over episode and rule context |
| **Matcher context** | N/A (rule-centric) | Typed fields including `episode_status`, `rule.name`, `rule.labels`, and `data.*` |

### How action policies apply to rules

Action policies are **global** within the space. Rules do not store or reference a list of action policies.

- **Scoping** is expressed with the policy's **KQL matcher**. To limit a policy to certain rules, include conditions on rule metadata in KQL (for example `rule.labels` or `rule.name`). If you omit the matcher or leave it empty, any episode in the space can match, subject to suppression, grouping, throttling, and other checks.
- **One rule, many policies:** Not every episode needs the same response. You can define several policies with different matchers so that, for example, critical episodes go to one workflow and warnings to another. See [Matchers](#matcher-v2).
- **Independent evaluation:** Policies are separate objects. Multiple policies can match the same episode; each runs on its own with **no precedence** and **no merge** between policies. If nothing matches, the episode gets **no** notification from action policies by default (with an **`unmatched`** outcome for auditing). For the full dispatcher sequence, refer to [How action policies are evaluated](#how-action-policies-evaluated-v2).
- Policies that are **not enabled** or are **snoozed** are not evaluated for new dispatch.

### Matchers [matcher-v2]

$$$matcher-v2$$$

**Action policy matchers** are optional KQL expressions that determine which **alert episodes** a policy applies to. **Episodes** that satisfy the matcher (or all episodes in the space when the matcher is empty) are candidates to be routed to the policy's workflow destinations, subject to suppression, grouping, throttling, and whether the policy is enabled or snoozed.

#### Why matchers matter

Not every alert needs the same response. The matcher lets **one rule** drive **multiple policies**: for example one policy for critical episodes routed to PagerDuty and another for warnings routed to Slack. Policies are global in the space; matchers are how you segment traffic.

An **empty matcher** (`""`) is a **catch-all** that matches every episode in the space (still subject to grouping, throttling, suppression, and policy enablement). The expression is **validated when you save** the policy so syntax errors are caught before the dispatcher evaluates it.

#### Fields you can use in KQL

The matcher editor in {{kib}} suggests valid field names for your build. Typical fields include:

| Field | Example use |
|---|---|
| `episode_status` | `"active"`, `"inactive"`, `"pending"`, `"recovering"` |
| `data.*` | Payload from the rule, for example `data.severity`, `data.env`, `data.host.name` |
| `rule_id` or `rule.id` | Rule identifier, for example `"rule-001"` |
| `rule.name`, `rule.labels` | Rule metadata for scoping (see [Action policies](#action-policies-v2)) |

Use the suggestions in the matcher UI to confirm exact spellings (`rule_id` versus `rule.id`, and how `episode` fields appear in KQL).

### Notification grouping on action policies [reduce-noise-grouping-v2]

$$$reduce-noise-grouping-v2$$$

**Notification grouping** on an action policy batches related **alert episodes** into fewer messages, reducing notification count without dropping evaluation results.

#### Grouping modes (API)

When you configure an action policy, select how matched episodes are **batched** into a single notification. Saved policies and APIs use these values:

| Mode | When to use |
|---|---|
| `per_episode` (default) | Each episode is notified independently. |
| `all` | Batch **all** matching episodes into **one** notification for that policy evaluation. |
| `per_field` | Group by values of a `data.*` field (for example `data.host.name`) so episodes sharing a key collapse into one notification per key. |

#### Dispatch per (in the UI)

In the policy editor, **Dispatch per** controls how many notifications you receive when **multiple** alert episodes match the policy at once.

**Example:** Your rule tracks services separately. Each service that crosses a threshold becomes its own episode. If three services are in a bad state at the same time, do you want **three** notifications, **one per group** you define, or **a single** bundled message?

| UI option | Maps to | What it means |
|---|---|---|
| **Episode** | `per_episode` | **One notification per episode.** For example `checkout-service` gets its own message and `api-gateway` gets its own. |
| **Group** | `per_field` | **Bundle** episodes that share a value into one notification. When you select this, specify **Group by** (a `data.*` field such as `data.service.name` or `data.host.name`). |
| **Digest** | `all` | **One notification** that includes everything that matched, regardless of how many episodes or services are involved. |

For a rule that only ever produces **one** episode at a time (for example a single monitored service), **Episode** is usually enough.

For **Frequency** options that pair with each **Dispatch per** value, refer to [Throttling on action policies](#throttle-v2).

#### Why notification grouping matters

Without notification grouping, a rule that produces many series-level episodes (for example **50** hosts) can generate **50** separate notifications. Grouping by a field such as `data.host.name` collapses those into **one notification per host** (for the modes that support field grouping).

**Episodes from different rules are never merged**, even when they share the same policy and group key. A batched notification always belongs to **exactly one rule**.

### Throttling on action policies [throttle-v2]

$$$throttle-v2$$$

**Throttling** controls how often a policy may send notifications for a **notification group**. It reduces notification volume without changing rule execution or **alert episode** lifecycle state in `.rule-events`.

#### Throttle strategies (API)

Select a strategy to control **notification frequency**. Saved policies and APIs use these values:

| Strategy | Behavior |
|---|---|
| `on_status_change` | Notify when **episode status changes** (for example active → inactive). |
| `per_status_interval` | At most **once per interval** for each **episode status** value. |
| `time_interval` | At most **once per interval**, regardless of status changes. |
| `every_time` | Eligible to fire on **every dispatcher evaluation** for matching episodes (subject to other policy limits). |

#### Frequency (in the UI)

**Frequency** in the policy editor controls how often you are **reminded** about the **same ongoing** issue. The choices available depend on **Dispatch per** (see [Notification grouping on action policies](#reduce-noise-grouping-v2)).

##### When **Episode** is selected (`per_episode`)

| UI option | Typical API mapping | What it means |
|---|---|---|
| **On status change** | `on_status_change` | Notify when the episode becomes active and again when it **recovers** (or otherwise changes status). **No** repeat reminders while the problem stays in the same state. |
| **On status change + repeat at interval** | `per_status_interval` (with **`interval`**) | Same as **On status change**, plus a **reminder** at most every **X minutes** while the episode stays active (or per status, depending on your {{kib}} version). |
| **Every evaluation (no throttle)** | `every_time` | A notification can fire on **every** evaluation cycle. This can produce a very high volume of messages. Use only when you intentionally want that behavior. |

Evaluation runs on a short **dispatcher** interval (on the order of **seconds**), and rules may also run on their own schedule. **Every evaluation** can still mean **very frequent** notifications.

##### When **Group** is selected (`per_field`)

| UI option | Typical API mapping | What it means |
|---|---|---|
| **At most once every…** | `time_interval` (with **`interval`**) | No matter how many episodes sit in the group, you get **at most one** notification per **interval** for that group. |
| **Every evaluation (no throttle)** | `every_time` | Fires on every evaluation, with **no** cap. Same caution as for **Episode**: volume can explode. |

##### When **Digest** is selected (`all`)

| UI option | Typical API mapping | What it means |
|---|---|---|
| **Every evaluation (no throttle)** | `every_time` | **One** bundled notification that includes all matching episodes, **every** evaluation cycle. |

::::{note}
**Digest** often exposes **only** the **every evaluation** style frequency today. Pairing that with a rule or dispatcher that runs **very often** still yields **frequent** bundled messages. **Digest** is a better fit for rules on **longer** schedules (for example every **30 minutes**) where you want a **periodic summary** of everything currently active.
::::

#### Interval

Set an **`interval`** duration (for example `1h`, `30m`). The UI may pre-fill a default such as **`5m`**.

##### Why throttling exists

Without throttling, a condition that stays true could generate a notification as often as the **dispatcher** runs evaluations. Throttling keeps paging and chat noise at a manageable rate. The interval **resets from the last time the policy fired** for that group, so successive notifications stay at least **`interval`** apart. Timing details depend on your {{kib}} version.

## Create and manage action policies [create-manage-action-policies-v2]

$$$create-manage-action-policies-v2$$$

Create action policies to control which alerts trigger notifications, how alerts are grouped, how frequently notifications are sent, and where they are routed. Policies are **global** within a space: you create and edit them from the **Action Policies** area, not from the rule form. Rules do not “link” to policies. Which rules and episodes a policy can apply to is defined with an optional **KQL matcher** over episode and rule fields (for example `rule.name` and `rule.labels`). See [Action policies](#action-policies-v2) above.

### Create an action policy

1. Open **{{manage-app}}** > **V2 Alerting Preview** > **Action Policies**. Some deployments also list **Action Policies** under **Alerts and Insights**; use whichever entry your layout provides.
2. Click **Create policy**.
3. **Matcher** — Optional KQL over episode and rule fields. An empty matcher matches every episode in the space. Refer to [Matchers](#matcher-v2).
4. **Grouping** — In the UI, **Dispatch per** (**Episode**, **Group**, or **Digest**) controls how many notifications you get when multiple episodes match. Refer to [Notification grouping on action policies](#reduce-noise-grouping-v2).
5. **Throttling** — In the UI, **Frequency** pairs with **Dispatch per** (for example **On status change** or **At most once every…**). Refer to [Throttling on action policies](#throttle-v2).
6. **Destinations** — One or more targets; only **workflow** type is supported in the current UI. See [Destinations](#destinations).
7. **Snooze** (optional) — Time window when the policy does not dispatch.
8. Click **Save**. The matcher is validated when you save so invalid KQL is rejected before dispatch runs.

### Policy list columns

The list supports **search, filters, and sorting** so you can narrow policies by name, state, and other criteria. Typical columns include:

| Column | Description |
|---|---|
| **Name** | Policy display name |
| **Status** | Whether the policy is **enabled**, **disabled**, or **snoozed** |
| **Matcher** | Optional KQL condition; when empty, episodes in the space can match unless other limits apply |
| **Last updated** | Last save time |

There is **no “linked rule count”** in the global model. Policies are not attached to a fixed set of rules. Use the **matcher** and rule fields such as `rule.labels` in KQL to understand which rules and episodes a policy can cover. For the evaluation flow, refer to [How action policies are evaluated](#how-action-policies-evaluated-v2).

### Destinations

Destinations route matching episodes to workflows. Specify **one or more** destinations. In the current UI, only **`workflow`** destinations are supported.

In the policy editor, use the **workflow search** field instead of a static list: it queries available workflows through the **`/api/workflows/search`** endpoint. Type to search and select each workflow to attach.

The underlying saved shape is an array of destination objects. For example, a policy with two workflow destinations might look like this:

```json
[
  {
    "type": "workflow",
    "id": "workflow-id-one"
  },
  {
    "type": "workflow",
    "id": "workflow-id-two"
  }
]
```

Exact property names (`id` versus other identifiers) follow the API and UI version you use; rely on the editor for valid values.

### Enable, snooze, and maintenance

You can **disable** a policy so it is not evaluated for new episodes. You can **snooze** a policy for a defined window so that it does not dispatch notifications during that period. Policies that are **not enabled** or are **snoozed** are skipped when the dispatcher evaluates policies.

### Update API keys

You can **rotate the API key** used to run a policy’s workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies. Rotating or changing a policy still triggers the same API key invalidation behavior described under **Production considerations** below.

::::{important} Production considerations
When you **update** or **delete** an action policy, previous API keys used for execution are **marked for invalidation** and removed on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch. Administrators can tune how often invalidation runs and how long to wait before cleanup using `xpack.alerting_v2.invalidateApiKeysTask` in `kibana.yml`. For defaults and guidance, refer to [Set up](get-starting.md#kibana-advanced-settings-v2).
::::

### Bulk actions

On the action policies list, select one or more policies to **enable**, **disable**, **snooze**, **delete**, or **update API keys** in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.

## How action policies are evaluated [how-action-policies-evaluated-v2]

$$$how-action-policies-evaluated-v2$$$

Action policies are separate from rules. After a rule runs and produces or updates alert episodes, the system decides which policies apply, whether notifications should go out, and which workflows receive them. You configure policies once. They can apply to many rules.

Evaluation runs in the **same {{kib}} space** as the rule and episode: policies and workflow destinations are resolved in that space, not across spaces.

### Policies are standalone

**Action policies** (notification policies) are **standalone saved objects** in the space. They are not embedded in the rule document. In the current **global** model, rules do **not** store a list of policy IDs; the dispatcher considers **eligible policies in the space** and uses **KQL matchers** to decide which episodes each policy applies to.

**Multiple policies can match the same episode**, and each match is handled **independently**. There is **no precedence** between policies and **no cross-policy de-duplication**: if two policies both match, both can run their own grouping, throttling, and destinations (subject to each policy’s settings).

If **no** policy matches an episode, **no notification** is sent under action policies. That behavior is **intentional**: unmatched episodes do not notify by default. The system still records an **`unmatched`** outcome in alert actions so you can audit what happened, as described in [Possible outcomes](#possible-outcomes).

### Runtime: how the dispatcher processes an episode

When an episode is produced or updated, the **dispatcher** runs on a timer (about **10 seconds** between cycles in typical configurations) and walks a pipeline similar to the following:

1. **Suppression** — Determines whether the episode is blocked from generating notifications (for example **acknowledged**, **snoozed**, or **deactivated**), according to suppression rules and episode state.
2. **Policy candidates** — **Loads** action policies in the space that are **enabled** and not **snoozed**. Other policies are skipped.
3. **Matcher** — For each candidate policy, evaluates the optional **KQL matcher** against the shared **matcher context** (episode + rule + payload fields such as `data.*`).
4. **Grouping** — For each policy that matches, applies **grouping** so episodes batch into notification groups the way that policy defines.
5. **Throttle** — For each group, checks **throttle** state and skips dispatch if a notification went out too recently for that policy’s rules.
6. **Destinations** — Sends to the policy’s **workflow** destinations when the throttle allows it.

Together, this shows why each policy control matters: **matcher** filters which episodes use that policy, **grouping** shapes how many messages you get, **throttle** how often, and **destinations** where they go.

In the policy UI, **grouping** appears as **Dispatch per** (**Episode**, **Group**, **Digest**), and **throttle** appears as **Frequency**; see [Notification grouping on action policies](#reduce-noise-grouping-v2) and [Throttling on action policies](#throttle-v2).

### How policies are matched to episodes

The dispatcher considers policies that are **enabled** and not **snoozed**. Policies that are **not enabled** or are **snoozed** are skipped.

For each candidate policy, an optional **KQL matcher** is evaluated against a shared **matcher context** that includes the episode and the rule (for example `episode_status`, `rule.name`, `rule.labels`, and fields from the alert payload, often under `data.*`). If you omit the matcher or leave it empty, every episode in the space can match that policy, subject to suppression, grouping, throttling, and other checks. Use the matcher editor suggestions to see which fields are available in your build.

An episode can match zero, one, or many policies. If it matches none, notifications are not sent for that episode under those policies. An `unmatched` outcome is recorded for auditing, as defined in the [Possible outcomes](#possible-outcomes) section.

### What happens after a policy matches

For each policy whose matcher passes, the runtime applies **grouping**, then **throttling**, then **workflow** dispatch, as summarized in [Runtime: how the dispatcher processes an episode](#runtime-how-the-dispatcher-processes-an-episode). Additional **suppression** may still apply depending on configuration and episode state.

Order matters: Lifecycle thresholds and no-data behavior on the rule run before action policies. Policies only affect routing and delivery, not whether rows are written to `.rule-events`.

### Possible outcomes

| Outcome | What it means for you |
|---|---|
| dispatched | Notifications were sent according to the policy |
| throttled | Delivery was suppressed because throttling rules said to wait |
| suppressed | The episode was suppressed before a notification went out, for example by an active suppression |
| unmatched | No action policy matched this episode, so no workflow ran for it under these policies |
| error | Processing failed. Check {{kib}} logs and any health indicators your team uses |

Notifications can arrive shortly after an episode becomes eligible. Heavy load or many policies can add noticeable delay. If something seems stuck, verify matchers, throttling, {{maint-windows-cap}}, that the policy is **enabled** and is not **snoozed**, and that the episode matches at least one policy.

## Workflows [workflows-v2]

$$$workflows-v2$$$

In {{alerting-v2}}, **action policies** invoke [Workflows](../../workflows.md) as notification destinations. You can also link workflows directly from rules for rule-triggered automation.

For authoring workflows, permissions, and step types, use the main [Workflows](../../workflows.md) documentation. Use this page for alerting-specific policy and destination behavior.