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

If your data spans ECH, ECE, ECK, or self-managed clusters rather than linked {{serverless-short}} projects, refer to [{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md) instead.

## {{cps-cap}} context in alerts and the event log [cps-context-in-alerts]

When a detection rule runs with {{cps}} enabled, the scope in effect at execution time is recorded on generated alerts and in rule execution events. During investigations, use the scope and linked project fields on the alert or in the event log to confirm which linked projects were in scope when an alert was created.

### When scope fields appear [cps-scope-fields-when]

Scope fields are written at rule execution time, not added to existing documents later. You need [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), a [configured space-level {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md), and at least one enabled detection rule that has run successfully with {{cps}} enabled.

On **alert documents**, `kibana.cps_scope.expression` and `kibana.cps_scope.linked_projects` are present only when that run generated an alert. Alerts created before {{cps}} was enabled are not updated retroactively.

On **event log entries**, `kibana.cps_scope_expression` and `kibana.cps_scope_linked_projects` are recorded for every {{cps}}-scoped execution, including runs that created no alerts.

### Alert documents

When a detection rule runs with {{cps}} enabled, each generated alert can include:

| Field | Description |
| --- | --- |
| `kibana.cps_scope.expression` | The {{cps}} scope that was in effect when the rule generated the alert. |
| `kibana.cps_scope.linked_projects` | The linked projects that were in scope. Each entry includes `id`, `alias`, `type`, and `organization`. |

For the full list of alert fields, refer to the [alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).

### Event log

Rule execution events in the [event log index](/explore-analyze/alerting/alerts/event-log-index.md) record the same scope and linked project information:

| Field | Description |
| --- | --- |
| `kibana.cps_scope_expression` | The {{cps}} scope that was in effect during the rule execution. |
| `kibana.cps_scope_linked_projects` | The linked projects that were in scope. Each entry includes `id`, `alias`, `type`, and `organization`. |

To find rule executions that ran with a particular scope, run a search against the event log in [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md) or your own API client. The following example returns recent detection rule execution events that include {{cps}} scope fields:

```txt
GET .kibana-event-log-*/_search
{
  "size": 5,  <1>
  "query": {
    "match": { "kibana.cps_scope_expression": "_alias:*" }  <2>
  },
  "_source": [  <3>
    "event.action",
    "message",
    "kibana.cps_scope_expression",
    "kibana.cps_scope_linked_projects",
    "kibana.space_ids"
  ]
}
```

1. Change `size` to return more or fewer events.
2. Replace `_alias:*` with the scope you want to find. To match the scope from a specific alert, copy the value from that alert's `kibana.cps_scope.expression` field.
3. Edit the `_source` array to include the fields you need in the response.

This request searches the event log indices (`.kibana-event-log-*`) for documents that have a `kibana.cps_scope_expression` value. It limits the response to five events and returns only the fields listed in `_source`, including the {{cps}} scope, linked projects, and space ID for each execution. The event log is a system index, so by default only users with a `superuser` role can run this search. For more example queries and details on required privileges, refer to the [event log index](/explore-analyze/alerting/alerts/event-log-index.md).
