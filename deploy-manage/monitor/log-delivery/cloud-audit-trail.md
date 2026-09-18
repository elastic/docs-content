---
navigation_title: Cloud audit trail
description: Track organization-level actions in Elastic Cloud Hosted by delivering audit logs to a hosted deployment you own.
applies_to:
  ech:
products:
  - id: cloud-hosted
---

# Cloud audit trail for {{ech}}

Cloud audit trail records actions that members of your organization perform through the {{ecloud}} Console, the Terraform Provider for {{ecloud}}, or any other client that calls the {{ecloud}} API.

Cloud audit trail is available on {{fedramp-mod}} environments only.

Audited actions include:

* Managing hosted deployments: creation, configuration changes, scaling, upgrades, and deletion
* Managing organization membership and invitations
* Managing Cloud API keys
* Managing network security configurations such as traffic filters, trust relationships, SSO, and role mappings
* Sign-in, sign-out, and authentication attempts

:::{note}
Cloud audit trail does not include {{es}} audit events, {{kib}} audit events, or {{serverless-full}} project activity. To capture activity within a deployment, enable audit logging on the deployment directly. Refer to [](/deploy-manage/security/logging-configuration/enabling-audit-logs.md). For serverless audit logging, refer to [](/deploy-manage/monitor/log-delivery/audit-trail.md).
:::

Using cloud audit trail data, you can answer questions such as:

* Which user or API key attempted to sign in, and did they succeed or fail?
* Which user scaled resources or changed the configuration of a deployment?
* Which API endpoints is a given API key calling?
* Who modified traffic filters, and when?
* Who upgraded or deleted a deployment?

## Before you begin

To use the cloud audit trail, you need:

* A Platinum or Enterprise subscription
* An [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with organization owner permissions. You must run the enablement API yourself. Support cannot enable it on your behalf.
* A hosted destination deployment in the same organization. You might choose to use a dedicated deployment to keep audit data separate from production workloads.
* Your [organization ID](/deploy-manage/cloud-organization.md) and the destination [deployment ID](/deploy-manage/deploy/elastic-cloud/manage-deployments.md), both available in the {{ecloud}} console

Audit trail events start flowing when you enable the stream. Historical cloud audit logs are not backfilled.

## Install the {{ecloud}} integration [install-integration]

Before you enable delivery, install the **{{ecloud}}** integration on the destination deployment.

The integration installs the following resources:

* Index templates for `logs-elastic_cloud.audit-*`
* An ingest pipeline for the `elastic_cloud.audit` data stream
* Field mappings, including ECS fields and `elastic_cloud.audit.api_key.*` fields
* The **{{ecloud}} audit logs** data view (`logs-elastic_cloud.audit-*`)
* The **[{{ecloud}}] Audit Logs** dashboard

In {{kib}} on the destination deployment:

1. Find **Integrations** in the navigation menu or use the global search field.
2. Search for **{{ecloud}}**.
3. Click **Add {{ecloud}}**.
4. Click **Install assets only**. No agent policy is needed because the audit service pushes logs directly to your destination deployment.
5. Confirm the installation.

## Enable cloud audit trail delivery [enable-delivery]

There is no {{ecloud}} Console UI for this step. As an organization owner, enable delivery by calling the audit logs API.

Send a `POST` request to the audit logs endpoint, specifying your destination deployment and a data stream name that matches `logs-elastic_cloud.audit-*`:

```console
POST /api/v1/organizations/<ORG_ID>/audit_logs
Authorization: ApiKey <CLOUD_API_KEY>
Content-Type: application/json

{
  "deployment_id": "<DESTINATION_DEPLOYMENT_ID>",
  "index": "logs-elastic_cloud.audit-default"
}
```

Replace the following values:

* `<ORG_ID>`: Your organization ID from the {{ecloud}} console
* `<CLOUD_API_KEY>`: Your {{ecloud}} API key
* `<DESTINATION_DEPLOYMENT_ID>`: The ID of the hosted deployment that receives the logs

To use a different data stream namespace, replace `default` with your preferred namespace, for example `logs-elastic_cloud.audit-production`. The name must match the `logs-elastic_cloud.audit-*` pattern so that the installed index templates apply.

The data stream is created with a configurable retention policy that defaults to 30 days, and the failure store enabled.

:::{important}
If you omit the `index` field, events land on a classic index named `elastic-org<ORG_ID>-audit` without field standardization. The installed dashboard does not display data from this index.
:::

### Check delivery status

To verify the current configuration:

```console
GET /api/v1/organizations/<ORG_ID>/audit_logs
```

The response returns the configured `deployment_id` and `index`.

### Stop delivery

To stop delivery:

```console
DELETE /api/v1/organizations/<ORG_ID>/audit_logs
```

This stops the delivery stream and invalidates the writer API key, but does not delete documents that were already indexed.

## Explore your audit trail [explore-audit-trail]

After enabling delivery, explore your audit logs in the destination deployment:

* Use the **{{ecloud}} audit logs** data view in **Discover** to browse individual events.
* Open the **[{{ecloud}}] Audit Logs** dashboard to visualize and filter audit activity.
