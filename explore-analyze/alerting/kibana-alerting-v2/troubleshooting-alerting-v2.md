---
navigation_title: Troubleshooting
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Troubleshoot {{alerting-v2}} rules, notifications, action policies, workflows, and alert lifecycle, including a validation checklist for noise controls."
---

# Troubleshooting [troubleshooting-alerting-v2]

This page collects symptom-based troubleshooting and a validation checklist for reducing noise. Use the section headings below to jump to a topic.

## Rules not generating alerts [rules-not-generating-alerts]

### Symptom

A rule runs on schedule but you see no new documents in `.rule-events`, no episodes in the alert inbox, or counts stay at zero when you expect breaches.

### Likely Causes

- The rule is **disabled** or not saved successfully.
- The {{esql}} query or **alert condition** does not match current data (wrong index pattern, time field, filters, or thresholds in the query).
- The **lookback** window is too short relative to the rule schedule, so evaluations miss data between runs.
- The rule is in **Detect** mode and you are looking only at **alert** rows in Discover.
- Index privileges or API key privileges for the rule author cannot read the source indices.
- {{alerting-v2}} is not enabled in the deployment or the {{rules-ui-v2}} UI entry is hidden by configuration.

### Diagnostic Steps

1. Open **{{manage-app}} > V2 Alerting Preview** and confirm the rule shows **Enabled**.
2. Open the rule **details** and read the **Rule conditions** section for the base query, alert condition, schedule, and lookback.
3. Run **Preview** from the rule editor (if available) or paste the {{esql}} into Discover and confirm rows return for the same time range.
4. In Discover on `.rule-events`, filter by `rule.id` for your rule and widen the time range.
5. Verify the rule mode: Detect emits `type: signal` without `episode.*`; Alert emits `type: alert` with episodes.
6. Confirm your user (or the rule’s execution API key owner) has read access to the indices in the `FROM` clause.

### Resolution

