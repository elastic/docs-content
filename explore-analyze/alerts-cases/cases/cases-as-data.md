---
applies_to:
  stack: preview 9.2
  serverless: unavailable
---

# Use cases as data [use-cases-as-data]

The cases as data feature lets you visualize data about cases in your [space](/deploy-manage/manage-spaces.md). After turning it on, you can query case data from dedicated case analytics indices and build dashboards and visualizations to track case trends and operational metrics. This information is particularly useful when reporting on key performance indicators (KPIs) such as Mean Time To Respond (MTTR), case severity trends, and analyst workload.

::::{admonition} Requirements
To use cases as data, you must have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

## Turn on cases as data [turn-on-cases-as-data]

To turn on cases as data, add `xpack.cases.analytics.index.enabled: true` to your [`kibana.yml`](/deploy-manage/stack-settings.md) file.

::::{warning} 
We only recommend turning this feature on if your deployment has 10 or fewer spaces with cases. The background tasks that refresh the case analytics indices in each space are run every five minutes and may overload Task Manager.  
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

## Explore case data with Discover and Lens [explore-case-data]

Use [Discover](../../discover.md) and [Lens](../../visualize/lens.md) to search and filter your case data and display your findings in visualizations. 

To get started, create a [{{data-source}}](../../find-and-organize/data-views.md) that points to one or more [case analytics indices or their aliases](../../../explore-analyze/alerts-cases/cases/cases-as-data.md#case-analytics-indices-names). To point to all case analytics indices in your space, use the `.internal.cases*` index pattern.

::::{note} 
Case data is stored in hidden indices. You can display hidden indices by selecting **Show advanced settings**, then turning on **Allow hidden and system indices**. 
::::

You can also interact with your case data using [{{esql}} in Discover](../../../explore-analyze/discover/try-esql.md). Here are some sample queries to get you started: 

* Find the total number of open {{observability}} cases in the default space:

  ```console
  FROM .internal.cases.observability-default | STATS count = COUNT(*) BY status | WHERE status  == "open"
  ```

* Find the total number of in progress Stack Management cases in the default space:

  ```console
  FROM .internal.cases.cases-default | STATS count = COUNT(*) BY status | WHERE status  == "in-progress"
  ```

* Find the total number of closed {{observability}} cases in the default space:

  ```console
  FROM .internal.cases.observability-default | STATS count = COUNT(*) BY status | WHERE status  == "closed"
  ```

* Find Security cases that are open in the default space, and sort them by time, with the most recent at the top:

  ```console
  FROM .internal.cases.securitysolution-default | WHERE status  == "open" | SORT created_at DESC
  ```

* Find the average time that it takes to close Security cases in the default space:

  ```console
  FROM .internal.cases.securitysolution-default | STATS average_time_to_close = AVG(time_to_resolve)
  ```

## Case analytics indices names and aliases [case-analytics-indices-names]

{{es}} automatically creates the following case analytics indices and their aliases in spaces with case data. 

% ::::{note} 
% Go to [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md) for schema details. 
% ::::

### General case data 

These indices store general data about cases. 

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases.cases-<space-name>` |  `.cases.cases-<space-name>` | Stack Management cases  | 
| `.internal.cases.observability-<space-name>` |  `.cases.observability-<space-name>` | {{observability}} cases   | 
| `.internal.cases.securitysolution-<space-name>` |  `.cases.securitysolution-<space-name>` | Security cases  | 

### Case comments

These indices store data related to comments.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-comments.cases-<space-name>` |  `.cases-comments.cases-<space-name>` | Stack Management cases    | 
| `.internal.cases-comments.observability-<space-name>` |  `.cases-comments.observability-<space-name>` | {{observability}} cases    | 
| `.internal.cases-comments.securitysolution-<space-name>` |  `.cases-comments.securitysolution-<space-name>` | Security cases   | 

### Case attachments 

These indices store data related to attachments.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-attachments.cases-<space-name>` |  `.cases-attachments.cases-<space-name>` | Stack Management cases    | 
| `.internal.cases-attachments.observability-<space-name>` |  `.cases-attachments.observability-<space-name>` | {{observability}} cases    | 
| `.internal.cases-attachments.securitysolution-<space-name>` |  `.cases-attachments.securitysolution-<space-name>` | Security cases    | 

### Case activity 

These indices store data related to activity.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-activity.cases-<space-name>` |  `.cases-activity.cases-<space-name>` | Stack Management cases    | 
| `.internal.cases-activity.observability-<space-name>` |  `.cases-activity.observability-<space-name>` | {{observability}} cases    | 
| `.internal.cases-activity.securitysolution-<space-name>` |  `.cases-activity.securitysolution-<space-name>` | Security cases    | 