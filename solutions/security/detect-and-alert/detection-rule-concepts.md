---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Understand key concepts that apply to all detection rules, including data sources, authorization, exceptions, and notifications.
---

# Detection rule concepts [detection-rule-concepts]

Before creating detection rules, familiarize yourself with the foundational concepts that apply across all rule types. Understanding these concepts helps you design effective rules and troubleshoot issues when they arise.

## Data sources [data-sources-concept]

Detection rules query data from {{es}} indices. When you create a rule (except for {{ml}} rules, which use anomaly jobs), you specify either:

* **Index patterns**: Wildcards like `logs-*` or `filebeat-*` that match one or more indices.
* **{{data-source-cap}}s**: Named references to index patterns that can include [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) for computed values at query time.

{{data-source-cap}}s are useful when you need consistent field definitions across multiple rules or want to add fields without reindexing data.

::::{note}
To use {{data-source}}s in {{stack}}, you must have the [required permissions](/explore-analyze/find-and-organize/data-views.md#data-views-read-only-access). In {{serverless-short}}, you must have the appropriate [predefined Security user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges.
::::

For guidance on configuring rule data sources, refer to [Set rule data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md).

::::{important}
System indices, such as the alert indices, contain important configuration and internal data. Do not change their mappings. Changes can lead to rule execution and alert indexing failures. Use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead to add fields to existing alert and event documents.
::::

## Rule authorization [rule-authorization-concept]

Rules execute using an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user who edited the rule. When you create or modify a rule, {{elastic-sec}} generates an API key that captures a snapshot of your current privileges. The rule uses this API key for all background tasks, including:

* Executing detection queries on the configured schedule
* Writing alerts to the alerts index
* Executing actions (sending notifications)

This authorization model means that rules continue to run with the privileges of their last editor, even when that user is not logged in.

::::{important}
If a user without the required privileges (such as index read access) updates a rule, the rule stops functioning. Ensure that only users with appropriate access edit rules. For required privileges, refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md).
::::

## Exceptions [exceptions-concept]

Exceptions prevent rules from generating alerts for specific conditions, even when the rule's query criteria are met. Use exceptions to:

* Exclude trusted processes, IP addresses, or user accounts
* Filter out known-benign activity specific to your environment
* Reduce alert noise without modifying the rule's query logic

Exceptions can be scoped to a [single rule](/solutions/security/detect-and-alert/add-manage-exceptions.md) or shared across multiple rules using [shared exception lists](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md). You can add exceptions to all rule types.

## Notifications and actions [notifications-concept]

Rules can trigger actions when they generate alerts. Actions send notifications or integrate with external systems through connectors. Common use cases include:

* Sending Slack or Microsoft Teams messages when high-severity alerts fire
* Creating tickets in {{jira}} or {{sn}} for analyst triage
* Triggering PagerDuty incidents for critical detections

You can configure actions to run for every alert, on a schedule, or when alerts meet specific conditions. Actions are configured in the rule's [Actions settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications).

::::{tip}
To temporarily stop notifications without disabling a rule, use [snooze](/solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions).
::::

## Related resources

* [Common rule settings](/solutions/security/detect-and-alert/common-rule-settings.md): Full reference for all rule configuration options
* [Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md): Compare rule types and find the best fit for your use case
* [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md): Required permissions for creating and managing rules
