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

Streams is a centralized {{kib}} feature that uses AI to turn raw, unstructured log data into actionable
insights.

::::{dropdown} What is Streams: Basic concepts
A Stream is defined by three intrinsic properties: where data comes from (sources), what happens to it in transit (pipeline), and where it ends up (destinations). These aren't separate systems — they're built into the stream itself.

### Sources

Sources define how data enters a stream. Elastic supports two models:

Push (OpenTelemetry, Syslog, _bulk, Splunk): external systems send data to Elastic endpoints. Built for high-volume, continuous telemetry with strong buffering and queuing guarantees.
Pull (S3, Kafka, SaaS APIs): Elastic fetches data on a schedule. Ideal for audit logs, SaaS integrations, and historical ingestion.
The underlying mechanism — Fleet agent, Agentless, Cloud forwarder — is invisible to the user. Adding a source means data starts flowing immediately. Multiple sources can feed the same stream simultaneously, letting diverse telemetry types converge naturally.

### Pipelines

A pipeline is not an external system — it's a property of the stream, expressed through Streamlang (with OTTL available for advanced cases). Pipelines handle filtering, enrichment, field extraction, and conditional routing. They're stateless by default, with stateful processing reserved for specialized cases like tail-based sampling.

### Destinations

A destination is itself a stream, making the model inherently composable. Routing is many-to-many: one stream can fan out to multiple destinations, and one destination can receive from multiple upstream streams. Destinations are queryable via ESQL views. Unlike today's implicit default storage, the unified model makes every routing decision explicit and visible.
::::

::::{dropdown} Why use Streams
Log data holds the answers to most production incidents, but raw logs are noisy, expensive, and
hard to query. Streams addresses each of these challenges:

**Organize logs automatically.**
Streams uses AI to partition your log data by source and component, without manual regex rules or
pipeline configuration. As new log formats arrive, Streams continues to learn and extend its
partitioning automatically.

**Get meaning from logs.**
The AI-powered processing pipeline detects log formats (including custom ones like Apache Spark)
and generates parsing rules that extract structured fields from unstructured text. You get clean,
queryable data without writing a single GROK expression.

**Find problems in logs. In minutes, not hours.**
Significant Events detection continuously scans your streams for critical signals: out-of-memory
errors, crash loops, certificate expirations, and anomalies. Instead of manually scanning
thousands of log lines, you get a prioritized list of what matters.

### Use cases [streams-use-cases]

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

::::

::::::{dropdown} Who Streams is for


:::::{tab-set}
::::{tab-item} Novice user
If you're new to log management or to Elastic, start with the **Streams UI** and let AI do the
heavy lifting:

- Use the **Streams** navigation entry in {{kib}} as your home base.
- Accept AI-suggested partitions and parsing rules to get structured data quickly.
- Use the **Significant Events** view to understand what's happening before diving into raw logs.
- Explore individual streams using **Discover** to build familiarity with ES|QL queries.
::::

::::{tab-item} Expert user
If you already manage {{es}} data pipelines and want full control:

- Use [Wired streams](./wired-streams.md) to build a parent-child stream hierarchy with inherited
  mappings, lifecycle settings, and processors.
- Automate stream configuration with the [Streams API]({{kib-apis}}group/endpoint-streams) to
  integrate Streams into your infrastructure-as-code workflows.
- Define advanced ILM policies and failure store management for fine-grained cost and quality
  control.
- Use the [**Advanced** tab](./management/advanced.md) to inspect and manage underlying
  {{es}} components when needed.
::::
:::::

::::::

::::::{dropdown} Get started with Streams

### Prerequisites

Before using Streams, make sure you have the following in place:

- **{{es}} and {{kib}}**: Streams is available from {{es}} 9.1 (API, preview), 9.2 (Wired streams,
  preview), and 9.2+ (GA for classic streams). For {{serverless-full}}, Streams is generally
  available.
- **Log data ingestion**: Logs can be sent to Streams via OpenTelemetry Collector, Fluentd,
  Fluentbit, or through Elastic one-click integrations. No agent deployment is required for
  agentless ingest via the `/logs` endpoint (Logs Streams, tech preview).

### Required permissions

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

### Get started with Streams

:::::{stepper}

::::{step} Ingest log data
Send logs via OpenTelemetry, Fluentd, Fluentbit, or an Elastic integration. For agentless ingest, send directly to the `/logs` endpoint.
::::

::::{step} Access Streams

**From {{kib}}**

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.

**Using the API**

{applies_to}`stack: preview 9.1` {applies_to}`serverless: preview` You can also access Streams features using the Streams API. Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.
::::

::::{step} Review AI-suggested partitions
Streams automatically organizes your logs by source and component. Accept, adjust, or add partitions manually.
::::

::::{step} Configure processing
Use the [**Processing** tab](./management/extract.md) to parse and extract fields from log messages. Accept AI-generated GROK rules or write your own.
::::

::::{step} Set retention policies
Use the [**Retention** tab](./management/retention.md) to define how long each stream stores data and to review ingestion volume.
::::

::::{step} Investigate with Significant Events
Review the [**Significant Events** view](./management/significant-events.md) to triage critical signals across your streams.
::::

:::::

::::::

### Alternatives paths to manage log data in Elastic [streams-alternatives]

Streams is not the only way, consider these alternatives depending on your needs:

- **Elastic Agent integrations**: Pre-built integrations with automatic parsing and dashboards for
  common data sources. Best when your sources are covered by the
  [Elastic integration catalog](https://www.elastic.co/integrations).
- **Logstash pipelines**: Highly customizable, code-first pipeline configuration. Best for complex
  transformations or when you need to fan out to multiple destinations.
- **{{es}} ingest pipelines**: Low-level pipeline configuration via the ES API. Best for teams who
  already manage {{es}} directly and want fine-grained control without a UI.

## Managed components [streams-managed-components]

When you configure classic or wired streams through the Streams UI or [Streams API](#streams-api),
{{es}}-level components like templates and pipelines are created for the stream. These components
are considered *managed* and shouldn't be modified using {{es}} APIs. When managing a stream
through the Streams UI or API, continue doing so whenever possible.

You can still edit non-managed ingest pipelines, templates, and other components, but avoid those
marked as managed or any per-data-stream mappings and settings. This behavior is similar to how
{{es}} handles components managed by integrations. Refer to the
[**Advanced** tab](./management/advanced.md) to review managed components.



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



## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [**Retention**](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [**Partitioning**](./management/partitioning.md): {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Route data into child streams.
- [**Processing**](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [**Schema**](./management/schema.md): Manage field mappings.
- [**Data quality**](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [**Advanced**](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.
- [**Knowledge Indicators**](./management/knowledge-indicators.md): Automatically extract structured facts about your environment from raw log data.
