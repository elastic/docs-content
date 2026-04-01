---
navigation_title: Cases
applies_to:
  stack: preview 9.3
  serverless: preview
description: Reference for Cases workflow action steps that use cases.* type strings in {{kib}}.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Cases workflow steps

Use this reference when you build workflows that call Cases with `cases.*` step types. Steps are grouped by what they do (for example, finding cases versus updating one field). Expand a group in the on-page table of contents, then open the step you need.

## Create, find, and load cases

Create a case, load one by id, search the case list, or find cases that look like an existing case.

### Cases - Create case

**Step type:** `cases.createCase`

This step creates a new case in the cases system. You can specify title, description, tags, assignees, severity, category, connector configuration, sync settings, and custom fields. The step returns the complete created case object. Documentation for generic {{kib}} actions also shows `kibana.createCaseDefaultSpace`; confirm which type string your deployment lists in the workflow editor.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | string | Yes | _None_ | Case title. Example accepted values include `"Security incident detected"`. |
| `description` | string | Yes | _None_ | Case description. Example accepted values include `"Suspicious activity in logs"`. |
| `owner` | string | Yes | _None_ | Case owner (solution scope). Example accepted values include `"securitySolution"`. |
| `tags` | array of strings | No | _None_ | Case tags. Example accepted values include `["security", "automated"]`. |
| `severity` | string (enum) | No | _None_ | Case severity level. Example accepted values include `"critical"`. |
| `category` | string | No | _None_ | Case category. Example accepted values include `"Malware"`. |
| `assignees` | array of objects | No | _None_ | Each object uses `uid` (user profile id). Up to 10 assignees. Example accepted values include `[{ uid: "user-123" }]`. |
| `settings` | object | No | _None_ | Case settings such as `syncAlerts` and observable extraction flags. Example accepted values include `syncAlerts: true`. |
| `customFields` | array of objects | No | _None_ | Each object has `key`, `type` (`text` or `toggle`), and `value`. Example accepted values include `[{ key: "...", type: "text", value: "..." }]`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Later `cases.*` steps, expressions | Full case document from the Cases API. Example: read `steps.<step_name>.output.case.id` or `steps.<step_name>.output.case.version` in a following step. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after creation. Example accepted values: `false` (default) or `true`. |
| `connector-id` | string | No | _None_ | Selects a connector; the server resolves connector fields into the created case. Example: id string from your connector configuration (not the literal `none` connector unless that is the stored id). |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Cases - Get case by ID

**Step type:** `cases.getCase`

This step retrieves a complete case object from the cases system using its ID. You can optionally include comments and attachments in the response.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `include_comments` | boolean | No | `false` | Include comments when `true`. Example accepted values include `true`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps, expressions | Full case document. Example: `steps.<step_name>.output.case` for `id`, `version`, and other fields. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Find cases

**Step type:** `cases.findCases`

