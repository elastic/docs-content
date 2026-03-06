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

Once the Detections feature is [turned on](/solutions/security/detect-and-alert/turn-on-detections.md), follow these steps to create a detection rule:

::::{tip}
At any step, you can preview the rule before saving it to see what kind of results you can expect.
::::

1. Define the [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md#rule-types). The configuration for this step varies depending on the rule type.
2. Configure [basic rule settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-basic-params).
3. Configure [advanced rule settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) (optional).
4. Set the [rule's schedule](/solutions/security/detect-and-alert/common-rule-settings.md#rule-schedule).
5. (Optional) Set up [rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications).
6. (Optional) Set up [response actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-response-action).
7. Create and enable the rule, or create the rule without enabling it. 

:::{admonition} Create rules programmatically
If you prefer to create rules programmatically instead of using the UI, refer to [Using the API](/solutions/security/detect-and-alert/using-the-api.md).
:::

::::{important}

Rules run in the background using the privileges of the user who last edited them. When you create or modify a rule, {{elastic-sec}} generates an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) that captures a snapshot of your current privileges. If a user without the required privileges (such as index read access) updates a rule, the rule can stop functioning correctly and no longer generate alerts. To fix this, a user with the right privileges to either modify the rule or update the API key. To learn more, refer to [](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept).

::::

## Detection rule requirements

To create detection rules, you must have:

* At least `Read` access to {{data-source}}s, which requires the `Data View {{manage-app}}` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
* The required privileges to preview rules, manage rules, and manage alerts. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md) for more details.

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

## Next steps

After creating the rule, you can change its settings, enable or disable it, and more. Refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) for more information.