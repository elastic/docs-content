---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detections-permissions-section.html
  - https://www.elastic.co/guide/en/serverless/current/security-detections-requirements.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Detections requirements

To use the [Detections feature](/solutions/security/detect-and-alert.md), you first need to configure a few settings. You also need the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) to send [notifications](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications) when detection alerts are generated. Additionally, there are some [advanced settings](/solutions/security/detect-and-alert/detections-requirements.md#adv-list-settings) used to configure {{kib}} [value list](/solutions/security/detect-and-alert/create-manage-value-lists.md) upload limits.

::::{important}
Several steps are **only** required for **self-managed** {{stack}} deployments. If you’re using an Elastic Cloud deployment, you only need to [enable detections](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui).
::::

## Configure self-managed {{stack}} deployments [detections-on-prem-requirements]

```yaml {applies_to}
stack:
```

These steps are only required for **self-managed** deployments:

- HTTPS must be configured for communication between [{{es}} and {{kib}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).
- In [`kibana.yml`](/deploy-manage/stack-settings.md):

  Add the `xpack.encryptedSavedObjects.encryptionKey` setting with any alphanumeric value of at least 32 characters. For example:

  `xpack.encryptedSavedObjects.encryptionKey: 'fhjskloppd678ehkdfdlliverpoolfcr'`

- In [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md):
  - Set the `xpack.security.enabled` setting to `true`. Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) for more information.
  - If the `search.allow_expensive_queries` setting is set to `false`, remove it. If set to its default value of `true` or not included in the `elasticsearch.yml` file, you don't need to make changes. This setting must be `true` for key detection features, such as [alerting rules](/explore-analyze/alerts-cases/alerts/alerting-setup.md#alerting-prerequisites) and rule exceptions, to work.

::::{important}
After changing the `xpack.encryptedSavedObjects.encryptionKey` value and restarting {{kib}}, you must restart all detection rules.
::::

## Enable and access detections [enable-detections-ui]

To use the Detections feature, it must be enabled, your role must have access to rules and alerts, and your {{kib}} space must have **Data View Management** [feature visibility](/deploy-manage/manage-spaces.md). If your role doesn’t have the cluster and index privileges needed to enable this feature, you can request someone who has these privileges to visit your {{kib}} space, which will turn it on for you.

::::{note}
For instructions about using {{ml}} jobs and rules, refer to [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md).
::::

### Custom role privileges [security-detections-requirements-custom-role-privileges]

```yaml {applies_to}
stack: ga
serverless: ga
```

| Action | Cluster Privileges | Index Privileges | Kibana Privileges |
| --- | --- | --- | --- |
| Enable detections in your space | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>- `.alerts-security.alerts-<space-id>`<br>- `.siem-signals-<space-id>` ^1^<br>- `.lists-<space-id>`<br>- `.items-<space-id>`<br><br>^1^ **NOTE**: If you’re upgrading to {{stack}} 8.0.0 or later, users should have privileges for the `.alerts-security.alerts-<space-id>` AND `.siem-signals-<space-id>` indices. If you’re newly installing the {{stack}}, then users do not need privileges for the `.siem-signals-<space-id>` index.<br> | * {applies_to}`ga 9.0`: `All` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` feature |
| Enable detections in all spaces<br><br>**NOTE**: To turn on detections, visit the Rules and Alerts pages for each space. | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams:<br><br>- `.alerts-security.alerts-<space-id>`<br>- `.siem-signals-<space-id>` ^1^<br>- `.lists-<space-id>`<br>- `.items-<space-id>`<br><br>^1^ **NOTE**: If you’re upgrading to {{stack}} 8.0.0 or later, users should have privileges for the `.alerts-security.alerts-<space-id>` AND `.siem-signals-<space-id>` indices. If you’re newly installing the {{stack}}, then users do not need privileges for the `.siem-signals-<space-id>` index.<br> | * {applies_to}`ga 9.0`: `All` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` feature |
| Preview rules | N/A | `read` for these indices:<br><br>- `.preview.alerts-security.alerts-<space-id>`<br>- `.internal.preview.alerts-security.alerts-<space-id>-*`<br> | * {applies_to}`ga 9.0`: `All` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` feature |
| Manage rules | N/A | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>- `.alerts-security.alerts-<space-id>`<br>- `.siem-signals-<space-id>`^1^<br>- `.lists-<space-id>`<br>- `.items-<space-id>`<br><br>^1^ **NOTE**: If you’re upgrading to {{stack}} 8.0.0 or later, users should have privileges for the `.alerts-security.alerts-<space-id>` AND `.siem-signals-<space-id>` indices. If you’re newly installing the {{stack}}, then users do not need privileges for the `.siem-signals-<space-id>` index.<br> | * {applies_to}`ga 9.0`: `All` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` feature<br><br>**NOTE:** You need additional `Action and Connectors` feature privileges (**Management → Action and Connectors**) to manage rules with actions and connectors:<br><br>- To provide full access to rule actions and connectors, give your role `All` privileges. With `Read` privileges, you can edit rule actions, but will have limited capabilities to manage connectors. For example, `Read` privileges allow you to add or remove an existing connector from a rule, but does not allow you to create a new connector.<br>- To import rules with actions, you need at least `Read` privileges for the `Action and Connectors` feature. To overwrite or add new connectors, you need `All` privileges for the `Actions and Connectors` feature. To import rules without actions,  you don’t need `Actions and Connectors` privileges.<br> |
| Manage alerts<br><br>**NOTE**: Allows you to manage alerts, but not modify rules. | N/A | `maintenance`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>- `.alerts-security.alerts-<space-id>`<br>- `.internal.alerts-security.alerts-<space-id>-*`<br>- `.siem-signals-<space-id>`^1^<br>- `.lists-<space-id>`<br>- `.items-<space-id>`<br><br> **NOTE**: Before a user can be assigned to a case, they must log into Kibana at least once, which creates a user profile.<br><br>^1^ **NOTE**: If you’re upgrading to {{stack}} 8.0.0 or later, users should have privileges for the `.alerts-security.alerts-<space-id>` AND `.siem-signals-<space-id>` indices. If you’re newly installing the {{stack}}, then users do not need privileges for the `.siem-signals-<space-id>` index.<br> | * {applies_to}`ga 9.0`: `Read` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `Read` for the `Rules` feature<br><br>**NOTE:** Alerts are managed through the ES privileges. To view the alert management flows requires at least the `Read` for th `Rules` feature. |
| Manage exceptions | N/A | N/A | * {applies_to}`ga 9.0`: `All` for the `Security` feature<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` feature |
| Manage value lists.<br><br>Create the `.lists` and `.items` data streams in your space<br><br>**NOTE**: To initiate the process that creates the data streams, you must visit the Rules page for each appropriate space. | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these data streams, where `<space-id>` is the space name:<br><br>- `.lists-<space-id>`<br>- `.items-<space-id>`<br> | * {applies_to}`ga 9.0`: `All` for the `Security` and `Saved Objects Management` features<br><br>* {applies_to}`ga 9.3` {applies_to}`serverless`: `All` for the `Rules` and `Saved Objects Management` features |

### Predefined {{serverless-full}} roles [predefined-serverless-roles-detections]
```yaml {applies_to}
serverless: ga
```

| Action                               | Predefined role                                                                                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manage rules                         | - Threat Intelligence Analyst<br>- Tier 3 Analyst<br>- Detections Eng<br>- SOC Manager<br>- Endpoint Policy Manager<br>- Tier 3 Analyst<br>- Platform Engineer<br>- Editor |
| Rules read only                      | - Tier 1 Analyst<br>- Tier 2 Analyst<br>- Viewer<br>- Endpoint Operations Analyst                                                                                          |
| Manage alerts                        | - All roles except for Viewer                                                                                                                                              |
| Manage exceptions and value lists    | - Threat Intelligence Analyst<br>- Tier 3 Analyst<br>- Detections Eng<br>- SOC Manager<br>- Endpoint Policy Manager<br>- Tier 3 Analyst<br>- Platform Engineer<br>- Editor |
| Exceptions and value lists read only | - Tier 1 Analyst<br>- Tier 2 Analyst<br>- Viewer<br>- Endpoint Operations Analyst                                                                                          |

### Authorization [alerting-auth-model]

```yaml {applies_to}
stack:
```

Rules, including all background detection and the actions they generate, are authorized using an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user to edit the rule. Upon creating or modifying a rule, an API key is generated for that user, capturing a snapshot of their privileges. The API key is then used to run all background tasks associated with the rule including detection checks and executing actions.

::::{important}
If a rule requires certain privileges to run, such as index privileges, keep in mind that if a user without those privileges updates the rule, the rule will no longer function.

::::

## Configure list upload limits [adv-list-settings]

```yaml {applies_to}
stack:
```

You can set limits to the number of bytes and the buffer size used to upload [value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md) to {{elastic-sec}}.

To set the value:

1. Open [`kibana.yml`](/deploy-manage/stack-settings.md) [configuration file](kibana://reference/configuration-reference/general-settings.md) or edit your {{kib}} cloud instance.
2. Add any of these settings and their required values:

   - `xpack.lists.maxImportPayloadBytes`: Sets the number of bytes allowed for uploading {{elastic-sec}} value lists (default `9000000`, maximum `100000000`). For every 10 megabytes, it is recommended to have an additional 1 gigabyte of RAM reserved for Kibana.

     For example, on a Kibana instance with 2 gigabytes of RAM, you can set this value up to 20000000 (20 megabytes).

   - `xpack.lists.importBufferSize`: Sets the buffer size used for uploading {{elastic-sec}} value lists (default `1000`). Change the value if you’re experiencing slow upload speeds or larger than wanted memory usage when uploading value lists. Set to a higher value to increase throughput at the expense of using more Kibana memory, or a lower value to decrease throughput and reduce memory usage.
