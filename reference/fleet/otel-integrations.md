---
navigation_title: OpenTelemetry integration packages
description: Fleet supports installing Elastic Agent integration packages for collecting and visualizing OpenTelemetry data such as logs, metrics, and traces.
applies_to:
  stack: preview 9.2
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Collect OpenTelemetry data with {{agent}} integrations

{{fleet}} now supports installing {{agent}} integration packages for collecting and visualizing OpenTelemetry (OTel) data such as logs, metrics, and traces. To find the available OpenTelemetry integration packages, open the **Integrations** page in {{kib}}, then select the **OpenTelemetry** category.

There are two types of OpenTelemetry integration packages:

- Input packages which include an OTel Collector configuration.
- Content packages which include {{es}} and {{kib}} assets such as prebuilt dashboards and visualizations.

Unlike {{agent}} integrations based on the [Elastic Common Schema](ecs://reference/index.md) (ECS), OpenTelemetry input packages use OTel Collector receivers to collect OTel data following [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv).

When OTel data is collected using an OpenTelemetry input package, content packages with assets related to the collected data type are automatically installed if available.

:::{important}
OpenTelemetry input packages are used with {{fleet}} and {{agent}} running in default mode. They are distinct from [running {{agent}} as an EDOT Collector](/reference/fleet/otel-agent.md), and cannot be used on {{agent}} running in `otel` mode.
:::

## Configure OpenTelemetry input packages

The installation and configuration of OpenTelemetry input packages is similar to that of ECS-based integrations and allow you to specify the namespace, dataset name, data stream type, and more. For more information, refer to [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md).

When the integration policy for the input package is created, {{fleet}} creates a managed index template with an OTel configuration and an index pattern with an `.otel` suffix. The index template uses {{fleet}} component templates for settings and OTel component templates for default mappings. It also includes `@custom` component templates that allow you to [customize your {{es}} index](/reference/fleet/data-streams.md#data-streams-index-templates-edit) similarly to ECS-based integrations.

On the OpenTelemetry input package's **Configs** page, you can view a generated sample configuration, which you can use as a starting point to set up the integration on a standalone {{agent}}. 

Note that this is a partial configuration as it does not include an exporter component. For more information on setting up the exporter, refer to [{{es}} exporter](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md).

:::{note}
Currently, OpenTelemetry input packages only support sending data using the {{es}} output.
:::

## Compatibility with ECS-based integrations

{{agent}} policies can include configurations for both ECS-based integrations and OpenTelemetry input packages, essentially converting the {{agents}} enrolled in the policy into hybrid agents.

Note that only {{agents}} on version 9.2 or later can collect OTel data using OpenTelemetry input packages. OpenTelemetry input packages added to an agent policy do not affect enrolled agents on prior versions.