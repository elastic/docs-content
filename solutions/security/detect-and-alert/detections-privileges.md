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
- **Predefined {{serverless-full}} roles**: {{serverless-short}} roles with detection privileges
- **Authorization model**: How rules inherit privileges from their last editor using API keys

For instructions on turning on the detections feature, refer to [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md).

:::{important}
Rules run in the background using the privileges of the user who last edited them. Ensure that only users with the appropriate access edit them. Refer to [](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept) for more details.
:::

## About index privileges

When creating custom roles for detection features, you'll need to grant access to system indices that include your space ID (`<space-id>`). For example, the default space uses `.alerts-security.alerts-default`. Refer to the following details to understand which system indices your role might require access to.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` You can give a role access to alerts only, rules only, or both.

:::{admonition} Role access to rules and alerts in 9.4
:applies_to: {"stack": "ga 9.4+", "serverless": "ga"}
Starting in {{stack}} 9.4, new custom roles require explicit **Rules and Exceptions** and **Alerts** privileges. Earlier releases sometimes granted alert-related access indirectly through broader **Security** privileges or the **Rules, Alerts, and Exceptions** feature. Review custom roles after an upgrade to confirm each role still has the intended access to alerts.
:::

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
To manage rules with actions and connectors, you need additional privileges for the `Actions and Connectors` feature (`Management` > `Actions and Connectors`):

- `All`: Provides full access to rule actions and connectors.
- `Read`: Allows you to edit rule actions and use existing connectors, but you cannot create new connectors.

To import rules with actions, you need at least `Read` privileges. To overwrite or add new connectors during import, you need `All` privileges.
::::

## Manage alerts

Allows you to manage alerts.

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
:   - {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` `Read` for `Alerts` to view alerts, open alert flyouts, and view alert tables on pages and dashboards with alert-related flows. To do everything that `Read` provides, plus changing alert status, setting assignees, setting tags, and bulk actions on alerts, set `Alerts` to `All`.  
    - {applies_to}`stack: ga 9.3` `All` for the `Rules, Alerts, and Exceptions` feature to view alert management flows
    - {applies_to}`stack: ga 9.0-9.2` `All` for the `Security` feature

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

