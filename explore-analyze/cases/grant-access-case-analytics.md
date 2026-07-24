---
navigation_title: Grant access
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
description: Grant read access to the case analytics indices by creating an Elasticsearch role with the required index privileges.
---

# Grant access to the analytics indices [grant-access-case-analytics]

To let users report on case data, grant them read access to the [case analytics indices](case-analytics-indices.md).

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5", "serverless": "ga" }
In {{stack}} 9.5+ and {{serverless-short}}, {{es}} stores case analytics data in three hidden indices:

| Index | Use it to report on |
| --- | --- |
| `.cases` | Your cases and their current state, such as status, severity, assignees, and timing metrics. |
| `.cases-activity` | What happened to cases over time, such as status changes, comments, and who made each change. |
| `.cases-attachments` | What's attached to cases, such as alerts, comments, files, dashboards, and visualizations. |

By default, only users with sufficient {{es}} privileges (such as a superuser) can read them. To give other users access, grant them the required privileges on the indices directly, because {{kib}} Cases feature privileges don't apply to these indices.

To grant access, create an {{es}} role with the `read` and `view_index_metadata` privileges on the analytics indices, and set `allow_restricted_indices` to `true`. Then assign the role to your users.

For example, the following request creates a `cases_analytics_reader` role with read access to all three indices:

```console
PUT _security/role/cases_analytics_reader
{
  "indices": [
    {
      "names": [".cases", ".cases-activity", ".cases-attachments"],
      "privileges": ["read", "view_index_metadata"],
      "allow_restricted_indices": true
    }
  ]
}
```

:::{warning}
A role with read access to these indices can query case data across all spaces and solutions, regardless of which spaces or solutions the user works in. Grant this access carefully, and filter by `space_id` and `owner` in your queries and visualizations to limit scope.
:::
::::

::::{applies-item} stack: preview 9.2-9.4
In 9.2-9.4, grant your role at least `read` and `view_index_metadata` privileges on the case analytics indices. Each solution and space has its own set of indices, so use the `.internal.cases*` pattern to cover them all, or target specific indices by name. To find the right index names, refer to [Case analytics indices](case-analytics-indices.md#case-analytics-indices-list).
::::

:::::
