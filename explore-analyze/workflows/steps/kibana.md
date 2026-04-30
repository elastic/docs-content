---
navigation_title: Kibana
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Reference for Kibana action steps, including detection alert management, the generic request escape hatch, and deprecated Case aliases.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Kibana action steps [workflows-kibana-action-steps]

{{kib}} action steps let a workflow interact with {{kib}} APIs. The namespace covers detection alert management, a generic request escape hatch for any {{kib}} API, and legacy Case aliases that are now deprecated in favor of the [`cases.*`](/explore-analyze/workflows/steps/cases.md) namespace.

For Cases operations, always use the dedicated [Cases action steps](/explore-analyze/workflows/steps/cases.md). For Observability Streams, use the [Streams action steps](/explore-analyze/workflows/steps/streams.md). Everything else lives here.

All {{kib}} actions are automatically authenticated using the permissions or API key of the user executing the workflow.

:::{important}
The detection alert step type IDs use **PascalCase**, not lowercase or snake_case: `kibana.SetAlertsStatus`, `kibana.SetAlertTags`. The editor rejects lowercase variants. This is the most common authoring surprise on the {{kib}} namespace.
:::

## Step types

- [`kibana.SetAlertsStatus`](#kibana-setalertsstatus): Change the status of one or more detection alerts.
- [`kibana.SetAlertTags`](#kibana-setalerttags): Add or remove tags on detection alerts.
- [`kibana.request`](#kibana-request): Generic escape hatch for any {{kib}} API.
- [Deprecated Case aliases](#deprecated-aliases): Use [`cases.*`](/explore-analyze/workflows/steps/cases.md) instead.

---

## `kibana.SetAlertsStatus` [kibana-setalertsstatus]

Update the status of one or more detection alerts. Note the PascalCase in the step type ID.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `signal_ids` | `with` | `string[]` | Yes | Alert signal IDs to update. |
| `status` | `with` | string | Yes | `open`, `acknowledged`, `in-progress`, or `closed`. |
| `reason` | `with` | string | No | Reason for the status change. Typically used when `status` is `closed`. |
| `conflicts` | `with` | string | No | Conflict-handling strategy when an update conflicts with concurrent changes. |
| `query` | `with` | object | No | Query DSL filter for selecting alerts to update (alternative to `signal_ids`). |

```yaml
- name: close_false_positive
  type: kibana.SetAlertsStatus
  with:
    signal_ids:
      - "{{ event.alerts[0]._id }}"
    status: "closed"
    reason: "false_positive"
```

## `kibana.SetAlertTags` [kibana-setalerttags]

Add or remove tags on one or more detection alerts. Note the PascalCase step type ID. The tag lists are **nested under a `tags` object**, not at the top level of `with`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string[]` | Yes | Alert IDs to tag. |
| `tags.tags_to_add` | `with` | `string[]` | Yes | Tags to add. Can be an empty array. |
| `tags.tags_to_remove` | `with` | `string[]` | Yes | Tags to remove. Can be an empty array. |

```yaml
- name: mark_reviewed
  type: kibana.SetAlertTags
  with:
    ids:
      - "{{ event.alerts[0]._id }}"
    tags:
      tags_to_add: ["analyst-reviewed"]
      tags_to_remove: []
```

:::{important}
Both `tags_to_add` and `tags_to_remove` are required, even when one is empty. Send `tags_to_remove: []` if you're only adding tags, and `tags_to_add: []` if you're only removing. Passing either field at the top level of `with` (instead of nested under `tags`) is rejected.
:::

## `kibana.request` [kibana-request]

Generic escape hatch for any {{kib}} API that doesn't have a named step. Authenticates as the workflow's execution identity. Use a named step when one exists; named steps validate parameters at save time.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `method` | `with` | string | No (defaults to `GET`) | HTTP method: `GET`, `POST`, `PUT`, or `DELETE`. |
| `path` | `with` | string | Yes | The API endpoint path, starting with `/api/`. |
| `body` | `with` | object | No | JSON request body. |
| `query` | `with` | object | No | URL query parameters. |
| `headers` | `with` | object | No | Custom HTTP headers. `kbn-xsrf` and `Content-Type` are added automatically. |

```yaml
- name: custom_kibana_api_call
  type: kibana.request
  with:
    method: "GET"
    path: "/api/status"
```

:::{note}
You do not need to pass an `Authorization` header. The workflow engine automatically attaches the correct authentication headers based on the execution context. Don't paste API keys or secrets into the `headers` block; they belong on a configured connector.
:::

### Example: Unisolate a host

This example calls the Security endpoint management API to unisolate a host.

```yaml
- name: unisolate_endpoint
  type: kibana.request
  with:
    method: "POST"
    path: "/api/endpoint/action/unisolate"
    body:
      endpoint_ids: ["{{ event.alerts[0].elastic.agent.id }}"]
      comment: "Unisolating endpoint as part of automated cleanup."
```

## Deprecated aliases [deprecated-aliases]

The following `kibana.*` step types are deprecated in 9.4. They still resolve in existing workflows so that 9.3 automations keep running, but the editor blocks new workflows from using them. Use the `cases.*` replacements instead.

| Deprecated | Use instead |
|---|---|
| `kibana.createCaseDefaultSpace` | [`cases.createCase`](/explore-analyze/workflows/steps/cases.md#cases-createcase) |
| `kibana.getCaseDefaultSpace` | [`cases.getCase`](/explore-analyze/workflows/steps/cases.md#cases-getcase) |
| `kibana.updateCaseDefaultSpace` | [`cases.updateCase`](/explore-analyze/workflows/steps/cases.md#cases-updatecase) |
| `kibana.addCaseCommentDefaultSpace` | [`cases.addComment`](/explore-analyze/workflows/steps/cases.md#cases-addcomment) |

See [Migrate workflows from 9.3 to 9.4](/explore-analyze/workflows/authoring-techniques/migrate-from-9.3.md) for side-by-side replacement patterns.

## Related

- [Cases action steps](/explore-analyze/workflows/steps/cases.md): 27 step types for working with cases. Use these instead of the deprecated Case aliases above.
- [Streams action steps](/explore-analyze/workflows/steps/streams.md): Observability Streams operations.
- [Elasticsearch action steps](/explore-analyze/workflows/steps/elasticsearch.md): For {{es}} API calls.
