---
navigation_title: Choose an ingest method
description: >
  Decide how to get data into Elastic. Compare Elastic Agent, agentless integrations,
  OpenTelemetry (EDOT), Logstash, APIs, and other ingest methods based on your data
  type, deployment, and use case.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-stack
  - id: fleet
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-serverless
---

# Choose an ingest method [choose-an-ingest-method]

::::{admonition} Draft
:class: note

This page is a draft for stakeholder review as part of the [unified ingest docs strategy](https://github.com/elastic/docs-content-internal/issues/1191). Content and structure will change before publication.

::::

Use the **simplest option that meets your needs** and satisfies your use case.

For a broader overview of ingest options, refer to [Ingest: Bring your data to Elastic](/manage-data/ingest.md). For a list of all tools, refer to [Ingest tools overview](/manage-data/ingest/tools.md).

## Before you choose [choose-ingest-prerequisites]

Most ingest paths require:

* A deployment — [{{ecloud}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), or self-managed
* For Fleet-managed {{agent}} and most integrations: {{kib}} with [{{fleet}}](/reference/fleet/index.md)
* Network connectivity from your data source to {{es}} (or a supported proxy or forwarder)

## Step 1: What kind of data are you ingesting? [choose-ingest-data-type]

| Data type | Examples | Start here |
| --- | --- | --- |
| **Time-series (timestamped)** | Logs, metrics, traces, security events | Continue to [Step 2](#choose-ingest-goal) |
| **General content (no timestamp)** | Knowledge bases, catalogs, web pages | [Ingest for search use cases](/solutions/search/ingest-for-search.md) |
| **Application data you control** | Custom JSON from your application | [APIs and language clients](#choose-ingest-apis) or [EDOT](#choose-ingest-edot) |
| **Quick test or evaluation** | Sample or file upload | [Sample data](/manage-data/ingest/sample-data.md) or [Upload data files](/manage-data/ingest/upload-data-files.md) |

## Step 2: What is your goal? [choose-ingest-goal]

| Goal | Recommended starting point |
| --- | --- |
| Monitor hosts, applications, or cloud (Observability) | {{agent}} + integration, or EDOT for OTel-native applications |
| Detect threats, run SIEM, or protect endpoints (Security) | {{agent}} + Security integration; [agentless](/manage-data/ingest/agentless/agentless-integrations.md) for supported cloud posture use cases |
| Search enterprise content | [Connectors](elasticsearch://reference/search-connectors/index.md) or [web crawler](https://www.elastic.co/web-crawler) |
| Custom analytics on your own data | {{agent}} + integration, APIs, or {{ls}} depending on the source |

For solution-specific quickstarts, refer to [Ingesting data for Elastic solutions](/manage-data/ingest/ingesting-data-for-elastic-solutions.md).

## Step 3: Choose a collection method [choose-ingest-collection]

::::{admonition} Default recommendation
:class: tip

For most timestamped data, use a **Fleet-managed {{agent}}** with an [Elastic integration](https://docs.elastic.co/en/integrations). Integrations include parsing rules, dashboards, and visualizations to help you get value quickly.

::::

Answer these questions in order:

1. Is there an [Elastic integration](https://docs.elastic.co/en/integrations/all_integrations) for your data source?
2. If yes, can you use an [agentless](/manage-data/ingest/agentless/agentless-integrations.md) deployment (cloud or API-only source)?
3. If no integration fits, is the source OpenTelemetry-instrumented or Kubernetes-native?
4. If none of the above, do you need {{ls}}, APIs, or a custom integration?

### Compare collection methods [choose-ingest-comparison]

| Method | Use when | Don't use when | Management |
| --- | --- | --- | --- |
| [Agentless integration](#choose-ingest-agentless) | A supported integration offers agentless deployment; you collect from cloud APIs without a host agent | You need host-level collection; the integration is not agentless-capable; you run self-managed only | {{fleet}} UI in {{kib}} |
| [Fleet-managed {{agent}} + integration](#choose-ingest-agent) | Default for logs, metrics, and security on hosts, VMs, or Kubernetes; an integration exists | You need unsupported {{beats}} outputs (Redis, file, console); the integration is not GA for {{agent}} | {{fleet}} |
| [Standalone {{agent}}](#choose-ingest-standalone-agent) | Advanced deployments without {{fleet}}; policies managed as YAML | Most new deployments; you want UI-driven setup | Local YAML |
| [EDOT (OpenTelemetry)](#choose-ingest-edot) | Application traces and metrics via OTel SDKs; Kubernetes observability; vendor-neutral instrumentation | You want a prebuilt integration with dashboards out of the box | Collector config or Kubernetes operator |
| [{{ls}}](#choose-ingest-logstash) | No {{agent}} integration; heavy transform or enrich; buffering (PQ); proxy bridge; multi-destination routing | Simple host log collection when an integration is available | {{ls}} pipelines |
| [{{beats}}](#choose-ingest-beats) | Legacy deployment; {{agent}} integration not GA; specific {{beats}}-only output needed | New deployments (prefer {{agent}}) | Beat config files |
| [APIs and language clients](#choose-ingest-apis) | You own the application and emit events directly | You collect from third-party systems without an integration | Your code |
| [Elastic Serverless Forwarder for AWS](#choose-ingest-esf) | Ship logs from AWS without persistent infrastructure | Non-AWS sources or rich edge processing requirements | AWS deployment |

### Agentless integration [choose-ingest-agentless]

[Agentless integrations](/manage-data/ingest/agentless/agentless-integrations.md) collect data without deploying {{agent}} on your infrastructure. They work well for cloud and API-based sources when a supported integration offers an agentless option.

Refer to the [agentless integrations quick reference](integration-docs://reference/agentless_integrations.md) for the current list.

### Fleet-managed {{agent}} and integrations [choose-ingest-agent]

A single [{{agent}}](/reference/fleet/index.md) can collect logs, metrics, security data, and more. Pair it with an [Elastic integration](https://docs.elastic.co/en/integrations) for your data source.

* [Install {{agent}}](/reference/fleet/install-elastic-agents.md)
* [Manage {{agent}}s in {{fleet}}](/reference/fleet/manage-elastic-agents-in-fleet.md)
* [Ingesting time series data](/manage-data/ingest/ingesting-timeseries-data.md#ingest-ea)

### Standalone {{agent}} [choose-ingest-standalone-agent]

Use [standalone {{agent}}](/reference/fleet/install-standalone-elastic-agent.md) when you manage policies locally as YAML and do not use {{fleet}}. This path suits advanced operators.

For Kubernetes without {{fleet}}, refer to [Run {{agent}} on Kubernetes in standalone mode](/reference/fleet/running-on-kubernetes-standalone.md).

### EDOT (OpenTelemetry) [choose-ingest-edot]

:::{include} /manage-data/_snippets/otel.md
:::

Refer to [Elastic Distributions of OpenTelemetry (EDOT)](opentelemetry://reference/index.md) and [Use OpenTelemetry with APM](/solutions/observability/apm/opentelemetry/index.md).

### {{ls}} [choose-ingest-logstash]

[{{ls}}](logstash://reference/index.md) collects, transforms, and routes data from many sources. Common use cases include extending integrations, enrichment, persistent queue buffering, and proxying.

Refer to [Ingesting time series data](/manage-data/ingest/ingesting-timeseries-data.md#ingest-logstash) and [Using Logstash with Elastic integrations](logstash://reference/using-logstash-with-elastic-integrations.md).

### {{beats}} [choose-ingest-beats]

:::{include} /manage-data/_snippets/beats.md
:::

Refer to [{{beats}} and {{agent}} capabilities](/reference/fleet/beats-agent-comparison.md) and [Migrate from {{beats}} to {{agent}}](/reference/fleet/migrate-from-beats-to-elastic-agent.md).

### APIs and language clients [choose-ingest-apis]

Send application data directly to {{es}} using the [document APIs]({{es-apis}}group/endpoint-document) or an [{{es}} language client](/reference/elasticsearch-clients/index.md).

### Elastic Serverless Forwarder for AWS [choose-ingest-esf]

The [Elastic Serverless Forwarder](elastic-serverless-forwarder://reference/index.md) ships logs from AWS to {{ecloud}}, self-managed {{es}}, or {{ls}}.

## Step 4: Do you need processing beyond collection? [choose-ingest-processing]

Collection and processing are separate decisions. Choose where to transform or enrich your data:

| Need | Where to process | Learn more |
| --- | --- | --- |
| Filter or redact at the source | {{agent}} processors | [{{agent}} processors](/reference/fleet/agent-processors.md) |
| Parse or enrich at ingest (most cases) | {{es}} ingest pipelines | [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) |
| Heavy transform, buffering, or routing | {{ls}} | [Transform and enrich data](/manage-data/ingest/transform-enrich.md) |

## Step 5: Choose an architecture [choose-ingest-architecture]

If a single collection method is not enough, refer to [Ingest architectures](/manage-data/ingest/ingest-reference-architectures.md). Common patterns include:

| Architecture | Use when |
| --- | --- |
| {{agent}} → {{es}} | An integration is available; no extra processing is required |
| {{agent}} → {{ls}} → {{es}} | You need enrichment, persistent queue buffering, proxying, or multi-destination routing |
| {{agent}} → proxy → {{es}} | {{agent}}s have network restrictions |
| {{agent}} → Kafka → {{es}} | Kafka is your middleware message queue |
| {{ls}} → {{es}} | {{agent}} cannot read the source (for example, some databases or AWS Kinesis) |
| Air-gapped {{stack}} | No access to outside networks {applies_to}`serverless: unavailable` |

## Deployment support [choose-ingest-deployment]

| Method | {{ecloud}} | {{serverless-short}} | Self-managed |
| --- | :---: | :---: | :---: |
| {{agent}} + {{fleet}} | ✓ | ✓ | ✓ |
| Agentless integrations | ✓ | ✓ | ✗ |
| EDOT | ✓ | ✓ | ✓ |
| {{ls}} | ✓ | ✓ | ✓ |
| {{beats}} | ✓ | ✓ | ✓ |

For {{serverless-short}} restrictions on {{fleet}} and {{agent}}, refer to [{{fleet}} and {{agent}} restrictions (Serverless)](/reference/fleet/fleet-agent-serverless-restrictions.md).

## What's next? [choose-ingest-whats-next]

After data is flowing:

1. Verify events in **Discover** or the integration's **Assets** tab.
2. Open prebuilt **dashboards** shipped with the integration.
3. Configure **alerts** and **rules** for Observability or Security use cases.
4. Explore **Streams** and **Content Packs** when they apply to your deployment.

## Still not sure? [choose-ingest-still-not-sure]

* [Ingest tools overview](/manage-data/ingest/tools.md) — full tool comparison table
* [Troubleshoot ingestion tools](/troubleshoot/ingest.md)
* [Integration catalog](https://docs.elastic.co/en/integrations)
* [Automatic Import](/explore-analyze/ai-features/automatic-import.md) — generate a custom integration when none exists