- **Enable** the rule if it was disabled.
- Tighten or broaden the {{esql}}, fix `FROM`, or adjust the **alert condition** so it reflects the signal you want. Cross-reference [Author rules](rules/author-rules-v2.md).
- Set **lookback** to at least the **schedule** interval unless you intentionally accept gaps; see [Configure a rule](rules/configure-a-rule-v2.md#schedule-lookback-v2).
- Switch to **Alert** mode when you need episodes and policy matching; see [Rules](rules-v2.md#detection-and-notification-v2).
- Restore **index privileges** or **rotate the rule API key** after privilege changes; see [Set up alerting](setup-alerting-v2.md#alerting-privileges-v2).
- Ask an administrator to confirm {{alerting-v2}} is enabled and navigation labels for your version; see [Set up and verify](setup-alerting-v2.md#alerting-set-up-v2).

### Still not working?

If documents never appear in `.rule-events` after the above checks, capture rule id, schedule, and a sample Discover query, then continue with [Unexpected alert behavior](#unexpected-alert-behavior) or open a support case with {{kib}} logs from evaluation time windows.

## Notifications not sending [notifications-not-sending]

### Symptom

Alert episodes appear active in the UI or in `.rule-events`, but no email, chat, or other channel message arrives; `.alert-actions` may show `unmatched`, `throttled`, or `suppressed` instead of `fire`.

### Likely Causes

**Action policy path**

- No global **action policy** matches the episode (overly strict **KQL matcher**, wrong `rule.name` / `rule.labels` / `data.*` fields).
- The matching policy is **disabled** or **snoozed**.
- **Throttling** or **Dispatch per** grouping prevents a new send for this evaluation cycle.
- **{{maint-windows-cap}}** or episode-level **snooze** / **suppress** blocks dispatch while evaluation continues.

**Workflow path**

- The policy has **no workflow destinations**, or destinations reference workflows that were **deleted** or renamed.
- The workflow exists but is **misconfigured** in core workflow tooling (channels, credentials, or steps), so delivery fails after handoff.
- **Workflow permissions** prevent the policy from resolving the destination in this space.

**Other**

- Heavy load or many policies delays dispatch; the dispatcher runs on an interval (on the order of tens of seconds).

### Diagnostic Steps

**If you suspect action policy misconfiguration**

1. Open **Action policies** in the same **{{kib}} space** as the rule.
2. For each policy that should apply, confirm **Status** is enabled and not snoozed.
3. Open the policy **matcher** and validate KQL against a sample episode payload (`data.*`, `rule.*`, episode status fields). An empty matcher matches all episodes subject to other controls.
4. Read [How action policies work](notifications-v2.md#how-action-policies-evaluated-v2) and map your episode to suppression, matcher, grouping, and throttle steps.
5. Query `.alert-actions` for `action.type` of `unmatched`, `throttled`, or `suppressed` for the episode id; see [Alert states and fields reference](alerts/alert-states-and-fields-reference-v2.md#alert-states-reference-v2).

**If you suspect workflow attachment or workflow health**

1. Open the policy and confirm **at least one** `workflow` destination is selected.
2. Open **[LINK: Core Workflows Documentation]** for each workflow id and verify the workflow is published, credentials are valid, and channel steps succeed in test runs.
3. Confirm your account can read the workflow objects referenced by the policy (privilege escalation guard); see [Action policy management](alerting-v2-privileges.md).
4. After policy edits, allow a short delay for **API key invalidation** cycles described in [Manage action policies](notifications/manage-action-policies-v2.md).

### Resolution

- Broaden or fix the **matcher**; align field names with the matcher editor suggestions.
- **Enable** the policy or clear **snooze** when you intend dispatch to resume.
- Adjust **Frequency** and **Dispatch per** so reminders can send when you expect; see [Create and configure an action policy](notifications/create-configure-action-policy-v2.md#throttle-v2).
- Respect **maintenance windows** and episode **snooze** semantics; adjust windows or triage state if dispatch should resume.
- Add or repair **workflow destinations** on the policy, then re-test from [Workflows for {{alerting-v2}}](workflows-alerting-v2.md).
- Fix workflow configuration using **[LINK: Core Workflows Troubleshooting]**.
- If privileges block destination resolution, grant workflow access or recreate the policy with a permitted workflow.

### Still not working?

If `.alert-actions` shows `error`, use [Possible outcomes](notifications-v2.md#possible-outcomes) for dispatcher outcome values and check {{kib}} server logs around evaluation timestamps. If outcomes are `unmatched` after matcher fixes, continue with [Action policy not triggering](#action-policy-not-triggering).

## Action policy not triggering [action-policy-not-triggering]

### Symptom

Episodes exist but policies appear to ignore them: repeated `unmatched` outcomes, or no `fire` / `throttled` rows for that episode in `.alert-actions`.

### Likely Causes

- **KQL matcher** is too narrow or uses field names that do not exist on the matcher context.
- Policy is **disabled** or **snoozed**.
- Episode or series is under **suppression** (acknowledge / snooze / deactivate flows) before policy evaluation.
- **Space mismatch**: The rule and policy are not in the same {{kib}} space.
- **Empty matcher** was intended, but a non-empty invalid expression was saved. Validation should catch this on save, but stale clients can still show errors at runtime.

### Diagnostic Steps

1. Confirm the rule and policy are listed under the **same space**.
2. Inspect the policy **matcher** text and compare to fields visible on a recent `.rule-events` document for the episode (`data.*`, `rule.*`, status fields).
3. Confirm the policy is **enabled** and not **snoozed**.
4. Review triage actions on the episode for **snooze** or **suppress** patterns; see [View, manage, and reference alerts](alerts/view-and-manage-alerts-v2.md#alert-actions-v2).
5. Query `.alert-actions` for the episode id and read `action.type` values chronologically.

### Resolution

- Edit the matcher to valid KQL that reflects your routing intent, or temporarily use an empty catch-all matcher to validate the rest of the pipeline (then tighten).
- **Enable** the policy or end **snooze**.
- Clear or adjust triage states only when consistent with your operational policy.
- Move or recreate objects so the rule and policy share one space.

### Still not working?

If matchers are empty and policies still never run, return to [Notifications not sending](#notifications-not-sending) and verify **workflow destinations**. For rule-side issues, refer to [Rules not generating alerts](#rules-not-generating-alerts).

## Workflow not executing [workflow-not-executing]

### Symptom

Action policy evaluation appears to succeed (for example `fire` or downstream logs) but no workflow-driven message arrives, or workflow runs fail in core workflow tooling.

### Likely Causes

- Workflow was **deleted** or **disabled** outside alerting while still referenced on a policy.
- **Channel configuration** inside the workflow is invalid (expired tokens, wrong recipients).
- **Runtime permissions** for the workflow or connector user block execution.
- You are looking only at alerting pages while the failure is logged in **workflow execution history** elsewhere.

### Diagnostic Steps

1. Open the action policy and note each **workflow** destination id.
2. Open **[LINK: Core Workflows Documentation]** and locate each workflow; confirm it exists in the same deployment and space expectations.
3. Run any **test** or **dry run** features your workflow product provides for the same channels used in production.
4. Check {{kib}} and workflow service logs around dispatcher timestamps for errors after policy handoff.

### Resolution

- Update the policy to reference a valid workflow, or restore the missing workflow definition.
- Fix credentials, recipients, and channel parameters in the core workflow editor.
- Align service accounts and API keys with least-privilege requirements from your administrators.

### Still not working?

Use **[LINK: Core Workflows Troubleshooting]** as the primary resolution path. Workflow configuration and retries are owned outside this alerting docset. If policies show `error` instead, refer to [Possible outcomes](notifications-v2.md#possible-outcomes) and {{kib}} logs.

## Alert not closing after resolution [alert-not-closing-after-resolution]

### Symptom

The underlying metric or log pattern looks healthy, but the episode remains **active** or oscillates between **recovering** and **active**.

### Likely Causes

- **Recovery thresholds** require more consecutive clear evaluations than have occurred yet.
- **No-data** handling treats gaps as **no_data** or **last_status** instead of recovery, so lifecycle does not move to inactive when you expect.
- **Grouping** or `group_hash` means you are viewing a different series than the one that recovered.
- **Resolve** / **deactivate** triage actions changed UI presentation while `.rule-events` history still shows transitional rows.

### Diagnostic Steps

1. Open the rule **configuration** and read **activation and recovery** settings; see [Configure a rule](rules/configure-a-rule-v2.md#activation-recovery-thresholds-v2).
2. Read **no-data** behavior for the rule; see [Configure a rule](rules/configure-a-rule-v2.md#no-data-handling-v2).
3. In Discover, query `.rule-events` for the episode’s `group_hash` and sort ascending by `@timestamp` to replay status transitions.
4. Compare **UI status** with raw `episode.status` fields for the latest rows.

[CONTENT NEEDED for M2: `group_hash` is being replaced by `series.key`. Update step 3 and the likely cause bullet about `group_hash` in this section to reference `series.key`. Also consider noting `series.tracked_by` as a way to confirm which series you are looking at when the series key alone is not recognizable.]

### Resolution

- Tighten or loosen **recovery** counts and timeframes to match how stable the signal must be before closing.
- Change **no-data** behavior if gaps should count as recovery or should hold last status explicitly.
- Align triage expectations: manual **Resolve** affects presentation and suppression; it is not a substitute for recovery thresholds unless that matches your process.

### Still not working?

If flapping is caused by noisy queries, return to [Unexpected alert behavior](#unexpected-alert-behavior) and the decision table on [Validation checklist](#reduce-noise-v2).

## Unexpected alert behavior [unexpected-alert-behavior]

### Symptom

Episodes open or close at surprising times, notifications repeat, multiple policies fire for one episode, or Discover rows disagree with the inbox.

### Likely Causes

- **Query** matches normal traffic or flapping metrics without enough **activation** dampening.
- **Multiple policies** match independently by design; there is **no precedence** between policies.
- **Dispatcher** timing differs from the rule schedule, so notification timing does not line up one-to-one with each rule run.
- **Manual triage** (snooze, resolve) interacts with lifecycle and dispatch in ways operators did not expect.

### Diagnostic Steps

1. Use the decision framing from [Validation checklist](#reduce-noise-v2) to decide whether to tune the rule, thresholds, matchers, throttles, or triage actions.
2. Re-read [How action policies work](notifications-v2.md#how-action-policies-evaluated-v2) for independent policy evaluation and `unmatched` behavior.
3. Compare **rule evaluation timestamps** in `.rule-events` with **dispatcher-driven** outcomes in `.alert-actions`.

### Resolution

Follow the **Resolution** column in the checklist table for your situation (for example tighten {{esql}}, adjust activation thresholds, add throttles, refine matchers, or use maintenance windows).

### Still not working?

Escalate with exported Discover queries for `.rule-events` and `.alert-actions`, policy ids, and workflow ids. For workflow-specific failures, use **[LINK: Core Workflows Troubleshooting]**.

## Validation checklist [reduce-noise-v2]

{{alerting-v2}} offers many ways to reduce noise. Controls live in three places:

- **[Configure a rule](rules/configure-a-rule-v2.md)**: Thresholds, no-data handling, rule-level grouping, and related evaluation settings.
- **[Manage action policies](notifications/manage-action-policies-v2.md)**: Enablement, snooze, **{{maint-windows-cap}}**, and bulk policy actions that affect dispatch.
- **[Notifications (Action Policies)](notifications-v2.md)**: Action policies: matchers, Dispatch per, Frequency, destinations, and dispatcher behavior.
- **[View, manage, and reference alerts](alerts/view-and-manage-alerts-v2.md)**: Snooze, acknowledge, deactivate, tags, and anything persisted in **`.alert-actions`**.

This section is a decision table so you can match a situation to the right mechanism. Deep content lives on the pages above.

If multiple rows in the table apply, refer to [Using them together](#using-them-together).

### Select the right approach

| Your situation | Use this | What it does |
|---|---|---|
| The {{esql}} query matches too much normal traffic with too many breaching rows | [Author rules](rules/author-rules-v2.md) | Narrows the query, `WHERE` clause, schedule, or lookback so evaluations only surface what matters |
| Short spikes or flapping metrics open alerts before they should | [Activation and recovery thresholds](rules/configure-a-rule-v2.md#activation-recovery-thresholds-v2) | Requires consecutive breaches or a minimum duration before an episode becomes active |
| The alert recovers and reopens too often, flapping | [Activation and recovery thresholds](rules/configure-a-rule-v2.md#activation-recovery-thresholds-v2) | Requires sustained clear conditions before an episode leaves recovering |
| The query returns no rows and no_data or recovery behavior is misleading | [No-data handling](rules/configure-a-rule-v2.md#no-data-handling-v2) | Configures how empty results are interpreted so gaps do not look like false recoveries or false alerts |
| Notifications repeat for the same group on every evaluation | [Throttling on action policies](notifications/create-configure-action-policy-v2.md#throttle-v2) | Enforces a minimum interval between notifications per notification group |
| Recipients get too many separate messages for related episodes | [Notification grouping on action policies](notifications/create-configure-action-policy-v2.md#reduce-noise-grouping-v2) | Batches related alerts into fewer notifications |
| Notifications should only go out for certain episodes by severity, labels, or payload fields | [Matchers](notifications/create-configure-action-policy-v2.md#matcher-v2) | Uses KQL on the action policy over episode and rule context (for example `rule.labels` and payload fields) so only matching episodes route to workflows |
| Planned maintenance: evaluations should continue but on-call should not be paged | [{{maint-windows-cap}}](notifications/manage-action-policies-v2.md#maintenance-windows-v2) | Pauses policy dispatch for a scheduled window; rule evaluation continues |
| A temporary quiet period is needed for a series or episode without changing the rule | [View, manage, and reference alerts](alerts/view-and-manage-alerts-v2.md#alert-actions-v2) (snooze, silence, acknowledge) | Snoozes or silences notifications. Acknowledge can also quiet an episode while work proceeds |
| Many low-level alerts should roll up into one higher-level signal | [Author rules](rules/author-rules-v2.md) ({{esql}} over `.rule-events`) | Runs follow-on rules on `.rule-events` or related data to correlate and notify once |
| One alert episode should stop notifying and leave the triage queue while the rule keeps running | [View, manage, and reference alerts](alerts/view-and-manage-alerts-v2.md#alert-actions-v2) (deactivate / resolve) | Deactivates that episode. The rule still evaluates and can detect new episodes for other series |

Use the links in the table for procedures and reference detail on each control.

### Key distinctions

|  | Tune rule / schedule | Activation / recovery thresholds | No-data handling | Matchers / grouping / throttle | {{maint-windows-cap}} / snooze / silence | Rules on alerts | Deactivate / resolve |
|---|---|---|---|---|---|---|---|
| Rule still evaluates | Yes | Yes | Yes | Yes | Yes | Yes, source rules | Yes |
| Changes breach detection logic | Yes | No, delays state only | Yes, empty-result policy | No | No | N/A | No |
| Reduces notifications | If fewer breaches | Indirectly | Indirectly | Yes | Yes | Yes | Yes |
| Typical time scope | Until next edit | Consecutive runs / duration | Per evaluation | Policy config | Window or until cleared | N/A | Until episode handled |

### Using them together [using-them-together]

These options stack. A common pattern is: tune the query for precision, add activation thresholds to ignore spikes, use matchers and throttling so action policies only fire for the right episodes at a sustainable rate, and use {{maint-windows-cap}} or snooze during known change windows.

Example: Noisy CPU rule

| Situation | Action | Mechanism |
|---|---|---|
| The {{esql}} query flags any host over 70% | Tighten the query or add a stricter `WHERE` | Write and tune the rule |
| Legitimate bursts open alerts for 1-minute spikes | Require 3 consecutive breaches before active | Activation thresholds |
| The same host pages every run for an hour | Add throttle and grouping on the action policy | Throttle, grouping |
| Only production hosts should page on-call | Add KQL on the policy matcher (for example on host or `rule.labels`) | Matchers |
| Database change window this evening | Open a {{maint-windows-cap}} or snooze the series | {{maint-windows-cap}}, snooze |

::::{note}
Order of application matters. Thresholds and no-data behavior affect lifecycle state before action policies run. Matchers and throttling apply when action policies are evaluated for each episode. Snooze and {{maint-windows-cap}} affect whether notifications send, not whether `.rule-events` documents are written. Check Discover if raw history is needed.
::::
