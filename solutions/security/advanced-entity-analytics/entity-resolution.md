---
description: Link entity records that represent the same real-world identity into a resolution group and consolidate their risk scores into a single view in Elastic Security.
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Entity resolution [entity-analytics-resolution]

::::{admonition} Requirements
This feature requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::


In enterprise environments, a single person or host often appears as multiple entity records across different identity providers — such as Okta or Active Directory — as well as local log sources. Without resolution, risk scores and alerts are fragmented across these duplicate records, making it difficult to assess the true risk of a real-world identity.

Entity resolution links multiple entity records that represent the same real-world identity into a *resolution group*, consolidates their risk scores into a single view, and reduces noise in the entities table by surfacing only the authoritative record. Resolution groups also receive a combined [resolution group risk score](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#resolution-scoring) that aggregates risk inputs from all members of the group.

Entity resolution can happen automatically or manually. Automated resolution matches user entities based on shared identifiers, such as email addresses. Manual resolution lets you explicitly link entity records using a CSV file or directly from the entity details flyout.

## Resolution groups [entity-resolution-groups]

A resolution group consists of:

* **Primary entity**: The authoritative representation of the real-world identity. It receives aggregated risk scores that combine the risk from all linked records in the group. When an entity from an identity provider (such as Okta or Active Directory) is linked with a local entity, the IDP entity is preferred as the primary entity.
* **Alias entities**: Records that point to the primary entity via a `resolved_to` field. In the **Entities** section of the [Entity analytics page](/solutions/security/advanced-entity-analytics/monitor-entity-risk.md), alias entities appear nested under their primary entity when the table is grouped by **Resolution** (the default view).

Resolution group relationships are also visible as **Resolved to** connections in the entity details flyout's [interactive graph](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations).

## Automated resolution [entity-resolution-automated]

Entity resolution runs an automated process that matches user entities across identity providers and other sources based on shared identifiers. For example, if an Okta user and an Active Directory user share the same email address, they are automatically linked into a resolution group. Automated resolution does not override manual resolution.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Automated resolution also matches user entities on identifiers other than email addresses, such as a Windows security identifier (SID) or a Microsoft Entra ID globally unique identifier (GUID), through the built-in rules in the following section.

::::{note}
:applies_to: {"stack": "ga 9.4-9.5"}
In these versions, automated resolution matches on email addresses only. Automated resolution might produce false-positive links when non-IDP entities happen to share an email address with an IDP entity.
::::

### Built-in automated resolution rules [entity-resolution-built-in-rules]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

Automated resolution uses built-in rules. Each rule links user entities that share a particular identifier.

You can use the Entity Store API to [list the rules]({{kib-apis}}operation/operation-get-security-entity-store-resolution-rules) in a space and to turn each rule [on]({{kib-apis}}operation/operation-put-security-entity-store-resolution-rules-id-enable) or [off]({{kib-apis}}operation/operation-put-security-entity-store-resolution-rules-id-disable) for a space. If a rule links the wrong accounts, turn that rule off.


`crowdstrike_sid_bridge`
:   **Default:** Off

    **What it links:** Existing [CrowdStrike](integration-docs://reference/crowdstrike.md) user entities in your entity store that share a SID (`user.id`) with an [Active Directory](integration-docs://reference/entityanalytics_ad.md) user.

    **What it needs:** CrowdStrike user entities already in your entity store, and Active Directory users with matching SIDs.

    **When to turn it on:** If the CrowdStrike user entities already in your entity store should still link to Active Directory users.

`email_exact_match`
:   **Default:** On

    **What it links:** User entities that share the same email address across different identity providers. Email addresses are compared case-insensitively. Several local users with that email — one for each user name and host — are linked too. Users from the same identity provider that share an address are left unlinked.

    **What it needs:** User entities with an email address.

    **When to turn it off:** If shared mailboxes or role accounts produce false links.

`entra_guid_bridge`
:   **Default:** On

    **What it links:** Microsoft Defender identities and Entra ID users that share a GUID (`user.id`).

    **What it needs:** Identity events from the [Microsoft Defender XDR](integration-docs://reference/m365_defender.md) integration, and the [Microsoft Entra ID Entity Analytics](integration-docs://reference/entityanalytics_entra_id.md) integration.

    **When to turn it off:** If Microsoft Defender identities are linked to the wrong Entra ID users. For example, where your Defender data doesn't use Entra ID GUIDs as user identifiers.

`related_user_alias_resolution`
:   **Default:** Off

    **What it links:** User entities that an identity provider's user record lists as related users of another user.

    **What it needs:** Identity provider user records that list related users.

    **When to turn it on:** If the related users listed in your identity provider records should be linked.

`upn_cross_field_bridge`
:   **Default:** Off

    **What it links:** [Microsoft 365](integration-docs://reference/o365.md) audit users and Entra ID users that share a user principal name. User principal names are compared case-insensitively.

    **What it needs:** Microsoft 365 audit events that create user entities, and the Microsoft Entra ID Entity Analytics integration.

    **When to turn it on:** If Microsoft 365 audit events create user entities in your environment. It's off by default because those audit events don't create user entities.

`windows_sid_bridge`
:   **Default:** On

    **What it links:** User entities that share a Windows SID (`user.id`), including users seen on multiple hosts in Windows or CrowdStrike data. Windows domain accounts seen on several hosts are linked even before the Active Directory user is available. When that user arrives, the group is linked to it. Well-known SIDs, such as `LocalSystem`, are excluded.

    **What it needs:** Windows or CrowdStrike data from hosts.

    **When to turn it off:** If the well-known SID exclusions are not enough for your environment.

## Manual resolution [entity-resolution-manual]

You can manually link entity records using a CSV bulk upload on the **Entity Analytics** management page, or by adding and removing entities directly from the entity details flyout.

:::{tip}
:applies_to: {stack: ga 9.6+, serverless: ga}
You can also inspect resolution groups, link or unlink entities, and enable or disable automated resolution rules conversationally with {{agent-builder}} using the `entity-resolution` [skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#security-skills). For example prompts, refer to [Entity resolution](/solutions/security/ai/agent-builder/skills-use-cases.md#entity-resolution).
:::

### Bulk link entities using CSV [entity-resolution-csv]

You can bulk-link entity records to primary entities by importing a CSV file from the **Entity Analytics** management page.

Each row in the CSV uses identity fields to find matching entities and links them to a primary entity specified by its entity ID.

#### CSV format [entity-resolution-csv-format]

The CSV must include a header row with `type` and `resolved_to` columns. Additional columns are identity fields (for example, `user.email`, `user.name`) used as AND-combined filters to find matching entities.

| Column | Description |
| --- | --- |
| `type` | Entity type: `user`, `host`, or `service` |
| `resolved_to` | The `entity.id` of the primary entity |
| Additional columns | Identity fields used to match alias entities (for example, `user.email`, `user.name`, `host.name`) |

**Supported file formats:** CSV, TXT, TSV (maximum 1 MB)

**Example:**

```txt
type,user.email,user.name,resolved_to
user,emily@acme.com,,user:emily.chen@acme.com@okta
user,echen@azure.com,,user:emily.chen@acme.com@okta
user,,bob.smith,user:bob@acme.com@active_directory
```

#### Import a CSV file [entity-resolution-csv-import]

1. Go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
    * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
    * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
2. Go to the **Entity Resolution** tab.
3. Select or drag and drop your CSV file.
4. Review the file validation results and fix any errors if needed.
5. Confirm to apply the links.

::::{note}
Bulk unlinking is not available in the UI; use the [Entity store API]({{kib-apis}}operation/operation-post-security-entity-store-resolution-unlink) instead.
::::

### Manage resolution groups from the entity flyout [entity-resolution-flyout]

You can view, add to, and remove entities from a resolution group directly from the entity details flyout. Open the [**Resolution** section's](/solutions/security/advanced-entity-analytics/view-entity-details.md#resolution) child flyout to view all linked records, search for entities to add, or remove individual aliases.
