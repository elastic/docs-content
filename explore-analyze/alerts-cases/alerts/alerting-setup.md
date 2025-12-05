---
navigation_title: Set up
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/alerting-setup.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Configuration instructions for setting up alerting, including prerequisites and production considerations.
---

# Set up alerting [alerting-setup]

{{kib}} {{alert-features}} are automatically enabled but might require additional configuration for encryption keys, email settings, and production deployments. This page covers prerequisites, required settings, and production considerations for running alerting at scale.

## Prerequisites [alerting-prerequisites]

If you are using an **on-premises** {{stack}} deployment:

* In the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file, add the [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/alerting-settings.md#general-alert-action-settings) setting.
* For emails to have a footer with a link back to {{kib}}, set the [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) configuration setting.

If you are using an **on-premises** {{stack}} deployment with [**security**](../../../deploy-manage/security.md):

* If you are unable to access {{kib}} {{alert-features}}, ensure that you have not [explicitly disabled API keys](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#api-key-service-settings).

The alerting framework uses queries that require the `search.allow_expensive_queries` setting to be `true`. See the scripts [documentation](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-query.md#_allow_expensive_queries_4).

## Production considerations and scaling guidance [alerting-setup-production]

When relying on alerting and actions as mission critical services, make sure you follow the [alerting production considerations](../../../deploy-manage/production-guidance/kibana-alerting-production-considerations.md).

For more information on the scalability of {{alert-features}}, go to [Scaling guidance](../../../deploy-manage/production-guidance/kibana-alerting-production-considerations.md#alerting-scaling-guidance).

## Security [alerting-security]

To use {{alert-features}} in a {{kib}} app, you must have the appropriate feature privileges:

### Give full access to manage alerts, connectors, and rules in **{{stack-manage-app}}** [_give_full_access_to_manage_alerts_connectors_and_rules_in_stack_manage_app]

**{{kib}} privileges**

* `All` for the **Management > {{stack-rules-feature}}** feature.
* `All` for the **Management > Rules Settings** feature.
* `All` for the **Management > {{connectors-feature}}** feature.

::::{note}
The **{{connectors-feature}}** feature privilege is required to manage connectors. To add rule actions and test connectors, you require only `Read` privileges. By default, `All` privileges include authority to run {{endpoint-sec}} connectors (such as SentinelOne and CrowdStrike) unless you customize the sub-feature privileges.

Likewise, you can customize the **Rules Settings** sub-feature privileges related to flapping detection settings.

To create a rule that uses the [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md), you must also have `All` privileges for the **Cases** feature.

The rule type also affects the privileges that are required to create and edit rules. For example:
* For {{ml}} rules, you must have `all` privileges for the **Analytics > {{ml-app}}** feature.
* For {{stack-monitor-app}} rules, you must have the `monitoring_user` role.
* For most {{observability}} rules, you must have `all` privileges for the appropriate {{observability}} features. However, for a custom threshold rule, you only need the `stack alerts` privilege.
* For Security rules, refer to [Detections prerequisites and requirements](../../../solutions/security/detect-and-alert/detections-requirements.md).

::::

### Give view-only access to alerts, connectors, and rules in  **{{stack-manage-app}}** [_give_view_only_access_to_alerts_connectors_and_rules_in_stack_manage_app]

**{{kib}} privileges**

* `Read` for the **Management > {{stack-rules-feature}}** feature.
* `Read` for the **Management > Rules Settings** feature.
* `Read` for the **Management > {{connectors-feature}}** feature.

::::{note}
The rule type also affects the privileges that are required. For example, to view {{ml}} rules, you must have `read` privileges for the **Analytics > {{ml-app}}** feature. For {{stack-monitor-app}} rules, you must have the `monitoring_user` role. For {{observability}} rules, you must have `read` privileges for the appropriate {{observability}} features. For Security rules, refer to [Detections prerequisites and requirements](../../../solutions/security/detect-and-alert/detections-requirements.md).

::::

### Give view-only access to alerts in **Discover** or **Dashboards** [_give_view_only_access_to_alerts_in_discover_or_dashboards]

**{{kib}} privileges**

* `Read` index privileges for the `.alerts-*` system indices.

### Revoke all access to alerts, connectors, and rules in **{{stack-manage-app}}**, **Discover**, or **Dashboards** [_revoke_all_access_to_alerts_connectors_and_rules_in_stack_manage_app_discover_or_dashboards]

**{{kib}} privileges**

* `None` for the **Management > {{stack-rules-feature}}** feature.
* `None` for the **Management > Rules Settings** feature.
* `None` for the **Management > {{connectors-feature}}** feature.
* No index privileges for the `.alerts-*` system indices.

### More details [_more_details]

For more information on configuring roles that provide access to features, go to [Feature privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges).

### API keys [alerting-authorization]

Rules are authorized using an API key. Its credentials are used to run all background tasks associated with the rule, including condition checks like {{es}} queries and triggered actions.

When you create a rule in {{kib}}, an API key is created that captures a snapshot of your privileges. Likewise when you update a rule, the API key is updated with a snapshot of your privileges at the time of the edit.

When you disable a rule, it retains the associated API key which is reused when the rule is enabled. If the API key is missing when you enable the rule, a new key is generated that has your current security privileges. When you import a rule, you must enable it before you can use it and a new API key is generated at that time.

You can generate a new API key at any time in **{{stack-manage-app}} > {{rules-ui}}** or in the rule details page by selecting **Update API key** in the actions menu.

If you manage your rules by using {{kib}} APIs, they support support both key- and token-based authentication as described in [Authentication](https://www.elastic.co/docs/api/doc/kibana/authentication). To use key-based authentication, create API keys and use them in the header of your API calls as described in [API Keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md). To use token-based authentication, provide a username and password; an API key that matches the current privileges of the user is created automatically. In both cases, the API key is subsequently associated with the rule and used when it runs.

::::{important}
If a rule requires certain privileges, such as index privileges, to run and a user without those privileges updates the rule, the rule will no longer function. Conversely, if a user with greater or administrator privileges modifies the rule, it will begin running with increased privileges. The same behavior occurs when you change the API key in the header of your API calls.

::::

### Restrict actions [alerting-restricting-actions]

For security reasons you may wish to limit the extent to which {{kib}} can connect to external services. You can use [Action settings](kibana://reference/configuration-reference/alerting-settings.md#action-settings) to disable certain [*Connectors*](../../../deploy-manage/manage-connectors.md) and allowlist the hostnames that {{kib}} can connect with.

## Space isolation [alerting-spaces]

Rules and connectors are isolated to the {{kib}} space in which they were created. A rule or connector created in one space will not be visible in another.

## {{ccs-cap}} [alerting-ccs-setup]

If you want to use alerting rules with {{ccs}}, you must configure privileges for {{ccs-init}} and {{kib}}. Refer to [Remote clusters](../../../deploy-manage/remote-clusters.md).
