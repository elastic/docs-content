---
applies_to:
  serverless: ga
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
description: Understand how Elastic Cloud API keys affect rule behavior, ownership, and scope in Serverless projects, and what to check after migration.
---

# Rules and {{ecloud}} API keys in {{serverless-short}}[rules-and-elastic-cloud-api-keys]

In {{serverless-full}} projects, rules authenticate using [{{ecloud}} API keys](../../../deploy-manage/api-keys/elastic-cloud-api-keys.md) rather than [{{es}} API keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md), which are used in Stack deployments and as a fallback in {{serverless-short}} when an {{ecloud}} API key isn't available.

{{kib}} creates an API key when a rule is created or edited, then uses it to authorize execution on every run. {{es}} API keys are scoped to a user's **privileges**, whereas {{ecloud}} API keys are scoped to a snapshot of a user's current **roles**.

Use this page to understand how {{ecloud}} API keys work for {{serverless-short}} alerting rules and how role changes affect rule access. If your organization was part of Elastic's migration from {{es}} to {{ecloud}} API keys, it also includes a checklist to verify your rules are still running correctly.

## About the {{ecloud}} API key migration [about-the-migration]

Elastic migrated existing alerting rules in {{serverless-short}} projects from {{es}} API keys to {{ecloud}} API keys in a controlled, phased rollout. In-product notices were shown when your organization was affected.

The migration was designed not to interrupt rule execution. Rules that couldn't be migrated automatically (for example, rules with a missing owner or incompatible custom role state) surfaced errors or indicators that require an administrator to fix the rule manually.

New and edited rules now use {{ecloud}} API keys by default. {{es}} API keys are used as a fallback only when an {{ecloud}} API key isn't available. 

### Find rules that are missing an {{ecloud}} API key [missing-api-key-tag]

When {{kib}} creates or edits a rule, it generates the rule's API key from the credentials used to make that request. If a rule is created or updated through the public APIs using a personal {{es}} API key rather than through the UI, that {{es}} API key becomes the rule's API key instead of an {{ecloud}} API key.

To find affected rules, check rule tags on the **Rules** page for your project type:

- **{{observability}} and {{es}} projects**: Find **{{rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
- **Security projects**: Find **{{siem-rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Any rule tagged **Missing Elastic Cloud API Key** is still running on an {{es}} API key. To migrate the rule to an {{ecloud}} API key, edit it in the UI (for example, by editing and saving the rule) or select **Update API key** from the rule's action menu. Follow any prompts the UI shows during the process.

### Check your rules after the migration [post-migration-checklist]

Use the following checklists to confirm your rules are running correctly after the migration.

:::{dropdown} Right after migration
- **Check rule execution status**: Go to the rules page for your project type and review the last run status for all rules. Investigate any rules showing a failed or warning status before moving on.
    - **{{observability}} and {{es}} projects**: Find **{{rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    - **Security projects**: Find **{{siem-rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Also check for gaps caused by the migration. Refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md) for instructions.

- **Resolve migration errors promptly**: If the UI shows an indicator that an {{ecloud}} API key isn't available for a rule, the rule continues to run using an {{es}} API key as a fallback. To create a new {{ecloud}} API key for the rule, open the rule's action menu in the UI and select **Update API key**.

- **Verify index access**: Confirm that migrated rules can still reach the indices they query. A warning status with an index-not-found message means the new key might have narrower access than the previous one. Review and update role assignments if needed.
:::

:::{dropdown} Within 90 days
- **Review API key expiration**: If a rule was created or updated through the {{kib}} API using an {{ecloud}} API key with a defined expiration, the rule is bound to that specific key and its expiration date. When the key expires, the rule stops running. To generate a new key for the rule, select **Update API key** from the rule's action menu.

- **Review rules that use custom roles**: If any rules rely on custom roles, confirm those roles still exist and are correctly defined. If a custom role was deleted or changed around the time of migration, affected rules might be silently running with reduced access or might have failed.
:::

## How rules use {{ecloud}} API keys [rule-behavior-changes]

Serverless alerting rules use {{ecloud}} API keys in the following ways:

- **Role assignments are captured when a rule is saved**: The key reflects the user's roles at the time the rule is created or edited. Roles assigned to the user afterward aren't picked up until the rule is saved again.

- **Role definition changes apply to the key's behavior**: If a role's definition changes, those updates propagate to the key because privileges are resolved at request time. If a custom role is deleted, rules that depended on it might fail until the rule is updated with a valid role assignment.

- **Rules continue running when the key owner leaves the organization**: {{ecloud}} API keys are not tied to the user's account. If the user who last edited a rule leaves, the key continues to authenticate using their assigned roles.