---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
navigation_title: Using the UI
description: Step-by-step guide to create detection rules using the Kibana rule builder UI.
---

# Create a detection rule using the UI [security-rules-create]

Once the Detections feature is [turned on](/solutions/security/detect-and-alert/requirements-privileges.md), follow these steps to create a detection rule:

1. Define the [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md#rule-types). The configuration for this step varies depending on the rule type.
2. Configure [basic rule settings](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-ui-basic-params).
3. Configure [advanced rule settings](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-ui-advanced-params) (optional).
4. Set the [rule's schedule](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-schedule).
5. Set up [rule actions](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-notifications) (optional).
6. Set up [response actions](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-response-action) (optional).

::::{tip}
* At any step, you can preview the rule before saving it to see what kind of results you can expect.
* To ensure rules don't search cold and frozen data when executing, either configure the `excludedDataTiersForRuleExecution` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#exclude-cold-frozen-data-rule-executions) (which applies to all rules in a space), or add a [Query DSL filter](/solutions/security/detect-and-alert/set-rule-data-sources.md) to individual rules. These options are only available if you're on the {{stack}}.
::::

## Detection rule requirements

To create detection rules, you must have:

* At least `Read` access to {{data-source}}s, which requires the `Data View {{manage-app}}` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
* The required privileges to preview rules, manage rules, and manage alerts. Refer to [](/solutions/security/detect-and-alert/requirements-privileges.md) for more details.

::::{note}
Additional configuration is required for detection rules using {{ccs}}. Refer to [{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/advanced-data-source-configuration.md).
::::

## Rule type guides

Each rule type has its own configuration and query requirements. Refer to the appropriate guide for type-specific instructions:

* [Custom query](/solutions/security/detect-and-alert/custom-query.md)
* [Event correlation (EQL)](/solutions/security/detect-and-alert/eql.md)
* [Threshold](/solutions/security/detect-and-alert/threshold.md)
* [Indicator match](/solutions/security/detect-and-alert/indicator-match.md)
* [New terms](/solutions/security/detect-and-alert/new-terms.md)
* [{{esql}}](/solutions/security/detect-and-alert/esql.md)
* [{{ml-cap}}](/solutions/security/detect-and-alert/machine-learning.md)

To understand which type to use, refer to [Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md).

## Related pages

* [Rule settings reference](/solutions/security/detect-and-alert/rule-settings-reference.md): All shared rule settings, including severity, risk score, schedule, actions, and notification variables.
* [Using the API](/solutions/security/detect-and-alert/using-the-api.md): Create and manage rules programmatically.
* [Manage detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md): Enable, export, duplicate, and bulk-edit rules.
