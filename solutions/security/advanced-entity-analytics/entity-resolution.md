---
applies_to:
  stack: ga 9.4+
  serverless:
    security: planned
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

Entity resolution can happen automatically or manually. Automated resolution matches user entities based on shared email addresses without any configuration. Manual resolution lets you explicitly link entity records using a CSV file or directly from the entity details flyout.

## Resolution groups [entity-resolution-groups]

A resolution group consists of:

* **Primary entity**: The authoritative representation of the real-world identity. It receives aggregated risk scores that combine the risk from all linked records in the group. When an entity from an identity provider (Okta, Active Directory, or Entra ID) is linked with a local entity, the IDP entity is preferred as the primary entity.
* **Alias entities**: Records that point to the primary entity via a `resolved_to` field. In the **Entities** section of the [Entity analytics page](/solutions/security/advanced-entity-analytics/overview.md), alias entities appear nested under their primary entity when the table is grouped by **Resolution** (the default view).

Resolution group relationships are also visible as **Resolved to** connections in the entity details flyout's [Graph View](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) tab.

## Automated resolution [entity-resolution-automated]

Entity resolution runs an automated process that matches user entities across identity providers based on shared email addresses. For example, if an Okta user and an Active Directory user share the same email address, they are automatically linked into a resolution group. Automated resolution does not override manual resolution.

::::{note}
Automated resolution currently matches on email addresses only. Automated resolution may produce false-positive links when non-IDP entities happen to share an email address with an IDP entity.
::::

## Manual resolution [entity-resolution-manual]

You can manually link entity records using a CSV bulk upload on the **Entity Analytics** management page, or by adding and removing entities directly from the entity details flyout.

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

1. Find the **Entity Analytics** management page in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Go to the **Entity Resolution** tab.
3. Select or drag and drop your CSV file.
4. Review the file validation results and fix any errors if needed.
5. Confirm to apply the links.

::::{note}
Bulk unlinking is not available in the UI; use the [Entity store API]({{kib-apis}}operation/operation-post-security-entity-store-resolution-unlink) instead.
::::

### Manage resolution groups from the entity flyout [entity-resolution-flyout]

You can view, add to, and remove entities from a resolution group directly from the [entity details flyout](/solutions/security/advanced-entity-analytics/view-entity-details.md#resolution). The flyout's **Resolution group** tab shows all linked records and lets you search for entities to add, or remove individual aliases.

:::{image} /solutions/images/security-resolution-from-flyout.png
:alt: Resolution group tab on the entity details flyout
:screenshot:
:::

