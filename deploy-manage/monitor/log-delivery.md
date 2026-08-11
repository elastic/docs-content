---
navigation_title: Log delivery
description: Ship selected log types from any Elastic Cloud Serverless project to a Security or Observability project in your organization, with per-type ignore filters and cross-region delivery.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Log delivery in {{serverless-full}} [log-delivery]

Log delivery lets you ship selected log types from a {{serverless-full}} project to a {{sec-serverless}} or {{obs-serverless}} project in your organization. Configure each log type independently — including destination and ignore filters — without restarting the project.

The first supported log type available for delivery is **Audit trail**. Additional types are coming soon and will follow the same configuration pattern.

## What you can do

With log delivery, you can:

* Centralize activity evidence from one or many source projects into {{sec-serverless}} and {{obs-serverless}} destinations.
* Follow an end-to-end user journey when audit trail is enabled — {{ecloud}} and organization administration together with {{es}} and {{kib}} project activity, as a single log type.
* Reduce volume and noise with subtractive ignore filters per log type.
* Apply configuration changes without restarting the project.
* Set retention on destination data streams to match compliance or cost needs.

## Requirements

* A {{serverless-full}} source project.
* A {{sec-serverless}} or {{obs-serverless}} project in the same organization to use as the destination (the source project itself is allowed).
* The **Admin** or **Editor** [role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) on the source project.

## Key concepts

Keep the following in mind before you configure log delivery:

* **Off by default.** Nothing is delivered until you set a destination, configure the log type, and save.
* **Empty ignore filters mean full delivery.** An empty ignore-filter list delivers all events for that log type. That is the highest volume option and directly affects your {{serverless-short}} bill. Selected ignore filters drop matching events **before** delivery.
* **Sources and destinations.** Any {{serverless-short}} project type can be a source. Initial destinations are {{sec-serverless}} or {{obs-serverless}} projects only.
* **Same project is valid.** Using the source project as its own destination works well for single-project estates. Multi-project organizations often ship to a dedicated {{sec-serverless}} or {{obs-serverless}} project.
* **Cross-region from day one.** The destination can be in a different cloud provider region than the source, as long as both are in the same organization. This differs from {{ech}} logging and monitoring, which requires the same region.
* **Preferred destinations (guidance only).** Prefer {{sec-serverless}} for audit trail and {{obs-serverless}} for query logs when those types are available.
* **At-least-once delivery.** Duplicates are possible; design investigations accordingly.
* **Source attribution.** Delivered records include fields such as `project.id`, `project.name`, `organization.id`, and region or cloud provider metadata when available, so you can correlate journeys across producers.
* **Who can configure.** Admin or Editor on the project. Configuration changes are themselves auditable when audit trail is enabled.

## Billing and cost control [billing]

Log delivery usage is metered so you can control cost without needing to manage cluster-side log shipping. Exact rates are on the pricing pages; this section covers what you can control and how usage is attributed.

For current rates, refer to:

* [{{sec-serverless}} pricing](https://www.elastic.co/pricing/serverless-security)
* [{{obs-serverless}} pricing](https://www.elastic.co/pricing/serverless-observability)

**What you can control**

* Enable or disable individual log types.
* Choose ignore filters to reduce delivered volume.
* Set retention on destination data streams.

Disabling a log type stops further ingest for that stream. Filters and retention affect ongoing ingest and storage consistently.

**How usage is attributed**

* Usage is attributed per **source → log type → destination** stream, so you can see which pairs drive volume.
* Delivered and billed volume is measured **after** ignore filters.
* Ingestion and retention are billed on the **destination** project.
* Data transfer is attributed on the **source → destination** path. Same-project delivery is not expected to incur transfer charges; cross-region delivery does. See the pricing pages for rates.

**High-volume configurations**

Configurations with few or no ignore filters (for example, a full audit trail) can generate substantial volume. Prefer a balanced filter set for general production use unless you need maximum evidence.

**Usage visibility**

On the destination project, [AutoOps](/deploy-manage/monitor/autoops/autoops-for-serverless.md) shows per–data-stream ingest rate and storage retained. Use it to answer how much you are shipping and keeping.

## The log delivery page [log-delivery-page]

Configure log delivery in the {{ecloud}} console:

1. Open your {{serverless-short}} project.
2. Go to **Settings → Log delivery**.

You need the **Admin** or **Editor** role on the project. Changes you make on this page are auditable.

:::{note}
Public API and Terraform support will be documented when they are published. Until then, configure log delivery in the Cloud UI only.
:::

The page lists one row per log type:

| Column | Meaning |
| --- | --- |
| **Log type** | For example, **Audit trail** (later types such as query logs use the same layout). |
| **Destination** | A {{sec-serverless}} or {{obs-serverless}} project in the same organization. May be the same project as the source. |
| **Ignore filters** | Type-specific multi-select filters that drop matching events before delivery. |

Additional rules for the page:

* The destination must be a {{sec-serverless}} or {{obs-serverless}} project. The console validates eligibility before activation.
* Cross-region destinations in the same organization are supported. Refer to [Billing and cost control](#billing) for transfer implications.
* Retention is configured on destination data streams, not on the log delivery page. Refer to [data stream retention](/manage-data/lifecycle/data-stream.md).
* Saving applies without a project restart. Delivery is at-least-once. Data is encrypted in transit and at rest.

**Generic flow**

1. Open **Log delivery**.
2. For a log type row, set **Destination** and **Ignore filters**.
3. Save.
4. In the destination project, set retention on the relevant data streams and explore the data. Use AutoOps to monitor volume.

## Log types

Configure and explore each log type on its own page. Shared UI behavior is described on this page; each log type page adds only type-specific filters, data streams, and investigation guidance.

* [](/deploy-manage/monitor/log-delivery/audit-logs.md) — first supported log type (Configure and Explore).

Additional log types (for example, query logs and user activity logs) will be documented here when they become available.

## Limitations [limitations]

* {{serverless-short}} data-plane audit events do not include {{ech}} topology fields such as `node.*` and `host.*`.
* Some HTTP response fields may be missing on {{es}} audit events at event time.
* The audit trail is a single log type. The set of events in the trail (including {{ecloud}} and organization administration signals) may expand over time under the same **Audit trail** row — not as a separate log delivery category.

## What this feature does not cover

* {{ech}} Logs and metrics / stack monitoring setup or migration. For {{ech}} deployments, refer to [](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md).
* {{ech}} or self-managed destinations. Initial {{serverless-short}} log delivery supports {{sec-serverless}} and {{obs-serverless}} destinations only.
* Implementation details of how events are produced inside the cluster. Customer-facing configuration is limited to log type, ignore filters, and destination.
