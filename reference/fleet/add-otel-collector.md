---
navigation_title: Add an OTel Collector
description: Add an OpenTelemetry Collector to Fleet using the Add collector flow.
type: how-to
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Add an OTel Collector in Fleet

Add an OpenTelemetry (OTel) Collector to {{fleet}} for centralized monitoring using the **Add collector** flow. {{fleet}} generates an OTel Collector configuration with the OpAMP extension wired to {{fleet-server}}, an OTLP receiver, OTLP-to-{{es}} pipelines, and internal telemetry configuration. You then apply the configuration to your collector.

## Before you begin

You'll need:

* An {{stack}} deployment version 9.4 or later or an {{serverless-full}} {{observability}} project
* A {{kib}} user with the **Admin** role. For more information, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* An OTel Collector with OpAMP extension support. For supported distributions and versions, refer to [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md).
* A running [{{fleet-server}}](/reference/fleet/fleet-server.md)

   :::{note}
   If you're using an {{ech}} deployment or a {{serverless-short}} {{observability}} project, {{fleet-server}} is already available. For self-managed deployments, refer to [Deploy on-premises and self-managed](/reference/fleet/add-fleet-server-on-prem.md).
   :::

## Add the collector through the Fleet UI

::::::{stepper}

:::::{step} Start adding a collector

1. In {{kib}}, enter **Fleet** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Fleet / Agents**.
2. Click **Add**, then select **Collector (OpAMP)** from the list.

A flyout opens where you can enter metadata for your OTel Collector and preview the generated configuration.

:::::

:::::{step} Enter collector metadata

Provide values for the fields in the flyout. {{fleet}} uses them to populate the OpAMP identity attributes and internal telemetry resource attributes in the generated configuration.

| Field | Required | Description |
|-------|----------|-------------|
| **Collector group display name** | Yes | Human-readable label for this group of collectors (for example, `Production West`). Defaults to `OTel Collector Group`. Sets `elastic.collector.group_name`. |
| **Collector group** | Yes | Identifier used for filtering collectors in the {{fleet}} UI. Auto-derived from the group display name as a slug. If you override the value, use only lowercase letters, numbers, and hyphens. Sets `elastic.collector.group` and `service.namespace`. |
| **Service name** | Yes | Identifier for the collector group in {{es}}. Auto-derived from the group display name as a slug. If you override the value, use only lowercase letters, numbers, and hyphens. Sets `service.name`. |
| **Collector display name** | Yes | Per-instance identity that distinguishes this collector within the group. Defaults to `${env:HOSTNAME}`. Sets `elastic.display.name` and `service.instance.id`. |
| **Config name** | No | A short name for this collector configuration (for example, `webserver-logs`). Appears as the configuration label in the {{fleet}} UI. Sets `config.name`. |
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

1. Copy the YAML configuration displayed in the flyout, or click **Download config** to save it as a YAML file. The snippet wires the OpAMP extension to {{fleet-server}}, sets up an OTLP receiver and OTLP-to-{{es}} pipelines, and adds internal telemetry configuration.

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
   3. Skips verification of the {{fleet-server}} TLS certificate. Before deploying to production, adjust the configuration to use a CA file as described in [Configure TLS for {{fleet-server}} connection](#configure-tls-for-fleet-server-connection).
   4. A UUID v7 instance identifier, automatically generated by {{fleet}}.
   5. Identity attributes populated from the form fields you provided in the previous step.
   6. The {{es}} endpoint, automatically populated from your default {{fleet}} output.
   7. The {{es}} API key. If you used **Create API key**, {{fleet}} replaces `${API_KEY}` with the generated key. Otherwise, replace `${API_KEY}` manually with your existing encoded key.

   ::::

2. Paste or merge the configuration into your OTel Collector configuration file (for example, `otel.yaml`).
3. Make sure every environment-variable placeholder in the configuration resolves at runtime:
   - `${API_KEY}`: replace it with your encoded {{es}} API key value, or set the `API_KEY` environment variable before starting or restarting the collector.
   - `${env:HOSTNAME}`: make sure `HOSTNAME` is set in the collector's runtime environment, or replace the placeholder with a static identifier.
4. Save your configuration.

:::::

:::::{step} Verify the collector connection

1. Start or restart your OTel Collector with the applied configuration.
2. Return to the {{fleet}} UI. The flyout displays a confirmation message when your collector successfully connects.
3. Your OTel Collector now appears in the **Agents** list.

:::::
::::::

:::{important}
The generated configuration uses `tls.insecure_skip_verify: true` for the {{fleet-server}} connection. Before deploying to production, adjust the configuration to use a CA file as described in [Configure TLS for {{fleet-server}} connection](#configure-tls-for-fleet-server-connection).
:::

::::{include} /reference/fleet/_snippets/otel-motlp-exporter-alternative.md
::::

## Configure TLS for {{fleet-server}} connection

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

* [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md)
* [Troubleshoot OTel Collectors in Fleet](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet)
