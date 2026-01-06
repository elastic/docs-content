---
navigation_title: Log threshold
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-threshold-alert.html
applies_to:
  stack: ga
products:
  - id: observability
---



# Create a log threshold rule [logs-threshold-alert]


:::{image} /solutions/images/observability-log-threshold-alert.png
:alt: Log threshold alert configuration
:screenshot:
:::


## Fields and comparators [fields-comparators-logs]

The comparators available for conditions depend on the chosen field. The combinations available are:

* Numeric fields: **more than**, **more than or equals**, **less than**, or **less than or equals**.
* Aggregatable fields: **is** or **is not**.
* Non-aggregatable fields: **matches**, **does not match**, **matches phrase**, **does not match phrase**.

    * **Matches** queries some or all of the contents of your entered value regardless of order. For example, `WITH message MATCHES your example message` looks for messages containing the words `your` and `example` and `message` and returns results with some or all of those words.
    * **Matches phrase** queries the exact contents of your entered value. For example, `WITH message MATCHES PHRASE your example message` looks for the phrase `your example message` and returns results with that exact phrase.


There are several key supported use cases. You can create rules based on fields containing or matching a text pattern, rules based on a numeric field and arithmetic operator, or a single rule with multiple conditions.

A different {{es}} query type backs each of these comparators, and in some scenarios, it is important to know what these are so that you can configure your rule correctly. The comparators listed above map to the following {{es}} query types:

* **more than**: **range** using **gt**
* **more than or equals**: **range** using **gte**
* **less than**: **range** using **lt**
* **less than or equals**: **range** using **lte**
* **is** and **is not**: **term**
* **matches** and **does not match**: **match**
* **matches phrase** and **does not match phrase**: **match_phrase**


### Group by [group-by]

It is possible to set a **group by** for log threshold rules. You may set one or multiple groupings.

When **group by** is set, a composite aggregation is performed against the selected fields. When any of these groups match the selected rule conditions, an alert fires **per group**.

In scenarios where there are multiple groupings selected, the group name is separated by commas.

For example, if `host.name` and `host.architecture` are selected as group by fields, and there are two hosts (`Host A` and `Host B`) and two architectures (`Architecture A` and `Architecture B`), the composite aggregation forms multiple groups. We’ll focus on the `Host A, Architecture A` and `Host B, Architecture B` groups.

If the group `Host A, Architecture A` matches the rule conditions, but `Host B, Architecture B` doesn’t, one alert is triggered.

Similarly, if there was a single group by selected, for example, `host.name`, and Host A matches the conditions, but Host B doesn’t, one alert is triggered for Host A. If both groups matches the conditions, then two alerts are triggered.

::::{important}
When group by fields are selected, but no documents contain the selected field(s) within the given time range of when the alert is triggered, then you can’t determine the group(s). This is relevant when the rule condition is sensitive to a certain number of documents, and that number might be `0`. For example, when querying if a host has less than five documents matching a condition, an alert is not triggered due to the host not reporting logs for the duration of the query.

::::


:::{image} /solutions/images/observability-log-threshold-alert-group-by.png
:alt: Log threshold rule group by
:screenshot:
:::


## Chart previews [chart-previews]

To determine how many log entries would match each part of your configuration, you can view a chart preview for each condition. This is useful for determining how many log entries would match each part of your configuration. When a group by is set, the chart displays a bar per group. To view the preview, select the arrow next to the condition.

:::{image} /solutions/images/observability-log-threshold-alert-chart-previews.png
:alt: Log threshold chart previews
:screenshot:
:::

The shaded area denotes the threshold that has been selected.


## Ratio rules [ratio-alerts]

To understand how one query compares to another query, create a ratio rule. This type of rule is triggered when a ratio value meets a specific threshold. The ratio threshold value is the document count of the first query (query A), divided by the document count of the second query (query B).

The following example triggers an alert when there are twice as many error logs to warning logs.

:::{image} /solutions/images/observability-log-threshold-alert-ratio.png
:alt: Log threshold ratio rule
:screenshot:
:::

::::{important}
As it is not possible to divide by 0, when the document count of query A or query B is 0, it results in an undefined/indeterminate ratio. In this scenario, no alert is triggered.

::::



## Action types [action-types-logs]

Extend your rules by connecting them to actions that use the following supported built-in integrations.

