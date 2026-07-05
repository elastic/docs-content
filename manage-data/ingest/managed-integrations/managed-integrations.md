---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/security-agentless-integrations.html
applies_to:
  stack: preview
  serverless: preview
products:
  - id: elastic-agent
  - id: fleet
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
description: Elastic Managed integrations let you ingest data from cloud sources into Elastic Cloud with no collectors to deploy or maintain.
type: overview
---

# {{managed-integrations}}

{{managed-integrations}} (previously known as agentless integrations) let you ingest data from cloud sources into Elastic without deploying or maintaining any collectors yourself. Elastic runs the collectors for you and writes the data directly to your cluster, so you can focus on the data rather than on the infrastructure that gathers it. {{managed-integrations}} are available on {{ech}} deployments and on {{obs-serverless}} and {{sec-serverless}} projects.

To enable an {{managed-integration}} in {{kib}}, refer to [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md).

:::{important}
{{managed-integrations}} are a technical preview feature. The design and code are less mature than GA features, and Elastic provides them as-is with no warranties. The support SLA for GA features doesn't apply. There are no additional costs for {{managed-integrations}} during technical preview.
:::

:::{note}
{{kib}} still uses the earlier name in some places. You'll see the term **Agentless** in filter options, deployment mode selectors, and other UI elements until they're updated in a future release.
:::

## How {{managed-integrations}} work [agentless-architecture]

When you enable an {{managed-integration}}, Elastic provisions a dedicated collector for it on Elastic-managed infrastructure. Under the hood, each collector runs the same {{agent}} and integration package you'd deploy yourself for the equivalent agent-based integration — but Elastic provisions, updates, and operates it for you.

The collector pulls data from the source API and writes documents to your {{es}} cluster through the standard `_bulk` API. For most integrations, data flows through the integration's ingest pipelines and lands in the same data streams as it would for a self-managed integration. {{managed-integrations}} built on OpenTelemetry are an exception: their data bypasses ingest pipelines and lands in the integration's dedicated data streams (typically in `.otel-*` data streams).

Each {{managed-integration}} runs in its own collector, which keeps your data isolated from other tenants while it's being ingested.

Behind the scenes, a small set of shared, stateless control plane components orchestrate the lifecycle of these collectors: an **Agentless API** that receives provisioning requests, an **Agentless Controller** that creates and updates the collectors, and an **Agentless Cleaner** that removes them when an integration is deleted. None of these components store customer data.

:::{image} /manage-data/images/managed-integrations-architecture.png
:alt: Architecture diagram for {{managed-integrations}}, showing the Agentless API, Controller, and Cleaner orchestrating per-integration collectors on Elastic-managed infrastructure. The collectors pull data from cloud sources through a cloud proxy and write to {{es}} over the `_bulk` API, while {{fleet-server}} delivers their policies.
:::

The dashed boundary labeled **MKI** (Managed Kibana Infrastructure) in the diagram represents the Elastic-managed infrastructure that hosts these control plane components and the per-integration collectors.

## Limits and scaling [agentless-limits]

{{managed-integrations}} are designed for cloud data sources that expose data through an API at moderate volumes. The following limits apply:

* **Maximum {{managed-integrations}} per project**: 50.
* **No horizontal scaling**: deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).
* **Rate limiting** {applies_to}`serverless: preview`: integrations whose underlying input type is `httpjson` or `cel` (two common pull-based input mechanisms in {{agent}}) are rate-limited on {{serverless-short}} to preserve quality of service. Rate limiting uses back-pressure rather than dropping events, so collection slows down until the source catches up.

## Security and data residency [agentless-data-security]

The collector for each {{managed-integration}} writes documents directly to your cluster. Data is stored in your project or deployment, and Elastic employees don't have access to it.

Each collector is dedicated to a single {{managed-integration}}: no other workloads can be added to it.

## Manage and monitor {{managed-integrations}} [manage-agentless-integrations]

{{managed-integrations}} are a fully managed service: Elastic operates the collectors and resolves service-level issues on your behalf, and the collectors aren't visible in **{{fleet}}** by default. You still keep visibility into the parts that matter to you — each integration's status is available in the **{{integrations}}** app, and the ingested data lands in your cluster so you can query, dashboard, and set [alerting rules](/explore-analyze/alerting.md) on it as you would for any other integration.

For service issues or to request diagnostics, contact [Elastic Support](https://support.elastic.co).

## Related [agentless-related]

* [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md)
* [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md)
* [Troubleshoot {{managed-integrations}}](/troubleshoot/ingest/managed-integrations.md)
* [Cloud connector authentication for {{managed-integrations}}](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md)
* [{{managed-integrations}} quick reference](integration-docs://reference/agentless_integrations.md)
