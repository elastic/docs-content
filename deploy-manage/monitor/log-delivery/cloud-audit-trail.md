---
navigation_title: Elastic Cloud audit trail
description: Track organization-level actions in Elastic Cloud Hosted by delivering audit logs to a hosted deployment you own.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# {{ecloud}} audit trail

:::{admonition} {{fedramp-mod}} only
{{ecloud}} audit trail is available on {{fedramp-mod}} environments only.
:::

{{ecloud}} audit trail records actions that members of your organization perform through the {{ecloud}} Console, the Terraform Provider for {{ecloud}}, the Elastic CLI, or any other client that calls the [{{ecloud}} API]({{cloud-apis}}).

Using {{ecloud}} audit trail data, you can answer questions such as:

* Which user or API key tried to authenticate, and did they succeed or fail?
* Which user increased resources on a deployment?
* Which resources is a given API key accessing?
* Who modified traffic filters, and when?
* Who upgraded, deleted, or changed the configuration of a deployment?

## What is audited

{{ecloud}} audit trail captures all calls to the {{ecloud}} API. Examples of audited actions include:

* Managing hosted deployments: creation, configuration changes, scaling, upgrades, and deletion
* Managing organization membership and invitations
* Managing [Cloud API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md)
* Managing [network security configurations](/deploy-manage/security/network-security.md) such as traffic filters, trust relationships, SSO, and role mappings
* Sign-in, sign-out, and authentication attempts to the {{ecloud}} Console

<!--
TODO when this expands to regular ECH: clarify which of these actions apply
org-wide vs. ECH-only. Membership and sign-in are org-scoped, but deployment
management is ECH-specific. Users with both ECH and serverless may need both
this feature and the serverless audit trail for full org coverage.
-->

:::{note}
{{ecloud}} audit trail does not capture activity inside your deployments.
<!--
TODO when this expands to regular ECH: add "and it does not cover serverless
project management or activity." Also add a serverless bullet pointing to
/deploy-manage/monitor/log-delivery/audit-trail.md, which covers org-level
actions, project-level ES and Kibana activity, and serverless project
management in a single stream.
-->

To audit {{es}} and {{kib}} activity within a deployment, enable [audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) on the deployment directly.
:::

## Requirements

To use the {{ecloud}} audit trail, you need the following:

* A [{{fedramp-mod}} {{ecloud}} organization](/deploy-manage/cloud-organization.md).
* A [Platinum or Enterprise subscription]({{subscriptions}}).
* An [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with organization owner permissions.
* A destination deployment in the same organization to store audit logs. You might choose to use a dedicated deployment to keep audit data separate from production workloads.
* Your organization ID. You can find this on the [**Organization**](https://cloud.elastic.co/organization/members) page under the organization name.
* The destination deployment ID. You can find this on the deployment's **Overview** page in the {{ecloud}} Console.

## Set up {{ecloud}} audit trail

To set up {{ecloud}} audit trail, you [install the integration](#install-integration) on a destination deployment, then [enable delivery](#enable-delivery) through the API. After events are flowing, you can [explore your audit trail](#explore-audit-trail) in {{kib}}.

:::::::{stepper}
:::::{step} Install the {{ecloud}} integration

Before you enable delivery, install the **{{ecloud}}** integration on the destination deployment. The integration sets up everything you need to index and explore audit log events.

To install the integration:

1. Open {{kib}} on the destination deployment.
2. Find **Integrations** in the navigation menu or use the global search field.
3. Search for **{{ecloud}}**, and then select the card from the list.
4. On the {{ecloud}} integration page, click **Add {{ecloud}}**.
5. On the installation page, click **Install assets only**. No agent policy is needed because the audit service pushes logs directly to your destination deployment.
6. Confirm the installation.

The following resources are installed:

* Index templates for `logs-elastic_cloud.audit-*`
* An ingest pipeline for the `elastic_cloud.audit` data stream
* Field mappings, including [ECS](https://www.elastic.co/docs/reference/ecs) fields and `elastic_cloud.audit.api_key.*` fields
* The **{{ecloud}} audit logs** data view (`logs-elastic_cloud.audit-*`)
* The **[{{ecloud}}] Audit Logs** dashboard
:::::

:::::{step} Enable audit log delivery

As an organization owner, enable delivery by calling the audit logs API.

Events start flowing when you enable delivery. Historical cloud audit logs are not backfilled.

1. Send a `POST` request to the audit logs endpoint, specifying your destination deployment and a data stream name that matches `logs-elastic_cloud.audit-*`. Replace the placeholders with your own values.

   ```console
   POST /api/v1/organizations/<ORG_ID>/audit_logs <1>
   Authorization: ApiKey <CLOUD_API_KEY> <2>
   Content-Type: application/json

   {
     "deployment_id": "<DESTINATION_DEPLOYMENT_ID>", <3>
     "index": "logs-elastic_cloud.audit-default" <4>
   }
   ```
   1. Replace `<ORG_ID>` with your organization ID from the {{ecloud}} console
   2. Replace `<CLOUD_API_KEY>` with your {{ecloud}} API key
   3. Replace `<DESTINATION_DEPLOYMENT_ID>` with the ID of the hosted deployment that receives the logs
   4. Represents the default data stream namespace.

   To use a different data stream namespace, replace the `default` segment of the index name with your preferred namespace, for example `logs-elastic_cloud.audit-production`. The name must match the `logs-elastic_cloud.audit-*` pattern so that the installed index templates apply.

   The data stream is created with a configurable retention policy that defaults to 30 days, and the failure store enabled.

   :::{important}
   If you omit the `index` field, events are indexed into a non-data stream index named `elastic-org<ORG_ID>-audit` without field standardization. The installed dashboard does not display data from this index.
   :::

2. Verify the configuration:

   ```console
   GET /api/v1/organizations/<ORG_ID>/audit_logs
   ```

   The response returns the configured `deployment_id` and `index`.
:::::

:::::{step} Explore your audit trail

After enabling delivery, explore your audit logs in the destination deployment:

* Use the **{{ecloud}} audit logs** data view in **Discover** to browse individual events.
* Open the **[{{ecloud}}] Audit Logs** dashboard to visualize and filter audit activity.
:::::
:::::::

## Stop delivery

If you need to decommission the destination deployment or switch to a different one, you can stop delivery at any time.

```console
DELETE /api/v1/organizations/<ORG_ID>/audit_logs
```

This stops the delivery stream and invalidates the writer API key, but does not delete documents that were already indexed.