* [D3 Security](kibana://reference/connectors-kibana/d3security-action-type.md)
* [Email](kibana://reference/connectors-kibana/email-action-type.md)
* [{{ibm-r}}](kibana://reference/connectors-kibana/resilient-action-type.md)
* [Index](kibana://reference/connectors-kibana/index-action-type.md)
* [Jira](kibana://reference/connectors-kibana/jira-action-type.md)
* [Microsoft Teams](kibana://reference/connectors-kibana/teams-action-type.md)
* [Observability AI Assistant connector](kibana://reference/connectors-kibana/obs-ai-assistant-action-type.md)
* [{{opsgenie}}](kibana://reference/connectors-kibana/opsgenie-action-type.md)
* [PagerDuty](kibana://reference/connectors-kibana/pagerduty-action-type.md)
* [Server log](kibana://reference/connectors-kibana/server-log-action-type.md)
* [{{sn-itom}}](kibana://reference/connectors-kibana/servicenow-itom-action-type.md)
* [{{sn-itsm}}](kibana://reference/connectors-kibana/servicenow-action-type.md)
* [{{sn-sir}}](kibana://reference/connectors-kibana/servicenow-sir-action-type.md)
* [Slack](kibana://reference/connectors-kibana/slack-action-type.md)
* [{{swimlane}}](kibana://reference/connectors-kibana/swimlane-action-type.md)
* [Torq](kibana://reference/connectors-kibana/torq-action-type.md)
* [{{webhook}}](kibana://reference/connectors-kibana/webhook-action-type.md)
* [xMatters](kibana://reference/connectors-kibana/xmatters-action-type.md)

::::{note}
Some connector types are paid commercial features, while others are free. For a comparison of the Elastic subscription levels, go to [the subscription page](https://www.elastic.co/subscriptions).

::::


After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that you choose how often the action runs (for example, at each check interval, only when the alert status changes, or at a custom action interval). In this case, you must also select the specific threshold condition that affects when actions run: `Fired` or `Recovered`.

:::{image} /solutions/images/observability-log-threshold-run-when-selection.png
:alt: Configure when a rule is triggered
:screenshot:
:::

You can also further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame:

* **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
* **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

:::{image} /solutions/images/observability-logs-threshold-conditional-alert.png
:alt: Configure a conditional alert
:screenshot:
:::


### Action variables [_action_variables_5]

Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available variables.

:::{image} /solutions/images/observability-logs-threshold-alert-default-message.png
:alt: Default notification message for log threshold rules with open "Add variable" popup listing available action variables
:screenshot:
:::

The following variables are specific to this rule type. You an also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

`context.alertDetailsUrl`
:   Link to the alert troubleshooting view for further context and details. This will be an empty string if the `server.publicBaseUrl` is not configured.

`context.grouping` {applies_to}`stack: ga 9.2`
:   The object containing groups that are reporting data.

`context.interval`
:   The length and unit of time period where the alert conditions were met.

`context.reason`
:   A concise description of the reason for the alert.

`context.serviceName`
:   The service the alert is created for.

`context.threshold`
:   Any trigger value above this value will cause the alert to fire.

`context.transactionName`
:   The transaction name the alert is created for.

`context.transactionType`
:   The transaction type the alert is created for.

`context.triggerValue`
:   The value that breached the threshold and triggered the alert.

`context.viewInAppUrl`
:   Link to the alert source.


### Performance considerations [performance-considerations]

When setting a **group by**, we recommend using the **more than** comparator for your threshold—this allows our queries to apply eager filtering, leading to significant performance improvements. Otherwise, we suggest using a **group by** field with the lowest cardinality (number of possibilities).


### {{es}} queries (advanced) [es-queries]

When a rule check is performed, a query is built based on the configuration of the rule. For the vast majority of cases it shouldn’t be necessary to know what these queries are. However, to determine an optimal configuration or to aid with debugging, it might be useful to see the structure of these queries. Below is an example {{es}} query for the following configuration:

:::{image} /solutions/images/observability-log-threshold-alert-es-query-ungrouped.png
:alt: Log threshold ungrouped {{es}} query example
:screenshot:
:::

```json
{
   "index":"filebeat-*", <1>
   "allowNoIndices":true,
   "ignoreUnavailable":true,
   "body":{
      "track_total_hits":true,
      "query":{
         "bool":{
            "filter":[
               {
                  "range":{
                     "@timestamp":{ <2>
                        "gte":1600771280862,
                        "lte":1600774880862,
                        "format":"epoch_millis"
                     }
                  }
               },
               {
                  "term":{
                     "log.level":{
                        "value":"error"
                     }
                  }
               }
            ],
            "must_not":[
               {
                  "term":{
                     "log.file.path":{
                        "value":"/nginx"
                     }
                  }
               }
            ]
         }
      },
      "size":0
   }
}
```

1. Taken from the **Log indices** setting
2. Taken from the **Timestamp** setting


:::{image} /solutions/images/observability-log-threshold-alert-es-query-grouped.png
:alt: Log threshold grouped {{es}} query example
:screenshot:
:::

```json
{
   "index":"filebeat-*", <1>
   "allowNoIndices":true,
   "ignoreUnavailable":true,
   "body":{
      "query":{
         "bool":{
            "filter":[
               {
                  "range":{
                     "@timestamp":{ <2>
                        "gte":1600768208910,
                        "lte":1600779008910,
                        "format":"epoch_millis"
                     }
                  }
               }
            ]
         }
      },
      "aggregations":{
         "groups":{
            "composite":{
               "size":40,
               "sources":[
                  {
                     "group-0-host.name":{
                        "terms":{
                           "field":"host.name"
                        }
                     }
                  }
               ]
            },
            "aggregations":{
               "filtered_results":{
                  "filter":{
                     "bool":{
                        "filter":[
                           {
                              "range":{
                                 "@timestamp":{
                                    "gte":1600771808910,
                                    "lte":1600775408910,
                                    "format":"epoch_millis"
                                 }
                              }
                           },
                           {
                              "term":{
                                 "log.level":{
                                    "value":"error"
                                 }
                              }
                           }
                        ],
                        "must_not":[
                           {
                              "term":{
                                 "log.file.path":{
                                    "value":"/nginx"
                                 }
                              }
                           }
                        ]
                     }
                  }
               }
            }
         }
      },
      "size":0
   }
}
```

1. Taken from the **Log indices** setting
2. Taken from the **Timestamp** setting



## Settings [settings]

With log threshold rules, it’s not possible to set an explicit index pattern as part of the configuration. The index pattern is instead inferred from the **Log sources** [advanced setting](kibana://reference/advanced-settings.md#kibana-search-settings).

With each execution of the rule check, the **Log indices** setting is checked, but it is not stored when the rule is created.

The **Timestamp** field that is set under **Settings** determines which field is used for timestamps in queries.

