---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-secret-token.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Secret token [apm-secret-token]

::::{important}
Secret tokens are sent as plain-text, so they only provide security when used in combination with [TLS](/solutions/observability/apm/apm-agent-tls-communication.md).
::::

When defined, secret tokens are used to authorize requests to the APM Server. Both the {{apm-agent}} and APM Server must be configured with the same secret token for the request to be accepted.

To secure the communication between APM agents and the APM Server with a secret token:

1. Make sure [TLS](/solutions/observability/apm/apm-agent-tls-communication.md) is enabled
2. [Create a secret token](#apm-create-secret-token)
3. [Configure the secret token in your APM agents](#apm-configure-secret-token)

::::{note}
Secret tokens are not applicable for the RUM Agent, as there is no way to prevent them from being publicly exposed.
::::

## Create a secret token [apm-create-secret-token]

% This should be checked and updated, it doesn't looks like it's there by default vv

::::{note}
{{ech}} and {{ece}} deployments provision a secret token when the deployment is created. The secret token can be found and reset in the {{ecloud}} Console under the deployment's **APM & Fleet** page.
::::

:::::::{tab-set}

::::::{tab-item} Fleet-managed
Create or update a secret token in {{fleet}}.

Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Navigate to **Agent authorization** > **Secret token** and set the value of your token.
5. Click **Save integration**. The APM Server will restart before the change takes effect.
::::::

::::::{tab-item} APM Server binary
Set the secret token in `apm-server.yaml`:

```yaml
apm-server.auth.secret_token: <secret-token>
```
::::::

:::::::

## Configure the secret token in your APM agents [apm-configure-secret-token]

Each Elastic {{apm-agent}} has a configuration option to set the value of the secret token:

* **Android agent**: [`secretToken`](apm-agent-android://reference/edot-android/configuration.md)
* **Go agent**: [`ELASTIC_APM_SECRET_TOKEN`](apm-agent-go://reference/configuration.md#config-secret-token)
* **iOS agent**: [`secretToken`](apm-agent-ios://reference/edot-ios/configuration.md#secrettoken)
* **Java agent**: [`secret_token`](apm-agent-java://reference/config-reporter.md#config-secret-token)
* **.NET agent**: [`ELASTIC_APM_SECRET_TOKEN`](apm-agent-dotnet://reference/config-reporter.md#config-secret-token)
* **Node.js agent**: [`Secret Token`](apm-agent-nodejs://reference/configuration.md#secret-token)
* **PHP agent**: [`secret_token`](apm-agent-php://reference/configuration-reference.md#config-secret-token)
* **Python agent**: [`secret_token`](apm-agent-python://reference/configuration.md#config-secret-token)
* **Ruby agent**: [`secret_token`](apm-agent-ruby://reference/configuration.md#config-secret-token)

In addition to setting the secret token, ensure the configured server URL uses `HTTPS` instead of `HTTP`:

* **Go agent**: [`ELASTIC_APM_SERVER_URL`](apm-agent-go://reference/configuration.md#config-server-url)
* **Java agent**: [`server_urls`](apm-agent-java://reference/config-reporter.md#config-server-urls)
* **.NET agent**: [`ServerUrl`](apm-agent-dotnet://reference/config-reporter.md#config-server-url)
* **Node.js agent**: [`serverUrl`](apm-agent-nodejs://reference/configuration.md#server-url)
* **PHP agent**: [`server_url`](apm-agent-php://reference/configuration-reference.md#config-server-url)
* **Python agent**: [`server_url`](apm-agent-python://reference/index.md)
* **Ruby agent**: [`server_url`](apm-agent-ruby://reference/configuration.md#config-server-url)
