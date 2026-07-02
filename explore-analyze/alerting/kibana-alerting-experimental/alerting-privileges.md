---
navigation_title: Privileges
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Privilege requirements for the {{alerting-v2}}: what {{kib}} feature access and {{es}} index access each role needs to manage rules, policies, alerts, and query alert data."
---

# {{alerting-v2-cap}} privileges [alerting-privileges]


Privileges for the {{alerting-v2}} control what you can do with rules, alerts, action policies, and alert data queries. The {{alerting-v2}} are part of Kibana and are marked **Experimental** in the UI.

In Kibana role management, the {{alerting-v2}} privileges appear under the **Alerting** category. There are four privileges, each independent. Holding one does not grant another. For example, if you have **Action Policies: All**, you cannot create or edit rules unless you also have **Rules: All**.

## Manage rules [alerting-manage-rules-privileges]

The **Rules** privilege controls who can create and manage rules.

| Level | What you can do |
|---|---|
| **All** | Create, edit, delete, enable, and disable rules |
| **Read** | View rules and their configuration |

If you need to create or modify rules, use **Rules: All**. If you only need to view existing rules and their configuration, use **Rules: Read**.

## Manage action policies [action-policy-management]

The **Action Policies** privilege controls who can manage the policies that route alert episode notifications.

| Level | What you can do |
|---|---|
| **All** | Create, update, delete, snooze, and unsnooze action policies |
| **Read** | View action policies |

If you need to create or configure action policies, use **Action Policies: All**. Having **Rules: All** does not include the ability to manage action policies unless you also have **Action Policies: All**.

## Manage alerts [alerting-manage-alerts-privileges]

The **Alerts** privilege controls who can take triage actions on alert episodes.

| Level | What you can do |
|---|---|
| **All** | Acknowledge, snooze, assign, tag, activate, and deactivate alert episodes |
| **Read** | View alert episodes |

If you need to acknowledge or snooze active episodes, use **Alerts: All**. If you only need to monitor the alerts list, use **Alerts: Read**.

## View execution history [alerting-execution-history-privileges]

The **Execution history** privilege controls who can view rule execution history.

| Level | What you can do |
|---|---|
| **All** | View rule execution history |
| **Read** | View rule execution history |

Execution history is read-only. Both **All** and **Read** grant the same access. There is no write surface for execution history.

## Query alert data in Discover [alerting-discover-privileges]

To query alert data in Discover using {{esql}}, you need both Kibana feature access and Elasticsearch index access.

### Kibana feature access

You need **Discover: Read** access in the space where you plan to run queries.

### Elasticsearch index access

The {{alerting-v2}} writes alert data to two hidden system data streams: `.rule-events` and `.alert-actions`. To query them in Discover, you need the `read` index privilege on each data stream.

| Data stream | Required privilege |
|---|---|
| `.rule-events` | `read` |
| `.alert-actions` | `read` |

Because these are hidden system data streams, request access through a custom role with the appropriate index privileges.
