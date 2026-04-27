---
navigation_title: Monitor OTel Collectors
description: Add and monitor OpenTelemetry Collectors in Fleet to gain centralized visibility into your OTel infrastructure.
type: how-to
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Monitor OpenTelemetry Collectors in Fleet

Use {{fleet}} to centrally monitor {{edot}} (EDOT) Collectors and third-party OpenTelemetry (OTel) Collectors running in your infrastructure. 

{{fleet}} provides visibility into the health, configuration, and telemetry of any OTel Collector with the OpAMP extension, enabling you to troubleshoot issues, plan capacity, and monitor operations from a single interface.

For monitoring OTel Collectors, {{fleet}} uses the Open Agent Management Protocol (OpAMP). Collectors report their status and configuration to {{fleet-server}}, which acts as an OpAMP server.

## Before you begin

You'll need:

* An {{stack}} deployment version 9.4 or later or an {{serverless-full}} {{observability}} project
* A {{kib}} user with the **Admin** role. For more information, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* An [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) (required when setting up internal telemetry)
* An OTel Collector with OpAMP extension support:
  * Upstream and contrib OTel Collectors: version 0.103.0 or later
  * EDOT Collector: version 9.2 or later
* A running [{{fleet-server}}](/reference/fleet/fleet-server.md)

   :::{note}
   If you're using an {{ech}} deployment or a {{serverless-short}} {{observability}} project, {{fleet-server}} is already available. For self-managed deployments, refer to [Deploy on-premises and self-managed](/reference/fleet/add-fleet-server-on-prem.md).
   :::

## Add an OTel Collector in Fleet

Follow these steps to add and configure an OTel Collector in {{fleet}}:

:::::{stepper}

::::{step} Start adding an OTel Collector in Fleet

1. In {{kib}}, enter **Fleet** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Fleet / Agents**.
2. Click **Add**, then select **Collector (OpAMP)** from the list. A flyout opens with instructions for configuring your OTel Collector.
3. Copy the OpAMP configuration snippet displayed in the flyout. This configuration includes:

   ```yaml
   extensions:
     opamp:
       server:
         http:
           endpoint: https://<fleet-server-host-url>/v1/opamp <1>
           headers:
             Authorization: ApiKey <fleet-enrollment-api-key> <2>
       instance_uid: <instance-uid> <3>
   
   service:
     extensions: [opamp]
   ```
   1. The {{fleet-server}} host URL with the OpAMP endpoint, automatically provided by {{fleet}}
   2. An enrollment API key for authentication, automatically provided by {{fleet}}
   3. A placeholder for the OTel Collector instance's UUID v7

::::

::::{step} Configure the OpAMP extension

1. Paste the configuration in your OTel Collector configuration file (for example, `otel.yml`).
2. Replace `<instance-uid>` with a valid UUID v7.
3. Save your configuration.

::::

::::{step} Start your OTel Collector and verify the connection

1. Start your OTel Collector with the applied configuration changes.
2. Return to the {{fleet}} UI. The flyout displays a confirmation message when your Collector successfully connects.
3. Your OTel Collector now appears in the **Agents** list.

::::
:::::

