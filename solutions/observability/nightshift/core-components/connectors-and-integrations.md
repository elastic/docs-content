---
applies_to:
  serverless:
    observability: preview
description: Learn which connectors Elastic nightshift investigations can use, such as External Elasticsearch, GitHub, and Slack, and why Tech Preview supports only some.
products:
  - id: observability
  - id: cloud-serverless
---

# Connectors and integrations [nightshift-connectors]

Investigations reach your data and tools through connectors. A connector gives the investigation agent access to an external system, such as another {{es}} cluster, the code in a GitHub repository, or a Slack channel.

## Supported connectors [nightshift-connectors-supported]

Tech Preview supports only connectors that work with the sandbox that runs investigations.

- **[External Elasticsearch](kibana://reference/connectors-kibana/elasticsearch-action-type.md)**: Lets the investigation agent query your data.
- **[GitHub](kibana://reference/connectors-kibana/github-action-type.md)**: Gives the agent access to the code, runbooks, and other files behind your systems.
- **[Slack](kibana://reference/connectors-kibana/slack-v2-action-type.md)**: Lets you chat with Elastic nightshift in a channel and receive results there.
- **HTTP**: Lets the agent call any endpoint that returns data, such as an API for your runbooks or build status.

To add a connector, refer to [Connect your data and tools](../get-started/connect-your-data-and-tools.md).

## How investigations use connectors [nightshift-connectors-use]

Each connector instance is described to the investigation agent, so it knows what the instance is for. A connector is usable from the sandbox when it's sandbox capable and the person who runs the investigation can execute it. How an investigation queries {{es}} depends on the connectors in the space. Refer to [What enabling sets up](../get-started.md#nightshift-get-started-enable-sets-up).

## Learn more [nightshift-connectors-nav]

- [How Elastic nightshift works](./index.md#nightshift-how-it-works): See where connectors fit in
- [Requirements](../get-started.md#nightshift-get-started-requirements): Check what Elastic nightshift depends on
