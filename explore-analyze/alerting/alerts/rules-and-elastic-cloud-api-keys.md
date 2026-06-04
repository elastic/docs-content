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

In {{serverless-full}} projects, rules use [{{ecloud}} API keys](../../../deploy-manage/api-keys/elastic-cloud-api-keys.md) instead of [{{es}} API keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md). When you create or save a rule, {{kib}} automatically creates a key scoped to your current roles — you don't need to select or provide one. This page explains how the key type affects rule behavior and scope, what doesn't update automatically after the migration, and what to check to make sure your rules are running as expected.

| Term | Definition |
|---|---|
| **{{es}} API key** | Authenticates access to {{es}} and {{kib}} APIs on a specific cluster or deployment. In alerting, the key is scoped to the permissions of the user who creates or manages the rule. |
| **{{ecloud}} API key** | Authenticates access to {{ecloud}} management APIs and {{es}} and {{kib}} APIs for {{serverless-short}} projects. In alerting, the key is scoped to the roles assigned at creation time and is not tied to an individual user's account. |

## About the migration [about-the-migration]

Elastic migrated existing alerting rules in {{serverless-full}} projects from {{es}} API keys to {{ecloud}} API keys in a controlled, phased rollout. In-product notices were shown when your organization was affected.

The migration was designed not to interrupt rule execution. Rules that couldn't be migrated automatically — for example, rules with a missing owner or incompatible custom role state — surfaced errors or indicators that require an administrator to fix the rule manually.

New and edited rules now use {{ecloud}} API keys by default. {{es}} API keys are used as a fallback only when an {{ecloud}} API key isn't available. If you manage rules through the public APIs using a personal {{es}} API key, certain rule management UI actions will convert those rules to {{ecloud}} API keys. Follow in-product guidance for your deployment.

## How API keys affect rule behavior [rule-behavior-by-key-type]

The type of API key a rule uses determines what it can access, how its permissions are managed, and what happens when organizational changes occur. The following table summarizes the key differences.

| | {{es}} API keys | {{ecloud}} API keys |
|---|---|---|
| Deployment type | Stack-versioned deployments | {{serverless-short}} projects only |
| Rules stop if owner leaves | Yes. Rules stop running if the owner's account is deactivated or their key is deleted | No. Rules continue running regardless of the creator's account status |
| Privilege scope | Capped by the owner's role-based privileges at the time of creation | Explicitly assigned at key creation and not tied to any individual user's roles |
| Risk when a different user edits a rule | Ownership transfers to the new editor, which can silently narrow or change the rule's access scope | No ownership transfer. Privileges remain unchanged when rules are edited |
| Impact of key expiry on rules | None by default. Keys never expire | Rules stop running when the key expires. Default expiry is 90 days |
| Key management | {{kib}} API keys page | {{ecloud}} Console |

## API key ownership and rule scope [api-key-ownership]

The type of API key a rule uses determines who owns it, what access it has, and what happens when ownership changes. It also determines what doesn't update automatically when your organization or roles change.

### {{es}} API key ownership

For [{{es}} API keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md), the owner is the user whose role-based privileges determine the key's access scope. The key can be scoped to a subset of the owner's privileges at creation time, but can never exceed them. Ownership transfers to whoever last creates or updates a rule, so a rule's scope can silently change when a different user edits it. If the owner's account is deactivated or their key is deleted, dependent rules stop running.

### {{ecloud}} API key ownership

[{{ecloud}} API keys](../../../deploy-manage/api-keys/elastic-cloud-api-keys.md) are owned by the user who creates them. Unlike {{es}} API keys, ownership doesn't transfer when a rule is edited. The key stays tied to the original creator and the roles they held when the key was created. Rules continue running regardless of the creator's account status.

### What doesn't automatically update [what-does-not-update]

After the migration, each rule's key is tied to the original owner and the roles assigned to them at migration time. The following changes don't apply automatically.

- **New roles added after migration**: If the key owner receives new roles after the migration, those roles aren't automatically reflected in the key. If a rule needs expanded access, the rule or key may need to be updated manually.

- **Changes to existing roles**: If a role's definition changes, those updates can propagate to the key's behavior. This is common with {{ecloud}}-defined roles and custom roles in {{serverless-short}}. If a custom role is deleted, rules that depended on it may fail until the rule is updated with a valid role assignment.

- **Organizational changes and orphaned rules**: {{ecloud}} API keys don't automatically follow every organizational change. If the key owner no longer exists in the organization, affected rules become orphaned and require manual intervention to re-bind them to a valid owner and key.

### Updating a rule's API key [updating-rule-api-key]

