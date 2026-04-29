---
navigation_title: Cases
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the Cases action steps that let workflows create, query, update, attach content, and manage the lifecycle of cases in Kibana, Observability, and Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Cases action steps [workflows-cases-steps]

Cases action steps let workflows create, query, update, and manage cases. The `cases.*` namespace provides full coverage of the Cases API through a single, consistent set of step types so you can automate case workflows without leaving the Elastic platform.

Use Cases steps for patterns like:

- Create a case when a detection rule fires, then attach the alert and relevant observables.
- Open a case, assign it to an on-call user, and post a notification to a team channel.
- Find similar cases for deduplication before creating a new one.
- Close a case automatically when a condition is met, and append an analyst note first.

## Shared conventions [workflows-cases-conventions]

Every `cases.*` step shares the same conventions, so once you learn one step the others are predictable.

**Parameter casing.** Case-level parameters use `snake_case`: `case_id`, not `caseId`. The editor rejects camelCase for these fields. Individual payloads, such as the alert object attached by `cases.addAlerts`, use the casing of the originating API (for example, `alertId`, `index`) because they match external API shapes.

**Optional `push-case` config.** Most `cases.*` steps accept an optional top-level `push-case` boolean (defaults to `false`). When `true`, the step pushes the updated case to a connected external system (for example, {{jira}} or ServiceNow) after the workflow operation succeeds.

`push-case` applies only to steps that change a case. It is not supported on the read-only and internal steps: `cases.deleteCase`, `cases.findCases`, `cases.findSimilarCases`, `cases.getAllAttachments`, `cases.getCase`, `cases.getCases`, `cases.getCasesByAlertId`, and `cases.updateObservable`.

```yaml
- name: create_and_push
  type: cases.createCase
  push-case: true
  with:
    title: "Triage required"
    severity: high
```

**Getting the case ID.** The response from `cases.createCase` includes the new case ID at `steps.<step_name>.output.case.id`. Reference it in subsequent steps:

```yaml
- name: new_case
  type: cases.createCase
  with:
    title: "..."

- name: tag_case
  type: cases.addTags
  with:
    case_id: "{{ steps.new_case.output.case.id }}"
    tags: ["triaged"]
```

## Step catalog [workflows-cases-catalog]

The 27 Cases steps group into six operational categories. Jump to any step:

