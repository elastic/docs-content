---
navigation_title: Monitor OTel Collectors
description: Add and monitor OpenTelemetry Collectors in Fleet to gain centralized visibility into your OpenTelemetry infrastructure.
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
* An OTel Collector with OpAMP extension support:
  * OpenTelemetry Collector (upstream and community-contributed distributions): version 0.103.0 or later
  * EDOT Collector: version 9.2 or later
* A running [{{fleet-server}}](/reference/fleet/fleet-server.md)

   :::{note}
   If you're using an {{ech}} deployment or a {{serverless-short}} {{observability}} project, {{fleet-server}} is already available. For self-managed deployments, refer to [Deploy on-premises and self-managed](/reference/fleet/add-fleet-server-on-prem.md).
   :::

## Add an OTel Collector in Fleet

Follow these steps to add and configure an OTel Collector in {{fleet}}:

::::::{stepper}

:::::{step} Start adding a collector

1. In {{kib}}, enter **Fleet** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Fleet / Agents**.
2. Click **Add**, then select **Collector (OpAMP)** from the list.

A flyout opens where you can enter metadata for your OTel Collector and preview the generated configuration.

:::::

:::::{step} Enter collector metadata

Provide values for the fields in the flyout. {{fleet}} uses them to populate the OpAMP identity attributes and self-telemetry resource attributes in the generated configuration.

| Field | Required | Description |
|-------|----------|-------------|
| **Collector group display name** | Yes | Human-readable label for this group of collectors (for example, `Production West`). Defaults to `OTel Collector Group`. Sets `elastic.collector.group_name`. |
| **Collector group** | Yes | Identifier used for filtering collectors in the {{fleet}} UI. Auto-derived from the group display name as a slug. If you override the value, use only lowercase letters, numbers, and hyphens. Sets `elastic.collector.group` and `service.namespace`. |
| **Service name** | Yes | Identifier for the collector group in {{es}}. Auto-derived from the group display name as a slug. If you override the value, use only lowercase letters, numbers, and hyphens. Sets `service.name`. |
| **Collector display name** | Yes | Per-instance identity that distinguishes this collector within the group. Defaults to `${env:HOSTNAME}`. Sets `elastic.display.name` and `service.instance.id`. |
| **Config description** | No | A human-readable summary of what the collector does. Appears as a comment header in the effective configuration view. Sets `config.description`. |
| **Tags** | No | Comma-separated labels (for example, `prod,west-region,k8s`). Tags appear in the {{fleet}} UI tag filter and as resource attributes on self-emitted metrics and logs. |
| **Environment** | No | Label for the deployment environment (for example, `production` or `staging`). Sets `deployment.environment.name`. |

A generated configuration preview appears when all required fields contain valid values.

:::{note}
If you override the **Collector group** or **Service name** fields, they stop auto-updating from the group display name.
:::

:::::

:::::{step} Supply an {{es}} API key

:::{note}
This applies to the `elasticsearch/otel` exporter included in the generated configuration. If your collector already exports to {{es}} with a valid API key, skip this step.
:::

Choose how to provide an {{es}} API key for the `elasticsearch/otel` exporter:

* **Create one in the flyout**: Click **Create API key**. {{fleet}} creates an API key with default privileges and substitutes it for `${API_KEY}` in the generated configuration.
* **Use an existing key**: Skip this action in the flyout, and replace `${API_KEY}` manually after copying the configuration in the next step. The key must have `create_index`, `write`, and `auto_configure` index privileges on `metrics-*`, `logs-*`, and `traces-*` data streams.

:::::

:::::{step} Apply the configuration