:::{note}
If you need TLS configuration, refer to the [TLS configuration](#configure-tls-for-fleet-server-connection) section.
:::

## View OTel Collectors in the Agents list

The **Fleet** > **Agents** page displays all OTel Collectors alongside {{agents}}. The list shows key health and performance metrics from each Collector, including status, CPU and memory usage (when internal telemetry is enabled), host name and tags, version, and last activity timestamp.

:::{note}
Unlike {{agents}}, OTel Collectors don't display an agent policy in the **Agents** list. OTel Collectors use managed policies that cannot be modified and are not displayed in the **Agent policies** tab.
:::

To view detailed information about a specific OTel Collector, click its host name in the list. For more information, refer to [View details about your OTel Collector](#view-details-about-your-otel-collector).

:::{tip}
To display only OTel Collectors in the list of agents:
* From the **Tags** filter, select one or more tags to filter the list. EDOT Collectors are automatically assigned the `elastic-otel-collector` tag. Upstream/contrib OTel Collectors are automatically assigned the `otel-contrib` tag.
* From the **Agent policies** filter, select the **OpAMP** option to display all OTel Collectors.
:::

## View details about your OTel Collector

To view detailed information about an OTel Collector, click its host name in the **Agents** list. The **Agent details** page displays the following information:

### Overview

The Overview section provides key information about the OTel Collector's current state and configuration:

| Field | Description |
|-------|-------------|
| **CPU** | Average CPU usage in the last 5 minutes. Available only if internal telemetry is enabled. |
| **Memory** | Average memory usage in the last 5 minutes. Available only if internal telemetry is enabled. |
| **Status** | Current health status of the OTel Collector (for example, `Healthy`, `Unhealthy`, or `Offline`). |
| **Last activity** | Timestamp of the most recent checkin. |
| **Last checkin message** | Status message from the last checkin (for example, `StatusOK`). |
| **Agent ID** | The UUID assigned to the OTel Collector instance. |
| **Agent policy** | Shows a dash (`-`) because OTel Collectors use managed policies. |
| **Agent version** | The version of the upstream/contrib OTel Collector or EDOT Collector. |
| **Host name** | The name of the host machine running the OTel Collector. |
| **Host ID** | Shows a dash (`-`) for OTel Collectors. |
| **Platform** | The operating system platform (for example, darwin, linux, windows). |
| **Tags** | Automatically assigned tags based on collector type (`elastic-otel-collector` for EDOT Collector, `otel-contrib` for upstream/contrib collector). |
| **Collector capabilities** | The OpAMP capabilities reported by the collector: ReportsAvailableComponents, ReportsEffectiveConfig, ReportsHealth, and ReportsStatus. |

### Component health

The Component health section displays the operational status of the OTel Collector's pipeline components:

* Collector status: Shows the Collector's overall health status
* Pipeline and extension sections: Separate expandable sections for each configured extension and pipeline.

Within each section, click **Components** to view the health status of individual pipeline elements:

* Extensions: Service extension components
* Receiver: Input components collecting telemetry data
* Processor: Components transforming, filtering, or enriching data
* Exporter: Output components sending data to destinations

Each component displays a colored indicator showing its health status:

* Green indicator (Healthy): A healthy component operating normally
* Yellow indicator (Degraded): A degraded component with warnings
* Red indicator (Error): An unhealthy component with errors

Components with errors or warnings display the status message and error details.

### Effective configuration

To view the OTel Collector's running configuration, click **View Collector Configuration**. A flyout opens displaying the effective configuration currently applied to the collector. This shows the actual configuration the collector is using, which may differ from your source configuration if the collector merges multiple configuration files.

## Monitor internal telemetry for your OTel Collector

Internal telemetry allows an OTel Collector to monitor its own health and performance through a self-loop mechanism: it collects metrics, logs, and traces about its operation and sends this data to its own OTLP receiver, which exports it to {{es}}. This provides visibility into resource usage, pipeline performance, and component health without requiring an external monitoring solution.

To enable internal telemetry, extend the OTel Collector configuration provided by {{fleet}} with the following components:

1. Configure the OTLP receiver:

    ```yaml
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    ```

2. Configure the {{es}} exporter:

    ```yaml
    exporters:
      elasticsearch/otel:
        endpoints: [https://elasticsearch:9200] <1>
        api_key: "<es-api-key>" <2>
        mapping:
          mode: otel
    ```
    1. Replace with your {{es}} endpoint.
    2. Replace with an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md).

3. Set up the service pipelines:

    ```yaml
    service:
      pipelines:
        metrics:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        logs:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        traces:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
    ```

4. Set up internal telemetry for the OTel Collector:

    ```yaml
    service:
      telemetry:
        resource:
          service.instance.id: "<instance-uid>" <1>
        metrics:
          level: detailed
          readers:
            - periodic:
                interval: 3000
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        logs:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        traces:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
    ```
    1. Replace with the UUID value provided in `extensions.opamp.instance_uid`.

5. Save your configuration, then restart the OTel Collector.

Once the Collector ingests data, {{fleet}} automatically installs the OpenTelemetry Collector Internal Telemetry content package.

To view dashboards visualizing the internal telemetry, go to **Dashboards** and search for **OTel Collector internal telemetry**.

### Sample configuration with enabled internal telemetry

The following sample provides a complete OTel Collector configuration for Fleet monitoring with internal telemetry enabled. This configuration uses environment variables for sensitive values.

To use this configuration:

1. Copy the configuration from the dropdown to your OTel Collector configuration file.

    ::::{dropdown} Complete OTel Collector configuration

    ```yml
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    exporters:
      elasticsearch/otel:
        endpoints: [https://elasticsearch:9200]
        api_key: "${ES_API_KEY}"
        mapping:
          mode: otel

    extensions:
      opamp:
        server:
          http:
            endpoint: https://fleet-server:8220/v1/opamp
            headers:
              Authorization: ApiKey ${FLEET_ENROLLMENT_API_KEY}
        instance_uid: ${INSTANCE_UID}

    service:
      extensions: [opamp]
      pipelines:
        logs:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        metrics:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        traces:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
      telemetry:
        resource:
          service.instance.id: "${INSTANCE_UID}"
        metrics:
          level: detailed
          readers:
            - periodic:
                interval: 3000
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        logs:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        traces:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
    ```

    ::::

2. Update the endpoints in the configuration:
   * Replace `https://elasticsearch:9200` with your {{es}} endpoint.
   * Replace `https://fleet-server:8220` with your {{fleet-server}} host URL.
3. Export the environment variables:

   ```bash
   export INSTANCE_UID=<uuid-v7>
   export OTEL_RESOURCE_ATTRIBUTES="service.instance.id=$INSTANCE_UID"  # Ensures internal telemetry includes the instance ID
   export ES_API_KEY=<elasticsearch-api-key>
   export FLEET_ENROLLMENT_API_KEY=<fleet-enrollment-api-key> # The enrollment API key provided when you add an OTel Collector in Fleet
   ```

4. Restart your OTel Collector with the new configuration.

## Configure TLS for Fleet Server connection

If your {{fleet-server}} uses a self-signed certificate or a certificate from a non-public Certificate Authority (CA), you need to configure the OpAMP extension to trust it.

### Use a custom CA certificate

When {{fleet-server}} uses a certificate signed by a private CA, provide the CA certificate to your OTel Collector:

```yaml
extensions:
  opamp:
    server:
      http:
        endpoint: https://fleet-server:8220/v1/opamp
        tls:
          ca_file: /path/to/ca.crt <1>
        headers:
          Authorization: ApiKey <fleet-enrollment-api-key>
    instance_uid: <instance-uid>

service:
  extensions: [opamp]
```
1. Replace `/path/to/ca.crt` with the path to your CA certificate file.

### Skip certificate verification (testing only)

For testing purposes only, you can skip TLS certificate verification:

```yaml
extensions:
  opamp:
    server:
      http:
        endpoint: https://fleet-server:8220/v1/opamp
        tls:
          insecure_skip_verify: true <1>
        headers:
          Authorization: ApiKey <fleet-enrollment-api-key>
    instance_uid: <instance-uid>

service:
  extensions: [opamp]
```
1. Set to `true` to skip TLS certificate verification.

:::{warning}
Using `insecure_skip_verify: true` disables TLS certificate verification and makes your connection vulnerable to man-in-the-middle attacks. Only use this for testing in isolated environments, never in production.
:::

## Troubleshooting

For troubleshooting information related to adding OTel Collectors in {{fleet}}, refer to [OpenTelemetry Collectors in Fleet](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet) in the [Common problems with Fleet and Elastic Agent](/troubleshoot/ingest/fleet/common-problems.md) guide.

## Related pages

- [Elastic Distributions of OpenTelemetry (EDOT)](opentelemetry://reference/index.md)
- [Troubleshoot the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md)
