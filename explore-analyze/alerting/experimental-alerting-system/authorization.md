---
navigation_title: Authorization
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Authorization in the {{alerting-v2-system}} determines which user's privileges a rule uses when it runs, how API keys are stored and refreshed, and how to resolve authorization errors."
tags:
  - experimental-alerting
  - alerting
  - kibana
---

# API keys and authorization in the {{alerting-v2-system}} [experimental-alerting-authorization]

Rule, action policy, and workflow runs in the {{alerting-v2-system}} are each authorized separately, and not every one uses a stored [{{es}} API key](../../../deploy-manage/api-keys/elasticsearch-api-keys.md) to do it. Use this page to understand which credential authorizes each operation, diagnose authorization errors, and keep credentials current.

## Which key authorizes each operation [key-per-operation]

The type of operation determines which credential authorizes it.

| Operation | How it's authorized |
|---|---|
| Rule executes | The rule uses the API key of the user who last saved it. That key determines what data the rule can query. |
| Action policy evaluates and dispatches | Uses different credentials at different phases. Refer to [How action policies authorize a workflow run](#action-policy-workflow-keys). |
| Workflow steps run | The workflow uses its own API key, separate from the action policy's, to run its steps. |

## How action policies authorize a workflow run [action-policy-workflow-keys]

An action policy matches alert episodes as an internal system process, without using a stored credential.

Once a policy matches and needs to notify someone, it uses its own stored API key, captured from the user who last saved the policy, to schedule the workflow. The workflow then uses its own separate stored API key to run its steps. Refer to [How steps use the API key](../../workflows/authorization.md#workflows-authorization-scope) for how a workflow's key applies across its steps.

## Check and fix authorization errors [check-and-fix-errors]

The following authorization errors can cause a rule to fail or prevent an action policy from delivering a notification. If a workflow produces authorization errors, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | Save the rule as a user who has the required index privileges, or update that user's role and save again. |
| Stale or not valid API key | The stored key is no longer valid, for example because an administrator deleted or expired a role it depended on. | An API key error in rule execution history. | Refresh the key by saving the rule again or toggling it off and back on. |
| Action policy's API key is missing or not valid | The action policy's own stored API key is no longer valid, so it can't schedule the workflow it should trigger. | Not shown in the UI or execution history. Check the {{kib}} server logs. | Save the action policy again to refresh its stored API key. |
| Workflow's API key is missing or not valid | The action policy successfully schedules the workflow, but the workflow's own stored API key is no longer valid, so its steps fail. | Not shown in the UI or execution history. Check the {{kib}} server logs, or refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-audit) to confirm which credentials a run used. | Save the workflow again to refresh its stored API key. |
