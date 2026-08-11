---
navigation_title: Audit trail
description: Configure and explore audit trail log delivery for Elastic Cloud Serverless, including ignore filters, destinations, data streams, and investigation recipes.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Deliver and explore audit trail logs [serverless-audit-log-delivery]

Audit trail is the first log delivery log type for {{serverless-full}}. Enabling it ships a unified audit trail so you can follow a user from {{ecloud}} and organization actions through {{es}} and {{kib}} project activity — without separate control-plane and data-plane switches.

Preferred destination: a {{sec-serverless}} project. {{obs-serverless}} destinations are also eligible. The curated audit trail experience is aimed at {{elastic-sec}}.

For shared concepts (RBAC, destinations, billing, and the log delivery page), refer to [](/deploy-manage/monitor/log-delivery.md).

## What is in the trail

Audit trail is **one** log delivery category. The following describes content only — not separate enablement:

* **{{ecloud}} and organization administration:** Sign-in, membership, IAM, and project settings where applicable. Authentication follows the {{serverless-short}} model (organization-level identity and API keys).
* **Project activity:** {{es}} and {{kib}} on the project — index, template, and pipeline lifecycle; data searches, reads, and writes when not ignored; {{kib}} saved-object and UI access when not ignored.

:::{note}
If {{ecloud}} or organization administration events land with phased richness under the same **Audit trail** row, they remain part of this single log type — not a second log delivery category.
:::

## Configure audit trail [configure-audit-trail]

### Requirements

* Complete the [log delivery requirements](/deploy-manage/monitor/log-delivery.md#requirements).
* On the source project, open **Settings → Log delivery**.

### Steps

1. In the **Audit trail** row, select a **Destination**.
   * Prefer a {{sec-serverless}} project.
   * The same project as the source is allowed.
   * The destination can be in another region in the same organization.
2. Set **Ignore filters** for the volume and evidence profile you need. Refer to [Ignore filters](#ignore-filters).
3. Save. Changes apply without restarting the project.
4. In the destination project, set retention on the audit data streams listed in [Explore](#explore-audit-trail). Refer to [data stream retention](/manage-data/lifecycle/data-stream.md).

:::{note}
Public API and Terraform examples will be added when the public API is published. Until then, configure audit trail in the Cloud UI only.

When the API is available, expect a patch or update body shaped like the following (illustrative; confirm against the published OpenAPI):

```yaml
monitoring:
  logging:
    audit:
      enabled: true
      destination:
        project_id: <id>
      ignore_filters:
        - audit-ignore-data-reads
        - audit-ignore-ui-views
```
:::

### Ignore filters [ignore-filters]

Ignore filters are **subtractive**. Selected filters drop matching events before delivery. An event is dropped if it matches **any** selected filter (logical OR).

An empty list delivers **all** audit trail events. That is the highest volume option; the UI warns when you configure full or high delivery.

#### Filter catalog

| Filter ID | Display name (UI) | Group | Approx. volume cut | UI default |
| --- | --- | --- | --- | --- |
| `audit-ignore-ui-views` | Ignore UI page views | Admin | ~10–20% | On |
| `audit-ignore-data-reads` | Ignore data searches and reads | Data access | ~50–70% | On |
| `audit-ignore-data-writes` | Ignore data writes | Data access | ~5–15% | Off |
| `audit-ignore-successful-authentications` | Ignore successful sign-ins | Security | ~5–15% | Off |
| `audit-ignore-successful-iam-checks` | Ignore routine user and role checks | Admin | ~2–5% | Off |

**UI default (Balanced):** `audit-ignore-data-reads` and `audit-ignore-ui-views`.

#### Tooltips

| Display name | Tooltip |
| --- | --- |
| Ignore data searches and reads | Don’t deliver audit events for successful searches and reads. |
| Ignore UI page views | Don’t deliver audit events for read-only UI page views. |
| Ignore successful sign-ins | Don’t deliver audit events for successful sign-ins. |
| Ignore data writes | Don’t deliver audit events for successful index, bulk, and update operations. |
| Ignore routine user and role checks | Don’t deliver audit events for routine successful user and role checks. |

#### When to use each filter

* **Data searches and reads:** Highest volume on search-heavy projects. Leave this filter off when evidence of who searched or read data is required (for example, HIPAA or PCI access evidence).
* **UI page views:** Reduces read-only UI navigation noise. Saved-object mutations are still delivered.
* **Successful sign-ins / routine IAM checks:** Apply to authentication and IAM-related events in the unified audit trail (including {{ecloud}} and organization signals when present). Useful for SOC or minimal profiles; leave off when sign-in or IAM accountability is required.
* **Data writes:** Omits authorized ingest and bulk activity when you want configuration and object-change evidence without write volume.

#### Recommended combinations

These combinations are documentation guidance only. They are not separate UI presets beyond the Balanced default.

| Combination | Ignore filters to select | Est. volume | Typical use |
| --- | --- | --- | --- |
| Balanced (UI default) | Data reads, UI views | Moderate | General production |
| Full audit trail | (none) | Full | Forensics / maximum end-to-end evidence |
| Compliance (changes and sign-ins) | Data reads | Elevated | Change accountability without search noise |
| Security events only | Data reads, UI views, successful authentications | Low | Failure-oriented monitoring |
| Admin and configuration | Data reads, UI views, data writes | Low | ITGC / change management |
| Minimal | All five | Minimal | Dev / sandbox |

What each combination still tends to deliver:

| Combination | Security | Admin | Data reads | Data writes | UI access |
| --- | --- | --- | --- | --- | --- |
| Balanced | ✓ | ✓ | ✗ | ✓ | ✗ |
| Full audit trail | ✓ | ✓ | ✓ | ✓ | ✓ |
| Compliance (changes and sign-ins) | ✓ | ✓ | ✗ | ✓ | ✓ |
| Security events only | ✓ | Partial | ✗ | ✗ | ✗ |
| Admin and configuration | Partial | ✓ | ✗ | ✗ | ✗ |
| Minimal | Partial | Partial | ✗ | ✗ | ✗ |

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

### Limitations

Platform-wide log delivery limitations also apply. Refer to [](/deploy-manage/monitor/log-delivery.md#limitations).
