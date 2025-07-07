---
navigation_title: Centrally configure APM agents in Kibana
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html
applies_to:
  stack:
products:
  - id: observability
  - id: apm
---

# APM agent central configuration [apm-agent-configuration]

APM Agent configuration allows you to fine-tune your APM agent configuration from within the Applications UI. Changes are automatically propagated to your APM agents, so there’s no need to redeploy.

To get started, choose the services and environments you wish to configure. The Applications UI will let you know when your APM agents have applied your configurations.

:::{image} /solutions/images/observability-apm-agent-configuration.png
:alt: APM Agent configuration in Kibana
:screenshot:
:::

## Precedence [_precedence]

Configurations set from the Applications UI take precedence over configurations set locally in each APM agent. However, if APM Server is slow to respond, is offline, reports an error, etc., APM agents will use local defaults until they’re able to update the configuration. For this reason, it is still essential to set custom default configurations locally in each of your APM agents.

## Supported configurations [_supported_configurations]

Each APM agent has a list of supported configurations. After selecting a Service name and environment in the Applications UI, a list of all supported configuration options, including descriptions and default values, will be displayed.

Supported configurations are also tagged with the ![dynamic config](/solutions/images/observability-dynamic-config.svg "") badge in each APM agent’s configuration reference:

Android agent
:   [Configuration reference](opentelemetry://reference/edot-sdks/android/configuration.md)

Go agent
:   [Configuration reference](apm-agent-go://reference/configuration.md)

iOS agent
:   [Configuration reference](opentelemetry://reference/edot-sdks/ios/configuration.md)

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

See [configure APM agent configuration](/solutions/observability/apm/configure-apm-agent-central-configuration.md) to learn how to configure APM Server to avoid these problems.

