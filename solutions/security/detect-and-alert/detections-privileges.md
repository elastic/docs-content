---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detections-permissions-section.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Find privilege requirements, predefined roles, and the authorization model for Elastic Security detection features.
---

# Detections privileges [security-detections-requirements-custom-role-privileges]

Learn about the access requirements for detection features, including:

- **Privilege requirements**: Cluster, index, and {{kib}} privileges that your role needs to enable detections, manage rules, and more
- **Predefined roles**: {{serverless-full}} roles with detection privileges
- **Authorization model**: How detection rules use API keys to run background tasks

For instructions on turning on the detections feature, refer to [Turn on detections](/solutions/security/detect-and-alert/detections-requirements.md).

## About index privileges

When creating custom roles for detection features, you'll need to grant access to system indices that include your space ID (`<space-id>`). For example, the default space uses `.alerts-security.alerts-default`. Refer to the following details to understand which system indices your role might require access to. 

:::::{tab-set}

::::{tab-item} {{sec-serverless}}
Only uses the `.alerts-security.alerts-<space-id>` index.
::::

::::{tab-item} {{elastic-sec}}
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
:   - {applies_to}`stack: ga 9.0` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature

## Preview rules

Cluster privileges
:   None

Index privileges
:   `read` on:
    - `.preview.alerts-security.alerts-<space-id>`
    - `.internal.preview.alerts-security.alerts-<space-id>-*`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.0+` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature

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
:   - {applies_to}`stack: ga 9.0+` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature

::::{note}
To manage rules with actions and connectors, you need additional privileges for the `Actions and Connectors` feature (`Management`→ `Actions and Connectors`):

- `All`: Provides full access to rule actions and connectors.
- `Read`: Allows you to edit rule actions and use existing connectors, but you cannot create new connectors.

To import rules with actions, you need at least `Read` privileges. To overwrite or add new connectors during import, you need `All` privileges.
::::

## Manage alerts

Allows you to manage alerts without modifying rules.

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
:   - {applies_to}`stack: ga 9.0` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3` {applies_to}`serverless: ga` `All` for the `Rules, Alerts, and Exceptions` feature

::::{note}
Alerts are managed through {{es}} index privileges. To view alert management flows, you need at least `Read` for the `Rules, Alerts, and Exceptions` feature.

Before a user can be assigned to a case, they must log into {{kib}} at least once to create a user profile.
::::

## Manage exceptions

Cluster privileges
:   None

Index privileges
:   None

{{kib}} privileges
:   - {applies_to}`stack: ga 9.0` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3` `All` for the `Rules, Alerts, and Exceptions` feature
    - {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` `Read` for the `Rules, Alerts, and Exceptions` feature and `All` for the `Exceptions` subfeature

## Manage value lists [detections-privileges-manage-value-lists]

Cluster privileges
:   `manage`

Index privileges
:   `manage`, `write`, `read`, `view_index_metadata` on:
    - `.lists-<space-id>`
    - `.items-<space-id>`

{{kib}} privileges
:   - {applies_to}`stack: ga 9.0` `All` for the `Security` feature
    - {applies_to}`stack: ga 9.3` {applies_to}`serverless: ga` `All` for the `Rules` and `Saved Objects Management` features

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

## Authorization [alerting-auth-model]

```yaml {applies_to}
stack:
```

Detection rules, including all background detection checks and the actions they generate, are authorized using an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user to edit the rule. When a rule is created or modified, an API key is generated that captures a snapshot of that user's privileges. This API key is used to run all background tasks associated with the rule, including detection checks and executing actions.

::::{important}
If a rule requires certain privileges to run (such as index privileges), and a user without those privileges updates the rule, the rule will no longer function.
::::
