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
description: Ingest data from cloud sources into Elastic with no agents to deploy or manage. Agentless integrations on Elastic Cloud are a fully managed service for cloud telemetry.
type: overview
---

# {{managed-integrations-cap}}

{{managed-integrations-cap}} let you ingest data from cloud sources into Elastic without deploying or managing {{agents}} yourself. Elastic provisions, scales, and operates the underlying infrastructure on your behalf, so you can focus on your data instead of the infrastructure that collects it. {{managed-integrations-cap}} are available on {{ech}} deployments and on {{obs-serverless}} and {{sec-serverless}} projects.

To enable an {{managed-integration}} in {{kib}}, see [Enable an {{managed-integration}}](/manage-data/ingest/agentless/enable-agentless-integration.md).

:::{important}
{{managed-integrations-cap}} are a technical preview feature. The design and code are less mature than GA features, and Elastic provides them as-is with no warranties. The support SLA for GA features doesn't apply. There are no additional costs for {{managed-integrations}} during technical preview.
:::

## How {{managed-integrations}} work [agentless-architecture]

When you enable an {{managed-integration}}, Elastic provisions a dedicated {{agent}} for it on Elastic-managed infrastructure. The {{agent}} pulls data from the source API and writes documents to your {{es}} cluster through the standard `_bulk` API. Data flows through the integration's ingest pipelines and lands in the same data streams as it would for a self-managed {{agent}}. Each {{managed-integration}} runs in its own {{agent}}, which keeps your data isolated from other tenants while it's collected.

A small set of shared, stateless control plane components — **Agentless API**, **Agentless Controller**, and **Agentless Cleaner** — orchestrate the lifecycle of these {{agents}}. These components don't store customer data.

:::{image} /manage-data/images/agentless-architecture.png
:alt: Architecture diagram for {{managed-integrations}}, showing the Agentless API, Controller, and Cleaner orchestrating per-integration {{agents}} on Elastic-managed infrastructure. The agents pull data from cloud sources through a cloud proxy and write to {{es}} over the `_bulk` API, while {{fleet-server}} delivers their policies.
:::

The dashed boundary labeled **MKI** (Managed Kibana Infrastructure) in the diagram represents the Elastic-managed infrastructure that hosts the agentless control plane and the per-integration {{agents}}.

## Limits and scaling [agentless-limits]

{{managed-integrations-cap}} are designed for cloud data sources that expose data through an API at moderate volumes. The following limits apply:

* **Maximum {{managed-integrations}} per project**: 50.
* **No horizontal scaling**: deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).
* **Rate limiting** {applies_to}`serverless: preview`: integrations whose underlying input type is `httpjson` or `cel` (two common pull-based input mechanisms in {{agent}}) are rate-limited on {{serverless-short}} to preserve quality of service. Rate limiting uses back-pressure rather than dropping events, so collection slows down until the source catches up.

## Security and data residency [agentless-data-security]

The {{agent}} for each {{managed-integration}} writes documents directly to your cluster. Data is stored in your project or deployment, and Elastic employees don't have access to it.

The agentless service is locked down so that only the integration you configured runs on a given {{agent}}. Other workloads can't be added to it.

## Manage and monitor {{managed-integrations}} [manage-agentless-integrations]

{{managed-integrations-cap}} are a fully managed service: the underlying {{agents}} aren't visible in **{{fleet}}** by default, and you don't need to monitor their health. Elastic operates the infrastructure and resolves service-level issues on your behalf.

You can observe data flow into your cluster the same way you would for any other integration — by querying the destination data streams, building dashboards, or setting up [alerting rules](/explore-analyze/alerting.md) on the data.

For service issues or to request diagnostics, contact [Elastic Support](https://support.elastic.co).

## Related [agentless-related]

* [Enable an {{managed-integration}}](/manage-data/ingest/agentless/enable-agentless-integration.md)
* [{{managed-integrations-cap}} FAQ](/manage-data/ingest/agentless/agentless-integrations-faq.md)
* [Troubleshoot {{managed-integrations}}](/troubleshoot/ingest/agentless-integrations.md)
* [Cloud connector authentication for {{managed-integrations}}](/manage-data/ingest/agentless/cloud-connector-deployment.md)
* [{{managed-integrations-cap}} quick reference](integration-docs://reference/agentless_integrations.md)
