---
navigation_title: Privileges
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "Privilege requirements for {{alerting-v2}}: what {{kib}} feature access and {{es}} index access each role needs to manage rules, policies, alerts, and query alert data."
---

# {{alerting-v2}} privileges [alerting-privileges-v2]

$$$alerting-privileges-v2$$$

This page describes the access requirements for {{alerting-v2}}, including {{kib}} feature privileges, {{es}} index privileges, and how rules and policies inherit those privileges through API keys.

:::{important}
Rules and action policies run in the background using the API key of the user who last saved them. That key inherits the saving user's privileges at save time. If those privileges are later reduced, rule or policy execution reflects the new limits. Ensure that only users with appropriate access save rules and policies.
:::

## Manage rules [alerting-manage-rules-privileges]

{{kib}} privileges
:   `{{rules-ui}} V2`: `All` to create, edit, enable, disable, and delete rules. `Read` to view rules and their details.

{{es}} index privileges
:   `read` on every index the rule's {{esql}} query reads (for example `logs-*`, `metrics-*`). The rule's API key must have the same read access.

## Manage action policies [action-policy-management]

{{kib}} privileges
:   `{{rules-ui}} V2`: `All` to create and edit action policies. `Read` to view policies.

Workflow attachment
:   To attach a workflow as a policy destination, you need permission to access that workflow in the space. This prevents users from routing notifications through high-privilege workflows they don't otherwise have access to.

## Manage alerts [alerting-manage-alerts-privileges]

{{kib}} privileges
:   `{{rules-ui}} V2`: `Read` or higher to view alert episodes and their details. `All` to use triage actions (acknowledge, snooze, resolve, tag).

{{es}} index privileges
:   `read` on `.rule-events` to view alert event data. `write` on `.alert-actions` to persist triage actions such as acknowledge, snooze, and tag.

## Query alert data in Discover [alerting-discover-privileges]

{{kib}} privileges
:   Standard Discover access. No additional {{alerting-v2}}-specific privilege is required.

{{es}} index privileges
:   `read` on `.rule-events` and `.alert-actions`. Anyone with this access can query alert history and triage records in Discover or build dashboards from them.
