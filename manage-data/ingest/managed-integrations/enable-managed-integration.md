---
description: Enable an Elastic Managed integration in Kibana to ingest data from a cloud source. Elastic provisions and manages the collector for you.
applies_to:
  stack: ga 9.5+, preview 9.0-9.4
  serverless: preview
products:
  - id: elastic-agent
  - id: fleet
  - id: cloud-serverless
  - id: cloud-hosted
  - id: elasticsearch
  - id: observability
  - id: security
type: how-to
---

# Enable an {{managed-integration}} [enable-managed-integration]

Enable an {{managed-integration}} in {{kib}} to start collecting data from a cloud source. Elastic provisions and operates the collector for you on Elastic-managed infrastructure, so there's nothing to install or maintain. For details on the architecture, refer to [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md).

## Before you begin [enable-managed-integration-before-you-begin]

To enable an {{managed-integration}}, you need:

* One of these deployment types:
  * An {{serverless-full}} project
  * An {{ech}} deployment on version 9.5 or later, or on version 9.0 to 9.4 to use the technical preview
* The `Fleet: All` and `Integrations: All` [{{kib}} privileges](/reference/fleet/fleet-roles-privileges.md) to create or edit an {{managed-integration}}. These are the same privileges required for any {{fleet}} integration.
* On {{ech}}, a working default [{{fleet-server}}](/reference/fleet/fleet-server.md)

## Find {{managed-integrations}} [enable-managed-integration-find]

```{applies_to}
stack: ga 9.5+, preview 9.2-9.4
```

To find which {{product.integrations}} can run as {{managed-integrations}} in {{kib}}:

::::{applies-switch}

:::{applies-item} {serverless: preview, stack: ga 9.5+}
1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the **Setup method** filter and select **Managed Integration**.
:::

:::{applies-item} stack: preview =9.4
1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the **Setup method** filter and select **Agentless**.
:::

:::{applies-item} stack: preview 9.2-9.3
1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Enable the **Only agentless integrations** toggle.
:::

::::

For a complete list of integrations that can run as {{managed-integrations}}, refer to [Managed integrations quick reference](integration-docs://reference/managed_integrations.md).

## Enable the integration [enable-managed-integration-steps]

1. In {{kib}}, go to **{{integrations}}** and select an integration that can be deployed as an {{managed-integration}}.
2. Select **Add `<integration>`**.
3. Provide the credentials and any other required configuration for the source.
4. Choose the deployment mode:
   - {applies_to}`{serverless: preview, stack: ga 9.5+}` In the **Deployment** section, select **Elastic Managed Integration**.
   - {applies_to}`{stack: preview 9.0-9.4}` In the **Deployment options** section, select **Agentless**.
5. Select **Save and continue**.

Within a few minutes, data from the source appears in the integration's data streams in your cluster.

:::{tip}
For integrations that authenticate to a cloud provider, you can use [cloud connector authentication](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md) to avoid managing API keys directly.
:::

## Next steps [enable-managed-integration-next-steps]

* Learn more about [how {{managed-integrations}} work](/manage-data/ingest/managed-integrations/managed-integrations.md#managed-integrations-architecture).
* Review common questions in the [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md).
