---
navigation_title: Authorization
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Learn which credentials authorize rule, action policy, and workflow runs in the experimental alerting system, and how to diagnose and resolve authorization errors."
---

# Rule, action policy, and workflow authorization in the {{alerting-v2-system}} [experimental-alerting-authorization]

The {{alerting-v2-system}} authorizes rules, action policies, and workflows differently. Use this page to understand which credential applies to each operation, diagnose authorization errors, and keep credentials current.

## Which key authorizes each operation [key-per-operation]

The type of operation determines which credential authorizes it.

| Operation | How it's authorized |
|---|---|
| Rule executes | The rule uses the [API key](../alerts/alerting-setup.md#alerting-authorization) of the user who last saved it. That key determines what data the rule can query. |
| Action policy evaluates and dispatches | Uses different credentials at different phases. Refer to [How action policies authorize a workflow run](#action-policy-workflow-keys). |
| Workflow steps run | The workflow uses its own API key, separate from the action policy's, to run its steps. |

## How action policies authorize a workflow run [action-policy-workflow-keys]

Authorizing a workflow run happens in three steps, and each step uses a different credential:

1. The action policy checks alert episodes against its match conditions. This step runs as an internal system process and doesn't use a stored credential.
2. Once a match is found, the policy schedules the workflow using its own stored API key, captured from the user who last saved the policy.
3. The workflow then runs its steps using its own separate stored API key, not the policy's. Refer to [How steps use the API key](../../workflows/authorization.md#workflows-authorization-scope) for how a workflow's key applies across its steps.

## Check and fix authorization errors [check-and-fix-errors]

The following authorization errors can cause a rule to fail or prevent an action policy from delivering a notification. If a workflow produces authorization errors, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | Save the rule as a user who has the required index privileges, or update that user's role and save again. |
| Stale or not valid API key | The stored key is no longer valid, for example because an administrator deleted or expired a role it depended on. | An API key error in rule execution history. | Refresh the key by saving the rule again or toggling it off and back on. |
| Action policy's API key is missing or not valid | The action policy's own stored API key is no longer valid, so it can't schedule the workflow it should trigger. | Not shown in the UI or execution history. Check the {{kib}} server logs. | Save the action policy again to refresh its stored API key. |
| Workflow's API key is missing or not valid | The action policy successfully schedules the workflow, but the workflow's own stored API key is no longer valid, so its steps fail. | Not shown in the UI or execution history. Check the {{kib}} server logs, or refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-audit) to confirm which credentials a run used. | Save the workflow again to refresh its stored API key. |
