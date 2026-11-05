---
navigation_title: Cases
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Use Cases action steps to create, update, and manage cases from a workflow. Find the right step for a task and learn how steps pass a case between them.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Cases action steps [workflows-cases-steps]

Cases action steps let workflows create, query, update, and manage cases in any Cases-enabled app, including {{elastic-sec}}, Observability, and Stack Cases. Use them to automate case work without leaving the Elastic platform.

Use Cases steps for patterns like:

- Create a case when a detection rule fires, then attach the alert and relevant observables.
- Open a case, assign it to an on-call user, and post a notification to a team channel.
- Find similar cases for deduplication before creating a new one.
- Close a case automatically when a condition is met, and append an analyst note first.

For each step's inputs, which inputs are required, and which steps support `push-case`, refer to Cases workflow steps.

## Which Cases step to use [workflows-cases-catalog]

### Create, get, and search cases

- `cases.createCase`
- `cases.createCaseFromTemplate`
- `cases.getCase`
- `cases.getCases`
- `cases.findCases`
- `cases.findSimilarCases`
- `cases.getCasesByAlertId`

### Update case fields

- `cases.updateCase`
- `cases.updateCases`
- `cases.setStatus`
- `cases.setSeverity`
- `cases.setTitle`
- `cases.setDescription`
- `cases.setCategory`
- `cases.setCustomField`
- `cases.closeCase`

### Attach content

- `cases.addComment`
- `cases.addAlerts`
- `cases.addEvents`
- `cases.addObservables`
- `cases.addAttachments`
- `cases.getAllAttachments`

### Manage tags and assignees

- `cases.addTags`
- `cases.removeTags`
- `cases.assignCase`
- `cases.unassignCase`

### Update and delete observables

- `cases.updateObservable`
- `cases.deleteObservable`

### Push cases to an external system

- `cases.pushCases`

### Delete cases

- `cases.deleteCases`

## Pass a case between steps [workflows-cases-conventions]

Most Cases steps take a `case_id` input and return the case they worked on. `cases.createCase` returns the new case at `steps.<step_name>.output.case`, so later steps can use its ID:

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

To send a case to an external system, such as {{jira}} or ServiceNow, after a step changes it, set `push-case` to `true` on that step. To push several cases at once, use `cases.pushCases`.

## Migrate from `kibana.*` case steps [workflows-cases-migration]

In 9.3, case management steps used the `kibana.*` namespace. Those step types still work as deprecated aliases, but new workflows must use `cases.*`. For side-by-side replacements, refer to [Migrate from 9.3 to 9.4](/explore-analyze/workflows/authoring-techniques/migrate-from-9-3.md#workflows-migrate-cases).

## Related

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): The primary source of cases in a SOC workflow.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Use an AI classification or summary to enrich a case description.
- [Kibana Cases documentation](/solutions/security/investigate/security-cases.md): The Cases feature in {{elastic-sec}}.
