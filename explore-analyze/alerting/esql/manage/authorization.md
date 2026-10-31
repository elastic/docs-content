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
| Rule runs | The rule runs on an {{ecloud}} API key in {{serverless-short}} or an {{es}} API key in {{stack}}. The key determines what data the rule can query. It comes from the user who created the rule, last enabled it, or last rotated its key. Editing the rule doesn't replace the key. For how each key type handles role changes, refer to [Which type of API key a rule uses](#rule-api-key-type). To replace the key with one based on your credentials, refer to [Rotate a rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key). |
| Action policy evaluates and dispatches | Uses different credentials at different phases. Refer to [How action policies authorize a workflow run](#action-policy-workflow-keys). |
| Workflow steps run | The workflow runs with the action policy's API key, so its steps can do only what that key's privileges allow. |

## Which type of API key a rule uses [rule-api-key-type]

In {{serverless-short}}, rules run on an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md). In {{stack}}, rules run on an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md). A rule's key owner is the user who created the rule, last enabled it, or last rotated its key. Each key type keeps a different record of the key owner's access, so the same role change affects rules differently in each deployment.

If you create or enable a rule through the {{kib}} API while authenticated with your own API key, {{kib}} creates a separate key for the rule instead of reusing yours.

### {{serverless-short}} projects [rule-api-key-serverless]

```yaml {applies_to}
serverless: ga
```

A rule's {{ecloud}} API key records which roles the key owner has when {{kib}} creates the key, but not what those roles allow. Each time the rule runs, it uses the current privileges of those roles.

:::{note}
If an {{ecloud}} API key isn't available for a rule, the rule runs on an {{es}} API key instead. That key works like the key in [{{stack}} deployments](#rule-api-key-stack), so later role changes don't affect the rule.
:::

The following table shows how common role changes affect the rule and what to do:

| Change | Effect on the rule | What to do |
|---|---|---|
| An administrator edits one of the recorded roles | The rule uses the updated privileges on its next run. | You don't need to do anything. |
| An administrator assigns the key owner a new role | The rule doesn't get the new role's privileges. | [Rotate the rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key) as a user who has the new role. |
| An administrator deletes a custom role that the key recorded | The rule loses that role's privileges and might fail. | Rotate the rule's API key as a user who has the privileges the rule needs. |
| The key owner leaves your organization | The rule keeps running with the recorded roles. | To stop the rule from using those roles, rotate the rule's API key as a different user. |

For example, you create a rule while you have the `logs-reader` custom role, which can read `logs-*`. Later, you edit the rule's query to include `metrics-*`. If an administrator adds `metrics-*` to `logs-reader`, the rule can query `metrics-*` on its next run. If the administrator gives you a separate `metrics-reader` role instead, the rule can't query `metrics-*` until you rotate its API key.

### {{stack}} deployments [rule-api-key-stack]

```yaml {applies_to}
stack: ga 9.6+
```

A rule's {{es}} API key records a snapshot of the key owner's privileges when {{kib}} creates the key. The snapshot doesn't change after that, so later role changes don't affect the rule.

The following table shows how common role changes affect the rule and what to do:

| Change | Effect on the rule | What to do |
|---|---|---|
| An administrator gives the key owner more privileges by editing a role or assigning a new one | The rule doesn't get the new privileges. | [Rotate the rule's API key](../rules/view-manage-rules.md#rotate-rule-api-key) as a user who has them. |
| An administrator takes privileges away from the key owner by editing a role, deleting a role, or removing a role assignment | The rule keeps running with the privileges in the snapshot. | To remove that access from the rule, rotate the rule's API key as a user who has only the access the rule needs. |

For example, you create a rule while your role can read `logs-*`. Later, an administrator adds `metrics-*` to that role, and you edit the rule's query to include `metrics-*`. The rule still can't query `metrics-*`, because its key keeps the privileges you had when {{kib}} created the key. After you rotate the rule's API key, the rule can query both.

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
