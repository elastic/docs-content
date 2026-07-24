---
navigation_title: Indices
applies_to:
  stack: preview=9.2-9.4, ga 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Reference for the case analytics indices that store case data, covering how they're organized and how often they refresh.
---

# Case analytics indices [case-analytics-indices]

Elastic mirrors your case data into dedicated analytics indices that are built for reporting and aggregation. This page describes those indices and how often they refresh.

## Indices [case-analytics-indices-list]

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5", "serverless": "ga" }
In {{stack}} 9.5+ and {{serverless-short}}, {{es}} automatically creates three analytics indices and keeps them in sync with your case data:

| Index | What it holds | Example |
| --- | --- | --- |
| `.cases` | One document per case, with each case's current details | Status, severity, assignees, and timing metrics |
| `.cases-activity` | One document per action taken on a case | A status change, severity change, or comment |
| `.cases-attachments` | One document per item attached to a case | An alert, comment, file, dashboard, or visualization |

The `.cases-activity` and `.cases-attachments` indices join back to `.cases` on the `case.id` field.

These indices store status and severity as readable text and precalculate common timing metrics like time to resolve. They hold data from {{elastic-sec}}, {{observability}}, and {{stack-manage-app}} together, so use the `owner` and `space_id` fields to filter by solution or space.

:::{important}
Field names use the singular `case.*` form, such as `case.status`. A plural path like `cases.status` isn't a valid field, and the {{esql}} query fails.
:::

For the fields available in each index, refer to [Case analytics field reference](case-analytics-fields.md).
::::

::::{applies-item} stack: preview 9.2-9.4
In 9.2-9.4, {{es}} automatically creates the analytics indices for you, so you don't need to create them or manage their lifecycle policies. It creates a separate set of indices for each solution in every space that has cases.

{{es}} names each index `.internal.<type>.<solution>-<space-name>`, with a matching alias that drops the `.internal` prefix. For example, Security case attachments in the `default` space use the index `.internal.cases-attachments.securitysolution-default` and the alias `.cases-attachments.securitysolution-default`.

Combine a type and a solution to build the name for the data you want:

| `<type>` | Contents |
| --- | --- |
| `cases` | General case data |
| `cases-comments` | Case comments |
| `cases-attachments` | Case attachments |
| `cases-activity` | Case activity |

| Solution | `<solution>` |
| --- | --- |
| {{stack-manage-app}} | `cases` |
| {{observability}} | `observability` |
| Security | `securitysolution` |

:::{important}
In 9.2-9.4, fields are unprefixed. For example, use `status` and `time_to_resolve`, not `case.status`. This differs from 9.5 and later, where fields use the `case.*` prefix.
:::

For schema details, refer to [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md).
::::

:::::

## Data freshness [case-analytics-data-freshness]

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5", "serverless": "ga" }
In {{stack}} 9.5+ and {{serverless-short}}, case analytics keeps your data current in two ways:

1. It updates the indices as soon as you create, edit, or delete a case.
2. As a backup, a background task checks for recently changed cases on a regular schedule (every 30 minutes by default) and fills in anything the immediate update missed.

Because updates take a moment to apply, a new or edited case can take a short time to appear in your queries.
::::

::::{applies-item} stack: preview 9.2-9.4
In 9.2-9.4, a background task refreshes the analytics indices every five minutes with a snapshot of the most current case data. During each refresh, {{es}} overwrites the historical case data.

:::{note}
- After you create a case, indexing the new case data can take up to 10 minutes.
- After you create a space, the case analytics indices for that space can take up to an hour to form.
:::
::::

:::::
