---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
description: Elastic Managed integrations let you ingest data from cloud sources into Elastic Cloud with no collectors to deploy or maintain.
applies_to:
  stack: ga 9.5+, preview 9.0-9.4
  serverless: preview
products:
  - id: elastic-agent
  - id: fleet
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
type: overview
---

# {{managed-integrations}}

{{managed-integrations}} let you ingest data from cloud sources into Elastic without deploying or maintaining any collectors yourself. Elastic runs the collectors for you and writes the data directly to your cluster, so you can focus on the data rather than on the infrastructure that collects it. {{managed-integrations}} are available on {{serverless-full}} and {{ech}} deployments.

To enable an {{managed-integration}} in {{kib}}, refer to [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md).

:::{important}
:applies_to: stack: preview 9.0-9.4
{{managed-integrations}} are a technical preview feature. The design and code are less mature than GA features, and Elastic provides them as-is with no warranties. The support SLA for GA features doesn't apply. There are no additional costs for {{managed-integrations}} during technical preview.
:::

## How {{managed-integrations}} work [managed-integrations-architecture]

When you enable an {{managed-integration}}, Elastic provisions a dedicated collector for it on Elastic-managed infrastructure. Under the hood, each collector runs the same {{agent}} and integration package you'd deploy yourself for the equivalent agent-based integration but Elastic provisions, updates, and operates it for you.

The collector pulls data from the source API and writes documents to your {{es}} cluster through the standard `_bulk` API. For most integrations, data flows through the integration's ingest pipelines and lands in the same data streams as it would for a self-managed integration. {{managed-integrations}} built on OpenTelemetry are an exception: their data bypasses ingest pipelines and lands in the integration's dedicated data streams (typically in `.otel-*` data streams).

Each {{managed-integration}} runs in its own collector, which keeps your data isolated from other tenants while it's being ingested.

Behind the scenes, a shared, stateless Controller orchestrates the lifecycle of these collectors. When you enable an integration in {{kib}}, the Controller creates and updates the collector, and it removes the collector when you delete the integration. The Controller doesn't store customer data.

:::{image} /manage-data/images/managed-integrations-architecture.png
:alt: Architecture diagram for {{managed-integrations}}. A request in {{kib}} triggers the Controller to create per-integration collectors on Elastic-managed infrastructure. Each collector pulls data from a cloud source (such as Okta or Snyk) through a cloud proxy, writes documents to {{es}} over the `_bulk` API, and receives its configuration from {{es}}.
:::

## Limits and scaling [managed-integrations-limits]

{{managed-integrations}} are designed for cloud data sources that expose data through an API at moderate volumes. The following limits apply:

* **Maximum {{managed-integrations}} per project**: 50.
* **No horizontal scaling**: Deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).
* **Rate limiting**: Integrations whose underlying input type is `httpjson` or `cel` (two common pull-based input mechanisms in {{agent}}) are rate-limited on {{serverless-short}} to preserve quality of service. Rate limiting uses back-pressure rather than dropping events, so collection slows down until the source catches up.

## Security and data residency [managed-integrations-data-security]

The collector for each {{managed-integration}} writes documents directly to your cluster. Data is stored in your project or deployment, and Elastic employees don't have access to it.

Each collector is dedicated to a single {{managed-integration}}: no other workloads can be added to it.

## Manage and monitor {{managed-integrations}} [managed-integrations-management]

{{managed-integrations}} are a fully managed service: Elastic operates the collectors and resolves service-level issues on your behalf. The collectors aren't visible in {{fleet}} by default. You still keep visibility into the parts that matter to you — each integration's status is available in the {{integrations}} app, and the ingested data lands in your cluster so you can query it, use dashboards, and set [alerting rules](/explore-analyze/alerting.md) on it as you would for any other integration.

For service issues or to request diagnostics, contact [Elastic Support](https://support.elastic.co).

## Related pages [managed-integrations-related]

* [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md)
* [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md)
* [Authenticate {{managed-integrations}} using cloud connectors](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md)
* [Managed integrations quick reference](integration-docs://reference/managed_integrations.md)