If a rule needs updated access (for example, because the owner's roles changed after migration, a key expired, or you need to assign ownership to a different user) you can regenerate the key manually at any time. In **{{stack-manage-app}} > {{rules-ui}}**, open the rule's action menu and select **Update API key**. You can also do this from the rule details page. The new key is scoped to the roles of the user who triggers the update at the time of the action.

For Elastic Security detection rules, which are primarily managed from the **Detection rules (SIEM)** page, use the **Type** filter in **{{stack-manage-app}} > {{rules-ui}}** to find them and trigger the same **Update API key** action.

## After the migration [post-migration-checklist]

Use the following checklists to confirm your rules are running correctly after the migration.

:::{dropdown} Right after migration
- **Check rule execution status**: Go to **{{stack-manage-app}} > {{rules-ui}}** or your app's rules page and review the last run status for all rules. Investigate any rules showing a failed or warning status before moving on. If you use Elastic Security detection rules, also check for gaps caused by the migration. Refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md) for instructions.

- **Resolve migration errors promptly**: If the UI shows API key errors for a rule, open the rule and save it with a valid user following the in-product prompts. Rules with missing owners or invalid role assignments won't run until resolved.

- **Verify index access**: Confirm that migrated rules can still reach the indices they query. A warning status with an index-not-found message means the new key may have narrower access than the previous one. Review and update role assignments if needed.
:::

:::{dropdown} Within 90 days
- **Review API key expiration**: {{ecloud}} API keys expire after 90 days by default. When a key expires, dependent rules stop running. Check the expiration date for keys created during migration and extend or adjust them if 90 days is too short for your use case. Elastic sends an expiration warning email to the key creator and operational contacts as the date approaches.

- **Check rule tags**: On the **{{stack-manage-app}} > {{rules-ui}}** page, review rule tags. Any rule tagged **Missing Elastic Cloud Api Key** is still running on an {{es}} API key. This typically happens when rules were created or updated through the public APIs using a personal {{es}} API key rather than through the UI. Edit the rule in the UI or update its API key to migrate it to an {{ecloud}} API key.

- **Review rules that use custom roles**: If any rules rely on custom roles, confirm those roles still exist and are correctly defined. If a custom role was deleted or changed around the time of migration, affected rules may be silently running with reduced access or may have failed.
:::

:::{dropdown} Ongoing
- **After organizational changes, check for orphaned rules**: If a key owner leaves the organization, rules tied to their key become orphaned and require manual intervention. Re-bind affected rules to a valid owner and key.

- **After role changes, review affected rules**: New roles granted to a key owner after migration are not automatically reflected in the key. If a rule needs expanded access, update the rule or key manually. If a role definition changes, those updates may propagate to the key's behavior, so review any rules that depend on the changed role.

- **When editing rules, be aware that ownership no longer transfers**: Unlike {{es}} API keys, the key stays tied to the original owner when a different user edits a rule. Privileges don't change on edit, but this also means any access issues from migration won't resolve themselves when a rule is updated.

- **For new {{serverless-short}} rules, use {{ecloud}} API keys**: Don't rely on {{es}} API key behavior for new rules in {{serverless-short}} projects.

- **For automation, use the documented APIs for your {{serverless-short}} tier**: Avoid depending on {{es}} API key behavior for automated workflows long term.
:::

## How your rules improve after the migration [post-migration-rule-improvements]

Migrating to {{ecloud}} API keys brings your rules in line with the rest of the platform. The following table summarizes the key improvements.

| Improvement | Details |
|---|---|
| **Rules work the same way as the rest of {{ecloud}}** | Before the migration, rules used a separate authentication model from other {{ecloud}} workflows. After the migration, rules use the same model as everything else, which removes a layer of complexity for administrators managing access across the platform. |
| **Rules can now work across projects** | Rules that need to query or act across multiple {{serverless-short}} projects now have the credentials to do so. Features like cross-project search require {{ecloud}} API keys, so migrated rules are now compatible with these capabilities without additional setup. |
| **Rule access aligns with how your organization manages roles in Cloud** | Migrated rules use the same {{ecloud}} roles that administrators already manage, including any custom roles you have defined. This makes it easier to understand and audit what your rules can access, without needing to track separate role definitions for alerting. |
| **Role updates can apply to your rules going forward** | When a role's definition changes, those updates can apply to rules that already use that role. This keeps rule access aligned with how your organization manages permissions over time. You should still review role changes that affect alerting, in particular custom role deletions, which can cause rules to fail if not addressed. |
| **Your rules are covered by consistent auditing and security controls** | Centralizing on {{ecloud}} API keys means rule activity is captured in the same audit trail as the rest of your organization's {{ecloud}} usage, and positions your rules to benefit from future access controls as they become available. |
