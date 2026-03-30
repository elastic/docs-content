---
navigation_title: How notification policies are evaluated
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "How Kibana alerting v2 notification policies match alert episodes, apply throttling and suppression, and produce dispatch outcomes."
---

# How Kibana alerting v2 notification policies are evaluated [how-notification-policies-evaluated-v2]

Notification policies are separate from rules. After a rule runs and produces or updates alert episodes, the system decides which policies apply, whether notifications should go out, and which workflows receive them. You configure policies once. They can apply to many rules.

## How policies are matched to episodes

Policies are global in the space unless you narrow them:

1. Rule labels: If a policy specifies rule labels, only rules whose labels satisfy that selector are considered. If you leave rule labels empty, the policy acts as a catch-all for every rule, subject to the KQL matcher below.
2. KQL matcher: For each candidate policy, the KQL condition is evaluated against the episode and rule context. For example, it can use rule name, rule labels, episode status, and fields from the alert payload, often under `data.*` in the matcher. Use the matcher editor suggestions to find which fields are available in your build.

An episode can match zero, one, or many policies. If it matches none, notifications are not sent for that episode under those policies. An `unmatched` outcome is recorded for auditing, as defined in the [Possible outcomes](#possible-outcomes) section.

## What happens after a policy matches

For episodes that match a policy, the system applies suppression if configured, grouping for how messages are batched, and throttling for the minimum time between notifications for the same group. Then it sends notifications to the workflow destinations you configured on the policy.

Order matters: Lifecycle thresholds and no-data behavior on the rule run before notification policies. Policies only affect routing and delivery, not whether rows are written to `.rule-events`.

## Possible outcomes

| Outcome | What it means for you |
|---|---|
| dispatched | Notifications were sent according to the policy |
| throttled | Delivery was suppressed because throttling rules said to wait |
| suppressed | The episode was suppressed before a notification went out, for example by an active suppression |
| unmatched | No notification policy matched this episode, so no workflow ran for it under these policies |
| error | Processing failed. Check {{kib}} logs and any health indicators your team uses |

Notifications can arrive shortly after an episode becomes eligible. Heavy load or many policies can add noticeable delay. If something seems stuck, verify matchers, throttling, maintenance windows, and that the episode matches at least one policy.
