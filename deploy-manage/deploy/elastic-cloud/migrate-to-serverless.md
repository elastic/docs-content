---
navigation_title: Migrate to Serverless
description: Assess your existing solution, prepare and test a Serverless project, and plan the move to production.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: overview
---

# Migrate to {{serverless-full}}

Moving to {{serverless-full}} involves creating a project and adapting your existing solution to it. You can transfer supported user data and export some configuration, while other components require manual setup or redesign. The work involved depends on the features and integrations your solution uses.

This guide covers the full migration process, from assessing the source and preparing and testing the destination to completing the production transition.

## Before you begin [migrate-to-serverless-before-you-begin]

Before starting the migration, make sure that you have:

- **Source access:** Use credentials with the {{es}} and {{kib}} privileges needed to read the source data and retrieve the resource configuration required for the migration. A practical broad custom role grants the `all` cluster privilege, `read` and `view_index_metadata` on `*`, and the {{kib}} `all` base privilege for all spaces. You can use the `superuser` role instead, but it is not required. If you use a narrower custom role, confirm that it supports every inventory and export operation in this guide.
- **Destination access:** Make sure that you can create {{serverless-short}} projects in the {{ecloud}} organization. The [predefined **Admin** role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) or an equivalent role is required. If the destination project already exists, you need the **Admin** role scoped to that project with **Cloud Console, {{es}}, and {{kib}}** access.

## Migration overview [migrate-to-serverless-order]

The migration process includes these phases:

1. **[Assess your existing solution](migrate-to-serverless-assess.md):** Inventory the data, configuration, integrations, clients, and dependencies your solution relies on. Identify a candidate project type, check feature compatibility, and determine the adaptations and migration work required.
2. **[Create the destination project](migrate-to-serverless-create-project.md):** Confirm the project type and feature tier, create the project, and configure initial connectivity and access.
3. **[Prepare and test the destination](migrate-to-serverless-prepare.md):** Migrate or recreate assets, transfer a subset of data for testing, and validate the complete solution with representative clients. Repeat preparation or recreate the destination until it is ready for production.
4. **[Complete the migration and switch to production](migrate-to-serverless-production.md):** Plan the migration window and rollback procedure, pause source changes, complete the remaining transfer, switch production clients and ingestion, validate production, and monitor the destination before retiring the source.

The following diagram summarizes these phases and shows the preparation loop you can repeat before moving to production.

:::{image} /deploy-manage/images/serverless-migration-proposed-order.svg
:alt: Assess the solution and create the destination project. Prepare assets, transfer data, test reads and indexing, and evaluate the destination. Return to preparation to refine or recreate the project, or continue to complete the migration and switch to production.
:::

Start with [Assess your existing solution](migrate-to-serverless-assess.md).

## Supporting procedures

Use [Transfer data](migrate-to-serverless-transfer-data.md) during preparation and production for index and data stream transfer methods, considerations, verification, and incremental transfer mechanisms.
