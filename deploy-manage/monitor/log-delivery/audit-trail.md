---
navigation_title: Audit trail
description: Configure and explore audit trail log delivery for Elastic Cloud Serverless, including ignore filters, destinations, data streams, and investigation recipes.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Audit trail log delivery

Audit trail is the first log type available for [log delivery](/deploy-manage/monitor/log-delivery.md) in {{serverless-full}}. Enabling it delivers audit logs to your selected destination project so you can track and investigate organization actions in the source project.

## What's included

An audit trail includes the following events:

* **{{ecloud}} and organization administration:** Sign-in, membership, IAM, and project settings where applicable
* **Project activity:** {{es}} and {{kib}} on the project — index, template, and pipeline lifecycle; data searches, reads, and writes; {{kib}} saved-object and UI access.

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
    * In the **Destination** column, select one or more {{sec-serverless}} or {{obs-serverless}} projects to receive the logs.
      :::{tip}
      We recommend selecting an {{sec-serverless}} project as the destination for your audit trail.
      :::
    * Choose [ignore filters](#audit-trail-ignore-filters) to exclude certain events before delivery. Leave the list empty only if you want to deliver all events for that log type.
    * Switch the toggle to **Enabled**.
4. Select **Save**.

## Audit trail ignore filters

Apply ignore filters to exclude certain events from being delivered. Refer to [](/deploy-manage/monitor/log-delivery.md#ignore-filters) to learn more about their impact on your delivery volume and bill.

The following table describes which ignore filters are available for the audit trail log type, when to select them, and how much they reduce your delivery volume.

| Name | When to select | Approx. volume cut |
| --- | --- | --- |
| Ignore data searches and reads | Select to exclude the highest-volume events on search-heavy projects. Do not select if you need evidence of who searched or read data (for example, HIPAA or PCI). <br>On by default. | ~50–70% |
| Ignore data writes | Select when you want configuration and object-change evidence without ingest and bulk write volume. | ~5–15% |
| Ignore successful sign-ins | Select for SOC or minimal profiles that focus on failures. Do not select if you need successful sign-in accountability. Applies to authentication events in the unified audit trail, including {{ecloud}} and organization signals when present. | ~5–15% |
| Ignore routine user and role checks | Select for SOC or minimal profiles that focus on failures. Do not select if you need IAM accountability. Applies to IAM-related events in the unified audit trail, including {{ecloud}} and organization signals when present. | ~2–5% |
| Ignore UI requests | Select to exclude read-only UI navigation noise. Saved-object mutations are still delivered. <br>On by default. | ~10–20% |

### Recommended usage

| Combination | Ignore filters to select | Est. volume | Typical use |
| --- | --- | --- | --- |
| Balanced (UI default) | Data reads, UI views | Moderate | General production |
| Full audit trail | (none) | Full | Forensics / maximum end-to-end evidence |
| Compliance (changes and sign-ins) | Data reads | Elevated | Change accountability without search noise |
| Security events only | Data reads, UI views, successful authentications | Low | Failure-oriented monitoring |
| Admin and configuration | Data reads, UI views, data writes | Low | ITGC / change management |
| Minimal | All five | Minimal | Dev / sandbox |

:::{note}
For **Security events only**, successful sign-ins are ignored when that filter is on, so the Security column is failure-oriented. Security and Admin columns include {{ecloud}} and organization signals when those events are present in the delivered trail.
:::

#### Compliance starting points

These starting points are **not legal advice**. Validate retention, scope, and evidence requirements with your compliance team.

| Need | Start from | Important |
| --- | --- | --- |
| HIPAA / PCI (data access evidence) | Full audit trail | Do not enable **Ignore data searches and reads** |
| GDPR (accountability) | Balanced or Compliance | Enable the data-reads ignore unless access proof is required |
| SOX (ITGC) | Compliance or Admin and configuration | — |
| Dev / test | Minimal | Enable all ignore filters |

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