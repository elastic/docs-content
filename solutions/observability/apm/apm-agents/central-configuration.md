---
navigation_title: Centrally configure APM agents
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# APM Agent Central Configuration [apm-agent-configuration]

APM Agent Central Configuration allows you to fine-tune your APM agents from within the Applications UI. Changes are automatically propagated to your agents, so there’s no need to redeploy.

To get started, select the services and environments you want to configure. The Applications UI lets you know when your APM agents have applied your configurations.

:::{image} /solutions/images/observability-apm-agent-configuration.png
:alt: APM central configuration in Kibana
:screenshot:
:::

::::{important}
To configure EDOT SDKs through APM Agent Central Configuration, refer to [EDOT SDKs Central Configuration](/solutions/observability/apm/opentelemetry/edot-sdks-central-configuration.md).
::::

## Precedence [_precedence]

Configurations set from the Applications UI take precedence over configurations set locally in each APM agent or EDOT SDK. However, if APM Server is slow to respond, is offline, reports an error, etc., agents and SDKs will use local defaults until they’re able to update the configuration. For this reason, it is still essential to set custom default configurations locally in each of your APM agents and EDOT SDKs.

## Supported configurations [_supported_configurations]

Each APM agent has a list of supported configurations. After selecting a Service name and environment in the Applications UI, a list of all supported configuration options, including descriptions and default values, will be displayed.

Supported configurations are also tagged with the ![dynamic config](/solutions/images/observability-dynamic-config.svg "") badge in each APM agent’s configuration reference:

Android agent
:   [Configuration reference](apm-agent-android://reference/edot-android/configuration.md)

Go agent
:   [Configuration reference](apm-agent-go://reference/configuration.md)

iOS agent
:   [Configuration reference](apm-agent-ios://reference/edot-ios/configuration.md)

Java agent
:   [Configuration reference](apm-agent-java://reference/configuration.md)

.NET agent
:   [Configuration reference](apm-agent-dotnet://reference/configuration.md)

Node.js agent
:   [Configuration reference](apm-agent-nodejs://reference/configuration.md)

PHP agent
:   [Configuration reference](apm-agent-php://reference/configuration.md)

Python agent
:   [Configuration reference](apm-agent-python://reference/configuration.md)

Ruby agent
:   [Configuration reference](apm-agent-ruby://reference/configuration.md)

Real User Monitoring (RUM) agent
:   [Configuration reference](apm-agent-rum-js://reference/configuration.md)

## APM Server configuration [_apm_server_configuration]

For most users, APM agent configuration should work out-of-the-box. If you run into trouble, it may be because you’re not using the {{es}} output, or because your {{es}} credentials don’t have sufficient privileges.

Refer to [configure APM agent configuration](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md) to learn how to configure APM Server to avoid these problems.

::::{note}
You can't configure APM agents through the EDOT Collector. Use APM Server for that purpose.
::::
