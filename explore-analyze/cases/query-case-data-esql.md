---
navigation_title: Query with ES|QL
applies_to:
  stack: preview 9.2-9.4, ga 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Analyze case data directly with ES|QL queries against the case analytics indices.
---

# Query case data with {{esql}} [query-case-analytics-esql]

{{esql}} queries the analytics indices directly, which is ideal for calculating metrics like case volume, closure rates, and mean time to respond (MTTR). This page provides sample queries you can adapt in [{{esql}} in Discover](../discover/try-esql.md).

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5", "serverless": "ga" }
In {{stack}} 9.5+ and {{serverless-short}}, query the shared `.cases`, `.cases-activity`, and `.cases-attachments` indices, and reference fields with the singular `case.*` prefix, such as `case.status`. For field units and other details, refer to the [field reference](case-analytics-fields.md). Here are some sample queries to get you started:

* Count open cases by severity:

  ```esql
  FROM .cases
  | WHERE case.status == "open"
  | STATS case_count = COUNT(*) BY case.severity
  | SORT case_count DESC
  ```

* Find mean time to resolve by severity:

  ```esql
  FROM .cases
  | WHERE case.status == "closed" AND case.time_to_resolve IS NOT NULL
  | STATS mttr_seconds = AVG(case.time_to_resolve) BY case.severity
  | EVAL mttr_hours = ROUND(mttr_seconds / 3600, 1)
  | SORT mttr_seconds DESC
  ```

* Count open cases by solution (`owner`):

  ```esql
  FROM .cases
  | WHERE case.status == "open"
  | STATS case_count = COUNT(*) BY owner
  | SORT case_count DESC
  ```

* Join activity to current case attributes:

  ```esql
  FROM .cases-activity
  | STATS actions = COUNT(*) BY case.id
  | LOOKUP JOIN .cases ON case.id
  | KEEP case.id, case.title, case.status, actions
  ```
::::

::::{applies-item} stack: preview 9.2-9.4
In 9.2-9.4, each index covers one solution in one space, so use the [index name](case-analytics-indices.md) for the data you want, such as `.internal.cases.observability-default`. Reference fields without the `case.*` prefix, such as `status` instead of `case.status`. These examples use the `default` space. Here are some sample queries to get you started:

* Count cases by status. Change the index name to target a different solution or space:

  ```esql
  FROM .internal.cases.observability-default
  | STATS count = COUNT(*) BY status
  ```

* Find open Security cases, with the most recent first:

  ```esql
  FROM .internal.cases.securitysolution-default
  | WHERE status == "open"
  | SORT created_at DESC
  ```

* Find the average time to close Security cases:

  ```esql
  FROM .internal.cases.securitysolution-default
  | STATS average_time_to_close = AVG(time_to_resolve)
  ```
::::

:::::
