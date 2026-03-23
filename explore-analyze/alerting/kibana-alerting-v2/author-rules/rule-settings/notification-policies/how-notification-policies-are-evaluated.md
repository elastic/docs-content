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

The dispatcher is the asynchronous component that bridges rule execution and notification delivery. It polls for new alert episodes and processes them through a 10-step pipeline.

The dispatcher runs every 10 seconds and processes up to 10,000 episodes per run.

## Dispatcher pipeline

1. **Load candidate episodes** — Fetch episodes that are ready for notification processing.
2. **Apply suppression rules** — Remove or defer episodes that match active suppression configuration.
3. **Resolve rule context** — Load rule metadata needed for matching and routing.
4. **Build matcher context** — Construct the typed context used for policy evaluation (including rule and episode fields).
5. **Load notification policies** — Call **`findAllDecrypted()`** and load **all** notification policies for the space. Policies are not filtered by per-rule references; loading is independent of which rule produced the episode.
6. **Evaluate policies (two phases)** — For each policy:
   1. **Rule label scoping** — Determine whether the episode’s rule satisfies the policy’s **`rule_labels`** selector. If not, skip this policy for the episode.
   2. **KQL episode matcher** — If label scoping passes, evaluate the policy’s KQL condition against the typed **`MatcherContext`**, including fields such as **`rule.name`**, **`rule.labels`**, and **`data.*`** (alongside other context fields the platform exposes for matching).
7. **Group and throttle** — Apply grouping keys and throttling windows according to matching policies.
8. **Select destinations** — Resolve workflow destinations and channels for dispatch.
9. **Dispatch notifications** — Send notifications and record outcomes.
10. **Record outcomes** — Persist dispatcher results for auditing and follow-up processing.

### Outcomes (step 10)

| Outcome | Description |
|---|---|
| **dispatched** | Notifications were sent according to policy |
| **throttled** | Delivery was suppressed by throttling rules |
| **suppressed** | Episode was suppressed before dispatch |
| **unmatched** | Episode did not match any notification policy |
| **error** | Processing failed; see logs and health indicators |
