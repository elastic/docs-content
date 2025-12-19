---
navigation_title: Create APM agent key for EDOT SDKs
description: Learn how to create an APM agent key for Elastic Distribution of OpenTelemetry (EDOT) SDKs using the Applications UI in Kibana.
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

## Create an {{apm-agent}} key in the Applications UI

The Applications UI provides a built-in workflow to create {{apm-agent}} keys specifically for ingesting telemetry data. These keys have the minimum required privileges for EDOT SDKs to send data to Elastic.

:::::::{tab-set}

::::::{tab-item} {{fleet}}-managed or {{apm-server}} binary

To create an {{apm-agent}} key:

1. In {{kib}}, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Go to **Settings** → **Agent keys**.
3. Enter a name for your API key.
4. Select at least one privilege:
   - **Ingest** (`event:write`): Required to ingest agent events from EDOT SDKs.
   - **Agent configuration** (`config_agent:read`): Required to use [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md) for remote configuration.
5. Click **Create API key**.
6. Copy the Base64-encoded API key. You'll need it to configure your EDOT SDKs. You won't be able to view it again.

:::{image} /solutions/images/observability-apm-ui-api-key.png
:alt: Applications UI API key
:screenshot:
:::

::::::

::::::{tab-item} {{serverless-full}}

To create an {{apm-agent}} key:

1. In your {{obs-serverless}} project, go to any Applications page.
2. Click **Settings**.
3. Select the **Agent keys** tab.
4. Click **Create API key**.
5. Name the API key and assign at least one privilege:
   - **Ingest** (`event:write`): Required to ingest agent events from EDOT SDKs.
   - **Agent configuration** (`config_agent:read`): Required to use [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md) for remote configuration.
6. Click **Create API key**.
7. Copy the API key now. You won’t be able to view it again. API keys do not expire.

To view all project API keys:

1. Expand **{{project-settings}}**.
2. Select **{{manage-app}}**.
3. Select **API keys**.

::::::

:::::::

## Use the API key with EDOT SDKs

After creating the {{apm-agent}} key, configure your EDOT SDK to use it. Configuration details vary by language and deployment:

* **Android**: [`apiKey`](apm-agent-android://reference/edot-android/configuration.md)
* **.NET**: [`ApiKey`](apm-agent-dotnet://reference/config-reporter.md#config-api-key)
* **iOS**: [`withApiKey`](apm-agent-ios://reference/edot-ios/configuration.md#withapikey)
* **Java**: [`api_key`](apm-agent-java://reference/config-reporter.md#config-api-key)
* **Node.js**: [`apiKey`](apm-agent-nodejs://reference/configuration.md#api-key)
* **PHP**: [`api_key`](apm-agent-php://reference/configuration-reference.md#config-api-key)
* **Python**: [`api_key`](apm-agent-python://reference/configuration.md#config-api-key)

## Required user privileges

To create an {{apm-agent}} key, a user must have the required privileges:

:::::::{tab-set}

::::::{tab-item} {{fleet}}-managed or {{apm-server}} binary

The user must have the `manage_own_api_key` cluster privilege and the {{product.apm}} application privileges they intend to assign. Additionally, appropriate {{kib}} Space and Feature privileges are needed to access the Applications UI.

For details on configuring the minimum required privileges, see [API keys for Elastic {{product.apm}}](/solutions/observability/apm/api-keys.md#apm-create-api-key-user).

::::::

::::::{tab-item} {{serverless-full}}

For {{observability}} {{serverless-short}} projects, the Editor role or higher is required to create and manage API keys. Learn more in [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::::

:::::::

## Difference from {{stack-manage-app}} API keys

There are two ways to create API keys in {{kib}}:

1. **{{stack-manage-app}} → API keys → Create API key**: Creates general-purpose API keys for {{es}} operations. For more information, see [{{es}} API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).
2. **Applications → Settings → Agent keys → Create API key** (this method): Creates least-privilege API keys specifically for ingesting {{product.apm}} data. **EDOT SDKs should use this method.**

{{apm-agent}} keys created through the Applications UI are optimized for telemetry data ingestion and provide better security by limiting privileges to only what's needed.