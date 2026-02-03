---
navigation_title: Collect NGINX logs and metrics with hybrid Fleet-managed agent
description: Collect NGINX logs and metrics with a hybrid Fleet-managed Elastic Agent using Elastic's Nginx integration and NGINX OpenTelemetry Input Package.
applies_to:
  stack: preview 9.2+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Collect NGINX logs and metrics with a hybrid {{fleet}}-managed {{agent}}

Follow this guide to learn how to configure a {{fleet}}-managed {{agent}} on a Linux host to collect:

- NGINX logs with Elastic's [Nginx integration](https://www.elastic.co/docs/reference/integrations/nginx), based on the [Elastic Common Schema](ecs://reference/index.md) (ECS)
- NGINX metrics with Elastic's [NGINX OpenTelemetry Input Package](https://www.elastic.co/docs/reference/integrations/nginx_otel_input), which uses the [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OpenTelemetry (OTel) Collector receiver

## Prerequisites

:::::{applies-switch}

::::{applies-item} serverless: preview
* An {{observability}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* {{agent}} 9.2 or later installed on a Linux host.
* NGINX installed on the same Linux host.
::::

::::{applies-item} stack: preview 9.2+
* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* {{agent}} 9.2 or later installed on a Linux host.
* NGINX installed on the same Linux host.
::::

:::::

## Configure the NGINX status endpoint

The [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OTel Collector receiver needs an endpoint that exposes NGINX status metrics.

1. Make sure the [`ngx_http_stub_status_module`](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html) module is enabled.
2. In your NGINX configuration file (for example, `/etc/nginx/nginx.conf`), add or modify the `location` block in the `server { ... }` block with the following:

    ```nginx
    location = /status {
      stub_status;
    }
    ```

3. Save the configuration and restart NGINX:

    ```bash
    sudo systemctl restart nginx
    ```

4. Verify that the endpoint is active:

    ```bash
    curl http://localhost:80/status <1>
    ```
    1. Use the port number specified in the `listen` directive in the NGINX configuration.

    If the endpoint returns data, you are ready to set up {{agent}}.

For more details, refer to [Configuring NGINX for Metric Collection](https://docs.nginx.com/nginx-amplify/nginx-amplify-agent/configuring-metric-collection/#metrics-from-stub_status).

## Configure the hybrid agent policy

:::::::{stepper}

::::::{step} Create an agent policy and enroll an agent

1. In {{kib}}, go to **Fleet** → **Agent policies**.
2. Create a new agent policy (for example, `nginx-telemetry`), or select an existing policy you want to use to collect NGINX telemetry.
3. Add an {{agent}} running version 9.2 or later to the policy.

   For detailed steps, refer to [Install {{fleet}}-managed {{agents}}](/reference/fleet/install-fleet-managed-elastic-agent.md).

::::::

::::::{step} Configure log collection with the Nginx integration

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for "nginx", then select the **Nginx** integration.
3. Select **Add Nginx**, then configure the integration. Log collection from NGINX instances is enabled by default.

   1. Confirm the **Paths** fields for access and error logs match your NGINX configuration.
   2. Turn off **Collect metrics from Nginx instances**. In this tutorial, you’ll use the OpenTelemetry input package for metrics collection.

4. In the **Where to add this integration?** section, select **Existing hosts**.
5. Select the agent policy to which you want to add the integration (for example, `nginx-telemetry`).
6. Select **Save and continue**.

For more details, refer to [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md).

::::::

::::::{step} Configure metrics collection with the NGINX OpenTelemetry input package

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In Integrations, select **Display beta integrations** (the NGINX OpenTelemetry packages are in technical preview).
3. Search for "nginx", then select **NGINX OpenTelemetry Input Package**.
4. Select **Add NGINX OpenTelemetry Input Package**, then configure the integration. **NGINX OpenTelemetry Input** is enabled by default.

   1. Select **Change defaults**, then expand **Advanced options**.
   2. Set the data stream type to **Metrics**.
   3. Set **endpoint** to your NGINX `stub_status` URL (for example, `http://localhost:80/status`).

5. In the **Where to add this integration?** section, select **Existing hosts**.
6. Select the agent policy you used for the NGINX log collection (for example, `nginx-telemetry`).
7. Select **Save and continue**.

::::{note}
The NGINX OpenTelemetry Assets content package is installed automatically when data is ingested through the NGINX OpenTelemetry Input Package. You can find it in the **Installed integrations** list and use it to visualize OTel-based metrics.
::::

::::{note}
OpenTelemetry input packages are distinct from [running {{agent}} as an EDOT Collector](/reference/fleet/otel-agent.md), and cannot be used with {{agent}} running in `otel` mode.
::::

::::::

:::::::

## Validate your data

After you apply the policy changes, validate that both the ECS-based logs and the OTel-based metrics are flowing in.

:::::::{stepper}

::::::{step} Validate the log collection

1. In {{kib}}, go to **Discover**, then filter the results using the KQL search bar.
2. Search for NGINX data stream datasets such as `nginx.access` and `nginx.error`, or enter:

   ```
   data_stream.dataset : "nginx.access" or "nginx.error"
   ```

3. Go to **Dashboards**, then select **[Logs Nginx] Access and error logs** to view the dashboard installed with the Nginx integration.

::::::

::::::{step} Validate the metrics collection

Go to **Dashboards**, then select **[Metrics Nginx OTEL] Overview** to view the dashboard for visualizing OTel-based metrics.

This dashboard is provided by the NGINX OpenTelemetry Assets content package, installed automatically when data is ingested through the NGINX OpenTelemetry Input Package.

::::::

:::::::

## Related pages

- [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md)
- [Collect NGINX logs and metrics with a hybrid standalone {{agent}}](/solutions/observability/infra-and-hosts/collect-nginx-data-otel-integration-standalone.md)
- [Elastic integrations](integration-docs://reference/index.md)