**Create, fetch, and search**
[`cases.createCase`](#cases-createcase) ·
[`cases.createCaseFromTemplate`](#cases-createcasefromtemplate) ·
[`cases.getCase`](#cases-getcase) ·
[`cases.getCases`](#cases-getcases) ·
[`cases.findCases`](#cases-findcases) ·
[`cases.findSimilarCases`](#cases-findsimilarcases) ·
[`cases.getCasesByAlertId`](#cases-getcasesbyalertid)

**Update fields**
[`cases.updateCase`](#cases-updatecase) ·
[`cases.updateCases`](#cases-updatecases) ·
[`cases.setStatus`](#cases-setstatus) ·
[`cases.setSeverity`](#cases-setseverity) ·
[`cases.setTitle`](#cases-settitle) ·
[`cases.setDescription`](#cases-setdescription) ·
[`cases.setCategory`](#cases-setcategory) ·
[`cases.setCustomField`](#cases-setcustomfield) ·
[`cases.closeCase`](#cases-closecase)

**Attach content**
[`cases.addComment`](#cases-addcomment) ·
[`cases.addAlerts`](#cases-addalerts) ·
[`cases.addEvents`](#cases-addevents) ·
[`cases.addObservables`](#cases-addobservables) ·
[`cases.getAllAttachments`](#cases-getallattachments)

**Tags and assignees**
[`cases.addTags`](#cases-addtags) ·
[`cases.assignCase`](#cases-assigncase) ·
[`cases.unassignCase`](#cases-unassigncase)

**Update and delete observables**
[`cases.updateObservable`](#cases-updateobservable) ·
[`cases.deleteObservable`](#cases-deleteobservable)

**Delete**
[`cases.deleteCases`](#cases-deletecases)

---

## Create, fetch, and search

### `cases.createCase` [cases-createcase]

Create a case with a title, description, severity, tags, and optional assignees. Accepts an optional top-level `connector-id` to associate the case with a configured external connector (for example, {{jira}} or ServiceNow).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | ID of a configured external connector to attach to the case. |
| `title` | `with` | string | Yes | Case title. |
| `description` | `with` | string | Yes | Case description. Markdown supported. |
| `owner` | `with` | string | Yes | Case owner: `securitySolution`, `observability`, or `cases`. |
| `severity` | `with` | string | No | `low`, `medium`, `high`, or `critical`. |
| `tags` | `with` | `string[]` | No | Tags to apply to the case. |
| `assignees` | `with` | array | No | Array of `{ uid }` objects. |
| `category` | `with` | string | No | Case category. |
| `customFields` | `with` | array | No | Custom field values. |
| `settings` | `with` | object | No | Case settings, for example `syncAlerts`. |

```yaml
- name: create_case
  type: cases.createCase
  with:
    title: "{{ event.rule.name }} on {{ event.alerts[0].host.name }}"
    description: "Automatically created from detection rule."
    severity: high
    tags: ["auto-triage", "malware"]
    owner: "securitySolution"
```

### `cases.createCaseFromTemplate` [cases-createcasefromtemplate]

Create a case from a configured case template. Useful when a team has pre-defined case shapes (default title, description, tags, severity) for common scenarios.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_template_id` | `with` | string | Yes | ID of the template to apply. |
| `overwrites` | `with` | object | No | Fields to override on the templated case, for example `title`, `tags`. |

```yaml
- name: create_from_template
  type: cases.createCaseFromTemplate
  with:
    case_template_id: "malware-triage-template"
    overwrites:
      title: "Malware: {{ event.alerts[0].host.name }}"
```

### `cases.getCase` [cases-getcase]

Retrieve a complete case object by ID. Optionally include comments and attachments in the response.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `include_comments` | `with` | boolean | Yes | Whether to include comments and attachments in the response. |

```yaml
- name: fetch_case
  type: cases.getCase
  with:
    case_id: "{{ inputs.case_id }}"
    include_comments: true
```

### `cases.getCases` [cases-getcases]

Retrieve up to 1000 cases in a single request. IDs that can't be fetched are reported in the `errors` array on the output. Use this to avoid N sequential `cases.getCase` calls in fan-out workflows.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_ids` | `with` | `string[]` | Yes | Array of case IDs. Maximum 1000. |

Output: `{ cases: array, errors: array }`. The `errors` array contains entries for any IDs that couldn't be fetched.

```yaml
- name: fetch_cases
  type: cases.getCases
  with:
    case_ids: ["case-1", "case-2", "case-3"]
```

### `cases.findCases` [cases-findcases]

Search for cases matching filter criteria. Supports paging, sorting, and filtering by many fields. The output includes a `cases` array plus per-status counts (`count_open_cases`, `count_in_progress_cases`, `count_closed_cases`), `page`, `per_page`, and `total`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `search` | `with` | string | No | Free-text search. |
| `searchFields` | `with` | `string \| string[]` | No | Fields to search in. |
| `defaultSearchOperator` | `with` | string | No | `AND` or `OR` for multi-term search. |
| `status` | `with` | `string \| string[]` | No | Filter by status. |
| `severity` | `with` | `string \| string[]` | No | Filter by severity. |
| `tags` | `with` | `string \| string[]` | No | Filter by tag. |
| `category` | `with` | `string \| string[]` | No | Filter by category. |
| `owner` | `with` | `string \| string[]` | No | Filter by case owner. |
| `assignees` | `with` | `string \| string[]` | No | Filter by assignee UID. |
| `reporters` | `with` | `string \| string[]` | No | Filter by reporter. |
| `customFields` | `with` | object | No | Map of custom-field ID to allowed values. |
| `from` | `with` | string | No | Start of the time range. |
| `to` | `with` | string | No | End of the time range. |
| `page` | `with` | number | No | Page number. Defaults to `1`. |
| `perPage` | `with` | number | No | Results per page. Defaults to `20`. |
| `sortField` | `with` | string | No | `title`, `category`, `createdAt`, `updatedAt`, `closedAt`, `status`, or `severity`. |
| `sortOrder` | `with` | string | No | `asc` or `desc`. |

```yaml
- name: find_open_high_sev
  type: cases.findCases
  with:
    owner: "securitySolution"
    status: "open"
    severity: ["high", "critical"]
    tags: ["investigation"]
    sortField: "updatedAt"
    sortOrder: "desc"
    perPage: 20
```

### `cases.findSimilarCases` [cases-findsimilarcases]

Find cases similar to a given case, matched by shared observables. Useful for deduplication before creating a new case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Source case ID to find similar cases for. |
| `page` | `with` | integer | Yes | Page number (1-based). |
| `perPage` | `with` | integer | Yes | Results per page. |

The output includes a `cases` array, `page`, and `per_page`.

```yaml
- name: find_similar
  type: cases.findSimilarCases
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    page: 1
    perPage: 20
```

### `cases.getCasesByAlertId` [cases-getcasesbyalertid]

Find every case that contains a specific alert. The canonical "does a case already exist for this alert?" query.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `alert_id` | `with` | string | Yes | Alert signal ID. |
| `owner` | `with` | string | No | Filter by case owner. |

```yaml
- name: check_existing
  type: cases.getCasesByAlertId
  with:
    alert_id: "{{ event.alerts[0]._id }}"
```

---

## Update fields

### `cases.updateCase` [cases-updatecase]

Update one case's fields. Changes go inside a required `updates` object. An optional `version` field enforces optimistic concurrency.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `version` | `with` | string | No | Case version for optimistic concurrency. |
| `updates` | `with` | object | Yes | Fields to update. At least one field required. Includes `title`, `description`, `status`, `severity`, `category`, `tags`, `assignees`, `settings`, and more. |

```yaml
- name: escalate
  type: cases.updateCase
  with:
    case_id: "{{ steps.find.output.cases[0].id }}"
    updates:
      status: "in-progress"
      severity: "critical"
      tags: ["escalated"]
```

:::{important}
Update fields must sit inside the `updates` object, not at the top level of `with`. `updates: { status: open }` is valid; `with: { status: open, case_id: ... }` is not.
:::

### `cases.updateCases` [cases-updatecases]

Bulk-update multiple cases. Each element specifies its own `case_id`, optional `version`, and `updates` object.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `cases` | `with` | array | Yes | Array of `{ case_id, version?, updates }` objects. |

```yaml
- name: bulk_close
  type: cases.updateCases
  with:
    cases:
      - case_id: "c1"
        updates:
          status: "closed"
      - case_id: "c2"
        updates:
          status: "closed"
```

### `cases.setStatus` [cases-setstatus]

Set a case's status.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `status` | `with` | string | Yes | `open`, `in-progress`, or `closed`. |

```yaml
- name: mark_in_progress
  type: cases.setStatus
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    status: "in-progress"
```

### `cases.setSeverity` [cases-setseverity]

Set a case's severity.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `severity` | `with` | string | Yes | `low`, `medium`, `high`, or `critical`. |

### `cases.setTitle` [cases-settitle]

Update a case's title.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `title` | `with` | string | Yes | New title. |

### `cases.setDescription` [cases-setdescription]

Update a case's description.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `description` | `with` | string | Yes | New description. Markdown supported. |

### `cases.setCategory` [cases-setcategory]

Set a case's category.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `category` | `with` | string | Yes | Category name. |
| `owner` | `with` | string | No | Case owner. Optional, helps with auto-completion. |

### `cases.setCustomField` [cases-setcustomfield]

Set a single custom-field value on a case. The `field_name` parameter is the system-set custom-field identifier (a UUID-style string), not the human-readable label you see in the UI.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `field_name` | `with` | string | Yes | Custom-field identifier. System-set, typically a UUID. |
| `value` | `with` | `string \| number \| boolean` | Yes | Field value. |
| `owner` | `with` | string | No | Case owner. Optional, helps with auto-completion. |
| `version` | `with` | string | No | Case version for optimistic concurrency. |

```yaml
- name: set_investigation_owner
  type: cases.setCustomField
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    field_name: "4b8c9d2e-1a5f-4f7a-9c3b-2d6e8f1a3b5c"
    value: "soc-team"
```

### `cases.closeCase` [cases-closecase]

Close a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `version` | `with` | string | No | Case version for optimistic concurrency. |

```yaml
- name: close_case
  type: cases.closeCase
  with:
    case_id: "{{ steps.find.output.cases[0].id }}"
```

To record why a case was closed, pair with `cases.addComment` beforehand:

```yaml
- name: note_reason
  type: cases.addComment
  with:
    case_id: "{{ inputs.case_id }}"
    comment: "Closing: duplicate of case {{ inputs.duplicate_of }}."

- name: close
  type: cases.closeCase
  with:
    case_id: "{{ inputs.case_id }}"
```

---

## Attach content

### `cases.addComment` [cases-addcomment]

Add a Markdown-formatted comment to a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `comment` | `with` | string | Yes | Comment body. |

```yaml
- name: add_triage_note
  type: cases.addComment
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    comment: |
      AI classification: **{{ steps.classify.output.category }}**

      Rationale: {{ steps.classify.output.rationale }}
```

### `cases.addAlerts` [cases-addalerts]

Attach detection alerts to a case. Each entry is an **object** with `alertId` and `index`; the optional `rule` describes the rule that generated the alert.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `alerts` | `with` | array | Yes | Array of `{ alertId, index, rule? }` objects. |

```yaml
- name: attach_alert
  type: cases.addAlerts
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    alerts:
      - alertId: "{{ event.alerts[0]._id }}"
        index: "{{ event.alerts[0]._index }}"
        rule:
          id: "{{ event.rule.id }}"
          name: "{{ event.rule.name }}"
```

:::{important}
`alerts` takes an array of objects, not an array of ID strings. Each alert object requires both `alertId` and the `index` where the alert document lives. Cases uses both to resolve the alert document.
:::

### `cases.addEvents` [cases-addevents]

Attach arbitrary event documents to a case. Each entry is `{ eventId, index }`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `events` | `with` | array | Yes | Array of `{ eventId, index }` objects. |

```yaml
- name: attach_context_events
  type: cases.addEvents
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    events:
      - eventId: "{{ steps.search_context.output.hits.hits[0]._id }}"
        index: "{{ steps.search_context.output.hits.hits[0]._index }}"
```

### `cases.addObservables` [cases-addobservables]

Add observables (indicators of compromise such as IPs, file hashes, domains, or URLs) to a case. `typeKey` must match one of the built-in observable types in {{elastic-sec}}.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `observables` | `with` | array | Yes | Array of `{ typeKey, value, description? }` objects. |

```yaml
- name: add_iocs
  type: cases.addObservables
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    observables:
      - typeKey: "observable-type-ipv4"
        value: "{{ event.alerts[0].source.ip }}"
        description: "Source of malicious activity"
      - typeKey: "observable-type-hash-sha256"
        value: "{{ event.alerts[0].file.hash.sha256 }}"
```

The `typeKey` must match one of the built-in observable type keys. Examples of accepted values include: `observable-type-ipv4`, `observable-type-ipv6`, `observable-type-url`, `observable-type-domain`, `observable-type-hash-sha256`, `observable-type-hash-md5`

### `cases.getAllAttachments` [cases-getallattachments]

Fetch every attachment associated with a case without pagination. Use this when you need the complete set of attachments for decision-making, for example when checking evidence before closing or escalating.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |

The output is a list of attachments associated with the case you specified.

```yaml
- name: list_attachments
  type: cases.getAllAttachments
  with:
    case_id: "{{ inputs.case_id }}"
```

---

## Tags and assignees

### `cases.addTags` [cases-addtags]

Add tags to a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `tags` | `with` | `string[]` | Yes | Tags to add. |

### `cases.assignCase` [cases-assigncase]

Assign a case to one or more users.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `assignees` | `with` | array | Yes | Array of `{ uid }` objects. |

```yaml
- name: assign_oncall
  type: cases.assignCase
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    assignees:
      - uid: "{{ consts.oncall_uid }}"
```

### `cases.unassignCase` [cases-unassigncase]

Remove assignees from a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `assignees` | `with` | array | Yes | Array of `{ uid }` objects to remove. Pass an empty array (`[]`) to remove all assignees from the case. |

---

## Update and delete observables

### `cases.updateObservable` [cases-updateobservable]

Update an existing observable on a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `observable_id` | `with` | string | Yes | Observable ID. |
| `value` | `with` | string | Yes | Updated value. |
| `description` | `with` | `string \| null` | No | Updated description. |

### `cases.deleteObservable` [cases-deleteobservable]

Remove an observable from a case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_id` | `with` | string | Yes | Case ID. |
| `observable_id` | `with` | string | Yes | Observable ID. |

---

## Delete

### `cases.deleteCases` [cases-deletecases]

Delete one or more cases permanently, including their attachments and comments.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `case_ids` | `with` | `string[]` | Yes | Array of case IDs to delete. |

```yaml
- name: cleanup
  type: cases.deleteCases
  with:
    case_ids: ["old-case-1", "old-case-2"]
```

:::{warning}
Deleted cases can't be recovered. If you don't want to permanently delete a case, use [`cases.closeCase`](#cases-closecase) instead.
:::

## Migrating from `kibana.*` case aliases [workflows-cases-migration]

In 9.3, case management lived under the `kibana.*` namespace. Those step types remain as deprecated aliases so existing workflows keep running, but new workflows must use `cases.*`:

| Deprecated (9.3 alias) | Current (9.4) |
|---|---|
| `kibana.createCaseDefaultSpace` | [`cases.createCase`](#cases-createcase) |
| `kibana.getCaseDefaultSpace` | [`cases.getCase`](#cases-getcase) |
| `kibana.updateCaseDefaultSpace` | [`cases.updateCase`](#cases-updatecase) |
| `kibana.addCaseCommentDefaultSpace` | [`cases.addComment`](#cases-addcomment) |

Refer to [Migrate from 9.3 to 9.4](/explore-analyze/workflows/authoring-techniques/migrate-from-9.3.md) for side-by-side replacement patterns.

## Related

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): The primary source of cases in a SOC workflow.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Use an AI classification or summary to enrich a case description.
- [Kibana Cases documentation](/solutions/security/investigate/security-cases.md): The Cases feature in {{elastic-sec}}.
