---
navigation_title: Configure access
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Privilege requirements for Kibana experimental alerting features: which Kibana feature privileges and Elasticsearch index privileges each role needs to manage rules, action policies, alerts, and query rule events and alert actions."
---

# Configure access to the {{alerting-v2-system}} [experimental-alerting-system-access]

To use the {{alerting-v2-system}}, your role needs specific {{kib}} feature privileges and, if you're querying alerting data in Discover, {{es}} index privileges. [Create or update a role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) and add the privileges that match the tasks your team performs.

This page is organized by user activity. Most privileges are set under the **Alerting** category in {{kib}} role management. Exceptions are noted in each section.

:::{note}
This page covers access to the {{alerting-v2-system}} features and data. Depending on how your rules and notifications are configured, your role might also need `read` index privileges on the indices their rules query and **Actions and Connectors: All** (under **Management**) to create or edit workflow connectors. Refer to [{{kib}} role management](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for guidance on building roles that combine privileges across features.
:::

## Quick reference [alerting-quick-reference]

The following table shows the minimum privileges required for each activity. Higher privilege levels include the access shown here. Refer to the following sections for the full breakdown.

| To... | Minimum required |
|---|---|
| Author and manage rules | **Rules: All** (under **Alerting**) |
| Monitor rule execution | **Execution history: Read** (under **Alerting**) |
| Triage alert episodes | **Alerts: All** (under **Alerting**) |
| Configure notifications | **Action Policies: All** (under **Alerting**) + **Workflows: Read** (under **Analytics > Workflows**) |
| Query `.rule-events` and `.alert-actions` in Discover | **Discover: Read** (under **Analytics > Discover**) + **Alerts: Read** (Elasticsearch `read` access is bundled automatically) |
| Query `.kibana-event-log-*` in Discover | **Discover: Read** (under **Analytics > Discover**) + custom role with `read` index privilege on `.kibana-event-log-*` |

## Author and monitor rules [alerting-authoring-monitoring-privileges]

These privileges control who can create rules and review their execution history.

### Rules [alerting-manage-rules-privileges]

The **Rules** privilege controls who can create and manage rules.

| Level | What you can do |
|---|---|
| **All** | Create, edit, delete, enable, and turn off rules |
| **Read** | View rules and their configuration |

:::{note}
**Rules: All** also grants access to the **Alerts** menu in Discover, which routes rule creation to the {{alerting-v2-system}} rule form when the system is enabled in your space.
:::

### View rule execution history [alerting-execution-history-privileges]

The **Execution history** privilege controls who can view rule execution history. Execution history is read-only; both **All** and **Read** grant the same access. There is no write surface for execution history.

| Level | What you can do |
|---|---|
| **All** | View rule execution history |
| **Read** | View rule execution history |

## Triage alerts [alerting-triage-privileges]

The **Alerts** privilege controls who can take triage actions on alert episodes.

| Level | What you can do |
|---|---|
| **All** | Acknowledge, snooze, assign, tag, activate, and deactivate alert episodes |
| **Read** | View alert episodes |

:::{note}
Granting **Alerts: All** or **Alerts: Read** also gives the role direct Elasticsearch `read` access to `.rule-events` and `.alert-actions`, scoped to that role's spaces. This is bundled into the privilege — no separate custom role or index privilege is needed to query these data streams in Discover.
:::

## Configure notifications [alerting-notifications-privileges]

These privileges control who can set up the action policies and workflows that route alert episode notifications.

### Action policies [action-policy-management]

The **Action Policies** privilege controls who can manage the action policies that route alert episode notifications.

| Level | What you can do |
|---|---|
| **All** | Create, update, delete, snooze, and unsnooze action policies |
| **Read** | View action policies |

:::{note}
Having **Action Policies: All** does not include the ability to create or edit rules. Add **Rules: All** if rule management is also required.
:::

### Workflows [alerting-workflows-access]

Action policies route notifications through workflows. The **Workflows** privilege is set under **Analytics > Workflows** in {{kib}} role management. To create or manage action policies, your role also needs access to the workflows they reference.

| Level | What you can do |
|---|---|
| **All** | Create and edit workflows; view and select existing workflows in action policies |
| **Read** | View and select existing workflows in action policies |

## Query rule output and episode data [alerting-data-investigation-privileges]

The {{alerting-v2-system}} writes rule output and episode data to three queryable data sources. To query them in Discover using {{esql}}, your role needs {{kib}} feature access and {{es}} index access.

### {{kib}} feature access

Set Discover privileges under **Analytics > Discover** in {{kib}} role management.

| Level | What you can do |
|---|---|
| **All** | Run {{esql}} queries against rule events, alert actions, and execution history in Discover |
| **Read** | Run {{esql}} queries against rule events, alert actions, and execution history in Discover |

Both levels grant the same query access. There is no write surface for any of these data sources in Discover.

### {{es}} index access

For `.rule-events` and `.alert-actions`, {{es}} `read` access is bundled into the **Alerts** {{kib}} privilege. For `.kibana-event-log-*`, a custom role is still required.

| Data source | What it stores | How to grant access |
|---|---|---|
| `.rule-events` | A record for every rule evaluation; one document per result row per run | Automatic with **Alerts: All** or **Alerts: Read**. If access is missing, grant `read` using a custom role as a fallback. |
| `.alert-actions` | User-triggered triage records (acknowledge, snooze, resolve, assign) and system-written dispatcher records. | Automatic with **Alerts: All** or **Alerts: Read**. If access is missing, grant `read` using a custom role as a fallback. |
| `.kibana-event-log-*` | Action policy dispatch outcomes written by the dispatcher: `dispatched`, `throttled`, and `unmatched` | Custom role with `read` index privilege. Not covered by the automatic grant. |

<!-- TODO: When PR #6527 merges, update the `.alert-actions` row above ("What it stores" column) to add a link to the field reference. Full updated cell:
"User-triggered triage records (acknowledge, snooze, resolve, assign) and system-written dispatcher records. For all `action_type` values, refer to the [alert data stream field reference](../alerts/field-reference.md)." -->

## Next steps [alerting-access-next-steps]

With access configured, you're ready to [create your first rule](create-your-first-rule.md).

<!-- TODO: When PRs #6523 (rules) and #6525 (workflows/notifications) are merged, replace the sentence
above with the bulleted list below (delete the prose line, uncomment the list).

- **[Create a rule](../rules/create-a-rule.md):** Write the {{esql}} query that defines what to detect, choose Signal or Alert mode, and configure grouping and thresholds. ← PR #6523
- **[Set up workflows](../notifications-actions.md):** Configure the automation objects that deliver notifications — email, Slack, webhook, and so on. ← PR #6525
- **[Create action policies](../action-policies/create-configure-action-policy.md):** Define who gets notified, how often, and under what conditions. ← PR #6525
-->