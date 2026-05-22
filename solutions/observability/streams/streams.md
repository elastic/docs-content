---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Streams

Streams is a centralized {{kib}} feature that turns raw, unstructured log data into actionable
insights — automatically. It uses AI to parse logs, detect significant events, organize data into
streams, and manage retention, so you spend less time configuring pipelines and more time
understanding what's happening in your systems.

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/kibana/streams
:::

## Why use Streams [streams-why]

Log data holds the answers to most production incidents, but raw logs are noisy, expensive, and
hard to query. Streams addresses each of these challenges:

**Organize logs automatically**
Streams uses AI to partition your log data by source and component — without manual regex rules or
pipeline configuration. As new log formats arrive, Streams continues to learn and extend its
partitioning automatically.

**Get meaning from logs**
The AI-powered processing pipeline detects log formats (including custom ones like Apache Spark)
and generates parsing rules that extract structured fields from unstructured text. You get clean,
queryable data without writing a single GROK expression.

**Find problems in logs — in minutes, not hours**
Significant Events detection continuously scans your streams for critical signals: out-of-memory
errors, crash loops, certificate expirations, and anomalies. Instead of manually scanning
thousands of log lines, you get a prioritized list of what matters.

## Prerequisites [streams-prerequisites]

Before using Streams, make sure you have the following in place:

- **{{es}} and {{kib}}**: Streams is available from {{es}} 9.1 (API, preview), 9.2 (Wired streams,
  preview), and 9.2+ (GA for classic streams). For {{serverless-full}}, Streams is generally
  available.
- **Log data ingestion**: Logs can be sent to Streams via OpenTelemetry Collector, Fluentd,
  Fluentbit, or through Elastic one-click integrations. No agent deployment is required for
  agentless ingest via the `/logs` endpoint (Logs Streams, tech preview).
