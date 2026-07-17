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

# Authorization in the {{alerting-v2-system}} [experimental-alerting-authorization]

Each rule stores an API key, captured from the user who last saved it, and that key's privileges determine what data the rule can query. The key stays in place until someone updates it, even if that user later changes roles or leaves the team. Use this page to understand how the API key model works, keep credentials current, and resolve authorization errors.

## Whose privileges authorize a run [privs-that-authorize-runs]

The {{alerting-v2-system}} uses a different authorization model depending on which type of operation is running.

| Operation | Authorization model |
|---|---|
| Rule executes | The rule uses the API key of the user who last saved it. That key determines what data the rule can query. |
| Action policy evaluates | Action policy evaluation doesn't use any stored credentials. |
| Workflow is invoked by an action policy | The workflow uses the API key of the user who last saved it. |

## How {{kib}} records execution identity [record-execution-identity]

When a rule runs, {{kib}} records the identity of the user whose API key authorized the execution. This identity appears in rule execution history, so you can audit which credentials each run used.

Workflow runs triggered by action policies are recorded the same way, so you can audit them too. For details, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-audit).

## How the API key works [how-api-key-works]

When you save a rule, {{kib}} creates an API key that captures your privileges and authorizes the rule's {{esql}} query and writes to `.rule-events`. Workflow invocations use the workflow's own key, not the rule's.

::::{important}
If a user with fewer privileges saves the rule, the rule runs with those reduced privileges. If a user with greater privileges saves the rule, the rule runs with those elevated privileges. The API key always reflects the privileges of the user who most recently saved the rule.
::::

## How to keep a rule's privileges current [keep-rules-privileges-current]

To refresh the stored API key for future runs, save the rule again with the desired user, or toggle the rule off and back on. A rule retains its key when turned off. If the key is missing when you turn it back on, {{kib}} generates a new one using your current privileges.

::::{important}
Deactivating a user or changing their role doesn't automatically update the stored key. To remove an outgoing user's access from future runs, save the rule again with a different user, or toggle it off and back on.
::::

## Check and fix authorization errors [check-and-fix-errors]

The following table covers authorization errors that can cause a rule or an action policy to fail. If a workflow produces authorization errors, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | Save the rule as a user who has the required index privileges, or update that user's role and save again. |
| Stale or not valid API key | The stored key is no longer valid, for example because an administrator deleted or expired a role it depended on. | An API key error in rule execution history. | Refresh the key by saving the rule again or toggling it off and back on. |
| Action policy's API key is missing or not valid | The workflow the action policy should trigger doesn't run. | Not shown in the UI or execution history. Check the {{kib}} server logs. | Save the action policy again to refresh its stored API key. |