This step searches cases and returns matching results, including pagination metadata and case status counters.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `assignees` | string or array of strings | No | _None_ | Filter by assignee identifiers. Example accepted values include `"u_123"`. |
| `category` | string or array of strings | No | _None_ | Filter by category. Example accepted values include `"Malware"`. |
| `customFields` | object | No | _None_ | Map of field keys to value arrays. Accepted value shape: _To be confirmed._ |
| `defaultSearchOperator` | `AND` or `OR` | No | _None_ | Combines search terms. Example accepted values include `"AND"`. |
| `from` | string | No | _None_ | Start of time range (with `to`). Example accepted values include `"2025-01-01"`. |
| `owner` | string or array of strings | No | _None_ | Filter by case owner. Example accepted values include `"securitySolution"`. |
| `page` | integer | No | `1` | Page number (positive). Example accepted values include `1`. |
| `perPage` | integer | No | `20` | Page size; maximum `100`. Example accepted values include `20`. |
| `reporters` | string or array of strings | No | _None_ | Filter by reporters. Example accepted values include `"u_456"`. |
| `search` | string | No | _None_ | Free-text search. Example accepted values include `"critical incident"`. |
| `searchFields` | string or array of strings | No | _None_ | Fields to search; includes API search field enums plus `incremental_id.text`. Example accepted values include `["title"]`. |
| `severity` | string or array of strings | No | _None_ | Filter by severity. Example accepted values include `["high", "critical"]`. |
| `sortField` | string (enum) | No | _None_ | One of `title`, `category`, `createdAt`, `updatedAt`, `closedAt`, `status`, `severity`. Example accepted values include `"updatedAt"`. |
| `sortOrder` | `asc` or `desc` | No | _None_ | Sort direction. Example accepted values include `"desc"`. |
| `status` | string or array of strings | No | _None_ | Filter by status. Example accepted values include `"open"`. |
| `tags` | string or array of strings | No | _None_ | Filter by tags. Example accepted values include `["investigation"]`. |
| `to` | string | No | _None_ | End of time range. Example accepted values include `"2025-12-31"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `cases` | array of objects | Downstream steps | Cases that matched the filters. Example: first hit id `steps.<step_name>.output.cases[0].id`. |
| `count_closed_cases` | integer | Reporting, conditions | Closed cases in the result set. Example: `0` when none closed. |
| `count_in_progress_cases` | integer | Reporting, conditions | In-progress cases in the result set. Example: compare to `total`. |
| `count_open_cases` | integer | Reporting, conditions | Open cases in the result set. Example: use in conditions or dashboards. |
| `page` | integer | Pagination | Page index returned. Example: `1` with default `page` input. |
| `per_page` | integer | Pagination | Page size applied. Example: `20` with default `perPage` input. |
| `total` | integer | Pagination | Total matching cases before paging. Example: drive loop exit conditions. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Find similar cases

**Step type:** `cases.findSimilarCases`

This step returns cases similar to the given case, based on shared observables, with pagination metadata.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Source case. Example accepted values include `"abc-123-def-456"`. |
| `page` | integer | No | `1` | Page number (positive). Example accepted values include `1`. |
| `perPage` | integer | No | `20` | Page size; maximum `100`. Example accepted values include `20`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `cases` | array of objects | Downstream steps | Similar cases; each item includes `similarities.observables` (`typeKey`, `typeLabel`, `value`). Example: `steps.<step_name>.output.cases[0].id`. |
| `page` | integer | Pagination | Page index returned. Example: `1` with default input. |
| `per_page` | integer | Pagination | Page size applied. Example: `20` with default input. |
| `total` | integer | Pagination | Count of similar cases found. Example: `0` when none match. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Update case content

Apply broad edits to one case or batch the same pattern across many cases.

### Cases - Update case

**Step type:** `cases.updateCase`

This step updates a case using the provided fields. If a version is provided, it is used directly. Otherwise, the step fetches the case to resolve the latest version before updating.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `updates` | object | Yes | _None_ | At least one updatable field. Allowed keys include `title`, `description`, `status`, `severity`, `tags`, `category`, `settings`, `assignees`, `connector`, and `customFields` (Cases bulk update schema, without `id` or `version`). Example accepted values include `status: "in-progress", severity: "high"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Case after the update, including a new `version` when the server bumps it. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after update. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Update cases

**Step type:** `cases.updateCases`

This step updates multiple cases at once. Each case can provide a version directly or let the step fetch the latest version before applying updates.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `cases` | array of objects | Yes | _None_ | Between 1 and 100 items. Each item has `case_id`, optional `version`, and `updates` (same shape as `cases.updateCase` updates). See the YAML example below for shape and accepted values. |

Example:

```yaml
cases:
  - case_id: "abc-123-def-456"
    updates:
      status: "in-progress"
  - case_id: "ghi-789-jkl-012"
    version: "WzQ3LDFd"
    updates:
      title: "Use provided version"
```

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `cases` | array of objects | Downstream steps | Updated cases in the same order as the input list (up to 100). Example: `steps.<step_name>.output.cases[0].version`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes cases after update. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Comments

### Cases - Add comment

**Step type:** `cases.addComment`

This step appends a new user comment to the selected case.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `comment` | string | Yes | _None_ | Maximum length 30,000 characters. Example accepted values include `"Investigating now."`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Case after the comment is added. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the comment is added. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Update one field at a time

These steps change a single attribute (or replace the full tag list) without sending a full `updates` object.

### Set case severity

**Step type:** `cases.setSeverity`

This step sets only the severity field of an existing case. If version is not provided, the latest case version is resolved automatically.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `severity` | string (enum) | Yes | _None_ | Case severity. Example accepted values include `"high"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Set case status

**Step type:** `cases.setStatus`

This step sets only the status field of an existing case. If version is not provided, the latest case version is resolved automatically.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `status` | string (enum) | Yes | _None_ | Case status. Example accepted values include `"in-progress"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Set case title

**Step type:** `cases.setTitle`

