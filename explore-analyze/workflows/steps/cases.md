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

For each step's inputs, which inputs are required, and which steps support `push-case`, refer to [Cases workflow steps](kibana://reference/workflows/cases-steps.md).

## Which Cases step to use [workflows-cases-catalog]

| Task | Steps |
| --- | --- |
| Create, get, and search cases | [`cases.createCase`](kibana://reference/workflows/cases-steps.md#cases-createcase), [`cases.createCaseFromTemplate`](kibana://reference/workflows/cases-steps.md#cases-createcasefromtemplate), [`cases.getCase`](kibana://reference/workflows/cases-steps.md#cases-getcase), [`cases.getCases`](kibana://reference/workflows/cases-steps.md#cases-getcases), [`cases.findCases`](kibana://reference/workflows/cases-steps.md#cases-findcases), [`cases.findSimilarCases`](kibana://reference/workflows/cases-steps.md#cases-findsimilarcases), [`cases.getCasesByAlertId`](kibana://reference/workflows/cases-steps.md#cases-getcasesbyalertid) |
| Update case fields | [`cases.updateCase`](kibana://reference/workflows/cases-steps.md#cases-updatecase), [`cases.updateCases`](kibana://reference/workflows/cases-steps.md#cases-updatecases), [`cases.setStatus`](kibana://reference/workflows/cases-steps.md#cases-setstatus), [`cases.setSeverity`](kibana://reference/workflows/cases-steps.md#cases-setseverity), [`cases.setTitle`](kibana://reference/workflows/cases-steps.md#cases-settitle), [`cases.setDescription`](kibana://reference/workflows/cases-steps.md#cases-setdescription), [`cases.setCategory`](kibana://reference/workflows/cases-steps.md#cases-setcategory), [`cases.setCustomField`](kibana://reference/workflows/cases-steps.md#cases-setcustomfield), [`cases.closeCase`](kibana://reference/workflows/cases-steps.md#cases-closecase) |
| Attach content | [`cases.addComment`](kibana://reference/workflows/cases-steps.md#cases-addcomment), [`cases.addAlerts`](kibana://reference/workflows/cases-steps.md#cases-addalerts), [`cases.addEvents`](kibana://reference/workflows/cases-steps.md#cases-addevents), [`cases.addObservables`](kibana://reference/workflows/cases-steps.md#cases-addobservables), [`cases.addAttachments`](kibana://reference/workflows/cases-steps.md#cases-addattachments), [`cases.getAllAttachments`](kibana://reference/workflows/cases-steps.md#cases-getallattachments) |
| Manage tags and assignees | [`cases.addTags`](kibana://reference/workflows/cases-steps.md#cases-addtags), [`cases.removeTags`](kibana://reference/workflows/cases-steps.md#cases-removetags), [`cases.assignCase`](kibana://reference/workflows/cases-steps.md#cases-assigncase), [`cases.unassignCase`](kibana://reference/workflows/cases-steps.md#cases-unassigncase) |
| Update and delete observables | [`cases.updateObservable`](kibana://reference/workflows/cases-steps.md#cases-updateobservable), [`cases.deleteObservable`](kibana://reference/workflows/cases-steps.md#cases-deleteobservable) |
| Push cases to an external system | [`cases.pushCases`](kibana://reference/workflows/cases-steps.md#cases-pushcases) |
| Delete cases | [`cases.deleteCases`](kibana://reference/workflows/cases-steps.md#cases-deletecases) |

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

To send a case to an external system, such as {{jira}} or ServiceNow, after a step changes it, set [`push-case`](kibana://reference/workflows/cases-steps.md#cases-push-case) to `true` on that step. To push several cases at once, use [`cases.pushCases`](kibana://reference/workflows/cases-steps.md#cases-pushcases).

## Migrate from `kibana.*` case steps [workflows-cases-migration]

In 9.3, case management steps used the `kibana.*` namespace. Those step types still work as deprecated aliases, but new workflows must use `cases.*`. For side-by-side replacements, refer to [Migrate from 9.3 to 9.4](/explore-analyze/workflows/authoring-techniques/migrate-from-9-3.md#workflows-migrate-cases).

## Related

- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): The primary source of cases in a SOC workflow.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Use an AI classification or summary to enrich a case description.
- [Kibana Cases documentation](/solutions/security/investigate/security-cases.md): The Cases feature in {{elastic-sec}}.
