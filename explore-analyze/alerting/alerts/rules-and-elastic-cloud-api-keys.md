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

In {{serverless-full}} projects, rules authenticate using [{{ecloud}} API keys](../../../deploy-manage/api-keys/elastic-cloud-api-keys.md) rather than [{{es}} API keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md), which are used in Stack deployments and as a fallback in Serverless when an {{ecloud}} API key isn't available. 

{{kib}} uses an API key to authorize rule execution each time a rule runs, but the key type works differently depending on your deployment. {{es}} API keys are scoped to the permissions of the user who creates or manages the rule, while {{ecloud}} API keys are scoped to the roles the rule owner held at key creation time and are not tied to any individual user's account. 

If your organization was part of Elastic's migration from {{es}} to {{ecloud}} API keys for alerting, use this page to understand what changed, what to be aware of going forward, and what to review to confirm your rules are still running correctly.

## About the migration [about-the-migration]

Elastic migrated existing alerting rules in {{serverless-full}} projects from {{es}} API keys to {{ecloud}} API keys in a controlled, phased rollout. In-product notices were shown when your organization was affected.

The migration was designed not to interrupt rule execution. Rules that couldn't be migrated automatically (for example, rules with a missing owner or incompatible custom role state) surfaced errors or indicators that require an administrator to fix the rule manually.

New and edited rules now use {{ecloud}} API keys by default. {{es}} API keys are used as a fallback only when an {{ecloud}} API key isn't available. If you manage rules through the public APIs using a personal {{es}} API key, certain rule management UI actions will convert those rules to {{ecloud}} API keys. Follow in-product guidance for your deployment.

## How rule behavior changes after migration [rule-behavior-changes]

After the migration, your rules use {{ecloud}} API keys instead of {{es}} API keys. Two things to be aware of going forward:

- **New roles added after migration**: If the key owner receives new roles after the migration, those roles aren't automatically reflected in the key. If a rule needs expanded access, the rule or key may need to be updated manually.

- **Changes to existing roles**: If a role's definition changes, those updates can propagate to the key's behavior. This is common with {{ecloud}}-defined roles and custom roles in {{serverless-short}}. If a custom role is deleted, rules that depended on it may fail until the rule is updated with a valid role assignment.

## Check your rules after the migration [post-migration-checklist]

Use the following checklists to confirm your rules are running correctly after the migration.

:::{dropdown} Right after migration
- **Check rule execution status**: Go to **{{stack-manage-app}} > {{rules-ui}}** or your app's rules page and review the last run status for all rules. Investigate any rules showing a failed or warning status before moving on. If you use Elastic Security detection rules, also check for gaps caused by the migration. Refer to [Fill rule execution gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md) for instructions.

- **Resolve migration errors promptly**: If the UI shows API key errors for a rule, open the rule and save it with a valid user following the in-product prompts. Rules with missing owners or invalid role assignments won't run until resolved.

- **Verify index access**: Confirm that migrated rules can still reach the indices they query. A warning status with an index-not-found message means the new key may have narrower access than the previous one. Review and update role assignments if needed.
:::

:::{dropdown} Within 90 days
<!-- SME REVIEW: "Review API key expiration" is not in the source of truth. Verify the 90-day default expiry, that expired keys stop rules, and that Elastic sends expiration warning emails to the key creator and operational contacts. -->
- **Review API key expiration**: {{ecloud}} API keys expire after 90 days by default. When a key expires, dependent rules stop running. Check the expiration date for keys created during migration and extend or adjust them if 90 days is too short for your use case. Elastic sends an expiration warning email to the key creator and operational contacts as the date approaches.

- **Check rule tags**: On the **{{stack-manage-app}} > {{rules-ui}}** page, review rule tags. Any rule tagged **Missing Elastic Cloud Api Key** is still running on an {{es}} API key. This typically happens when rules were created or updated through the public APIs using a personal {{es}} API key rather than through the UI. Edit the rule in the UI or update its API key to migrate it to an {{ecloud}} API key.

- **Review rules that use custom roles**: If any rules rely on custom roles, confirm those roles still exist and are correctly defined. If a custom role was deleted or changed around the time of migration, affected rules may be silently running with reduced access or may have failed.
:::