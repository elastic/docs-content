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

Use this reference when you build workflows that call Cases with `cases.*` step types. Each section matches one registered step: status, category, inputs, outputs, optional config, and error documentation.

## Cases - Create case (`cases.createCase`)

**Status:** Active

**Category:** {{kib}}

Creates a new case with the specified attributes.

This step creates a new case in the cases system. You can specify title, description, tags, assignees, severity, category, connector configuration, sync settings, and custom fields. The step returns the complete created case object. The step type string is `cases.createCase`. Documentation for generic {{kib}} actions also shows `kibana.createCaseDefaultSpace`; confirm which type string your deployment lists in the workflow editor.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `title` | string | Yes | _None_ | `"Security incident detected"` | Case title. |
| `description` | string | Yes | _None_ | `"Suspicious activity in logs"` | Case description. |
| `owner` | string | Yes | _None_ | `"securitySolution"` | Case owner (solution scope). |
| `tags` | array of strings | No | _None_ | `["security", "automated"]` | Case tags. |
| `severity` | string (enum) | No | _None_ | `"critical"` | Case severity level. |
| `category` | string | No | _None_ | `"Malware"` | Case category. |
| `assignees` | array of objects | No | _None_ | `[{ uid: "user-123" }]` | Each object uses `uid` (user profile id). Up to 10 assignees. |
| `settings` | object | No | _None_ | `syncAlerts: true` | Case settings such as `syncAlerts` and observable extraction flags. |
| `customFields` | array of objects | No | _None_ | `[{ key: "...", type: "text", value: "..." }]` | Each object has `key`, `type` (`text` or `toggle`), and `value`. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Later `cases.*` steps, expressions | Full case response (Cases API shape). |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after creation. |
| `connector-id` | string | No | _None_ | Selects a connector; the server resolves connector fields into the created case. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Cases - Get case by ID (`cases.getCase`)

**Status:** Active

**Category:** {{kib}}

Retrieves a case using its unique identifier.

This step retrieves a complete case object from the cases system using its ID. You can optionally include comments and attachments in the response.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `include_comments` | boolean | No | `false` | `true` | Include comments when `true`. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps, expressions | Full case response. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Find cases (`cases.findCases`)

**Status:** Active

**Category:** {{kib}}

Searches and filters cases.

This step searches cases and returns matching results, including pagination metadata and case status counters.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `assignees` | string or array of strings | No | _None_ | `"u_123"` | Filter by assignee identifiers. |
| `category` | string or array of strings | No | _None_ | `"Malware"` | Filter by category. |
| `customFields` | object | No | _None_ | _To be confirmed._ | Map of field keys to value arrays. |
| `defaultSearchOperator` | `AND` or `OR` | No | _None_ | `"AND"` | Combines search terms. |
| `from` | string | No | _None_ | `"2025-01-01"` | Start of time range (with `to`). |
| `owner` | string or array of strings | No | _None_ | `"securitySolution"` | Filter by case owner. |
| `page` | integer | No | `1` | `1` | Page number (positive). |
| `perPage` | integer | No | `20` | `20` | Page size; maximum `100`. |
| `reporters` | string or array of strings | No | _None_ | `"u_456"` | Filter by reporters. |
| `search` | string | No | _None_ | `"critical incident"` | Free-text search. |
| `searchFields` | string or array of strings | No | _None_ | `["title"]` | Fields to search; includes API search field enums plus `incremental_id.text`. |
| `severity` | string or array of strings | No | _None_ | `["high", "critical"]` | Filter by severity. |
| `sortField` | string (enum) | No | _None_ | `"updatedAt"` | One of `title`, `category`, `createdAt`, `updatedAt`, `closedAt`, `status`, `severity`. |
| `sortOrder` | `asc` or `desc` | No | _None_ | `"desc"` | Sort direction. |
| `status` | string or array of strings | No | _None_ | `"open"` | Filter by status. |
| `tags` | string or array of strings | No | _None_ | `["investigation"]` | Filter by tags. |
| `to` | string | No | _None_ | `"2025-12-31"` | End of time range. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `cases` | array of objects | Downstream steps | Matching cases; capped by server limits (large upper bound). |
| `count_closed_cases` | integer | Reporting, conditions | Closed count for the query context. |
| `count_in_progress_cases` | integer | Reporting, conditions | In-progress count. |
| `count_open_cases` | integer | Reporting, conditions | Open count. |
| `page` | integer | Pagination | Current page. |
| `per_page` | integer | Pagination | Page size used. |
| `total` | integer | Pagination | Total hits. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Find similar cases (`cases.findSimilarCases`)