- **Required permissions**: See [Required permissions](#streams-required-permissions) for the full
  list of cluster and data stream permissions needed to manage or view streams.

## Use cases [streams-use-cases]

**Incident investigation**
An SRE receives an alert that a trading application is down. Instead of manually searching through
millions of log lines, they open Streams, where Significant Events has already surfaced a Java
out-of-memory error with the relevant context. In minutes — not hours — they identify the root
cause, escalate to the right team, and restore service.

**High-volume log management for platform teams**
A platform team ingests logs from dozens of microservices and needs to control costs without losing
context. Using Streams, they set per-stream retention policies, route high-value logs to longer
retention tiers, and use the failure store to catch and investigate parsing errors — all from a
single UI.

## Get started with Streams [streams-get-started]

### End-to-end user journey [streams-journey]

A typical Streams workflow looks like this:

1. **Ingest log data** — send logs via OpenTelemetry, Fluentd, Fluentbit, or an Elastic
   integration. For agentless ingest, send directly to the `/logs` endpoint.
2. **Access Streams in {{kib}}** — select **Streams** from the navigation menu, or open it from
   the **Discover** document details flyout.
3. **Review AI-suggested partitions** — Streams automatically organizes your logs by source and
   component. Accept, adjust, or add partitions manually.
4. **Configure processing** — use the [**Processing** tab](./management/extract.md) to parse and
   extract fields from log messages. Accept AI-generated GROK rules or write your own.
5. **Set retention policies** — use the [**Retention** tab](./management/retention.md) to define
   how long each stream stores data and to review ingestion volume.
6. **Investigate with Significant Events** — review the
   [**Significant Events** view](./management/significant-events.md) to triage critical signals
   across your streams.

### Novice path [streams-novice]

If you're new to log management or to Elastic, start with the **Streams UI** and let AI do the
heavy lifting:

- Use the **Streams** navigation entry in {{kib}} as your home base.
- Accept AI-suggested partitions and parsing rules to get structured data quickly.
- Use the **Significant Events** view to understand what's happening before diving into raw logs.
- Explore individual streams using **Discover** to build familiarity with ES|QL queries.

### Expert path [streams-expert]

If you already manage {{es}} data pipelines and want full control:

- Use [Wired streams](./wired-streams.md) to build a parent-child stream hierarchy with inherited
  mappings, lifecycle settings, and processors.
- Automate stream configuration with the [Streams API]({{kib-apis}}group/endpoint-streams) to
  integrate Streams into your infrastructure-as-code workflows.
- Define advanced ILM policies and failure store management for fine-grained cost and quality
  control.
- Use the [**Advanced** tab](./management/advanced.md) to inspect and manage underlying
  {{es}} components when needed.

### Alternatives [streams-alternatives]

Streams is not the only way to manage log data in Elastic. Consider these alternatives depending
on your needs:

- **Elastic Agent integrations**: Pre-built integrations with automatic parsing and dashboards for
  common data sources. Best when your sources are covered by the
  [Elastic integration catalog](https://www.elastic.co/integrations).
- **Logstash pipelines**: Highly customizable, code-first pipeline configuration. Best for complex
  transformations or when you need to fan out to multiple destinations.
- **{{es}} ingest pipelines**: Low-level pipeline configuration via the ES API. Best for teams who
  already manage {{es}} directly and want fine-grained control without a UI.

## Classic versus wired streams [streams-classic-vs-wired]

Streams can operate in two modes: wired and classic. Both manage data streams in {{es}}, but differ
in configuration, inheritance, and field mapping.

### Classic streams [streams-classic-streams]

Classic streams work with existing {{es}} data streams. Use classic streams when you want the ease
of extracting fields and configuring data retention while working with data that's already being
ingested into {{es}}.

Classic streams:

- Are based on existing data streams, index templates, and component templates.
- Can follow the data retention policy set in the existing index template.
- Do not support hierarchical inheritance or cascading configuration updates.

### Wired streams [streams-wired-streams]
```{applies_to}
stack: preview 9.2
serverless: preview
```

Wired streams send data directly to an endpoint, from which you can route data into child streams
based on [partitioning](./management/partitioning.md) set up manually or with the help of AI
suggestions.

Wired streams:
- Allow you to organize streams in a parent-child hierarchy.
- Let child streams automatically inherit mappings, lifecycle settings, and processors.
- Send configuration changes through the hierarchy to keep streams consistent.

For more information, refer to [Wired streams](./wired-streams.md).

## Managed components [streams-managed-components]

When you configure classic or wired streams through the Streams UI or [Streams API](#streams-api),
{{es}}-level components like templates and pipelines are created for the stream. These components
are considered *managed* and shouldn't be modified using {{es}} APIs. When managing a stream
through the Streams UI or API, continue doing so whenever possible.

You can still edit non-managed ingest pipelines, templates, and other components, but avoid those
marked as managed or any per-data-stream mappings and settings. This behavior is similar to how
{{es}} handles components managed by integrations. Refer to the
[**Advanced** tab](./management/advanced.md) to review managed components.

## Required permissions [streams-required-permissions]

Streams requires the following permissions:

::::{applies-switch}

:::{applies-item} serverless:
Streams requires these {{serverless-full}} roles:

- Admin: Ability to manage all Streams
- Editor/Viewer: Limited access, cannot perform all actions

:::

:::{applies-item} stack:
To manage all streams, you need the following permissions:

- **Cluster permissions**: `manage_index_templates`, `manage_ingest_pipelines`, `manage_pipeline`, `read_pipeline`
- **Data stream level permissions**: `read`, `write`, `create`, `manage`, `monitor`, `manage_data_stream_lifecycle`, `read_failure_store`, `manage_failure_store`, `manage_ilm`.

To view streams, you need the following permissions:
- **Data stream level**: `read`, `view_index_metadata`, `monitor`

For more information, refer to [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) and [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md)

:::

::::

## Manage Streams visibility [streams-space-privileges]
```{applies_to}
stack: ga 9.3+
serverless: ga
```

You can set Streams visibility on a space-by-space basis by defining users' access to specific
spaces. Refer to [Define access to a space](../../../deploy-manage/manage-spaces.md#spaces-control-user-access)
for more information.

Space settings only affect visibility. Set permissions to manage and edit Streams at the {{es}}
level. Refer to [Required permissions](#streams-required-permissions) for more information.

% :::{note}
% Creating [significant events](./management/significant-events.md) requires access to the `default` space.
% :::

## Access Streams [streams-access]

Open Streams from the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.

### Streams API [streams-api]
``` yaml {applies_to}
stack: preview 9.1
serverless: preview
```

You can also access Streams features using the Streams API. Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.

## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [**Retention**](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [**Partitioning**](./management/partitioning.md): {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Route data into child streams.
- [**Processing**](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [**Schema**](./management/schema.md): Manage field mappings.
- [**Data quality**](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [**Advanced**](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.
- [**Knowledge Indicators**](./management/knowledge-indicators.md): Automatically extract structured facts about your environment from raw log data.
