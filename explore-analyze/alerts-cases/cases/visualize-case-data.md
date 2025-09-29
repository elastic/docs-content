---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Visualize case data [visualize-case-data]

Case analytics indices store data for cases in Stack Management, Observability, and Security. This includes information about case comments, attachments, and activity. You can query case data to build dashboards and metrics that improve your visibility into case usage, patterns, and trends.

::::{admonition} Requirements

* To use case analytics indices, you must first turn on the feature by adding the following line to your [`kibana.yml`](/deploy-manage/stack-settings.md) file.

    ```yaml
    xpack.cases.incrementalId.enabled: true
    ```

    If you already have cases in your {{kib}} space, the case analytics indices and their aliases are automatically generated. If you don't, you must create a case in Stack Management, Observability, or Security to auto-generate the indices. 

    If you're creating cases in a new {{kib}} space, it can take around an hour for case analytics indices to generate.

* To query the case analytics indices, your role must have at least `Read` and `view_index_metadata` access to the indices.

::::

## About case analytics indices [about-case-analytics-indices]

Case data is stored in indices that are auto-created per space and for each Elastic solution (Stack Management, Observability, and Security). The following table lists these indices and their aliases.

| Index    | Alias | Description | 
| ---------------------------- | ---------------------- |----------------------------------------- | 
| • `.internal.cases.<space-name>-cases` (Stack Management cases) <br>• `.internal.cases.<space-name>-observability` (Observability cases) <br>• `.internal.cases.<space-name>-securitysolution` (Security cases) |  • `.cases.<space-name>-cases` <br>• `.cases.<space-name>-observability` (Observability cases) <br>• `.cases.<space-name>-securitysolution` (Security cases) | Stores general data related to Stack Management, Observability, and Security cases.    | 
| • `.internal.cases-comments.<space-name>-cases` (Stack Management cases) <br>• `.internal.cases-comments.<space-name>-observability` (Observability cases) <br>• `.internal.cases-comments.<space-name>-securitysolution` (Security cases) |  • `.cases-comments.<space-name>-cases` <br>• `.cases-comments.<space-name>-observability` (Observability cases) <br>• `.cases-comments.<space-name>-securitysolution` (Security cases) | Stores data related to case comments for cases in each Elastic solution.    | 
| • `.internal.cases-activity.<space-name>-cases` (Stack Management cases) <br>• `.internal.cases-activity.<space-name>-observability` (Observability cases) <br>• `.internal.cases-activity.<space-name>-securitysolution` (Security cases) |  • `.cases-activity.<space-name>-cases` <br>• `.cases-activity.<space-name>-observability` (Observability cases) <br>• `.cases-activity.<space-name>-securitysolution` (Security cases) | Stores data related to case activity for cases in each Elastic solution.    | 
| • `.internal.cases-attachments.<space-name>-cases` (Stack Management cases) <br>• `.internal.cases-attachments.<space-name>-observability` (Observability cases) <br>• `.internal.cases-attachments.<space-name>-securitysolution` (Security cases) |  • `.cases-attachments.<space-name>-cases` <br>• `.cases-attachments.<space-name>-observability` (Observability cases) <br>• `.cases-attachments.<space-name>-securitysolution` (Security cases) | Stores data related to case attachments for cases in each Elastic solution.    | 

Every five minutes, the indices are refreshed with a snapshot of the most current case data in your space. Historical case data isn't stored; it's overwritten whenever the indices refresh.

## Explore case data [explore-case-analytics-indices]

Once the case analytics indices are created, you can start querying them for case data. To learn more about queryable fields in the indices, refer to 
% [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md) 

Search and filter case data in [Discover](../../discover.md) and [Lens](../../visualize/lens.md), and build visualizations for [dashboards](../../dashboards.md). To help you start visualizing your case data, here are some sample {{esql}} queries that you can run from the [{{esql}} editor](../../../explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-get-started) in Discover.

* Find the total number of {{elastic-sec}}cases that are currently open in the default {{kib}} space:
  ```console
  FROM .internal.cases.default-securitysolution | STATS count = COUNT(*) BY status | WHERE status  == "open"
  ```

* Find the total number of {{elastic-sec}} cases that are currently in progress in the default {{kib}} space:
  ```console
  FROM .internal.cases.default-securitysolution | STATS count = COUNT(*) BY status | WHERE status  == "in-progress"
  ```

* Find the total number of {{elastic-sec}} cases that are closed in the default {{kib}} space:
  ```console
  FROM .internal.cases.default-securitysolution | STATS count = COUNT(*) BY status | WHERE status  == "closed"
  ```

* Find {{elastic-sec}} cases that are open and sort them by time, with the most recent at the top:
  ```console
  FROM .internal.cases.default-securitysolution | WHERE status  == "open" | SORT created_at DESC
  ```

* Find the average time that it takes to close {{elastic-sec}} cases in the default {{kib}} space:
  ```console
  FROM .internal.cases.default-securitysolution | STATS average_time_to_close = AVG(time_to_resolve)
  ```
