---
navigation_title: Collect NGINX logs and metrics with hybrid standalone agent
description: Collect NGINX logs and metrics with a hybrid standalone Elastic Agent using Elastic's Nginx integration and NGINX OpenTelemetry Input Package.
applies_to:
  stack: preview 9.2+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Collect NGINX logs and metrics with a hybrid standalone {{agent}}

Learn how to monitor your NGINX server by collecting logs and metrics with a hybrid standalone {{agent}} on Linux.

You'll use {{kib}} and {{fleet}} to create a [hybrid agent policy](/reference/fleet/otel-integrations.md#otel-integrations-hybrid-policies), then download the policy file and deploy it to your standalone {{agent}}.

You’ll collect:

- NGINX logs with Elastic's [Nginx integration](https://www.elastic.co/docs/reference/integrations/nginx), based on the [Elastic Common Schema](ecs://reference/index.md) (ECS)
- NGINX metrics with Elastic's [NGINX OpenTelemetry Input Package](https://www.elastic.co/docs/reference/integrations/nginx_otel_input), which uses the [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OpenTelemetry (OTel) Collector receiver

:::{note}
OpenTelemetry input packages cannot be used with an [{{agent}} running as an EDOT Collector](/reference/fleet/otel-agent.md) (an agent in `otel` mode).
:::

## Prerequisites [collect-nginx-data-standalone-prereqs]

::::{include} _snippets/collect-nginx-data-prerequisites.md
::::

## Configure the NGINX status endpoint [collect-nginx-data-standalone-status-endpoint]

::::{include} _snippets/collect-nginx-data-status-endpoint.md
::::

## Configure the hybrid standalone agent policy [collect-nginx-data-standalone-policy]

To deploy a hybrid agent policy to a standalone {{agent}}, start by creating the policy in {{kib}}. This approach allows you to configure all integration settings in advance, create an API key for the agent, and then generate a working agent policy, already populated with the output and integration details.

:::::{stepper}

::::{step} Create an agent policy in {{kib}}

1. In {{kib}}, find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Go to **Agent policies**, then create a new agent policy (for example, `nginx-telemetry-standalone`).

   For detailed steps, refer to [Create a standalone {{agent}} policy](/reference/fleet/create-standalone-agent-policy.md).

   :::{note}
   You don't need to enroll any agents to this policy. You'll download the policy file and deploy it manually to your standalone {{agent}}.
   :::

::::

::::{step} Configure log collection with the Nginx integration

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for "nginx", then select the **Nginx** integration.
3. Select **Add Nginx**, then configure the integration. Log collection from NGINX instances is enabled by default.

   1. Confirm the **Paths** fields for access and error logs match your NGINX configuration.
   2. Turn off **Collect metrics from Nginx instances**. In this tutorial, you'll use the OpenTelemetry input package for metrics collection.

4. In the **Where to add this integration?** section, select **Existing hosts**.
5. Select the agent policy you created for your standalone agent (for example, `nginx-telemetry-standalone`).
6. Select **Save and continue**.

For more details, refer to [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md).

::::

::::{step} Configure metrics collection with the NGINX OpenTelemetry input package

1. In {{kib}}, go to **Integrations**.
2. Select **Display beta integrations** (the NGINX OpenTelemetry packages are in technical preview).
3. Search for "nginx", then select **NGINX OpenTelemetry Input Package**.
4. Select **Add NGINX OpenTelemetry Input Package**, then configure the integration. **NGINX OpenTelemetry Input** is enabled by default.

   1. Select **Change defaults**, then expand **Advanced options**.
   2. Set the data stream type to **Metrics**.
   3. Set **endpoint** to your NGINX `stub_status` URL (for example, `http://localhost:80/status`).

5. In the **Where to add this integration?** section, select **Existing hosts**.
6. Select the agent policy you created for your standalone agent (for example, `nginx-telemetry-standalone`).
7. Select **Save and continue**.

:::{note}
The NGINX OpenTelemetry Assets content package is installed automatically when data is ingested through the NGINX OpenTelemetry Input Package. You can find it in the **Installed integrations** list and use it to visualize OTel-based metrics.
:::

::::

::::{step} Download the standalone policy

1. In {{kib}}, go to **Fleet** → **Agents**, then click **Add agent**. 
2. Select the agent policy you created (for example, `nginx-telemetry-standalone`).
3. Select **Run standalone**.
4. Select **Create API key** to generate an API key and use it directly in the policy configuration.
5. Select **Download policy** to download the policy file (`elastic-agent.yml`).
6. Replace the `elastic-agent.yml` on the host where the {{agent}} is installed with the generated policy file. 

The downloaded policy includes the default {{es}} host address and port. You can modify the policy to update the {{es}} connection details and the API key, or to adjust any integration-specific settings for your environment.

For more details on customizing standalone policies, refer to [Create a standalone {{agent}} policy](/reference/fleet/create-standalone-agent-policy.md).

::::

::::{step} Deploy the policy to your standalone {{agent}}

1. Copy the downloaded `elastic-agent.yml` policy file to the {{agent}} installation directory on your Linux host (typically `/opt/Elastic/Agent/`).
2. Start the {{agent}} using the standalone policy:

   ```bash
   sudo systemctl start elastic-agent
   ```

::::

:::::

## Validate your data [collect-nginx-data-standalone-validate]

After you deploy the hybrid agent policy to your standalone {{agent}}, validate that both the ECS-based logs and the OTel-based metrics are flowing in.

:::::{stepper}

::::{step} Validate the log collection

1. In {{kib}}, go to **Discover**, then filter the results using the KQL search bar.
2. Search for NGINX data stream datasets such as `nginx.access` and `nginx.error`, or enter:

   ```text
   data_stream.dataset : "nginx.access" or "nginx.error"
   ```

3. Go to **Dashboards**, then select **[Logs Nginx] Access and error logs** to view the dashboard installed with the Nginx integration.

::::

::::{step} Validate the metrics collection

Go to **Dashboards**, then select **[Metrics Nginx OTEL] Overview** to view the dashboard for visualizing OTel-based metrics.

This dashboard is provided by the NGINX OpenTelemetry Assets content package, installed automatically when data is ingested through the NGINX OpenTelemetry Input Package.

::::

:::::

## Related pages [collect-nginx-data-standalone-related]

- [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md)
- [Collect NGINX logs and metrics with a hybrid {{fleet}}-managed {{agent}}](/solutions/observability/infra-and-hosts/collect-nginx-data-otel-integration-fleet-managed.md)
- [Elastic integrations](integration-docs://reference/index.md)
