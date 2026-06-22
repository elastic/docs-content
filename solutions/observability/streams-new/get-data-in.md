---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to get data into Streams.
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

# Get data in

**Goal**: Logs are flowing into Elastic via Streams. User can see them.

Two entry points based on user situation:

- **New ingestion (Wired Streams)**
User sends logs to a Streams endpoint. Data lands in a managed hierarchy with inheritance, partitioning, and cascading configuration.
Best for: new deployments, custom logs, mixed-format sources.

- **Existing data (Classic Streams)**
User already has data in Elastic. They open Streams and their existing data streams appear. No migration, no config changes.
Best for: adding processing to data already flowing. or otherwise managing data (see B1/B2).

**Why Streams**: One place to point logs at. No need to understand index templates, ingest pipelines, or component templates upfront.

**Verification**: User confirms data appears in Discover.


## Prerequisites

Before using Streams, make sure you have the following in place:

- **{{es}} and {{kib}}**: Streams is available from {{es}} 9.1 (API, preview), 9.2 (Wired streams,
  preview), and 9.2+ (GA for classic streams). For {{serverless-full}}, Streams is generally
  available.
- **Log data ingestion**: Logs can be sent to Streams via OpenTelemetry Collector, Fluentd,
  Fluentbit, or through Elastic one-click integrations. No agent deployment is required for
  agentless ingest via the `/logs` endpoint (Logs Streams, tech preview).
- **Required permissions**:
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