---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/detections-permissions-section.html
  - https://www.elastic.co/guide/en/serverless/current/security-detections-requirements.html
---


% Used the Serverless content for this page

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/security-docs/security/detections-permissions-section.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-detections-requirements.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$enable-detections-ui$$$

$$$adv-list-settings$$$

$$$detections-on-prem-requirements$$$

# Detections requirements [security-detections-requirements]

To use the [Detections feature](../detect-and-alert.md), you first need to configure a few settings. You also need the appropriate role to send [notifications](create-detection-rule.md) when detection alerts are generated.

Additionally, there are some [advanced settings]() used to configure [value list](create-manage-value-lists.md) upload limits.


## Enable and access detections [enable-detections-ui]

To use the Detections feature, it must be enabled and you must have either the appropriate [predefined Security user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with privileges to access rules and alerts. If your role doesn’t have the privileges needed to enable this feature, you can request someone who has these privileges to visit your {{kib}} space, which will turn it on for you.

::::{note}
For instructions about using {{ml}} jobs and rules, refer to [Machine learning job and rule requirements](../advanced-entity-analytics/machine-learning-job-rule-requirements.md).

::::



### Custom role privileges [security-detections-requirements-custom-role-privileges]

The following table describes the required custom role privileges to access the Detections feature, including rules and alerts. For more information on {{kib}} privileges, refer to [Custom roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md).

| Action | Cluster Privilege | Index Privileges | {{kib}} Privileges |
| --- | --- | --- | --- |
| Enable detections in your space | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>* `.alerts-security.alerts-<space-id>`<br>* `.lists-<space-id>`<br>* `.items-<space-id>`<br> | `All` for the `Security` feature |
| Enable detections in all spaces<br><br>**NOTE:** To turn on detections, visit the Rules and Alerts pages for each space.<br> | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams:<br><br>* `.alerts-security.alerts-<space-id>`<br>* `.lists-<space-id>`<br>* `.items-<space-id>`<br> | `All` for the `Security` feature |
| Preview rules | N/A | `read` for these indices:<br><br>* `.preview.alerts-security.alerts-<space-id>`<br>* `.internal.preview.alerts-security.alerts-<space-id>-*`<br> | `All` for the `Security` feature |
| Manage rules | N/A | `manage`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>* `.alerts-security.alerts-<space-id`<br>* `.lists-<space-id>`<br>* `.items-<space-id>`<br> | `All` for the `Security` feature<br><br>**NOTE:** You need additional `Action and Connectors` feature privileges (**Management → Action and Connectors**) to manage rules with actions and connectors:<br><br>* To provide full access to rule actions and connectors, give your role `All` privileges. With `Read` privileges, you can edit rule actions, but will have limited capabilities to manage connectors. For example, `Read` privileges allow you to add or remove an existing connector from a rule, but does not allow you to create a new connector.<br>* To import rules with actions, you need at least `Read` privileges for the `Action and Connectors` feature. To overwrite or add new connectors, you need `All` privileges for the `Actions and Connectors` feature. To import rules without actions,  you don’t need `Actions and Connectors` privileges.<br> |
| Manage alerts<br><br>**NOTE**: Allows you to manage alerts, but not modify rules.<br> | N/A | `maintenance`, `write`, `read`, and `view_index_metadata` for these system indices and data streams, where `<space-id>` is the space name:<br><br>* `.alerts-security.alerts-<space-id>`<br>* `.internal.alerts-security.alerts-<space-id>-*`<br>* `.lists-<space-id>`<br>* `.items-<space-id>`<br> | `Read` for the `Security` feature |
| Create the `.lists` and `.items` data streams in your space<br><br>**NOTE**: To initiate the process that creates the data streams, you must visit the Rules page for each appropriate space.<br> | `manage` | `manage`, `write`, `read`, and `view_index_metadata` for these data streams, where `<space-id>` is the space name:<br><br>* `.lists-<space-id>`<br>* `.items-<space-id>`<br> | `All` for the `Security` and `Saved Objects Management` features |


### Authorization [alerting-auth-model]

Rules, including all background detection and the actions they generate, are authorized using an [API key](../../../deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user to edit the rule. Upon creating or modifying a rule, an API key is generated for that user, capturing a snapshot of their privileges. The API key is then used to run all background tasks associated with the rule including detection checks and executing actions.

::::{important}
If a rule requires certain privileges to run, such as index privileges, keep in mind that if a user without those privileges updates the rule, the rule will no longer function.

::::