**Status:** Active

**Category:** {{kib}}

Finds cases similar to the provided case ID.

This step returns cases similar to the given case, based on shared observables, with pagination metadata.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Source case. |
| `page` | integer | No | `1` | `1` | Page number (positive). |
| `perPage` | integer | No | `20` | `20` | Page size; maximum `100`. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `cases` | array of objects | Downstream steps | Each case includes `similarities.observables` with `typeKey`, `typeLabel`, and `value`. |
| `page` | integer | Pagination | Current page. |
| `per_page` | integer | Pagination | Page size used. |
| `total` | integer | Pagination | Total hits. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Cases - Update case (`cases.updateCase`)

**Status:** Active

**Category:** {{kib}}

Updates a case with the provided fields.

This step updates a case using the provided fields. If a version is provided, it is used directly. Otherwise, the step fetches the case to resolve the latest version before updating.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `updates` | object | Yes | _None_ | `status: "in-progress", severity: "high"` | At least one updatable field. Allowed keys include `title`, `description`, `status`, `severity`, `tags`, `category`, `settings`, `assignees`, `connector`, and `customFields` (Cases bulk update schema, without `id` or `version`). |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case response. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after update. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Update cases (`cases.updateCases`)

**Status:** Active

**Category:** {{kib}}

Updates multiple cases in one step.

This step updates multiple cases at once. Each case can provide a version directly or let the step fetch the latest version before applying updates.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `cases` | array of objects | Yes | _None_ | See example | Between 1 and 100 items. Each item has `case_id`, optional `version`, and `updates` (same shape as `cases.updateCase` updates). |

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

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `cases` | array of objects | Downstream steps | Updated case objects (up to 100). |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes cases after update. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Cases - Add comment (`cases.addComment`)

**Status:** Active

**Category:** {{kib}}

Adds a user comment to a case.

This step appends a new user comment to the selected case.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `comment` | string | Yes | _None_ | `"Investigating now."` | Maximum length 30,000 characters. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Case after comment is added. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the comment is added. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Set case severity (`cases.setSeverity`)

**Status:** Active

**Category:** {{kib}}

Sets severity for an existing case.

This step sets only the severity field of an existing case. If version is not provided, the latest case version is resolved automatically.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `severity` | string (enum) | Yes | _None_ | `"high"` | Case severity. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Set case status (`cases.setStatus`)

**Status:** Active

**Category:** {{kib}}

Sets status for an existing case.

This step sets only the status field of an existing case. If version is not provided, the latest case version is resolved automatically.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `status` | string (enum) | Yes | _None_ | `"in-progress"` | Case status. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Close case (`cases.closeCase`)

**Status:** Active

**Category:** {{kib}}

Closes an existing case.

This step closes an existing case by setting its status to `closed`. If version is not provided, the latest case version is resolved automatically.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Closed case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after close. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Delete cases (`cases.deleteCases`)

**Status:** Active

**Category:** {{kib}}

Deletes one or more cases.

This step deletes the provided cases, including their comments and user action history.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_ids` | array of strings | Yes | _None_ | `["id-1", "id-2"]` | Between 1 and 100 ids. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case_ids` | array of strings | Auditing, follow-up steps | Ids that were deleted. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| _None._ | — | — | — | This step has no step-level config schema in code. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Assign case (`cases.assignCase`)

**Status:** Active

**Category:** {{kib}}

Sets assignees for an existing case.

This step sets the assignees array on an existing case. The provided assignees become the full source of truth for assignment.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `assignees` | array of objects | Yes | _None_ | `[{ uid: "user-123" }]` | Up to 10 objects with `uid`. This value replaces the full assignee list on the case. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after assignment. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Unassign case (`cases.unassignCase`)

