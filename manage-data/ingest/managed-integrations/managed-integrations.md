---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
description: Elastic Managed integrations let you ingest data from cloud sources into Elastic Cloud with no collectors to deploy or maintain.
applies_to:
  stack: ga 9.5+, preview 9.0-9.4
  serverless: ga
products:
  - id: elastic-agent
  - id: fleet
  - id: cloud-serverless
  - id: cloud-hosted
  - id: elasticsearch
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

## Key benefits [managed-integrations-benefits]

{{managed-integrations}} remove the operational overhead of running your own collectors:

* **No infrastructure to manage**: Elastic deploys, patches, upgrades, and scales the collectors for you.
* **Quick to set up**: Enable an integration in {{kib}} and data starts flowing within minutes, with nothing to install.
* **Isolation by design**: Each integration runs in its own dedicated collector, which keeps your data separate from other workloads while it's being collected.
* **Data stays in your cluster**: Collectors write directly to your project or deployment, so you keep full ownership and access control.

## Use cases [managed-integrations-use-cases]

{{managed-integrations}} are a good fit whenever you need to pull data from a cloud service through an API at lower volumes, without setting up and running your own collectors. Some examples include:

* **Identity and access logs**: Collect audit and system logs from identity and access management providers to monitor authentication and access activity.
* **Security and vulnerability findings**: Ingest findings from security and vulnerability management tools to track risks alongside the rest of your data.
* **SaaS and cloud provider audit trails**: Centralize audit logs from cloud platforms and SaaS applications for security and compliance monitoring.

For the full list of integrations that can run as {{managed-integrations}}, refer to the [Managed integrations quick reference](integration-docs://reference/managed_integrations.md). Elastic continually adds more.

{{managed-integrations}} aren't intended for high-throughput ingestion or for sources that push large volumes of events. For more information, refer to [Limits and scaling](#managed-integrations-limits).

## How {{managed-integrations}} work [managed-integrations-architecture]

When you enable an {{managed-integration}}, Elastic provisions a dedicated collector for it on Elastic-managed infrastructure. Each collector runs the integration package you'd deploy yourself for the equivalent agent-based integration, but Elastic provisions, updates, and operates it for you.

The collector pulls data from the source API and writes documents to your {{es}} cluster through the standard `_bulk` API. For most integrations, data flows through the integration's ingest pipelines and lands in the same data streams as it would for a self-managed integration. {{managed-integrations}} built on OpenTelemetry are an exception: their data bypasses ingest pipelines and lands in the integration's dedicated data streams (typically in `.otel-*` data streams).

A shared, stateless Controller orchestrates the lifecycle of these collectors. When you enable an integration in {{kib}}, the Controller creates and updates the collector, and it removes the collector when you delete the integration. The Controller doesn't store user data.

:::{image} /manage-data/images/managed-integrations-architecture.png
:alt: Architecture diagram for {{managed-integrations}}. A request in {{kib}} triggers the Controller to create per-integration collectors on Elastic-managed infrastructure. Each collector pulls data from a cloud source through a cloud proxy, writes documents to {{es}} over the `_bulk` API, and receives its configuration from {{es}}.
:::

## Limits and scaling [managed-integrations-limits]

The following limits apply to {{managed-integrations}}:

* **Maximum {{managed-integrations}} per {{serverless-short}} project or {{ech}} deployment**: 50.
* **No horizontal scaling**: Deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).
* **Rate limiting**: Integrations are rate-limited on {{serverless-short}} and {{ech}} to preserve quality of service. Rate limiting uses back-pressure rather than dropping events, so collection slows down until it has caught up.

## Security and data residency [managed-integrations-data-security]

The collector for each {{managed-integration}} writes documents directly to your cluster. Data is stored in your project or deployment, and Elastic employees don't have access to it.

Data typically travels from Elastic-managed infrastructure to your cluster over Elastic's internal network. On an {{ech}} deployment in a region that isn't served by {{serverless-full}}, data might traverse the public internet to reach your cluster. For more information, refer to [Does my data travel over the public internet?](/manage-data/ingest/managed-integrations/managed-integrations-faq.md#managed-integrations-faq-public-internet) in the FAQ.

Each collector is dedicated to a single {{managed-integration}}: no other workloads can be added to it.

## Manage and monitor {{managed-integrations}} [managed-integrations-management]

Because Elastic operates the collectors on your behalf, they aren't visible in {{fleet}} by default, and Elastic resolves service-level issues for you. You still keep visibility into the parts that matter to you — each integration's status is available in the **{{integrations}}** app, and the ingested data lands in your cluster so you can query it, view it in dashboards, and set [alerting rules](/explore-analyze/alerting.md) on it as you would for any other integration.

For how {{managed-integrations}} behave during a service issue, refer to [What happens to my data if there's a service issue?](/manage-data/ingest/managed-integrations/managed-integrations-faq.md#managed-integrations-faq-service-issue) in the FAQ.

For service issues or to request diagnostics, contact [Elastic Support](https://support.elastic.co).

## Next steps [managed-integrations-next-steps]

* [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md) in {{kib}} to start collecting data from a cloud source.
* [Authenticate {{managed-integrations}} using cloud connectors](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md) to avoid managing API keys directly.

## Related pages [managed-integrations-related]

* [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md)
* [Managed integrations quick reference](integration-docs://reference/managed_integrations.md)
