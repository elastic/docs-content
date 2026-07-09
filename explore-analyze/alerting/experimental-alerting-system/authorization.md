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

Authorization in the {{alerting-v2-system}} determines which user's privileges a rule uses when it runs and how those credentials stay current as your team changes. Use this page to understand how the API key model works, keep credentials current, and resolve authorization errors.

## Whose privileges authorize a run [privs-that-authorize-runs]

The {{alerting-v2-system}} involves two execution contexts, each with its own authorization model.

| Operation | Whose privileges are used |
|---|---|
| Rule execution | The user who last saved the rule |
| Workflow invocation (triggered by an action policy) | The user who last saved the workflow |

A rule runs using an API key that was captured the last time the rule was saved. That key's privileges determine what data the rule can query.

When an action policy matches an alert episode and invokes a workflow, the workflow runs under its own stored API key, which belongs to the user who last saved the workflow. Action policy evaluation runs in a background dispatcher process and does not use a user's stored credentials.

<!-- TODO: Follow up with engineering to clarify dispatcher authorization:

Questions to clarify:
- What credentials does the dispatcher use when evaluating action policies? Does it need read access to alert episodes, and if so, how is that granted?
- If the dispatcher runs purely as a system process with no user-scoped credentials, can we state that explicitly?

Thing to do once clarified:
- If the dispatcher is a system process with no user-scoped credentials, add a sentence here to state this explicitly.
-->

## How {{kib}} records execution identity [record-execution-identity]

When a rule runs, {{kib}} records the identity of the user whose API key authorized the execution. This identity appears in rule execution history, so you can audit which credentials each run used.

Workflows that are invoked by action policies record execution identity the same way as directly invoked workflows. For details, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-audit).

## How the API key works [how-api-key-works]

When you save a rule, {{kib}} creates an API key that captures your privileges and authorizes the rule's {{esql}} query and writes to `.rule-events`. Workflow invocations use the workflow's own key, not the rule's.

::::{important}
If a user with fewer privileges saves the rule, the rule runs with those reduced privileges. If a user with greater privileges saves the rule, the rule runs with those elevated privileges. The API key always reflects the privileges of the user who most recently saved the rule.
::::

## How to keep a rule's privileges current [keep-rules-privileges-current]

To refresh the stored API key for future runs, save the rule again with the desired user, or toggle the rule off and back on. A rule retains its key when disabled. If the key is missing when you re-enable it, {{kib}} generates a new one using your current privileges.

::::{important}
Deactivating a user or changing their role doesn't automatically update the stored key. To remove an outgoing user's access from future runs, save the rule again with a different user, or toggle it off and back on.
::::

<!-- TODO: Follow up with engineering to clarify action policy authorization:

Questions to clarify:
- Can action policy evaluation produce its own authorization errors (separate from rule execution errors)? If yes, where do they surface (execution history? dispatcher logs?) and how should users fix them?

Thing to do once clarified:
- If the dispatcher can fail for authorization reasons, add a row to the table below and document where the error surfaces and how to fix it.
-->

## Check and fix authorization errors [check-and-fix-errors]

The following table covers authorization errors that can cause a rule to fail. If an action policy or workflow produces authorization errors, refer to [Workflow authorization](../../workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | Save the rule as a user who has the required index privileges, or update that user's role and save again. |
| Stale or invalid API key | The stored key is no longer valid, for example because an administrator deleted or expired a role it depended on. | An API key error in rule execution history. | Refresh the key by saving the rule again or toggling it off and back on. |
