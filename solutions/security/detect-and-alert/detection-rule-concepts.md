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

At a high level, a detection rule can be broken down into three parts:

| Part | Purpose |
|------|---------|
| Query | Specifies the threat behavior or pattern to detect. The query searches your [data sources](#data-sources-concept) using syntax that varies by [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) (for example, {{esql}}, KQL, or EQL). |
| Schedule | Controls how often the rule runs and how far back it searches. The interval you set determines both. For example, a rule with a 5-minute interval runs every 5 minutes and searches the last 5 minutes of data each time. An optional look-back setting extends the search window to help catch late-arriving events. |
| Rule actions | Specifies what happens when the rule detects a match. You can [send notifications](#notifications-concept), create tickets, or trigger actions on external systems. |

These three parts work together when a rule runs:

1. At each scheduled interval, the rule runs its query against your data sources.
2. The rule creates alerts for events that match the query (unless [exceptions](#exceptions-concept) apply).
3. Configured rule actions notify your team or trigger actions on external systems.

Behind the scenes, rules execute using the [authorization](#rule-authorization-concept) of the user who last edited them.

## Data sources [data-sources-concept]

A rule's query runs against the data sources you configure. When you create a rule (except for {{ml}} rules, which use anomaly jobs), you specify either:

* **Index patterns**: Wildcards like `logs-*` or `filebeat-*` that match one or more indices.
* **{{data-source-cap}}s**: Named references to index patterns that can include [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) for computed values at query time.

{{data-source-cap}}s are useful when you need consistent field definitions across multiple rules or want to add fields without reindexing data. {{esql}} rules do not support {{data-source}}s—specify source indices directly in the query's `FROM` command, using index patterns or [aliases](/manage-data/data-store/aliases.md).

For guidance on configuring rule data sources, refer to [Set rule data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md).

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

Rule actions are automated responses that a rule triggers when it generates alerts. You can configure rule actions to run for every alert, at scheduled intervals, or only when alerts meet specific conditions (such as high severity). Rule actions are configured in the **Actions** tab of the rule settings. For details, refer to [Rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications).


Rule actions fall into two categories: external and system actions.

### External actions

External actions use connectors to:

* Send notifications (Slack messages, emails, PagerDuty alerts) to inform your team in real time
* Create tickets in {{jira}} or {{sn}} for tracking and triage
* Trigger webhooks or custom integrations

### System actions

System actions operate within {{kib}} to:

* Create or update cases automatically
* Add entries to indices for tracking or enrichment
* Trigger [workflows](/explore-analyze/workflows.md) for more complex automation

## Rule authorization [rule-authorization-concept]

```{applies_to}
stack: ga
serverless: ga
```

{{kib}} uses an API key to authorize rule execution each time a rule runs. The key is used to:

* Execute detection queries against the configured data sources
* Write alerts to the alerts index
* Execute actions (send notifications)

On Stack deployments, {{elastic-sec}} generates an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) when you create or modify a rule. The key captures a snapshot of your current privileges, and ownership transfers to whoever last edited the rule. This means rules continue running with their editor's privileges, even when that user is not logged in.

In {{serverless-full}} projects, rules use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md). Refer to [Rules and {{ecloud}} API keys in {{serverless-short}}](/explore-analyze/alerting/alerts/rules-and-elastic-cloud-api-keys.md) for details on how this key type affects rule access and behavior.

### Impact of insufficient user privileges [rule-privilege-impact]

When a user without the [appropriate privileges](/solutions/security/detect-and-alert/detections-privileges.md) edits a rule, the rule can stop functioning correctly and no longer generate alerts. A user with the appropriate privileges must edit and save the rule to regenerate the API key with their credentials and restore access. On {{stack}} deployments, you can also [update the API key directly](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md#update-api-key) without changing the rule configuration.

## Key terms quick reference

**Rule actions**
:   Automated responses a rule triggers when it generates alerts. Rule actions can send data to external services using connectors, or perform operations within {{kib}} such as creating cases or triggering workflows.

**Alerts**
:   Records created when a rule's query finds matching events. Each alert represents a potential threat for analysts to investigate.

**API key**
:   A credential that rules use to execute queries and write alerts. The key type and ownership model depends on your deployment. Refer to [Elasticsearch API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md) and [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md) for details.

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
:   A type of action that signals something needs attention (Slack messages, emails, PagerDuty alerts).

**Query**
:   The logic that defines what threat behavior or pattern a rule detects. Syntax varies by rule type.

**Rule authorization**
:   The privilege model that determines what a rule can access. Refer to [Rule authorization](#rule-authorization-concept) for more details.

**Rule type**
:   The detection method a rule uses (custom query, EQL, threshold, indicator match, new terms, {{esql}}, or {{ml}}).

**Schedule**
:   How often a rule runs and how far back it looks for matching events.

## Related resources

* [Common rule settings](/solutions/security/detect-and-alert/common-rule-settings.md): Full reference for all rule configuration options
* [Select the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md): Compare rule types and find the best fit for your use case
* [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md): Required permissions for creating and managing rules
