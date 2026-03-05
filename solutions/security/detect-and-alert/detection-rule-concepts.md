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

## How detection rules work

A detection rule consists of three parts:

| Part | Purpose |
|------|---------|
| Query | Specifies the threat behavior or pattern to detect. The query searches your [data sources](#data-sources-concept) using syntax that varies by [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) (KQL, EQL, {{ml}} anomaly scores, or threat indicator matches). |
| Schedule | Controls when and how often the rule checks for matching events. Rules execute at intervals you define (for example, every 5 minutes) and look back over a configurable time window. |
| Rule actions | Specifies what happens when the rule detects a match. You can [send notifications](#notifications-concept), create tickets, or trigger integrations with external systems. |

These three parts work together when a rule runs:

1. At each scheduled interval, the rule runs its query against your data sources.
2. The rule creates alerts for events that match the query (unless [exceptions](#exceptions-concept) apply).
3. Configured rule actions notify your team or trigger external integrations.

Behind the scenes, rules execute using the [authorization](#rule-authorization-concept) of the user who last edited them.

## Data sources [data-sources-concept]

A rule's query runs against the data sources you configure. When you create a rule (except for {{ml}} rules, which use anomaly jobs), you specify either:

* **Index patterns**: Wildcards like `logs-*` or `filebeat-*` that match one or more indices.
* **{{data-source-cap}}s**: Named references to index patterns that can include [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) for computed values at query time.

{{data-source-cap}}s are useful when you need consistent field definitions across multiple rules or want to add fields without reindexing data. For guidance on configuring rule data sources, refer to [Set rule data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md).

::::{note}
To use {{data-source}}s in {{stack}}, you must have the [required permissions](/explore-analyze/find-and-organize/data-views.md#data-views-read-only-access). In {{serverless-short}}, you must have the appropriate [predefined Security user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges.
::::

::::{important}
System indices, such as the alert indices, contain important configuration and internal data. Do not change their mappings. Changes can lead to rule execution and alert indexing failures. Use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead to add fields to existing alert and event documents.
::::

## Exceptions [exceptions-concept]

Exceptions refine a rule's query by excluding specific conditions from generating alerts—even when the query criteria are met. Use exceptions to:

* Exclude trusted processes, IP addresses, or user accounts
* Filter out known-benign activity specific to your environment
* Reduce alert noise without modifying the rule's query logic

Exceptions can be scoped to a [single rule](/solutions/security/detect-and-alert/add-manage-exceptions.md) or shared across multiple rules using [shared exception lists](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md). You can add exceptions to all rule types.

## Rule actions and notifications [notifications-concept]

Rule actions are automated responses that a rule triggers when it generates alerts. Each action uses a connector to send data to an external service. Common action types include:

* Sending notifications (Slack messages, emails, PagerDuty alerts) to inform your team in real time

   :::{note}
   Notifications are a specific type of action focused on alerting people. They're how rules communicate that something needs attention.
   :::

* Creating tickets in {{jira}} or {{sn}} for tracking and triage
* Triggering webhooks or custom integrations for automated workflows

You can configure rule actions to run for every alert, at scheduled intervals, or only when alerts meet specific conditions (such as high severity). Rule actions are configured in the **Actions** tab of the rule settings. For details, refer to [Rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications).

## Rule authorization [rule-authorization-concept]

```{applies_to}
stack: ga
serverless: ga

Rules run in the background using the privileges of the user who last edited them. When you create or modify a rule, {{elastic-sec}} generates an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) that captures a snapshot of your current privileges. The rule uses this API key to:

* Execute detection queries against the configured data sources
* Write alerts to the alerts index
* Execute actions (send notifications)

This means rules continue running with their editor's privileges, even when that user is not logged in.

::::{important}
If a user without the required privileges (such as index read access) updates a rule, the rule stops functioning. Ensure that only users with appropriate access edit rules. For required privileges, refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md).
::::

## Key terms quick reference

**Rule actions**
:   Automated responses a rule triggers when it generates alerts. Rule actions use connectors to send data to external services.

**Alerts**
:   Records created when a rule's query finds matching events. Each alert represents a potential threat for analysts to investigate.

**API key**
:   A credential that captures the privileges of the user who last edited a rule. Rules use API keys to execute queries and write alerts.

**Connectors**
:   Integrations that connect actions to external services like Slack, {{jira}}, or PagerDuty.

**Data sources**
:   The {{es}} indices or data views that a rule's query searches. Configured using index patterns or {{data-source}}s.

**{{data-source-cap}}s**
:   Named references to index patterns that can include runtime fields. Useful for consistent field definitions across rules.

**Exceptions**
:   Conditions that prevent a rule from generating alerts, even when query criteria are met. Used to exclude trusted activity.

**Index patterns**
:   Wildcards (like `logs-*`) that match one or more {{es}} indices.

**Notifications**
:   A type of action that alerts people to something needing attention (Slack messages, emails, PagerDuty alerts).

**Query**
:   The logic that defines what threat behavior or pattern a rule detects. Syntax varies by rule type.

**Rule authorization**
:   The privilege model that determines what a rule can access. Rules execute using an API key tied to the user who last edited them.

**Rule type**
:   The detection method a rule uses (custom query, EQL, threshold, indicator match, new terms, {{esql}}, or {{ml}}).

**Schedule**
:   How often a rule runs and how far back it looks for matching events.

## Related resources

* [Common rule settings](/solutions/security/detect-and-alert/common-rule-settings.md): Full reference for all rule configuration options
* [Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md): Compare rule types and find the best fit for your use case
* [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md): Required permissions for creating and managing rules
