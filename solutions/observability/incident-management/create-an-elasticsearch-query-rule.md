---
navigation_title: "Elasticsearch query"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-create-elasticsearch-query-rule.html
---



# Create an Elasticsearch query rule [observability-create-elasticsearch-query-rule]


::::{admonition} Required role
:class: note

The **Editor** role or higher is required to create Elasticsearch query rules. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

::::


The {{es}} query rule type runs a user-configured query, compares the number of matches to a configured threshold, and schedules actions to run when the threshold condition is met.

1. To access this page, from your project go to **Alerts**.
2. Click **Manage Rules** → **Create rule**.
3. Under **Select rule type**, select **{{es}} query**.

An {{es}} query rule can be defined using {{es}} Query Domain Specific Language (DSL), {{es}} Query Language (ES|QL), {{kib}} Query Language (KQL), or Lucene.


## Define the conditions [observability-create-elasticsearch-query-rule-define-the-conditions]

When you create an {{es}} query rule, your choice of query type affects the information you must provide. For example:

:::{image} ../../../images/serverless-alerting-rule-types-es-query-conditions.png
:alt: Define the condition to detect
:class: screenshot
:::

1. Define your query

    If you use [query DSL](../../../explore-analyze/query-filter/languages/querydsl.md), you must select an index and time field then provide your query. Only the `query`, `fields`, `_source` and `runtime_mappings` fields are used, other DSL fields are not considered. For example:

    ```sh
    {
      "query":{
        "match_all" : {}
      }
    }
    ```

    If you use [KQL](../../../explore-analyze/query-filter/languages/kql.md) or [Lucene](../../../explore-analyze/query-filter/languages/lucene-query-syntax.md), you must specify a data view then define a text-based query. For example, `http.request.referrer: "https://example.com"`.

    If you use [ES|QL](../../../explore-analyze/query-filter/languages/esql.md), you must provide a source command followed by an optional series of processing commands, separated by pipe characters (|). For example:

    ```sh
    FROM kibana_sample_data_logs
    | STATS total_bytes = SUM(bytes) BY host
    | WHERE total_bytes > 200000
    | SORT total_bytes DESC
    | LIMIT 10
    ```

2. If you use query DSL, KQL, or Lucene, set the group and theshold.

    When
    :   Specify how to calculate the value that is compared to the threshold. The value is calculated by aggregating a numeric field within the time window. The aggregation options are: `count`, `average`, `sum`, `min`, and `max`. When using `count` the document count is used and an aggregation field is not necessary.

    Over or Grouped Over
    :   Specify whether the aggregation is applied over all documents or split into groups using up to four grouping fields. If you choose to use grouping, it’s a [terms](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) or [multi terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-multi-terms-aggregation.html); an alert will be created for each unique set of values when it meets the condition. To limit the number of alerts on high cardinality fields, you must specify the number of groups to check against the threshold. Only the top groups are checked.

    Threshold
    :   Defines a threshold value and a comparison operator  (`is above`, `is above or equals`, `is below`, `is below or equals`, or `is between`). The value calculated by the aggregation is compared to this threshold.

3. Set the time window, which defines how far back to search for documents.
4. If you use query DSL, KQL, or Lucene, set the number of documents to send to the configured actions when the threshold condition is met.
5. If you use query DSL, KQL, or Lucene, choose whether to avoid alert duplication by excluding matches from the previous run. This option is not available when you use a grouping field.
6. Set the check interval, which defines how often to evaluate the rule conditions. Generally this value should be set to a value that is smaller than the time window, to avoid gaps in detection.


## Test your query [observability-create-elasticsearch-query-rule-test-your-query]

Use the **Test query** feature to verify that your query is valid.

If you use query DSL, KQL, or Lucene, the query runs against the selected indices using the configured time window. The number of documents that match the query is displayed. For example:

:::{image} ../../../images/serverless-alerting-rule-types-es-query-valid.png
:alt: Test {{es}} query returns number of matches when valid
:class: screenshot
:::

