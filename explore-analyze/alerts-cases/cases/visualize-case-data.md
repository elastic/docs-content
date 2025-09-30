---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Visualize case data [visualize-case-data]

Case data, such as details about comments, activities, and attachments, is stored in case analytics indices. You can query these indices to build dashboards and metrics that improve your visibility into case patterns and trends. 

::::{tip} 
To learn more about queryable fields in the case analytics indices, refer to 
% [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md) 
::::

## About case analytics indices [about-case-analytics-indices]

The following case analytics indices and their aliases are automatically generated for _all_ {{kib}} spaces if any spaces have cases. 

::::{note} 
* Every five minutes, indices are updated with a snapshot of most current cases data in your spaces. Historical data for cases is not stored; it gets overwritten whenever the indices are refreshed.
* It may take around an hour for case analytics indices to form in a new {{kib}} space.
::::

### General case data

These indices store general data related to cases created in Stack Management, {{observability}}, and Security.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases.<space-name>-cases` |  `.cases.<space-name>-cases` | Stack Management cases  | 
| `.internal.cases.<space-name>-observability` |  `.cases.<space-name>-observability` | {{observability}} cases   | 
| `.internal.cases.<space-name>-securitysolution` |  `.cases.<space-name>-securitysolution` | Security cases  | 

### Case comments

These indices store data related to comments in Stack Management, {{observability}}, and Security cases.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-comments.<space-name>-cases` |  `.cases-comments.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-comments.<space-name>-observability` |  `.cases-comments.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-comments.<space-name>-securitysolution` |  `.cases-comments.<space-name>-securitysolution` | Security cases   | 


### Case attachments

These indices store data related to attachments in Stack Management, {{observability}}, and Security cases.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-attachments.<space-name>-cases` |  `.cases-attachments.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-attachments.<space-name>-observability` |  `.cases-attachments.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-attachments.<space-name>-securitysolution` |  `.cases-attachments.<space-name>-securitysolution` | Security cases    | 

### Case activity

These indices store data related to activity in Stack Management, {{observability}}, and Security cases.

| Index    | Alias | Created for | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| `.internal.cases-activity.<space-name>-cases` |  `.cases-activity.<space-name>-cases` | Stack Management cases    | 
| `.internal.cases-activity.<space-name>-observability` |  `.cases-activity.<space-name>-observability` | {{observability}} cases    | 
| `.internal.cases-activity.<space-name>-securitysolution` |  `.cases-activity.<space-name>-securitysolution` | Security cases    | 


## Explore case data [explore-case-analytics-indices]

::::{admonition} Requirements

* Enable the case analytics indices feature by adding `xpack.cases.incrementalId.enabled: true` to your [`kibana.yml`](/deploy-manage/stack-settings.md) file.
* Ensure your role has at least `read` and `view_index_metadata` access to the appropriate case anlaytics indices.

::::

Search and filter case data in [Discover](../../discover.md) and [Lens](../../visualize/lens.md), and build visualizations for [dashboards](../../dashboards.md). To help you start visualizing your case data, here are some sample {{esql}} queries that you can run from the [{{esql}} editor](../../../explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-get-started) in Discover.

* Find the total number of open cases in the default {{kib}} space:

  ```console
  FROM .internal.cases.default-observability | STATS count = COUNT(*) BY status | WHERE status  == "open"
  ```

* Find the total number of in progress Stack Management cases in the default {{kib}} space:

  ```console
  FROM .internal.cases.default-cases | STATS count = COUNT(*) BY status | WHERE status  == "in-progress"
  ```

* Find the total number of closed {{observability}} cases in the default {{kib}} space:

  ```console
  FROM .internal.cases.default-observability | STATS count = COUNT(*) BY status | WHERE status  == "closed"
  ```

* Find Security cases that are open in the default {{kib}} space, and sort them by time, with the most recent at the top:

  ```console
  FROM .internal.cases.default-securitysolution | WHERE status  == "open" | SORT created_at DESC
  ```

* Find the average time that it takes to close Security cases in the default {{kib}} space:

  ```console
  FROM .internal.cases.default-securitysolution | STATS average_time_to_close = AVG(time_to_resolve)
  ```