This step sets only the title field of an existing case. If version is not provided, the latest case version is resolved automatically.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `title` | string | Yes | _None_ | Non-empty title. Example accepted values include `"Updated incident title"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Set case description

**Step type:** `cases.setDescription`

This step sets only the description field of an existing case. If version is not provided, the latest case version is resolved automatically.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `description` | string | Yes | _None_ | Non-empty description. Example accepted values include `"Updated findings."`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Add case category

**Step type:** `cases.setCategory`

This step sets the category field on an existing case.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `category` | string | Yes | _None_ | Non-empty category value. Example accepted values include `"Malware"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Add case tag

**Step type:** `cases.addTags`

This step sets the full tags array on an existing case. Provide all tags that should remain on the case.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `tags` | array of strings | Yes | _None_ | Complete tag list to store on the case. Example accepted values include `["investigation", "high-priority"]`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after tags are updated. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Close or delete cases

### Close case

**Step type:** `cases.closeCase`

This step closes an existing case by setting its status to `closed`. If version is not provided, the latest case version is resolved automatically.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Case with status `closed`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after close. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Delete cases

**Step type:** `cases.deleteCases`

This step deletes the provided cases, including their comments and user action history.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_ids` | array of strings | Yes | _None_ | Between 1 and 100 ids. Example accepted values include `["id-1", "id-2"]`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case_ids` | array of strings | Auditing, follow-up steps | Confirms which ids were removed. Example: same list as input when the delete succeeds. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Assignees

### Assign case

**Step type:** `cases.assignCase`

This step sets the assignees array on an existing case. The provided assignees become the full source of truth for assignment.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `assignees` | array of objects | Yes | _None_ | Up to 10 objects with `uid`. This value replaces the full assignee list on the case. Example accepted values include `[{ uid: "user-123" }]`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after assignment. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Unassign case

**Step type:** `cases.unassignCase`

This step removes the given assignees from an existing case. Use `assignees: null` to clear every assignee, or pass `uid` objects to remove specific users.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `version` | string | No | _None_ | Optimistic concurrency; omit to resolve automatically. Example accepted values include `"WzQ3LDFd"`. |
| `assignees` | array of objects or null | Yes | _None_ | Use `null` to clear all assignees, or pass objects with `uid` to remove specific users (up to 10 per schema). Example accepted values include `null`. |

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

## Attach alerts, events, or observables

Link alerts or events from indices, or add observables derived from investigation data.

### Add alerts to case

**Step type:** `cases.addAlerts`

This step adds alert attachments to an existing case. Each alert requires an `alertId` and source `index`; rule metadata is optional.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `alerts` | array of objects | Yes | _None_ | Between 1 and 1000 alerts. Each object: `alertId` (string), `index` (string), optional `rule` (`id`, `name`). See the YAML example below for shape and accepted values. |

Example:

```yaml
alerts:
  - alertId: "alert-1"
    index: ".alerts-security.alerts-default"
    rule:
      id: "rule-1"
      name: "Suspicious process"
```

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Case after alerts are attached. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after attachments are added. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Add events to case

**Step type:** `cases.addEvents`

This step adds event attachments to an existing case. Each event requires an `eventId` and source `index`.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `events` | array of objects | Yes | _None_ | Between 1 and 1000 events. Each object: `eventId` (string), `index` (string). See the YAML example below for shape and accepted values. |

Example:

```yaml
events:
  - eventId: "event-1"
    index: ".ds-logs-*"
```

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Case after events are attached. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after attachments are added. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |

### Add observables to case

**Step type:** `cases.addObservables`

This step adds observables to an existing case using `typeKey`, `value`, and optional description fields.

#### Input (`with` block)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `case_id` | string | Yes | _None_ | Target case id. Example accepted values include `"abc-123-def-456"`. |
| `observables` | array of objects | Yes | _None_ | Between 1 and 50 items. Each object: `typeKey` (string), `value` (string), optional `description` (string or null). See the YAML example below for shape and accepted values. |

Example:

```yaml
observables:
  - typeKey: "ip"
    value: "10.0.0.8"
    description: "Source IP"
```

#### Output

| Field | Type | Used by | Description |
|-------|------|---------|-------------|
| `case` | object | Downstream steps | Updated case with refreshed fields and `version`. Example: `steps.<step_name>.output.case`. |

#### Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after observables are added. Example accepted values: `false` (default) or `true`. |

#### Error states

| Error | Condition | Description |
|-------|-----------|-------------|
| _No error states documented. Verify with developer before publishing._ | | |
