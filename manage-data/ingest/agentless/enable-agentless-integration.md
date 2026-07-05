---
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
description: Enable an Elastic Managed integration in Kibana to ingest data from a cloud source. Elastic provisions and manages the collector for you.
type: how-to
---

# Enable an {{managed-integration}} [enable-agentless-integration]

Enable an {{managed-integration}} (previously known as an agentless integration) in {{kib}} to start collecting data from a cloud source. Elastic provisions and operates the collector for you on Elastic-managed infrastructure, so there's nothing to install or maintain. For background and architecture, refer to [{{managed-integrations}}](/manage-data/ingest/agentless/agentless-integrations.md).

## Before you begin [enable-agentless-before-you-begin]

To enable an {{managed-integration}}, you need:

* An {{ech}} deployment, {{obs-serverless}}, or {{sec-serverless}}.
* The `Fleet: All` and `Integrations: All` [{{kib}} privileges](/reference/fleet/fleet-roles-privileges.md) to create or edit an {{managed-integration}}. These are the same privileges required for any {{fleet}} integration.
* On {{ech}}, a working default [{{fleet-server}}](/reference/fleet/fleet-server.md).

## Find {{managed-integrations}} [enable-agentless-find]

```{applies_to}
stack: preview 9.2
serverless: preview
```

To find which {{product.integrations}} can run as {{managed-integrations}} in {{kib}}:

::::{applies-switch}

:::{applies-item} { stack: preview 9.4, serverless: preview }
1. In {{kib}}, go to **{{integrations}}**.
2. Open the **Setup method** filter and select **Agentless**.
:::

:::{applies-item} stack: preview 9.2-9.3
1. In {{kib}}, go to **{{integrations}}**.
2. Enable the **Only agentless integrations** toggle.
:::

::::

For a complete list of integrations that can run as {{managed-integrations}}, refer to [{{managed-integrations}} quick reference](integration-docs://reference/agentless_integrations.md).

## Enable the integration [enable-agentless-steps]

1. In {{kib}}, go to **{{integrations}}** and select an integration that can run as an {{managed-integration}}.
2. Click **Add `<integration>`**.
3. Provide the credentials and any other required configuration for the source.
4. Under **Deployment options**, select **Agentless**. For some integrations, **Agentless** is the default deployment mode, and the picker isn't shown.
5. Click **Save and continue**.

Within a few minutes, data from the source appears in the integration's data streams in your cluster.

:::{tip}
For integrations that authenticate to a cloud provider, you can use [cloud connector authentication](/manage-data/ingest/agentless/cloud-connector-deployment.md) to avoid managing API keys directly.
:::

## Next steps [enable-agentless-next-steps]

* Learn more about [how {{managed-integrations}} work](/manage-data/ingest/agentless/agentless-integrations.md#agentless-architecture).
* Review common questions in the [{{managed-integrations}} FAQ](/manage-data/ingest/agentless/agentless-integrations-faq.md).
* If you run into issues, check [Troubleshoot {{managed-integrations}}](/troubleshoot/ingest/agentless-integrations.md).
