---
navigation_title: Collect nginx logs and metrics with hybrid standalone agent
description: Collect nginx logs and metrics with a hybrid standalone Elastic Agent using Elastic's Nginx integration and NGINX OpenTelemetry Input Package.
applies_to:
  stack: preview 9.2+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Collect nginx logs and metrics with a hybrid standalone {{agent}}

Follow this guide to learn how to configure a standalone {{agent}} on a Linux host to collect:

- nginx logs with Elastic's [Nginx integration](https://www.elastic.co/docs/reference/integrations/nginx), based on the [Elastic Common Schema](ecs://reference/index.md) (ECS)
- nginx metrics with Elastic's [NGINX OpenTelemetry Input Package](https://www.elastic.co/docs/reference/integrations/nginx_otel_input), which uses the [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OpenTelemetry (OTel) Collector receiver

## Prerequisites

:::::{applies-switch}

::::{applies-item} serverless: preview
* An {{observability}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* {{agent}} 9.2 or later installed on a Linux host.
* nginx installed on a Linux host.
::::

::::{applies-item} stack: preview 9.2+
* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* {{agent}} 9.2 or later installed on a Linux host.
* nginx installed on a Linux host.
::::

:::::

## Configure the nginx status endpoint

The [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OTel Collector receiver needs an endpoint that exposes nginx status metrics.

1. Make sure the [`ngx_http_stub_status_module`](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html) module is enabled.
2. In your nginx configuration file (for example, `/etc/nginx/nginx.conf`), add or modify the `location` block in the `server { ... }` block with the following:

    ```nginx
    location = /status {
      stub_status;
    }
    ```

3. Save the configuration and restart nginx:

    ```bash
    sudo systemctl restart nginx
    ```

4. Verify that the endpoint is active:

    ```bash
    curl http://localhost:80/status <1>
    ```
    1. Replace the port number with the port specified in the `listen` directive in the nginx configuration.

    If the endpoint returns data, you are ready to set up {{agent}}.

For more details, refer to [Configuring NGINX for Metric Collection](https://docs.nginx.com/nginx-amplify/nginx-amplify-agent/configuring-metric-collection/#metrics-from-stub_status).

## Configure the hybrid standalone agent policy

TODO

## Validate your data

After you apply the policy changes, validate both the ECS-based logs and the OTel-based metrics.

:::::::{stepper}

::::::{step} Validate the log collection

1. In {{kib}}, go to **Discover**, then filter the results using the KQL search bar.
2. Search for nginx data stream datasets such as `nginx.access` and `nginx.error`, or enter:

   ```
   data_stream.dataset : "nginx.access" or "nginx.error"
   ```

3. Go to **Dashboards**, then select **[Logs Nginx] Access and error logs** to view the dashboard installed with the Nginx integration.

::::::

::::::{step} Validate the metrics collection

Go to **Dashboards**, then select **[Metrics Nginx OTEL] Overview** to view the dashboard for visualizing OTel-based metrics.

This dashboard becomes available with the NGINX OpenTelemetry Assets content package, which is automatically installed when data is ingested trough the NGINX OpenTelemetry Input Package integration.

::::::

:::::::

## Related pages

- [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md)
- [Collect nginx logs and metrics with a hybrid {{fleet}}-managed {{agent}}](/solutions/observability/infra-and-hosts/collect-nginx-data-otel-integration-fleet-managed.md)
- [Elastic integrations](integration-docs://reference/index.md)
