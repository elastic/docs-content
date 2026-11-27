---
navigation_title: Create the destination project
description: Create a Serverless destination project and configure connectivity and access for migration.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Create the destination project [migrate-to-serverless-create]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-create-project.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Create project is the current phase.
:::

Previous: [Assess](migrate-to-serverless-assess.md) · Next: [Prepare and test](migrate-to-serverless-prepare.md)

Confirm the project type selected during assessment. For {{observability}} and {{elastic-sec}} projects, confirm that the selected [{{observability}} feature tier](/solutions/observability/observability-serverless-feature-tiers.md) or [Security feature tier](/solutions/security/security-serverless-feature-tiers.md) supports all capabilities identified during assessment.

1. [Create the destination project](create-serverless-project.md), then [find its connection details](find-connection-details-serverless.md), including the {{es}} and {{kib}} endpoints.
2. If you attach a [network security policy](/deploy-manage/security/network-security.md) to the destination, allow access from the environment where you run the migration. {{serverless-short}} projects accept public traffic by default, but after you attach a policy, traffic that does not match it is denied.
3. Create a temporary [{{serverless-short}} project API key](/deploy-manage/api-keys/serverless-project-api-keys.md) while signed in with the **Admin** role. Do not restrict its security privileges, so that it can access all {{es}} and {{kib}} resources required by the migration procedures in this guide. Store it securely and revoke it when the migration is complete.

## Next step

Continue to [Prepare and test the destination](migrate-to-serverless-prepare.md).