If you use an ES|QL query, a table is displayed. For example:

:::{image} ../../../images/serverless-alerting-rule-types-esql-query-valid.png
:alt: Test ES|QL query returns a table when valid
:class: screenshot
:::

If the query is not valid, an error occurs.


## Add actions [observability-create-elasticsearch-query-rule-add-actions]

You can optionally send notifications when the rule conditions are met and when they are no longer met. In particular, this rule type supports:

* alert summaries
* actions that run when the query is matched
* recovery actions that run when the rule conditions are no longer met

For each action, you must choose a connector, which provides connection information for a service or third party integration.

:::::{dropdown} Connector types
Connectors provide a central place to store connection information for services and integrations with third party systems. The following connectors are available when defining actions for alerting rules:

* [Cases](https://www.elastic.co/guide/en/kibana/current/cases-action-type.html)
* [D3 Security](https://www.elastic.co/guide/en/kibana/current/d3security-action-type.html)
* [Email](https://www.elastic.co/guide/en/kibana/current/email-action-type.html)
* [{{ibm-r}}](https://www.elastic.co/guide/en/kibana/current/resilient-action-type.html)
* [Index](https://www.elastic.co/guide/en/kibana/current/index-action-type.html)
* [Jira](https://www.elastic.co/guide/en/kibana/current/jira-action-type.html)
* [Microsoft Teams](https://www.elastic.co/guide/en/kibana/current/teams-action-type.html)
* [Observability AI Assistant](https://www.elastic.co/guide/en/kibana/current/obs-ai-assistant-action-type.html)
* [{{opsgenie}}](https://www.elastic.co/guide/en/kibana/current/opsgenie-action-type.html)
* [PagerDuty](https://www.elastic.co/guide/en/kibana/current/pagerduty-action-type.html)
* [Server log](https://www.elastic.co/guide/en/kibana/current/server-log-action-type.html)
* [{{sn-itom}}](https://www.elastic.co/guide/en/kibana/current/servicenow-itom-action-type.html)
* [{{sn-itsm}}](https://www.elastic.co/guide/en/kibana/current/servicenow-action-type.html)
* [{{sn-sir}}](https://www.elastic.co/guide/en/kibana/current/servicenow-sir-action-type.html)
* [Slack](https://www.elastic.co/guide/en/kibana/current/slack-action-type.html)
* [{{swimlane}}](https://www.elastic.co/guide/en/kibana/current/swimlane-action-type.html)
* [Torq](https://www.elastic.co/guide/en/kibana/current/torq-action-type.html)
* [{{webhook}}](https://www.elastic.co/guide/en/kibana/current/webhook-action-type.html)
* [xMatters](https://www.elastic.co/guide/en/kibana/current/xmatters-action-type.html)

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).

::::


For more information on creating connectors, refer to [Connectors](../../../deploy-manage/manage-connectors.md).

:::::


:::::{dropdown} Action frequency
After you select a connector, you must set the action frequency. You can choose to create a **Summary of alerts** on each check interval or on a custom interval. For example, you can send email notifications that summarize the new, ongoing, and recovered alerts at a custom interval:

:::{image} ../../../images/serverless-alerting-es-query-rule-action-summary.png
:alt: UI for defining alert summary action in an {{es}} query rule
:class: screenshot
:::

Alternatively, you can set the action frequency to **For each alert** and specify the conditions each alert must meet for the action to run.

With the **Run when** menu you can choose how often the action runs (at each check interval, only when the alert status changes, or at a custom action interval). You must also choose an action group, which indicates whether the action runs when the query is matched or when the alert is recovered. Each connector supports a specific set of actions for each action group. For example:

:::{image} ../../../images/serverless-alerting-es-query-rule-action-query-matched.png
:alt: UI for defining a recovery action
:class: screenshot
:::

You can further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame.

:::::


:::::{dropdown} Action variables
Use the default notification message or customize it. You can add more context to the message by clicking the Add variable icon ![Add variable](../../../images/serverless-indexOpen.svg "") and selecting from a list of available variables.

:::{image} ../../../images/serverless-action-variables-popup.png
:alt: Action variables list
:class: screenshot
:::

The following variables are specific to this rule type. You can also specify [variables common to all rules](../../../explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.conditions`
:   A string that describes the threshold condition. Example: `count greater than 4`.

`context.date`
:   The date, in ISO format, that the rule met the condition. Example: `2022-02-03T20:29:27.732Z`.

`context.hits`
:   The most recent documents that matched the query. Using the [Mustache](https://mustache.github.io/) template array syntax, you can iterate over these hits to get values from the {{es}} documents into your actions.

    For example, the message in an email connector action might contain:

    ```txt
    Elasticsearch query rule '{{rule.name}}' is active:

    {{#context.hits}}
    Document with {{_id}} and hostname {{_source.host.name}} has
    {{_source.system.memory.actual.free}} bytes of memory free
    {{/context.hits}}
    ```

    The documents returned by `context.hits` include the [`_source`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html) field. If the {{es}} query search API’s [`fields`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-param) parameter is used, documents will also return the `fields` field, which can be used to access any runtime fields defined by the [`runtime_mappings`](../../../manage-data/data-store/mapping/define-runtime-fields-in-search-request.md) parameter. For example:

    ```txt
    {{#context.hits}}
    timestamp: {{_source.@timestamp}}
    day of the week: {{fields.day_of_week}} <1>
    {{/context.hits}}
    ```

    1. The `fields` parameter here is used to access the `day_of_week` runtime field.


    As the [`fields`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-response) response always returns an array of values for each field, the [Mustache](https://mustache.github.io/) template array syntax is used to iterate over these values in your actions. For example:

    ```txt
    {{#context.hits}}
    Labels:
    {{#fields.labels}}
    - {{.}}
    {{/fields.labels}}
    {{/context.hits}}
    ```


`context.link`
:   Link to Discover and show the records that triggered the alert.

`context.message`
:   A message for the alert. Example: `rule 'my es-query' is active:` `- Value: 2` `- Conditions Met: Number of matching documents is greater than 1 over 5m` `- Timestamp: 2022-02-03T20:29:27.732Z`

`context.title`
:   A title for the alert. Example: `rule term match alert query matched`.

`context.value`
:   The value that met the threshold condition.

:::::



## Handling multiple matches of the same document [observability-create-elasticsearch-query-rule-handling-multiple-matches-of-the-same-document]

By default, **Exclude matches from previous run** is turned on and the rule checks for duplication of document matches across multiple runs. If you configure the rule with a schedule interval smaller than the time window and a document matches a query in multiple runs, it is alerted on only once.

The rule uses the timestamp of the matches to avoid alerting on the same match multiple times. The timestamp of the latest match is used for evaluating the rule conditions when the rule runs. Only matches between the latest timestamp from the previous run and the current run are considered.

Suppose you have a rule configured to run every minute. The rule uses a time window of 1 hour and checks if there are more than 99 matches for the query. The {{es}} query rule type does the following:

|  |  |  |
| --- | --- | --- |
| `Run 1 (0:00)` | Rule finds 113 matches in the last hour: `113 > 99` | Rule is active and user is alerted. |
| `Run 2 (0:01)` | Rule finds 127 matches in the last hour. 105 of the matches are duplicates that were already alerted on previously, so you actually have 22 matches: `22 !> 99` | No alert. |
| `Run 3 (0:02)` | Rule finds 159 matches in the last hour. 88 of the matches are duplicates that were already alerted on previously, so you actually have 71 matches: `71 !> 99` | No alert. |
| `Run 4 (0:03)` | Rule finds 190 matches in the last hour. 71 of them are duplicates that were already alerted on previously, so you actually have 119 matches: `119 > 99` | Rule is active and user is alerted. |
