---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Understand the difference between detection alerts created by the detection engine and external alerts ingested from third-party security tools.
---

# Detection alerts and external alerts [detection-vs-external-alerts]

{{elastic-sec}} works with two kinds of alerts that serve different roles. Understanding the difference is important for building rules, querying alert data, and triaging threats.


## Comparison [alert-comparison]

| | Detection alerts | External alerts |
|---|---|---|
| Source | Created by the {{elastic-sec}} detection engine | Ingested from third-party tools (for example, Suricata, CrowdStrike, Palo Alto Networks) |
| Event kind | `event.kind: "signal"` | `event.kind: "alert"` |
| Storage location | `.alerts-security.alerts-<space-id>` | Event indices (`logs-*`, `filebeat-*`, and others) |
| Alert metadata fields | Yes — includes `kibana.alert.*` fields for rule metadata, workflow status, and suppression data | No |
| Visible on | **Alerts** page | **Events** tabs on the Hosts, Users, and Network pages (use the **Show only external alerts** filter) |
| Workflow actions | Status, tags, assignees, cases, response actions | Standard event actions only |


## How they relate [how-alerts-relate]

External alerts are **inputs** to the detection engine. Detection alerts are the **outputs**. A detection rule can query event indices that contain external alerts and create detection alerts from them.

For example, the [External Alerts](https://www.elastic.co/docs/reference/security/prebuilt-rules/rules/promotions/external_alerts) prebuilt rule searches for documents with `event.kind: "alert"` in your event indices and creates corresponding detection alerts. Once converted, these alerts appear on the Alerts page with full workflow capabilities (status tracking, assignment, case attachment).

You can also write custom rules that specifically target external alerts from certain vendors or systems by filtering on fields like `event.module` or `event.dataset`.
