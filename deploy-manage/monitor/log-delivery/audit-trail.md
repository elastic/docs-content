---
navigation_title: Audit trail
description: Configure and explore audit trail log delivery for Elastic Cloud Serverless, including ignore filters, destinations, data streams, and investigation recipes.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Audit trail log delivery [serverless-audit-log-delivery]

Audit trail is the first log type available for [log delivery](/deploy-manage/monitor/log-delivery.md) in {{serverless-full}}. Enabling it delivers audit logs to your selected destination project so you can track organization actions throughout the source project.

## What's included

An audit trail includes the following events:

* **{{ecloud}} and organization administration:** Sign-in, membership, IAM, and project settings where applicable
* **Project activity:** {{es}} and {{kib}} on the project — index, template, and pipeline lifecycle; data searches, reads, and writes; {{kib}} saved-object and UI access.

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
| Ignore data searches and reads | Select to cut the highest-volume events on search-heavy projects. Do not select if you need evidence of who searched or read data (for example, HIPAA or PCI). <br>On by default. | ~50–70% |
| Ignore data writes | Select when you want configuration and object-change evidence without ingest and bulk write volume. | ~5–15% |
| Ignore successful sign-ins | Select for SOC or minimal profiles that focus on failures. Do not select if you need successful sign-in accountability. Applies to authentication events in the unified audit trail, including {{ecloud}} and organization signals when present. | ~5–15% |
| Ignore routine user and role checks | Select for SOC or minimal profiles that focus on failures. Do not select if you need IAM accountability. Applies to IAM-related events in the unified audit trail, including {{ecloud}} and organization signals when present. | ~2–5% |
| Ignore UI requests | Select to drop read-only UI navigation noise. Saved-object mutations are still delivered. <br>On by default. | ~10–20% |

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

## Explore audit trail [explore-audit-trail]

Explore delivered audit trail data in the **destination** project (which may be the same as the source).

### Where logs land

| Data stream | Contents |
| --- | --- |
| `logs-serverless.audit.otel-elastic_cloud` | Project-level audit logs ({{es}}, {{kib}}, and {{ecloud}} project signals) |
| `logs-org.audit.otel-elastic_cloud` | Organization-level audit logs (administration, configuration, billing, and similar) |
| `logs-*.audit.otel-*` | Catch-all index pattern |

All of these belong to the same audit trail delivery category — one enablement on log delivery.

Filter and correlate across producers with fields such as `project.id`, `project.name`, `organization.id`, `user.*`, and `service.name`. Producers include values such as `serverless-elasticsearch` and `serverless-kibana`, plus control-plane service names when present. Audit events use `log.type: audit`.

### Curated UI

A curated Audit Logs experience in {{elastic-sec}} is intended to present the unified trail (not separate {{ecloud}} versus project apps). Until that UI is available in your project, use **Discover** or {{esql}} across the audit data streams.

### What to investigate

Useful filters include `@timestamp`, `user.*`, `event.action` / `event.category` / `event.type` / `event.outcome`, `source.ip`, `project.id`, `organization.id`, `service.name`, and producer-specific fields.

Typical investigations:

* Organization sign-in → project access → index or saved-object changes
* Access denied on an index pattern
* IAM or membership changes
* Data reads or writes (only if the corresponding ignore filters are off)

To check volume and retention impact, use [AutoOps](/deploy-manage/monitor/autoops/autoops-for-serverless.md) on the destination for per–data-stream ingest rate and storage retained.

### Recipes

* Failed or successful sign-ins for a user ({{ecloud}} and organization portion of audit trail).
* Membership, IAM, or project-admin changes.
* Access denied on an index pattern (project activity).
* Index, template, or pipeline create, update, or delete.
* {{kib}} saved-object change or delete (for example, detection rules).
* Who searched a sensitive index — only if **Ignore data searches and reads** is off.
* One user journey across `service.name` values for the same `user.name` and time window.
