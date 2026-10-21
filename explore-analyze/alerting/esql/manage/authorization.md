---
navigation_title: Authorization
applies_to:
  stack: ga 9.6+, experimental =9.5
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: "Learn which credentials authorize rule, action policy, and workflow runs, and how to diagnose and resolve authorization errors."
---

# Rule, action policy, and workflow authorization [experimental-alerting-authorization]

{{alerting-v2-system-cap}} authorizes rules, action policies, and workflows with different credentials. Knowing which credential applies to each operation helps you diagnose authorization errors and keep credentials current.

## Which key authorizes each operation [key-per-operation]

The type of operation determines which credential authorizes it.

| Operation | How it's authorized |
|---|---|
| Rule executes | The rule uses the [API key](/explore-analyze/alerting/alerts/alerting-setup.md#alerting-authorization) of the user who last saved it. That key determines what data the rule can query. |
| Action policy evaluates and dispatches | Uses different credentials at different phases. Refer to [How action policies authorize a workflow run](#action-policy-workflow-keys). |
| Workflow steps run | The workflow runs with the action policy's API key, so its steps can do only what that key's privileges allow. |

## How action policies authorize a workflow run [action-policy-workflow-keys]

Authorizing a workflow run happens in three steps, and each step uses a different credential:

1. The action policy checks alerts against its match conditions. This step runs as an internal system process and doesn't use a stored credential.
2. Once a match is found, the policy schedules the workflow using its own stored API key, captured from the user who last saved the policy.
3. The workflow runs its steps with that same policy key, so the steps can do only what the key's privileges allow. Refer to [How steps use the API key](/explore-analyze/workflows/authorization.md#workflows-authorization-scope) for how a key applies across a workflow's steps.

## Check and fix authorization errors [check-and-fix-errors]

The following authorization errors can cause a rule to fail or prevent an action policy from invoking a workflow. If a workflow produces authorization errors, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | Save the rule as a user who has the required index privileges, or update that user's role and save again. |
| Stale or not valid API key | The stored key is no longer valid, for example because an administrator deleted or expired a role it depended on. | An API key error in rule execution history. | Refresh the key by saving the rule again or toggling it off and back on. |
| Action policy's API key is missing or not valid | The action policy has no stored API key (`MISSING_API_KEY`), or its stored key was deleted or changed (`SCHEDULE_ERROR`). The policy can't schedule the workflow, so the workflow doesn't run. | Not shown in the UI or execution history. Check the {{kib}} server logs. | Save the action policy again to refresh its stored API key. |
| Action policy's API key lacks the privileges the workflow needs | The action policy schedules the workflow, but its API key doesn't have the privileges the workflow's steps need, so the steps fail. | The workflow run fails at the affected steps. To confirm which credentials a run used, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-audit). | Save the action policy as a user who has the privileges the workflow needs, or update that user's role and save again. |