**Status:** Active

**Category:** {{kib}}

Removes assignees from an existing case.

This step removes the given assignees from an existing case. Use `assignees: null` to clear every assignee, or pass `uid` objects to remove specific users.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `assignees` | array of objects or null | Yes | _None_ | `null` | Use `null` to clear all assignees, or pass objects with `uid` to remove specific users (up to 10 per schema). |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Add alerts to case (`cases.addAlerts`)

**Status:** Active

**Category:** {{kib}}

Adds one or more alerts as case attachments.

This step adds alert attachments to an existing case. Each alert requires an `alertId` and source `index`; rule metadata is optional.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `alerts` | array of objects | Yes | _None_ | See below | Between 1 and 1000 alerts. Each object: `alertId` (string), `index` (string), optional `rule` (`id`, `name`). |

Example:

```yaml
alerts:
  - alertId: "alert-1"
    index: ".alerts-security.alerts-default"
    rule:
      id: "rule-1"
      name: "Suspicious process"
```

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Case after alerts are attached. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after attachments are added. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Add events to case (`cases.addEvents`)

**Status:** Active

**Category:** {{kib}}

Adds one or more events as case attachments.

This step adds event attachments to an existing case. Each event requires an `eventId` and source `index`.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `events` | array of objects | Yes | _None_ | See below | Between 1 and 1000 events. Each object: `eventId` (string), `index` (string). |

Example:

```yaml
events:
  - eventId: "event-1"
    index: ".ds-logs-*"
```

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Case after events are attached. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after attachments are added. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Add observables to case (`cases.addObservables`)

**Status:** Active

**Category:** {{kib}}

Adds one or more observables to a case.

This step adds observables to an existing case using `typeKey`, `value`, and optional description fields.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `observables` | array of objects | Yes | _None_ | See below | Between 1 and 50 items. Each object: `typeKey` (string), `value` (string), optional `description` (string or null). |

Example:

```yaml
observables:
  - typeKey: "ip"
    value: "10.0.0.8"
    description: "Source IP"
```

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after observables are added. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Add case tag (`cases.addTags`)

**Status:** Active

**Category:** {{kib}}

Sets tags for an existing case.

This step sets the full tags array on an existing case. Provide all tags that should remain on the case.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `tags` | array of strings | Yes | _None_ | `["investigation", "high-priority"]` | Complete tag list to store on the case. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after tags are updated. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Add case category (`cases.setCategory`)

**Status:** Active

**Category:** {{kib}}

Sets category for an existing case.

This step sets the category field on an existing case.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `category` | string | Yes | _None_ | `"Malware"` | Non-empty category value. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Set case description (`cases.setDescription`)

**Status:** Active

**Category:** {{kib}}

Sets description for an existing case.

This step sets only the description field of an existing case. If version is not provided, the latest case version is resolved automatically.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `description` | string | Yes | _None_ | `"Updated findings."` | Non-empty description. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |

---

## Set case title (`cases.setTitle`)

**Status:** Active

**Category:** {{kib}}

Sets title for an existing case.

This step sets only the title field of an existing case. If version is not provided, the latest case version is resolved automatically.

---

### Input (`with` block)

| Field | Type | Required | Default | Example | Notes |
|-------|------|----------|---------|---------|-------|
| `case_id` | string | Yes | _None_ | `"abc-123-def-456"` | Target case id. |
| `version` | string | No | _None_ | `"WzQ3LDFd"` | Optimistic concurrency; omit to resolve automatically. |
| `title` | string | Yes | _None_ | `"Updated incident title"` | Non-empty title. |

### Output

| Field | Type | Used by | Notes |
|-------|------|---------|-------|
| `case` | object | Downstream steps | Updated case. |

### Config

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `push-case` | boolean | No | `false` | When `true`, pushes the case after the change. |

### Error states

| Error | Condition | Notes |
|-------|-----------|-------|
| _No error states documented. Verify with developer before publishing._ | | |
