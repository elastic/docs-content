---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Visualize case data [visualize-case-data]

Case data is stored in case analytics indices, which include data from case comments, attachments, and activity. You can query this information to build dashboards and metrics that improve your visibility into case, usage, patterns, and trends.

## About case analytics indices [about-case-analytics-indices]

Case analytics indices and their aliases are automatically generated when{{kib}} starts up. Every five minutes, the indices are updated with a snapshot of most current cases data in your space. Historical cases data is not stored; it gets overwritten whenever the indices are refreshed.

You can begin querying case analytics indices as soon as you have cases in your space. To learn more about fields in the indices, refer to 
% [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md) 

| Index    | Alias | Description | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases`            | `.cases`               | Stores general data related to cases.    | 
| `.internal.cases-comments`   | `.cases-comments`      | Stores data related to case comments.    | 
| `.internal.cases-activity`   | `.cases-activity`      | Stores data related to case activity.    | 
| `.internal.cases-attachments`| `.cases-attachments`   | Stores data related to case attachments (only alerts and files added to the case). | 

## Explore case data [explore-case-analytics-indices]

::::{admonition} Requirements
To query the case analytics indices, your role must have at least `Read` and `view_index_metadata` access to the indices.
::::

Search and filter case data in [Discover](../../discover.md) and [Lens](../../visualize/lens.md), and build visualizations for [dashboards](../../dashboards.md). To help you start visualizing your case data, here are some sample {{esql}} queries that you can run from the [{{esql}} editor](../../../explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-get-started) in Discover.

* Find the total number of cases that are currently open:
  ```console
  FROM .internal.cases | STATS count = COUNT(*) BY status | WHERE status  == "open"
  ```

* Find the total number of cases that are currently in progress:
  ```console
  FROM .internal.cases | STATS count = COUNT(*) BY status | WHERE status  == "in-progress"
  ```

* Find the total number of cases that are closed:
  ```console
  FROM .internal.cases | STATS count = COUNT(*) BY status | WHERE status  == "closed"
  ```

* Find cases that are open and sort them by time, with the most recent at the top:
  ```console
  FROM .internal.cases | WHERE status  == "open" | SORT created_at DESC
  ```

* Find the average time that it takes to close a case:
  ```console
  FROM .internal.cases | STATS average_time_to_close = AVG(time_to_resolve)
  ```
