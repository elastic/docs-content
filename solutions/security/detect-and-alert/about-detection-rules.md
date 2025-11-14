---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/about-rules.html
  - https://www.elastic.co/guide/en/serverless/current/security-about-rules.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# About detection rules [security-about-rules]

Rules run periodically and search for source events, matches, sequences, or {{ml}} job anomaly results that meet their criteria. When a rule’s criteria are met, a detection alert is created.


## Rule types [rule-types]

You can create the following types of rules:

* [**Custom query**](/solutions/security/detect-and-alert/create-detection-rule.md#create-custom-rule): Query-based rule, which searches the defined indices and creates an alert when one or more documents match the rule’s query.
* [**Machine learning**](/solutions/security/detect-and-alert/create-detection-rule.md#create-ml-rule): {{ml-cap}} rule, which creates an alert when a {{ml}} job discovers an anomaly above the defined threshold (see [Anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md)).

    For {{ml}} rules, the associated {{ml}} job must be running. If the {{ml}} job isn’t running, the rule will:

    * Run and create alerts if existing anomaly results with scores above the defined threshold are discovered.
    * Issue an error stating the {{ml}} job was not running when the rule executed.

* [**Threshold**](/solutions/security/detect-and-alert/create-detection-rule.md#create-threshold-rule): Searches the defined indices and creates a detections alert when the number of times the specified field’s value is present and meets the threshold during a single execution. When multiple values meet the threshold, an alert is generated for each value.

    For example, if the threshold `field` is `source.ip` and its `value` is `10`, an alert is generated for every source IP address that appears in at least 10 of the rule’s search results.

* [**Event correlation**](/solutions/security/detect-and-alert/create-detection-rule.md#create-eql-rule): Searches the defined indices and creates an alert when results match an [Event Query Language (EQL)](/explore-analyze/query-filter/languages/eql.md) query.
* [**Indicator match**](/solutions/security/detect-and-alert/rule-types/indicator-match.md): Creates an alert when {{elastic-sec}} index field values match field values defined in the specified indicator index patterns. For example, you can create an indicator index for IP addresses and use this index to create an alert whenever an event’s `destination.ip` equals a value in the index. Indicator index field mappings should be [ECS-compliant](ecs://reference/index.md). For information on creating {{es}} indices and field types, see [Index some documents](/manage-data/ingest.md), [Create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create), and [Field data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). If you have indicators in a standard file format, such as CSV or JSON, you can also use the Machine Learning Data Visualizer to import your indicators into an indicator index. See [Explore the data in {{kib}}](/explore-analyze/machine-learning/anomaly-detection/ml-getting-started.md#sample-data-visualizer) and use the **Import Data** option to import your indicators.

    ::::{tip}
    You can also use value lists as the indicator match index. See [Use value lists with indicator match rules](solutions/security/detect-and-alert/rule-types/indicator-match.md#indicator-value-lists)  at the end of this topic for more information.
    ::::

* [**New terms**](/solutions/security/detect-and-alert/create-detection-rule.md#create-new-terms-rule): Generates an alert for each new term detected in source documents within a specified time range. You can also detect a combination of up to three new terms (for example, a `host.ip` and `host.id` that have never been observed together before).
* [**ES|QL**](/solutions/security/detect-and-alert/create-detection-rule.md#create-esql-rule): Searches the defined indices and creates an alert when results match an [Elasticsearch Query Language {{esql}}](elasticsearch://reference/query-languages/esql.md) query.

    ::::{note}
    {{esql}} is enabled by default in {{kib}}. It can be disabled using the `enableESQL` setting from the [Advanced Settings](kibana://reference/advanced-settings.md). This will hide the {{esql}} user interface from various applications. However, users will be able to access existing {{esql}} artifacts like saved searches and visualizations.
    ::::


:::{image} /solutions/images/security-all-rules.png
:alt: Shows the Rules page
:screenshot:
:::


## Data views and index patterns [views-index-patterns]

When you create a rule, you must either specify the {{es}} index pattens for which you’d like the rule to run, or select a [data view field](/solutions/security/get-started/data-views-elastic-security.md) as the data source. If you select a data view, you can select [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) associated with that data view to create a query for the rule (with the exception of {{ml}} rules, which do not use queries).

::::{note}
To access data views in {{stack}}, you must have the [required permissions](/explore-analyze/find-and-organize/data-views.md#data-views-read-only-access). To access them in {{serverless-short}}, you must have the appropriate [predefined Security user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges.
::::

::::{important}

System indices, such as the alert indices, contain important configuration and internal data; do not change their mappings. Changes can lead to rule execution and alert indexing failures. Use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) instead, which allow you to add fields to existing alert and event documents.

::::


## Notifications [about-notifications]

For both prebuilt and custom rules, you can send notifications when alerts are created. Notifications can be sent via {{jira}}, Microsoft Teams, PagerDuty, Slack, and others, and can be configured when you create or edit a rule.


## Authorization [alerting-authorization-model]

Rules, including all background detection and the actions they generate, are authorized using an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) associated with the last user to edit the rule. Upon creating or modifying a rule, an API key is generated for that user, capturing a snapshot of their privileges. The API key is then used to run all background tasks associated with the rule including detection checks and executing actions.

::::{important}
If a rule requires certain privileges to run, such as index privileges, keep in mind that if a user without those privileges updates the rule, the rule will no longer function.

::::



## Exceptions [about-exceptions]

When modifying rules or managing detection alerts, you can [add exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md) that prevent a rule from generating alerts even when its criteria are met. This is useful for reducing noise, such as preventing alerts from trusted processes and internal IP addresses.

::::{note}
You can add exceptions to custom query, machine learning, event correlation, and indicator match rule types.
::::


