---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: security
description: Learn which projects detection rules search under cross-project search, where their alerts are stored, which API key they need, and how alert limits apply.
---

# {{cps-cap}} and detection rules [sec-rules-cross-project-search]

:::{include} /solutions/_snippets/cps-sec-obs-rules.md
:::

If your data spans ECH, ECE, ECK, or self-managed clusters rather than linked {{serverless-short}} projects, refer to [{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md) instead.

## Which projects a rule searches and where alerts are stored [cps-rules-scope-and-alerts]

A rule that runs on the origin project queries the origin project and every linked project in the rule's scope. The rule writes every alert it generates to the origin project, no matter which project the matching events came from.

This lets one project hold your detections and your analysts' alert triage while the data stays in the projects that produce it. It also means the origin project's **Alerts** page shows every alert your origin project rules generated, but not every alert in your organization. Rules that run independently on a linked project write their alerts to that project, and the origin project's **Alerts** page doesn't read them.

To confirm which projects a rule covered when it created an alert, use the {{cps-init}} scope fields described in [{{cps-cap}} context in alerts and the event log](#cps-context-in-alerts).

## Which API key a rule needs to reach linked projects [cps-rules-api-key]

A rule runs with the API key of the user who created or last updated it, so that key determines which projects the rule can resolve indices in. Only [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md) authenticate across project boundaries. [{{es}} API keys](/deploy-manage/api-keys/serverless-project-api-keys.md) are scoped to a single project and return results from the origin project only.

Rules that you create or edit in the UI get an {{ecloud}} API key. A rule created or updated through the API with an {{es}} API key keeps that key, which makes the rule origin-scoped. Such a rule resolves no linked project indices, and if the origin project has no matching indices either, the rule skips execution and reports this warning:

```txt
Unable to find matching indices for rule <rule name>. This warning will persist until one of the following occurs: a matching index is created or the rule is disabled.
```

Plan for this when you migrate rules from another environment or create rules through automation. To move a rule to an {{ecloud}} API key, open the rule's actions menu {icon}`boxes_horizontal` on the **{{siem-rules-ui}}** page and select **Update API key**, or edit and save the rule in the UI.

Rules still running on an {{es}} API key are tagged **Missing {{ecloud}} API Key** on the **{{siem-rules-ui}}** page. For more about how this key type affects rule access, refer to [Rules and {{ecloud}} API keys in {{serverless-short}}](/explore-analyze/alerting/alerts/rules-and-elastic-cloud-api-keys.md).

## How the alert limit applies across linked projects [cps-rules-max-alerts]

The **Max alerts per run** [advanced setting](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) limits the number of alerts a rule creates in a single execution. Under {{cps}}, that cap covers the combined results from the origin project and all linked projects in the rule's scope rather than each project separately. The default is 100.

A rule that stayed comfortably under the limit on a single project can reach it once you link projects, which leaves matches without alerts. Review the limit for rules that run across a broad scope, and consider [narrowing the scope with project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) instead of raising the limit.

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
