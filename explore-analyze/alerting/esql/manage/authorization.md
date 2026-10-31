---
navigation_title: Authorization
applies_to:
  stack: ga 9.6+
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
| Rule runs | The rule's API key determines what data the rule can query. The key comes from the user who created the rule, last enabled it, or last rotated its key. Editing the rule doesn't replace the key. To replace it with a key based on your credentials, refer to [Rotate a rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key). For how the key type differs between deployments, refer to [How a rule's API key works by deployment](#rule-api-key-type). |
| Action policy evaluates and dispatches | Uses different credentials at different phases. Refer to [How action policies authorize a workflow run](#action-policy-workflow-keys). |
| Workflow steps run | The workflow runs with the action policy's API key, so its steps can do only what that key's privileges allow. |

## How a rule's API key works by deployment [rule-api-key-type]

The type of API key a rule uses, and what that key captures from the user, depends on your deployment:

- {applies_to}`serverless: ga` The rule uses an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) that captures the user's role assignments when {{kib}} creates the key. If an administrator changes one of those roles, the change applies on the rule's next run. If an administrator deletes a custom role that the key relies on, the rule might fail. If an {{ecloud}} API key isn't available, the rule uses an {{es}} API key instead.
- {applies_to}`stack: ga 9.6+` The rule uses an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) that captures a snapshot of the user's privileges when {{kib}} creates the key. Later changes to that user's roles don't affect the key.

If you create or enable a rule through the {{kib}} API while authenticated with your own API key, {{kib}} creates a separate key for the rule instead of reusing yours.

{{alerting-v2-system-cap}} rules don't get the **Missing Elastic Cloud API Key** tag, and the migration checklist in [Rules and {{ecloud}} API keys in {{serverless-short}}](/explore-analyze/alerting/alerts/rules-and-elastic-cloud-api-keys.md) doesn't apply to them.

## How action policies authorize a workflow run [action-policy-workflow-keys]

Authorizing a workflow run happens in three steps, and each step uses a different credential:

1. The action policy checks alerts against its match conditions. This step runs as an internal system process and doesn't use a stored credential.
2. Once a match is found, the policy schedules the workflow using its own stored API key, captured from the user who last saved the policy.
3. The workflow runs its steps with that same policy key, so the steps can do only what the key's privileges allow. Refer to [How steps use the API key](/explore-analyze/workflows/authorization.md#workflows-authorization-scope) for how a key applies across a workflow's steps.

## Check and fix authorization errors [check-and-fix-errors]

The following authorization errors can cause a rule to fail or prevent an action policy from invoking a workflow. If a workflow produces authorization errors, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-troubleshoot).

| Error type | Cause | Where it appears | How to resolve it |
|---|---|---|---|
| Insufficient privileges | The API key doesn't have the privileges required to query the rule's target data. | Rule execution history shows the run as failed. | As a user who has the required index privileges, [rotate the rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key), or disable the rule and enable it again. Saving the rule doesn't replace its key. |
| Stale or not valid API key | The stored key is no longer valid, for example because an administrator deleted it. | An API key error in rule execution history. | [Rotate the rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key), or disable the rule and enable it again. Saving the rule doesn't replace its key. |
| Action policy's API key is missing or not valid | The action policy has no stored API key (`missing_api_key`), or its stored key was deleted or changed (`schedule_error`). The policy can't schedule the workflow, so the workflow doesn't run. | The **Action policies** tab of the [execution history](../action-policies/review-action-policy-execution-history.md) shows the run as **Failed**, with the failure reason. | Save the action policy again to refresh its stored API key. |
| Action policy's API key lacks the privileges the workflow needs | The action policy schedules the workflow, but its API key doesn't have the privileges the workflow's steps need, so the steps fail. | The workflow run fails at the affected steps. To confirm which credentials a run used, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-audit). | Save the action policy as a user who has the privileges the workflow needs, or update that user's role and save again. |
