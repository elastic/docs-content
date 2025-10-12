---
applies_to:
  deployment:
    ess: preview 9.2
    ece: preview 9.2
---

# Use cases as data [use-cases-as-data]

The cases as data feature lets you visualize data about cases in your [space](/deploy-manage/manage-spaces.md). After turning it on, you can query case data from dedicated case analytics indices and build dashboards and visualizations to track case trends and operational metrics. This information is particularly useful when reporting on key performance indicators (KPIs) such as Mean Time To Respond (MTTR), case severity trends, and analyst workload.

::::{admonition} Requirements
To use cases as data, you must have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

## Turn on cases as data [turn-on-cases-as-data]

To turn on cases as data, add `xpack.cases.incrementalId.enabled: true` to your [`kibana.yml`](/deploy-manage/stack-settings.md) file.

::::{warning} 
3 tasks will be created that each execute in 5 minute interval. If you have lots of spaces with cases (for example, dozens), we do not reccomend enabling this feature as it will clog up task manager.
::::

## Create and manage indices for case data [create-manage-case-analytics-indices]

After turning on cases as data, you do not need to manually create the analytics indices. {{es}} will automatically create them for you in any space with cases and for each solution ({{stack-manage-app}}, {{observability}}, and Security). The indices are populated with general case data as well as data related to case comments, attachments, and activity.

You also do not need to manually manage the lifecycle policies of the analytics indices. Every five minutes, a background task runs to refresh the indices with a snapshot of the most current cases data. During the refresh, historical case data is overwritten. 

::::{note} 
- After making new cases, it may take up to 10 minutes to index the new case data. 
- After making a new space, it can take up to an hour for the case analytics indices for that space to form.  
::::

## Grant access to case analytics indices [case-analytics-indices-privs]

Ensure your role has at least `read` and `view_index_metadata` access to the appropriate [case analytics indices](../../../explore-analyze/alerts-cases/cases/cases-as-data.md#case-analytics-indices-names).

## Explore and visualize case data with Discover [explore-case-data]

By default, {{kib}} requires a [{{data-source}}](../../find-and-organize/data-views.md) to access your Elasticsearch data. When creating a {{data-source}} for case data, point to one or more [case analytics indices or their aliases](../../../explore-analyze/alerts-cases/cases/cases-as-data.md#case-analytics-indices-names).

You can also [try {{esql}}](../../../explore-analyze/discover/try-esql.md), which lets you query any data you have in {{es}} without specifying a {{data-source}} first. Here are some sample queries to get you started:

* Find the total number of open {{observability}} cases in the default space:

  ```console
  FROM .internal.cases.default-observability | STATS count = COUNT(*) BY status | WHERE status  == "open"
  ```

* Find the total number of in progress Stack Management cases in the default space:

  ```console
  FROM .internal.cases.default-cases | STATS count = COUNT(*) BY status | WHERE status  == "in-progress"
  ```

* Find the total number of closed {{observability}} cases in the default space:

  ```console
  FROM .internal.cases.default-observability | STATS count = COUNT(*) BY status | WHERE status  == "closed"
  ```

* Find Security cases that are open in the default space, and sort them by time, with the most recent at the top:

  ```console
  FROM .internal.cases.default-securitysolution | WHERE status  == "open" | SORT created_at DESC
  ```

* Find the average time that it takes to close Security cases in the default space:

  ```console
  FROM .internal.cases.default-securitysolution | STATS average_time_to_close = AVG(time_to_resolve)
  ```

## Case analytics indices names and aliases [case-analytics-indices-names]

{{es}} automatically creates the following case analytics indices and their aliases in spaces with case data. 

::::{note} 
Go to
% [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md) for schema details. 
::::

### General case data 

These indices store general data about cases. 

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases.<space-name>-cases` |  `.cases.<space-name>-cases` | Stack Management cases  | 
| `.internal.cases.<space-name>-observability` |  `.cases.<space-name>-observability` | {{observability}} cases   | 
| `.internal.cases.<space-name>-securitysolution` |  `.cases.<space-name>-securitysolution` | Security cases  | 

### Case comments

These indices store data related to comments.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-comments.<space-name>-cases` |  `.cases-comments.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-comments.<space-name>-observability` |  `.cases-comments.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-comments.<space-name>-securitysolution` |  `.cases-comments.<space-name>-securitysolution` | Security cases   | 

### Case attachments 

These indices store data related to attachments.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-attachments.<space-name>-cases` |  `.cases-attachments.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-attachments.<space-name>-observability` |  `.cases-attachments.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-attachments.<space-name>-securitysolution` |  `.cases-attachments.<space-name>-securitysolution` | Security cases    | 

### Case activity 

These indices store data related to activity.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-activity.<space-name>-cases` |  `.cases-activity.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-activity.<space-name>-observability` |  `.cases-activity.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-activity.<space-name>-securitysolution` |  `.cases-activity.<space-name>-securitysolution` | Security cases    | 