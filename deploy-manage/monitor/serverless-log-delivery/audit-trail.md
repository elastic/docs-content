---
navigation_title: Audit trail
description: Configure and explore audit trail log delivery for Elastic Cloud Serverless, including ignore filters, destinations, data streams, and investigation recipes.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Audit trail log delivery

Audit trail is the first log type available for [log delivery](/deploy-manage/monitor/serverless-log-delivery.md) in {{serverless-full}}. Enabling it delivers audit logs to your selected destination project so you can track and investigate organization actions in the source project.

## What's included

An audit trail includes the following events:

* **{{ecloud}} and organization administration:** Sign-in, membership, IAM, and project settings
* **Project activity:** {{es}} and {{kib}} activity including index, template, and pipeline lifecycle, data searches, reads, and writes, and UI access.

Audit trail delivery is applicable to {{serverless-short}} projects, so {{ech}} fields like `node.*` and `host.*` are not included.

### Why deliver an audit trail

Delivering an audit trail into a project lets you investigate end-to-end activity in one place. For example, you can:

* Trace failed or successful sign-ins for a user
* Review membership, IAM, or project-admin changes
* Investigate access denied on an index pattern
* Track create, update, or delete actions on indices, templates, or pipelines
* Detect changes or deletions of {{kib}} saved objects such as detection rules
* Determine who searched a sensitive index
* Follow one user journey across `service.name` values for the same `user.name` and time window

## Set up delivery for audit trail

Complete the following steps to configure log delivery in your project.

### Before you begin

You must have the **Admin** or **Editor** [role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) on the source project.

### Configuration steps

1. On your {{ecloud}} homepage, find the project that should be the source of your log deliveries and select **Manage**.
2. From the navigation menu, select **Log delivery**.
3. For **Audit trail**, complete the following fields.
    * In the **Destination** column, select a {{sec-serverless}} or {{obs-serverless}} project to receive the logs.
      :::{tip}
      Since audit logs are security data, we recommend selecting a {{sec-serverless}} project as the destination for your audit trail.
      :::
    * Choose [ignore filters](#audit-trail-ignore-filters) to exclude certain events before delivery. Leave the list empty only if you want to deliver all events for that log type.
    * Switch the toggle to **Enabled**.
4. Select **Save**.

## Audit trail ignore filters

Apply ignore filters to exclude certain events from being delivered. Refer to [](/deploy-manage/monitor/serverless-log-delivery.md#ignore-filters) to learn more about their impact on your delivery volume and bill.

The following table describes which ignore filters are available for the audit trail log type and when to select them.

| Name | When to select |
| --- | --- |
| Ignore data searches and reads | Select to exclude the highest-volume events on search-heavy projects. Do not select if you need evidence of who searched or read data. |
| Ignore data writes | Select when you want configuration and object-change evidence without ingest and bulk write volume. |
| Ignore successful sign-ins | Select for security operations or minimal profiles that focus on failures. Do not select if you need successful sign-in accountability. Applies to authentication events in the audit trail, including {{ecloud}} and organization signals when present. |
| Ignore routine user and role checks | Select for security operations or minimal profiles that focus on failures. Do not select if you need IAM accountability. Applies to IAM-related events in the audit trail, including {{ecloud}} and organization signals when present. |
| Ignore UI requests | Select to exclude read-only UI navigation noise. Saved object mutations are still delivered. |

### Ignore filter combinations

In the following table, find the recommended combination of filters to select for typical use cases.

| Typical use | Ignore filters to select |
| --- | --- |
| General production | • Ignore data searches and reads<br>• Ignore UI requests |
| Maximum end-to-end evidence | (none) |
| Change accountability without search noise | • Ignore data searches and reads |
| Failure-oriented monitoring | • Ignore data searches and reads<br>• Ignore UI requests<br>• Ignore successful sign-ins |
| Change management | • Ignore data searches and reads<br>• Ignore UI requests<br>• Ignore data writes |
| Dev or sandbox | • Ignore data searches and reads<br>• Ignore data writes<br>• Ignore successful sign-ins<br>• Ignore routine user and role checks<br>• Ignore UI requests |

### Compliance starting points

These starting points are **not legal advice**. Validate retention, scope, and evidence requirements with your compliance team.

| Need | Start from | Important |
| --- | --- | --- |
| HIPAA / PCI (data access evidence) | Forensics / maximum end-to-end evidence | Do not enable **Ignore data searches and reads** |
| GDPR (accountability) | General production or Change accountability without search noise | Enable the data-reads ignore unless access proof is required |
| SOX (ITGC) | Change accountability without search noise or ITGC / change management | — |
| Dev / test | Dev / sandbox | Enable all ignore filters |

## Explore delivered logs

Explore delivered audit trail logs in the following locations on your destination project:

| Data stream or index pattern | Contents |
| --- | --- |
| `logs-serverless.audit.otel-elastic_cloud` | Project-level audit logs ({{es}}, {{kib}}, and {{ecloud}} project signals) |
| `logs-org.audit.otel-elastic_cloud` | Organization-level audit logs (administration, configuration, billing, and similar) |
| `logs-*.audit.otel-*` | All audit logs |

Use Discover or {{esql}} to investigate these logs. Useful fields to query on include:

* `@timestamp`
* `user.*`
* `event.action` / `event.category` / `event.type` / `event.outcome`
* `source.ip`
* `project.id`
* `organization.id`
* `service.name`
* Producer-specific fields

Additionally, use [AutoOps](/deploy-manage/monitor/autoops/autoops-for-serverless.md) on the destination project to monitor your ingest rate and storage retained.