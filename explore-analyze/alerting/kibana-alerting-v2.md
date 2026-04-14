---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
description: Learn what Kibana alerting v2 offers, who it is for, and where to go next in the documentation.
---

# Kibana alerting v2 [alerting-overview-v2]

Kibana alerting v2 is a way to watch your data in Elastic, decide what counts as a finding, and control how people get notified. You describe what to look for using [ES|QL](elasticsearch://reference/query-languages/esql.md), the same query language you can use when exploring data elsewhere in the product.

It runs next to [Kibana alerting v1](kibana-alerting-v1.md). You can adopt Kibana alerting v2 at your own pace; there is no forced migration.

## What is Kibana alerting v2 [alerting-v2-what]

Kibana alerting v2 is a rules-based system that checks your data on a schedule, stores a clear record of what happened over time, and can send notifications through shared settings that apply across many rules. You can start with guided setup and grow into more advanced options when you are ready.

## Why use Kibana alerting v2 [alerting-v2-why]

Detection alone is not always enough. Teams often need a **record they can search later**, **notifications that do not repeat the same setup on every rule**, and a **consistent way to track an issue** from first sighting through resolution. Kibana alerting v2 is aimed at those needs.

It helps with challenges such as:

* **Limited visibility**: Store outcomes over time so you can review trends and past behavior, not only what is open right now.
* **Notification overload**: Reuse how and when messages go out instead of configuring each rule in isolation.
* **Rigid rule types**: Define what to watch with queries and carry the fields that matter for your responders.
* **Siloed tools**: Use one query language for exploration and for alerting so skills transfer.

## Who should use Kibana alerting v2 [alerting-v2-who]

Kibana alerting v2 is a good fit if you use {{serverless-full}} and want query-driven alerting, shared notification behavior, and searchable history.

## Key concepts [alerting-v2-concepts]

These topics are explained in depth on dedicated pages:

* **Rules and queries**: How you define what to evaluate, optional detect vs alert behavior, schedules, and authoring from the UI, Discover, or YAML. Refer to [Author rules](kibana-alerting-v2/author-rules.md).
* **Notifications**: How shared settings decide who gets notified and how messages are grouped or throttled. Refer to [Notification policies](kibana-alerting-v2/author-rules/rule-settings/notification-policies.md).
* **Alerts and investigation**: How to view, filter, and work with findings in the product and in Discover. Refer to [Manage alerts](kibana-alerting-v2/manage-alerts.md).
* **Noise and lifecycle**: Snooze, grouping, thresholds, maintenance windows, and related controls. Refer to [Reduce noise](kibana-alerting-v2/reduce-noise.md).
* **Fields and storage**: Names and meanings of fields written for rules and actions. Refer to [Rule event and action field reference](kibana-alerting-v2/alert-event-field-reference.md).

## Learn more

* [Before you begin](kibana-alerting-v2/before-you-begin.md) for prerequisites and permissions.
* [Author rules](kibana-alerting-v2/author-rules.md) to create and tune rules end to end.
* [Manage rules](kibana-alerting-v2/manage-rules.md) for day-to-day operations.

For a high-level comparison with Kibana alerting v1 and Watcher, read [Alerting overview](../alerting-overview.md). To pick a system by goal, read [Choose an alerting system](choose-an-alerting-system.md).
