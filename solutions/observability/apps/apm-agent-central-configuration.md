---
navigation_title: "Centrally configure APM agents in Kibana"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-configuration.html
applies_to:
  stack: all
---



# APM agent central configuration [apm-agent-configuration]

APM Agent configuration allows you to fine-tune your APM agent configuration from within the Applications UI. Changes are automatically propagated to your APM agents, so there’s no need to redeploy.

To get started, choose the services and environments you wish to configure. The Applications UI will let you know when your APM agents have applied your configurations.

:::{image} ../../../images/observability-apm-agent-configuration.png
:alt: APM Agent configuration in Kibana
:class: screenshot
:::


## Precedence [_precedence]

Configurations set from the Applications UI take precedence over configurations set locally in each APM agent. However, if APM Server is slow to respond, is offline, reports an error, etc., APM agents will use local defaults until they’re able to update the configuration. For this reason, it is still essential to set custom default configurations locally in each of your APM agents.


## Supported configurations [_supported_configurations]

Each APM agent has a list of supported configurations. After selecting a Service name and environment in the Applications UI, a list of all supported configuration options, including descriptions and default values, will be displayed.

Supported configurations are also tagged with the ![dynamic config](../../../images/observability-dynamic-config.svg "") badge in each APM agent’s configuration reference:

Android agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-android/docs/reference/configuration.md)

Go agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md)

iOS agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-ios/docs/reference/configuration.md)

Java agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-java/docs/reference/configuration.md)

.NET agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-dotnet/docs/reference/configuration.md)

Node.js agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuration.md)

PHP agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-php/docs/reference/configuration.md)

Python agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md)

Ruby agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md)

Real User Monitoring (RUM) agent
:   [Configuration reference](asciidocalypse://docs/apm-agent-rum-js/docs/reference/configuration.md)


## APM Server configuration [_apm_server_configuration]

For most users, APM agent configuration should work out-of-the-box. If you run into trouble, it may be because you’re not using the {{es}} output, or because your {{es}} credentials don’t have sufficient privileges.

See [configure APM agent configuration](/solutions/observability/apps/configure-apm-agent-central-configuration.md) to learn how to configure APM Server to avoid these problems.

