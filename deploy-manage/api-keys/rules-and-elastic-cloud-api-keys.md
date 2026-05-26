---
applies_to:
  serverless: ga
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
description: Understand how Elastic Cloud API keys affect rule behavior, ownership, and scope in Serverless projects, and what to check after migration.
---

# Rules and API keys in Serverless [rules-and-api-keys]

In Elastic Cloud Serverless projects, alerting rules use [Elastic Cloud API keys](elastic-cloud-api-keys.md) instead of [Elasticsearch API keys](elasticsearch-api-keys.md). This page explains how the key type affects rule behavior and scope, what does not update automatically after the migration, and what to check to make sure your rules are running as expected.

## How API keys affect rule behavior [rule-behavior-by-key-type]

The type of API key a rule uses determines what it can access, how its permissions are managed, and what happens when organizational changes occur. The following table summarizes the key differences.

| | Elasticsearch API keys | Elastic Cloud API keys |
|---|---|---|
| Deployment type | Stack-versioned deployments (ECH, ECE, ECK, self-managed) | Serverless projects only |
| Rules stop if owner leaves | Yes. Rules stop running if the owner's account is deactivated or their key is deleted | No. Rules continue running regardless of the creator's account status |
| Privilege scope | Capped by the owner's role-based privileges at the time of creation | Explicitly assigned at key creation and not tied to any individual user's roles |
| Risk when a different user edits a rule | Ownership transfers to the new editor, which can silently narrow or change the rule's access scope | No ownership transfer. Privileges remain unchanged when rules are edited |
| Impact of key expiry on rules | None by default. Keys never expire | Rules stop running when the key expires. Default expiry is 90 days |
| Key management | Kibana API keys page | Elastic Cloud Console (organization owners only) |

## API key ownership and rule scope [api-key-ownership]

The type of API key a rule uses determines who owns it, what access it has, and what happens when ownership changes. It also determines what does not update automatically when your organization or roles change.

### Elasticsearch API key ownership

For [Elasticsearch API keys](elasticsearch-api-keys.md), the owner is the user whose role-based privileges determine the key's access scope. The key can be scoped to a subset of the owner's privileges at creation time, but can never exceed them. Ownership transfers to whoever last creates or updates a rule, so a rule's scope can silently change when a different user edits it. If the owner's account is deactivated or their key is deleted, dependent rules stop running.

### Elastic Cloud API key ownership

[Elastic Cloud API keys](elastic-cloud-api-keys.md) are owned by the organization owner who creates them. Unlike Elasticsearch API keys, ownership does not transfer when a rule is edited. The key stays tied to the original owner and the roles they held when the key was created. Rules continue running regardless of the creator's account status.

### What does not automatically update [what-does-not-update]

After the migration, each rule's key is tied to the original owner and the roles assigned to them at migration time. The following changes do not apply automatically.

- **New roles added after migration**: If the key owner receives new roles after the migration, those roles are not automatically reflected in the key. If a rule needs expanded access, the rule or key may need to be updated manually.

- **Changes to existing roles**: If a role's definition changes, those updates can propagate to the key's behavior. This is common with Elastic Cloud-defined roles and custom roles in Serverless. If a custom role is deleted, rules that depended on it may fail until the rule is updated with a valid role assignment.

- **Organizational changes and orphaned rules**: Elastic Cloud API keys do not automatically follow every organizational change. If the key owner no longer exists in the organization, affected rules become orphaned and require manual intervention to re-bind them to a valid owner and key.

## After the migration [post-migration-checklist]

Use the following checklists to confirm your rules are running correctly after the migration.

:::{dropdown} Right after migration
- **Check rule execution status**: Go to the Rule Monitoring tab and review the Last response column for all rules. Rules should show Succeeded. Investigate any that show Failed or Warning before moving on.

