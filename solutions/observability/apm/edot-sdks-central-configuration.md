---
navigation_title: Centrally configure EDOT SDKs
applies_to:
  deployment:
      ess: preview 9.1
  stack: preview 9.1
  serverless: unavailable
    
products:
  - id: observability
  - id: kibana
  - id: edot-collector
---

# Central Configuration for EDOT SDKs [edot-sdks-central-configuration]

APM Agent Central Configuration allows you to fine-tune your EDOT SDKs from within the Applications UI. Changes are automatically propagated to your SDKs, so there’s no need to redeploy.

To get started, select the services and environments you want to configure. The Applications UI lets you know when your EDOT SDKs have applied your configurations.

::::{important}
To configure EDOT SDKs through APM Agent Central Configuration, refer to [EDOT SDKs Central Configuration](edot-sdks-central-configuration.md).
::::

## Precedence [_precedence]

Configurations set from the Applications UI take precedence over configurations set locally in each EDOT SDK. If the EDOT Collector is offline, reports an error, or is slow to respond, EDOT SDKs use local defaults until they’re able to update the configuration.

## Supported configurations [_supported_configurations]

Each EDOT SDK has a list of supported configurations. After selecting a Service name and environment in the Applications UI, a list of all supported configuration options, including descriptions and default values, will be displayed.

Supported configurations are also tagged with the ![dynamic config](/solutions/images/observability-dynamic-config.svg "") badge in each EDOT SDK’s configuration reference:

| Language/Platform | EDOT SDK | Configuration Reference |
| --- | --- | --- |
| Android | EDOT Android SDK | [Configuration reference](opentelemetry://reference/edot-sdks/android/configuration.md) |
| iOS | EDOT iOS SDK | [Configuration reference](opentelemetry://reference/edot-sdks/ios/configuration.md) |
| Java | EDOT Java SDK | [Configuration reference](opentelemetry://reference/edot-sdks/java/configuration.md) |
| Node.js | EDOT Node.js SDK | [Configuration reference](opentelemetry://reference/edot-sdks/nodejs/configuration.md) |
| PHP | EDOT PHP SDK | [Configuration reference](opentelemetry://reference/edot-sdks/php/configuration.md) |
| Python | EDOT Python SDK | [Configuration reference](opentelemetry://reference/edot-sdks/python/configuration.md) |

## EDOT configuration [_edot_configuration]

EDOT SDK configuration is an optional feature. To activate it, refer to [EDOT SDK Central Configuration](edot-sdks-central-configuration.md).

Refer to the [EDOT reference](opentelemetry://reference/central-configuration.md) to learn how to activate central configuration for EDOT SDKs.

::::{note}
You can't configure APM agents through the EDOT Collector. Use APM Server for that purpose. Refer to [Configure APM agent configuration](/solutions/observability/apm/configure-apm-agent-central-configuration.md) for more details.
::::
