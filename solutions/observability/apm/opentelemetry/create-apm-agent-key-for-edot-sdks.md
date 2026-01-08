---
navigation_title: Create APM agent key for EDOT SDKs
description: Learn how to create an APM agent key for Elastic Distribution of OpenTelemetry (EDOT) SDKs using Kibana.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Create {{apm-agent}} key for EDOT SDKs [create-apm-agent-key-for-edot-sdks]

{{apm-agent}} keys are least-privilege API keys used for ingesting data. When using [{{edot}} (EDOT) SDKs](opentelemetry://reference/edot-sdks/index.md), you should create an {{apm-agent}} key using the Applications UI in {{kib}}.

::::{important}
{{apm-agent}} keys are sent as plain text, so they only provide security when used in combination with [TLS](/solutions/observability/apm/apm-agent-tls-communication.md).
::::

## Create an {{apm-agent}} key

The Applications UI provides a built-in workflow to create {{apm-agent}} keys specifically for ingesting telemetry data. These keys have the minimum required privileges for EDOT SDKs to send data to Elastic.

:::{include} ../_snippets/create-apm-agent-key-applications-ui.md
:::

For EDOT SDKs, the **Agent configuration** privilege enables [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md) for remote configuration.

## Use the {{apm-agent}} key with EDOT SDKs

After creating the {{apm-agent}} key, configure your EDOT SDK to use it. Configuration details vary by language and deployment:

* **Android**: [`apiKey`](apm-agent-android://reference/edot-android/configuration.md)
* **.NET**: [`ApiKey`](apm-agent-dotnet://reference/config-reporter.md#config-api-key)
* **iOS**: [`withApiKey`](apm-agent-ios://reference/edot-ios/configuration.md#withapikey)
* **Java**: [`api_key`](elastic-otel-java://reference/edot-java/configuration.md)
* **Node.js**: [`apiKey`](elastic-otel-node://reference/edot-node/configuration.md)
* **PHP**: [`api_key`](elastic-otel-php://reference/edot-php/configuration.md)
* **Python**: [`api_key`](elastic-otel-python://reference/edot-python/configuration.md)

## Required user privileges

To create an {{apm-agent}} key, you must have the required privileges:

:::::::{tab-set}

::::::{tab-item} {{fleet}}-managed or {{apm-server}} binary

You must have the `manage_own_api_key` cluster privilege and the {{product.apm}} application privileges they intend to assign. Additionally, appropriate {{kib}} Space and Feature privileges are needed to access the Applications UI.

For details on configuring the minimum required privileges, refer to [API keys for Elastic {{product.apm}}](/solutions/observability/apm/api-keys.md#apm-create-api-key-user).

::::::

::::::{tab-item} {{serverless-full}}

For {{observability}} {{serverless-short}} projects, the Editor role or higher is required to create and manage API keys. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) for more information.

::::::

:::::::

## Difference from {{stack-manage-app}} API keys

There are two ways to create API keys in {{kib}}:

* **{{stack-manage-app}} > API keys > Create API key**: Creates general-purpose API keys for {{es}} operations. For more information, refer to [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).
* **Applications > Settings > Agent keys > Create {{apm-agent}} key** (the method described on this page): Creates least-privilege API keys specifically for ingesting {{product.apm}} data. All EDOT SDKs should use this method.

{{apm-agent}} keys are optimized for EDOT SDK telemetry data ingestion and provide better security by limiting privileges to only what's needed.