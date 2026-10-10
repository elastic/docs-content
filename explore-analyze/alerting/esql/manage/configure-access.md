---
navigation_title: Configure access
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: "Kibana feature privileges and Elasticsearch index privileges needed to manage rules, action policies, and alerts."
---

# Configure access [access]

To create rules, triage alerts, and configure notifications in {{alerting-v2-system}}, your role needs specific {{kib}} feature privileges and, if you're querying alerting data in Discover, {{es}} index privileges. [Create or update a role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) and add the privileges that match the tasks your team performs.

Most privileges are under the **Alerting V2** category in {{kib}} role management.

:::{note}
Depending on how your rules and notifications are configured, your role might also need `read` index privileges on the indices their rules query and **Actions and Connectors: All** (under **Management**) to create or edit workflow connectors. Refer to [{{kib}} role management](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for guidance on building roles that combine privileges across features.
:::

## Quick reference [alerting-quick-reference]

The following table shows the minimum privileges for each activity. Higher privilege levels include the access shown here.

| To... | Minimum required |
|---|---|
| Author and manage rules | **Rules: All** (under **Alerting V2**) |
| Monitor rule execution | **Execution history: Read** (under **Alerting V2**) |
| Triage alerts | **Alerts: All** (under **Alerting V2**) |
| Configure notifications | **Action Policies: All** (under **Alerting V2**) + **Workflows: Read** (under **Analytics** → **Workflows**) |
| Create rules and action policies with {{agent-builder}} {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.5+` | **{{agent-builder}}: Read** (under **Analytics**) + the privileges to [save what the agent creates](#alerting-agent-builder-privileges) |
| Query `.rule-events` and `.alert-actions` in Discover | **Discover: Read** (under **Analytics** → **Discover**) + **Alerts: Read** (Elasticsearch `read` access is bundled automatically) |
| Query `.kibana-event-log-*` in Discover | **Discover: Read** (under **Analytics** → **Discover**) + custom role with `read` index privilege on `.kibana-event-log-*` |

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

The **Execution history** privilege controls who can view rule execution history. Because execution history is read-only, **All** and **Read** grant the same access.

## Triage alerts [alerting-triage-privileges]

The **Alerts** privilege controls who can take triage actions on alerts.

| Level | What you can do |
|---|---|
| **All** | Acknowledge, unacknowledge, snooze, unsnooze, resolve, unresolve, tag, and assign alerts |
| **Read** | View alerts |

Both levels also grant read access to the alert data streams. Refer to [{{es}} index access](#alerting-index-access).

### Alerts from {{alerting-v1-system}} [alerting-classic-alert-privileges]

```{applies_to}
serverless: ga
stack: experimental 9.6+
```

The **Alerts** page also lists {{alerting-v1-system}} alerts. Your role's {{alerting-v1-system}} privileges for each alert's rule type decide which of these alerts you can see and act on:

- **To view an alert**: Your role must be able to view alerts from the alert's rule type in {{alerting-v1-system}}.
- **To triage an alert**: Your role needs **Alerts: All** and the {{alerting-v1-system}} privileges for the alert's rule type. With **Alerts: Read**, you can't triage {{alerting-v1-system}} alerts from the **Alerts** page.

For the {{alerting-v1-system}} privileges, refer to [Give access to triage alerts without managing rules](/explore-analyze/alerting/alerts/alerting-setup.md#_give_access_to_triage_alerts_without_managing_rules). To learn how each triage action affects these alerts, refer to [Triage alerts from {{alerting-v1-system}}](../alerts/triage-alert-episodes.md#triage-classic-alerts).

## Configure notifications [alerting-notifications-privileges]

These privileges control who can set up the action policies that invoke workflows and the workflows that send notifications.

### Action policies [action-policy-management]

The **Action Policies** privilege controls who can manage the action policies that invoke workflows for alerts.

| Level | What you can do |
|---|---|
| **All** | Create, update, delete, snooze, and unsnooze action policies |
| **Read** | View action policies |

:::{note}
Having **Action Policies: All** does not include the ability to create or edit rules. Add **Rules: All** if rule management is also required.
:::

### Workflows [alerting-workflows-access]

Action policies invoke workflows, which send notifications. The **Workflows** privilege is set under **Analytics** → **Workflows** in {{kib}} role management. To create or manage action policies, your role also needs access to the workflows they reference.

| Level | What you can do |
|---|---|
| **All** | Create and edit workflows; view and select existing workflows in action policies |
| **Read** | View and select existing workflows in action policies |

## Create rules and action policies with {{agent-builder}} [alerting-agent-builder-privileges]

```{applies_to}
serverless: experimental
stack: experimental 9.5+
```

To create rules and action policies with [{{agent-builder}}](../rules/create-rules-action-policies-agent-builder.md), your role needs these privileges:

| To... | Minimum required |
|---|---|
| Access and use {{agent-builder}} | **{{agent-builder}}: Read** (under **Analytics**) |
| Save the rule | **Rules: All** (under **Alerting V2**) |
| Save the action policy | **Action Policies: All** (under **Alerting V2**) |
| Select or create the workflow destination | **Workflows: Read** to select an existing workflow, or **Workflows: All** to create one (under **Analytics** → **Workflows**) |

## Query rule output and alert data [alerting-data-investigation-privileges]

{{alerting-v2-system-cap}} writes rule output and alert data to three queryable data sources. To query them in Discover using {{esql}}, your role needs {{kib}} feature access and {{es}} index access.

### {{kib}} feature access

Set Discover privileges under **Analytics** → **Discover** in {{kib}} role management. **All** and **Read** both let you run {{esql}} queries against rule events, alert actions, and execution history in Discover.

### {{es}} index access [alerting-index-access]

Granting **Alerts: All** or **Alerts: Read** also gives the role {{es}} `read` access to `.rule-events` and `.alert-actions` in the role's spaces, so you don't need a custom role for them. For `.kibana-event-log-*`, you still need a custom role.

| Data source | What it stores | How to grant access |
|---|---|---|
| `.rule-events` | One [rule event](../rules/rule-event-field-reference.md) per matching row, per run | Automatic. If access is missing, grant `read` using a custom role as a fallback. |
| `.alert-actions` | User-triggered triage records (acknowledge, snooze, resolve, assign) and system-written dispatcher records. For all `action_type` values, refer to the [field reference](../alerts/field-reference.md). | Automatic. If access is missing, grant `read` using a custom role as a fallback. |
| `.kibana-event-log-*` | Action policy dispatch outcomes written by the dispatcher: `dispatched`, `throttled`, and `unmatched` | Custom role with `read` index privilege |

## Set up rules and notifications [alerting-access-next-steps]

With access configured, you're ready to:

- [Create a rule](../rules/create-a-rule.md): Write the {{esql}} query that defines what to detect, set whether matches are grouped into an alert, and configure grouping and thresholds.
- [Set up workflows](../notifications-actions.md): Configure the workflows that deliver notifications, such as email, Slack, or webhook messages.
- [Create action policies](../action-policies/create-configure-action-policy.md): Define which alerts invoke a workflow, how often, and under what conditions.