- **Resolve migration errors promptly**: If the Alerting UI shows failed migration indicators or API key errors for a rule, open the rule and save it with a valid user following the in-product prompts. Rules with missing owners or invalid role assignments will not run until resolved.

- **Check for gaps in detection coverage**: The migration may have caused a brief gap in rule execution. Use the Rule Monitoring tab to get an overview of gaps across all rules. Open individual rule detail pages and check the Gaps table for the exact time range missed.

- **Fill any gaps**: Re-run rules over the missed window to generate alerts that should have been created during the migration. You can fill gaps for individual rules from the Gaps table, or use the Fill gaps bulk action for multiple rules at once. To do this programmatically, use `POST /api/alerting/rules/backfill/_find` to identify gaps, then schedule backfills via the Kibana alerting API.

- **Verify index access**: Confirm that migrated rules can still reach the indices they query. A Warning status with an index-not-found message means the new key may have narrower access than the previous one. Review and update role assignments if needed.
:::

:::{dropdown} Within 90 days
- **Review API key expiration**: Elastic Cloud API keys expire after 90 days by default. When a key expires, dependent rules stop running. Check the expiration date for keys created during migration and extend or adjust them if 90 days is too short for your use case. Elastic sends an expiration warning email to the key creator and operational contacts as the date approaches.

- **Review rules that use custom roles**: If any rules rely on custom roles, confirm those roles still exist and are correctly defined. If a custom role was deleted or changed around the time of migration, affected rules may be silently running with reduced access or may have failed.
:::

:::{dropdown} Ongoing
- **After organizational changes, check for orphaned rules**: If a key owner leaves the organization, rules tied to their key become orphaned and require manual intervention. Re-bind affected rules to a valid owner and key.

- **After role changes, review affected rules**: New roles granted to a key owner after migration are not automatically reflected in the key. If a rule needs expanded access, update the rule or key manually. If a role definition changes, those updates may propagate to the key's behavior, so review any rules that depend on the changed role.

- **When editing rules, be aware that ownership no longer transfers**: Unlike Elasticsearch API keys, the key stays tied to the original owner when a different user edits a rule. Privileges do not change on edit, but this also means any access issues from migration will not resolve themselves when a rule is updated.

- **For new Serverless alerting rules, use Elastic Cloud API keys**: Do not rely on Elasticsearch API key behavior for new rules in Serverless projects.

- **For automation, use the documented APIs for your Serverless tier**: Avoid depending on Elasticsearch API key behavior for automated workflows long term.
:::

## How your rules improve after the migration [post-migration-rule-improvements]

Migrating to Elastic Cloud API keys brings your alerting rules in line with the rest of the platform. The following table summarizes the key improvements.

| Improvement | Details |
|---|---|
| **Rules work the same way as the rest of Elastic Cloud** | Before the migration, alerting rules used a separate authentication model from other Elastic Cloud workflows. After the migration, rules use the same model as everything else, which removes a layer of complexity for administrators managing access across the platform. |
| **Rules can now work across projects** | Rules that need to query or act across multiple Serverless projects now have the credentials to do so. Features like cross-project search require Elastic Cloud API keys, so migrated rules are now compatible with these capabilities without additional setup. |
| **Rule access aligns with how your organization manages roles in Cloud** | Migrated rules use the same Elastic Cloud roles that administrators already manage, including any custom roles you have defined. This makes it easier to understand and audit what your rules can access, without needing to track separate role definitions for alerting. |
| **Role updates can apply to your rules going forward** | When a role's definition changes, those updates can apply to rules that already use that role. This keeps rule access aligned with how your organization manages permissions over time. You should still review role changes that affect alerting, in particular custom role deletions, which can cause rules to fail if not addressed. |
| **Your rules are covered by consistent auditing and security controls** | Centralizing on Elastic Cloud API keys means rule activity is captured in the same audit trail as the rest of your organization's Elastic Cloud usage, and positions your rules to benefit from future access controls as they become available. |
