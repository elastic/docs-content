---
navigation_title: Migrate workflows from 9.3 to 9.4
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Port workflows from the 9.3 technical preview to 9.4 GA. Covers the Cases namespace migration, HTTP timeout relocation, and schedule minimum interval.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Migrate workflows from 9.3 to 9.4 [workflows-migrate-from-9.3]

9.4 brings a handful of breaking changes to the workflow schema. Existing 9.3 workflows continue to run (the deprecated step aliases still resolve), but the editor blocks you from creating new workflows that use the old shapes, and several new capabilities are only available through the new shapes.

This guide is the side-by-side for the three migrations every 9.3 workflow author needs.

## Summary

| Change | Old (9.3) | New (9.4) | What happens to existing workflows |
|---|---|---|---|
| Case management | `kibana.createCaseDefaultSpace`, `kibana.getCaseDefaultSpace`, `kibana.updateCaseDefaultSpace`, `kibana.addCaseCommentDefaultSpace` | `cases.createCase`, `cases.getCase`, `cases.updateCase`, `cases.addComment` (plus 23 additional `cases.*` steps) | Deprecated aliases still work. New workflows must use `cases.*`. |
| HTTP step `timeout` | Inside `with` | At the step top level (common field) | Existing workflows auto-migrate on save. |
| Scheduled trigger interval minimum | Any duration | Minimum `1m` / `60s` | Sub-minute intervals auto-migrate to `1m` on first edit. |

## 1. Cases: `kibana.*` aliases to `cases.*` [workflows-migrate-cases]

Case management moved out of the `kibana.*` namespace into its own `cases.*` namespace, and the new namespace uses `snake_case` parameters instead of the old `camelCase`.

9.4 also adds many new case steps that have no 9.3 equivalent. Check [Cases action steps](/explore-analyze/workflows/steps/cases.md) for the complete catalog.

### Create a case

```yaml
# Old (9.3 — deprecated alias still works)
- name: open_case
  type: kibana.createCaseDefaultSpace
  with:
    title: "Alert on host-1"
    description: "..."
    severity: "high"
```

```yaml
# New (9.4)
- name: open_case
  type: cases.createCase
  with:
    title: "Alert on host-1"
    description: "..."
    severity: "high"
    owner: "securitySolution"
```

### Fetch a case

```yaml
# Old
- type: kibana.getCaseDefaultSpace
  with:
    caseId: "abc-123"
```

```yaml
# New
- type: cases.getCase
  with:
    case_id: "abc-123"
```

Note the parameter rename: `caseId` (camelCase) becomes `case_id` (snake_case). This pattern applies to every parameter in the `cases.*` namespace.

### Update a case

The new `cases.updateCase` wraps the field changes in a required `updates` object:

```yaml
# Old
- type: kibana.updateCaseDefaultSpace
  with:
    caseId: "abc-123"
    status: "closed"
    severity: "low"
```

```yaml
# New — fields go inside `updates`
- type: cases.updateCase
  with:
    case_id: "abc-123"
    updates:
      status: "closed"
      severity: "low"
```

For single-field changes, use the dedicated setters:

```yaml
- type: cases.setStatus
  with:
    case_id: "abc-123"
    status: "closed"
```

### Add a comment

```yaml
# Old
- type: kibana.addCaseCommentDefaultSpace
  with:
    caseId: "abc-123"
    comment: "Analyst note"
```

```yaml
# New
- type: cases.addComment
  with:
    case_id: "abc-123"
    comment: "Analyst note"
```

## 2. HTTP step `timeout` relocation [workflows-migrate-http-timeout]

In 9.3, the `http` step accepted `timeout` inside `with`. In 9.4, `timeout` is a standard common step field at the step top level, alongside `if`, `foreach`, `on-failure`, and others.

```yaml
# Old
- type: http
  with:
    url: "https://example.com/webhook"
    timeout: "30s"
```

```yaml
# New
- type: http
  timeout: "30s"
  with:
    url: "https://example.com/webhook"
```

Existing workflows auto-migrate on save. New workflows must use the new shape.

## 3. Scheduled trigger minimum interval [workflows-migrate-scheduled]

9.3 accepted any `with.every` value on a scheduled trigger, including sub-minute intervals such as `30s`. 9.4 enforces a minimum of `1m` / `60s`.

```yaml
# Old (9.3 — accepted)
triggers:
  - type: scheduled
    with:
      every: "30s"
```

```yaml
# New (9.4 — rejected at save time)
triggers:
  - type: scheduled
    with:
      every: "1m"   # minimum
```

Existing 9.3 workflows with sub-minute intervals auto-migrate to `1m` when first edited.

:::{tip}
If `every: "30s"` was a proxy for reacting quickly to something, consider switching to an [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) or an [event-driven trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md). Scheduled polling is the slowest of the three trigger types.
:::

## What else is new in 9.4 [workflows-whats-new-9.4]

Beyond the breaking changes, 9.4 adds many capabilities that don't require you to change existing workflows but are available for new ones:

- **Workflows is enabled by default.** The `workflows:ui:enabled` advanced setting now defaults to `true` on deployments with the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
- **27 `cases.*` steps.** Full Cases API coverage. To learn more, refer to [Cases action steps](/explore-analyze/workflows/steps/cases.md).
- **Composition (technical preview).** Call child workflows with typed inputs and outputs. To learn more, refer to [Composition steps](/explore-analyze/workflows/steps/composition.md).
- **Human-in-the-loop.** Pause a workflow and resume after a human provides input. To learn more, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).
- **Event-driven triggers (technical preview).** React to other workflow failures. To learn more, refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md).
- **`while` and `switch` flow control.** Even more control over workflow logic. To learn more, refer to [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md).
- **Expanded AI steps.** `ai.classify` and `ai.summarize` join `ai.prompt` and `ai.agent`. To learn more, refer to [AI steps](/explore-analyze/workflows/steps/ai-steps.md).
- **Data transformation steps.** 11 `data.*` steps for inline data work: filter, map, aggregate, parse JSON, regex extract, and more. To learn more, refer to [Data action steps](/explore-analyze/workflows/steps/data.md).

## Related

- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Complete `cases.*` reference.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): `while`, `switch`, and the other flow-control types added in 9.4.
- [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md): Trigger configuration reference.
