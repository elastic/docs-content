---
navigation_title: Cases
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about Cases workflow steps for creating, updating, searching, and attaching objects to cases in Elastic Workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Cases workflow steps

**Cases** workflow steps use the `cases.*` step types. They automate the [Cases](/explore-analyze/cases.md) APIs through named workflow actions so you can create and update cases, attach alerts and events, assign work, and search or remove cases without hand-authoring HTTP requests.

Implementation reference: [Kibana pull request 256922](https://github.com/elastic/kibana/pull/256922) (tracking issue: [elastic/security-team#15084](https://github.com/elastic/security-team/issues/15084)).

::::{note}
Exact step catalogs and validation rules ship with {{kib}}. Use the workflow **Actions** menu and step editor in {{kib}} to confirm `type` strings and required `with` fields for your deployment version.
::::

## Execution and permissions

Cases steps run **as the user or API key executing the workflow**, like other [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md). The principal must have the appropriate Cases permissions and access to the case owner (for example {{elastic-sec}} or {{observability}}). Refer to your solution's case documentation for roles and feature controls.

## When to use `cases.*` versus other {{kib}} steps

* **`cases.*` steps**: Use for full case lifecycle operations—attachments, assignees, category, bulk updates, and case search—using structured fields and stable outputs (typically `output.case` or lists of cases).
* **`kibana.createCaseDefaultSpace` and related `kibana.*` named actions**: May cover a narrower or default-space path; prefer `cases.*` when you need parity with Cases APIs used elsewhere in the product.
* **`kibana.request`**: Use for Cases HTTP APIs that do not yet have a named `cases.*` step, or for advanced options not exposed on a step ([generic request actions](/explore-analyze/workflows/steps/kibana.md#generic-request-actions)).

## Conventions

* **`case_id`**: Identifies the case targeted by a step. Often sourced from a prior step, for example `${{ steps.create_case.output.case.id }}`.
* **Optimistic concurrency**: Many updates require the current case **`version`**. Pass `version` from the latest `output.case.version` returned by the previous step that read or updated the case.
* **Outputs**: Most mutating steps return an updated **case** object (for example under `output.case`) so following steps can read `id`, `version`, and fields you changed.
* **Owners**: Workflows may expose an `owner` input (for example `securitySolution`)—align with the case owner configured in your solution.

## Step catalog

The following `cases.*` step types are introduced or expanded in [Kibana pull request 256922](https://github.com/elastic/kibana/pull/256922), alongside existing case steps such as `cases.createCase`, `cases.getCase`, `cases.updateCase`, and `cases.addComment`. Names and availability follow your {{kib}} version.

### Create, read, and close

| Step `type` | Summary |
|-------------|---------|
| `cases.createCase` | Create a new case (title, description, owner, tags, severity, settings). |
| `cases.getCase` | Fetches a case by ID; supports `include_comments` to load comments with the case. |
| `cases.updateCase` | Apply structured `updates` to a case (for example title, description, severity, status). |
| `cases.closeCase` | Closes a case when your workflow should finish the case lifecycle. |

### Find and delete

| Step `type` | Summary |
|-------------|---------|
| `cases.findCases` | List or search cases (for example by owner) with pagination (`page`, `perPage`). |
| `cases.findSimilarCases` | Find cases similar to a given case (`case_id` and pagination). |
| `cases.deleteCases` | Delete one or more cases in bulk (respects product limits for batch size). |

### Comments, tags, and fields

| Step `type` | Summary |
|-------------|---------|
| `cases.addComment` | Add a comment to a case. |
| `cases.addTags` | Add tags to a case. |
| `cases.setCategory` | Set the case category (requires current `version` where enforced). |
| `cases.setDescription` | Set the case description. |
| `cases.setSeverity` | Set severity. |
| `cases.setStatus` | Set workflow/status fields for the case. |
| `cases.setTitle` | Set the case title. |
| `cases.setCustomField` | Sets a custom field value. The step **might not appear** in the workflow UI until the workflow platform registers it; confirm in {{kib}} for your version. |
| `cases.updateCases` | Apply updates to multiple cases in one step (subject to maximum batch size). |

### People

| Step `type` | Summary |
|-------------|---------|
| `cases.assignCase` | Assign users to a case (for example by user `uid`). |
| `cases.unassignCase` | Remove assignees; `assignees` may be set to `null` to clear. |

### Attachments

| Step `type` | Summary |
|-------------|---------|
| `cases.addAlerts` | Attach detection alerts to a case (alert ID, index, rule metadata as required by the API). |
| `cases.addEvents` | Attach events (for example endpoint events) to a case. |
| `cases.addObservables` | Add observables to a case (subject to per-case observable limits in {{kib}}). |

::::{note}
Attaching alerts or events in the same workflow as other case mutations may **order dependencies** (for example closing a case before adding alerts). Structure steps accordingly; see the kitchen-sink example in [Kibana pull request 256922](https://github.com/elastic/kibana/pull/256922) for a full exercise of steps.
::::

## Example: Create a case and add a comment

```yaml
steps:
  - name: open_case
    type: cases.createCase
    with:
      title: "{{ inputs.case_title }}"
      description: "{{ inputs.case_description }}"
      owner: "{{ inputs.owner }}"
      tags: ["workflow"]
      severity: low
      settings:
        syncAlerts: false
        extractObservables: false

  - name: comment
    type: cases.addComment
    with:
      case_id: "${{ steps.open_case.output.case.id }}"
      comment: "Case opened from a workflow run."
```

## Related documentation

* [Cases in {{kib}}](/explore-analyze/cases.md)
* [Cases for {{elastic-sec}}](/solutions/security/investigate/security-cases.md)
* [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md): generic `kibana.request` and other named actions
* [Workflow steps overview](/explore-analyze/workflows/steps.md)

## Authoring template

To document another step family in the same style, start from [](/explore-analyze/workflows/steps/workflow-step-family-template.md).
