---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: security
description: Learn how detection rules work with cross-project search to query data across linked projects.
---

# {{cps-cap}} and detection rules [sec-rules-cross-project-search]

:::{include} /solutions/_snippets/cps-sec-obs-rules.md
:::

## {{cps-cap}} context in alerts and the event log [cps-context-in-alerts]

When a detection rule runs with {{cps}} enabled, the scope in effect at execution time is recorded on generated alerts and in rule execution events. Use these fields during investigations to confirm which linked projects were in scope when an alert was created.

### Alert documents

Each alert document created by a {{cps}}-scoped rule execution can include:

| Field | Description |
| --- | --- |
| `kibana.cps_scope.expression` | The resolved NPRE for the space-level {{cps}} scope. |
| `kibana.cps_scope.linked_projects` | The linked projects included in that scope, with `id`, `alias`, `type`, and `organization` for each project. |

These fields are omitted when the rule does not run with {{cps}} enabled. For the full list of alert fields, refer to the [alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).

### Event log

Rule execution events written to the [event log index](/explore-analyze/alerting/alerts/event-log-index.md) include the same {{cps}} context under the `kibana` object:

| Field | Description |
| --- | --- |
| `kibana.cps_scope_expression` | The resolved NPRE for the {{cps}} scope. |
| `kibana.cps_scope_linked_projects` | The linked projects in scope, with the same object structure as in alert documents. |

To find executions for a specific scope, query the event log. For example:

```txt
GET .kibana-event-log-*/_search
{
  "size": 5,
  "query": {
    "match": { "kibana.cps_scope_expression": "_alias:*" }
  },
  "_source": [
    "event.action",
    "message",
    "kibana.cps_scope_expression",
    "kibana.cps_scope_linked_projects",
    "kibana.space_ids"
  ]
}
```

:::{note}
For cross-cluster deployments, use [{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md) instead. {{cps}} is available for {{serverless-short}} projects only.
:::