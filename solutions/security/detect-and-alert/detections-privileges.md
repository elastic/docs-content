---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detections-permissions-section.html
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Find privilege requirements, predefined roles, and the authorization model for Elastic Security detection features.
---

# Detections privileges [security-detections-requirements-custom-role-privileges]

Learn about the access requirements for detection features, including:

- **Privilege requirements**: Cluster, index, and {{kib}} privileges that your role needs to enable detections, manage rules, view and edit alerts, and more
- **Predefined {{serverless-full}}  roles**: {{serverless-short}} roles with detection privileges
- **Authorization model**: How rules inherit privileges from their last editor via API keys

For instructions on turning on the detections feature, refer to [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md).

:::{important}
Rules run in the background using the privileges of the user who last edited them. Ensure that only users with the appropriate access edit them. Refer to [](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept) for more details.
:::

## About index privileges

When creating custom roles for detection features, you'll need to grant access to system indices that include your space ID (`<space-id>`). For example, the default space uses `.alerts-security.alerts-default`. Refer to the following details to understand which system indices your role might require access to. 

:::::{tab-set}

::::{tab-item} {{serverless-full}}
Only uses the `.alerts-security.alerts-<space-id>` index.
::::

::::{tab-item} {{ech}}
Uses the `.alerts-security.alerts-<space-id>` index. If you upgraded from version 8.0 or earlier, you might also need privileges on the legacy `.siem-signals-<space-id>` index.
::::

:::::

## Enable the detections feature [enable-detections-privileges]

Required to initialize the detection engine in a {{kib}} space.

Cluster privileges
:   `manage`

Index privileges
:   `manage`, `write`, `read`, `view_index_metadata` on:
    - `.alerts-security.alerts-<space-id>`
    - `.siem-signals-<space-id>` (only if you upgraded from version 8.0 or earlier)
    - `.lists-<space-id>`
    - `.items-<space-id>`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` `All` for the `Rules and Exceptions` feature and `All` for the `Alerts` feature 
    - {applies_to}`stack: ga =9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

## Preview rules

Cluster privileges
:   None

Index privileges
:   `read` on:
    - `.preview.alerts-security.alerts-<space-id>`
    - `.internal.preview.alerts-security.alerts-<space-id>-*`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` `All` for the `Rules and Exceptions` feature and `All` for the `Alerts` feature
    - {applies_to}`stack: ga =9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

## Manage rules

Cluster privileges
:   None

Index privileges
:   `manage`, `write`, `read`, `view_index_metadata` on:
    - `.alerts-security.alerts-<space-id>`
    - `.siem-signals-<space-id>` (only if you upgraded from version 8.0 or earlier)
    - `.lists-<space-id>`
    - `.items-<space-id>`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` `All` for the `Rules and Exceptions` feature and `All` for the `Alerts` feature
    - {applies_to}`stack: ga =9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

::::{note}
To manage rules with actions and connectors, you need additional privileges for the `Actions and Connectors` feature (`Management`> `Actions and Connectors`):

- `All`: Provides full access to rule actions and connectors.
- `Read`: Allows you to edit rule actions and use existing connectors, but you cannot create new connectors.

To import rules with actions, you need at least `Read` privileges. To overwrite or add new connectors during import, you need `All` privileges.
::::

## Manage alerts

Controls who can view and update detection alerts (for example, on the **Alerts** page, alert details flyout, rule details **Alerts** tab, **Alerts** tab in cases, and entity analytics).

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Alerts** feature (Security > Alerts):

- `Read`: View alerts, open the alert details flyout, see alert tables, and view alert data in entity analytics (for example, risk contributions). No status changes, assignees, tags, or bulk actions.
- `All`:** Everything you get with `Read`, plus: change alert statuses (open/closed/acknowledged), set assignees, add tags, and use bulk actions on alerts.

Cluster privileges
:   None

Index privileges
:   `maintenance`, `write`, `read`, `view_index_metadata` on:
    - `.alerts-security.alerts-<space-id>`
    - `.internal.alerts-security.alerts-<space-id>-*`
    - `.siem-signals-<space-id>` (only if you upgraded from version 8.0 or earlier)
    - `.lists-<space-id>`
    - `.items-<space-id>`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Set the **Alerts** feature (Security > Alerts): **Read** to view alerts, flyouts, and tables (no status, assignee, tag, or bulk actions); **All** for everything in Read plus status changes, assignees, tags, and bulk actions. Alerts access can be granted independently from **Rules**—you can have Alerts read or edit without Rules access, or Rules access without Alerts access.
    - {applies_to}`stack: ga 9.3` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

::::{note}
Alerts are managed through {{es}} index privileges. {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` **Alerts** feature: **Read** lets you view alerts, open flyouts, and see alert tables (including in entity analytics); **All** adds the ability to change status, set assignees, add tags, and use bulk actions. {applies_to}`stack: ga =9.3` To view alert management flows, you need at least `Read` for the `Rules, Alerts, and Exceptions` feature.

Before a user can be assigned to a case, they must log into {{kib}} at least once to create a user profile.
::::

## Manage exceptions

Cluster privileges
:   None

Index privileges
:   None

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` At least `Read` for the `Rules and Exceptions` feature and **Manage Exceptions** selected for the `Exceptions` sub-feature
    - {applies_to}`stack: ga =9.3` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

## Manage value lists [detections-privileges-manage-value-lists]

Cluster privileges
:   `manage`

Index privileges
:   `manage`, `write`, `read`, `view_index_metadata` on:
    - `.lists-<space-id>`
    - `.items-<space-id>`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` `All` for the `Rules and Exceptions` feature and `All` for the `Alerts` feature
    - {applies_to}`stack: ga =9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

::::{important}
To create the `.lists` and `.items` data streams in your space, visit the **Rules** page for each appropriate space. 
::::


## Predefined {{serverless-full}} roles [predefined-serverless-roles-detections]

```yaml {applies_to}
serverless: ga
```

{{serverless-full}} includes predefined roles with detection privileges:

| Action | Roles with access |
| --- | --- |
| Manage rules | Threat Intelligence Analyst, Tier 3 Analyst, Detections Eng, SOC Manager, Endpoint Policy Manager, Platform Engineer, Editor |
| View rules (read only) | Tier 1 Analyst, Tier 2 Analyst, Viewer, Endpoint Operations Analyst |
| Manage alerts | All roles except Viewer |
| Manage exceptions and value lists | Threat Intelligence Analyst, Tier 3 Analyst, Detections Eng, SOC Manager, Endpoint Policy Manager, Platform Engineer, Editor |
| View exceptions and value lists (read only) | Tier 1 Analyst, Tier 2 Analyst, Viewer, Endpoint Operations Analyst |

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` With the **Alerts** feature, you can grant alert access independently from rule management: **Read** for viewing alerts (flyouts, tables, entity analytics); **All** for viewing plus updating status, assignees, tags, and bulk actions. Custom roles can have Alerts without Rules access, or Rules without Alerts access. Prebuilt role mappings may be updated in a later release.