1. Copy the YAML configuration displayed in the flyout, or click **Download config** to save it as a YAML file. The snippet wires the OpAMP extension to {{fleet-server}}, sets up an OTLP receiver and pipelines for internal telemetry, and configures an {{es}} exporter.

   :::{note}
   If you already have a working OTel Collector with an {{es}} exporter, merge the generated configuration into your existing setup instead of replacing the whole file. Remove the `elasticsearch/otel` exporter block and adjust the pipelines to use your existing exporter.
   :::

   ::::{dropdown} Generated OTel Collector configuration

   ```yaml
   extensions:
     opamp:
       server:
         http:
           endpoint: "https://<fleet-server-host-url>/v1/opamp" <1>
           headers:
             Authorization: "ApiKey <fleet-enrollment-api-key>" <2>
           tls:
             insecure_skip_verify: true <3>
       instance_uid: "<instance-uid>" <4>
       agent_description:
         non_identifying_attributes: <5>
           elastic.collector.group_name: "OTel Collector Group"
           elastic.collector.group: "otel-collector-group"
           elastic.display.name: "${env:HOSTNAME}"

   receivers:
     otlp:
       protocols:
         grpc:
           endpoint: "0.0.0.0:4317"

   exporters:
     elasticsearch/otel:
       endpoints:
         - "https://<elasticsearch-host-url>" <6>
       api_key: "${API_KEY}" <7>
       mapping:
         mode: otel
     otlp:
       endpoint: "http://localhost:4317"
       tls:
         insecure: true

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
         elastic.collector.group_name: "OTel Collector Group"
         elastic.collector.group: "otel-collector-group"
         service.namespace: "otel-collector-group"
         service.name: "otel-collector-group"
         service.instance.id: "${env:HOSTNAME}"
       metrics:
         readers:
           - periodic:
               exporter:
                 otlp:
                   protocol: grpc
                   endpoint: "http://localhost:4317"
       logs:
         processors:
           - batch:
               exporter:
                 otlp:
                   protocol: grpc
                   endpoint: "http://localhost:4317"
       traces:
         processors:
           - batch:
               exporter:
                 otlp:
                   protocol: grpc
                   endpoint: "http://localhost:4317"
   ```
   1. The {{fleet-server}} host URL with the OpAMP endpoint, automatically populated by {{fleet}}.
   2. An enrollment API key, automatically populated by {{fleet}}.
   3. Skips verification of the {{fleet-server}} TLS certificate. Useful for first-run testing; for production, replace it with a CA file as described in [Configure TLS for {{fleet-server}} connection](#configure-tls-for-fleet-server-connection).
   4. A UUID v7 instance identifier, automatically generated by {{fleet}}.
   5. Identity attributes populated from the form fields you provided in the previous step.
   6. The {{es}} endpoint, automatically populated from your default {{fleet}} output.
   7. The {{es}} API key. If you used **Create API key**, {{fleet}} replaces `${API_KEY}` with the generated key. Otherwise, replace `${API_KEY}` manually with your existing encoded key.

   ::::

   For a breakdown of how the internal telemetry components are wired together, refer to [Monitor internal telemetry for your OTel Collector](#monitor-internal-telemetry-for-your-otel-collector).

2. Paste or merge the configuration into your OTel Collector configuration file (for example, `otel.yaml`).
3. Make sure every environment-variable placeholder in the configuration resolves at runtime:
   - `${API_KEY}`: replace it with your encoded {{es}} API key value, or set the `API_KEY` environment variable before starting the collector.
   - `${env:HOSTNAME}`: make sure `HOSTNAME` is set in the collector's runtime environment, or replace the placeholder with a static identifier.
4. Save your configuration.

:::::

:::::{step} Verify the collector connection

1. Start your OTel Collector with the applied configuration.
2. Return to the {{fleet}} UI. The flyout displays a confirmation message when your collector successfully connects.
3. Your OTel Collector now appears in the **Agents** list.

:::::
::::::

:::{important}
The generated configuration uses `tls.insecure_skip_verify: true` for the {{fleet-server}} connection — convenient for first-run testing, but not safe for production. Before deploying to production, replace it with a CA file as described in [Configure TLS for {{fleet-server}} connection](#configure-tls-for-fleet-server-connection).
:::

::::{include} /reference/fleet/_snippets/otel-motlp-exporter-alternative.md
::::

## View OTel Collectors in the Agents list

The **Fleet** > **Agents** page displays all OTel Collectors alongside {{agents}}. The list shows key health and performance metrics from each collector, including status, CPU and memory usage (when internal telemetry is enabled), host name and tags, version, and last activity timestamp.

:::{note}
Unlike {{agents}}, OTel Collectors don't display an agent policy in the **Agents** list. OTel Collectors use managed policies that can't be modified and aren't displayed in the **Agent policies** tab.
:::

To view detailed information about a specific OTel Collector, click its host name in the list. For more information, refer to [View details about your OTel Collector](#view-details-about-your-otel-collector).

:::{tip}
To display only OTel Collectors in the list of agents:
* From the **Tags** filter, select one or more tags to filter the list. EDOT Collectors are automatically assigned the `elastic-otel-collector` tag. Upstream and community-contributed OTel Collectors are automatically assigned the `otel-contrib` tag.
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
| **Last activity** | Timestamp of the most recent check-in. |
| **Last checkin message** | Status message from the last check-in (for example, `StatusOK`). |
| **Agent ID** | The UUID assigned to the OTel Collector instance. |
| **Agent policy** | Shows a dash (`-`) because OTel Collectors use managed policies. |
| **Agent version** | The version of the upstream and community-contributed OTel Collector or EDOT Collector. |
| **Host name** | The name of the host machine running the OTel Collector. |
| **Host ID** | Shows a dash (`-`) for OTel Collectors. |
| **Platform** | The operating system platform (for example, darwin, linux, windows). |
| **Tags** | Automatically assigned tags based on collector type (`elastic-otel-collector` for EDOT Collector, `otel-contrib` for upstream and community-contributed OTel Collectors). |
| **Collector capabilities** | The OpAMP capabilities reported by the collector: `ReportsAvailableComponents`, `ReportsEffectiveConfig`, `ReportsHealth`, and `ReportsStatus`. |

### Component health

The Component health section displays the operational status of the OTel Collector's pipeline components:

* Collector status: Shows the collector's overall health status
* Pipeline and extension sections: Separate expandable sections for each configured extension and pipeline

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

Internal telemetry allows an OTel Collector to monitor its own health and performance through a self-loop mechanism: the collector emits metrics, logs, and traces about its operation to its own OTLP (OpenTelemetry Protocol) receiver, which forwards the data through a pipeline to a backend such as {{es}}. This provides visibility into resource usage, pipeline performance, and component health without requiring an external monitoring solution.

The configuration generated by the **Add collector** flyout includes internal telemetry by default. The following components show how internal telemetry is wired together, so you can adapt your own configuration if you're not using the flyout, or you're starting from an existing collector setup.

To add internal telemetry to an existing collector configuration, extend it with the following components:

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

2. Configure an exporter that sends telemetry to your {{es}} backend. If your collector already exports telemetry, you can reuse the existing exporter — just add the OTLP receiver to its pipelines. Otherwise, configure the `elasticsearch/otel` exporter:

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

    ::::{include} /reference/fleet/_snippets/otel-motlp-exporter-alternative.md
    ::::

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

Once the collector ingests data, {{fleet}} automatically installs the OpenTelemetry Collector Internal Telemetry content package.

To view dashboards visualizing the internal telemetry, go to **Dashboards** and search for **OTel Collector internal telemetry**.

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
Using `insecure_skip_verify: true` skips TLS certificate verification and makes your connection vulnerable to man-in-the-middle attacks. Only use this for testing in isolated environments, never in production.
:::

## Related pages

- [OpenTelemetry Collectors in Fleet troubleshooting](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet)
- [Elastic Distributions of OpenTelemetry (EDOT)](opentelemetry://reference/index.md)
- [Troubleshoot the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md)
