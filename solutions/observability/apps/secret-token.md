---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-secret-token.html
---

# Secret token [apm-secret-token]

::::{important}
Secret tokens are sent as plain-text, so they only provide security when used in combination with [TLS](apm-agent-tls-communication.md).
::::


When defined, secret tokens are used to authorize requests to the APM Server. Both the {{apm-agent}} and APM Server must be configured with the same secret token for the request to be accepted.

To secure the communication between APM agents and the APM Server with a secret token:

1. Make sure [TLS](apm-agent-tls-communication.md) is enabled
2. [Create a secret token](#apm-create-secret-token)
3. [Configure the secret token in your APM agents](#apm-configure-secret-token)

::::{note}
Secret tokens are not applicable for the RUM Agent, as there is no way to prevent them from being publicly exposed.
::::



## Create a secret token [apm-create-secret-token]

::::{note}
{{ech}} and {{ece}} deployments provision a secret token when the deployment is created. The secret token can be found and reset in the {{ecloud}} Console under **Deployments** — **APM & Fleet**.
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

* **Android agent**: [`secretToken`](asciidocalypse://docs/apm-agent-android/docs/reference/ingestion-tools/apm-agent-android/configuration.md)
* **Go agent**: [`ELASTIC_APM_SECRET_TOKEN`](asciidocalypse://docs/apm-agent-go/docs/reference/ingestion-tools/apm-agent-go/configuration.md#config-secret-token)
* **iOS agent**: [`secretToken`](asciidocalypse://docs/apm-agent-ios/docs/reference/ingestion-tools/apm-agent-swift/configuration.md#secretToken)
* **Java agent**: [`secret_token`](asciidocalypse://docs/apm-agent-java/docs/reference/ingestion-tools/apm-agent-java/config-reporter.md#config-secret-token)
* **.NET agent**: [`ELASTIC_APM_SECRET_TOKEN`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/ingestion-tools/apm-agent-dotnet/config-reporter.md#config-secret-token)
* **Node.js agent**: [`Secret Token`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/ingestion-tools/apm-agent-nodejs/configuration.md#secret-token)
* **PHP agent**: [`secret_token`](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/configuration-reference.md#config-secret-token)
* **Python agent**: [`secret_token`](asciidocalypse://docs/apm-agent-python/docs/reference/ingestion-tools/apm-agent-python/configuration.md#config-secret-token)
* **Ruby agent**: [`secret_token`](asciidocalypse://docs/apm-agent-ruby/docs/reference/ingestion-tools/apm-agent-ruby/configuration.md#config-secret-token)

In addition to setting the secret token, ensure the configured server URL uses `HTTPS` instead of `HTTP`:

* **Go agent**: [`ELASTIC_APM_SERVER_URL`](asciidocalypse://docs/apm-agent-go/docs/reference/ingestion-tools/apm-agent-go/configuration.md#config-server-url)
* **Java agent**: [`server_urls`](asciidocalypse://docs/apm-agent-java/docs/reference/ingestion-tools/apm-agent-java/config-reporter.md#config-server-urls)
* **.NET agent**: [`ServerUrl`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/ingestion-tools/apm-agent-dotnet/config-reporter.md#config-server-url)
* **Node.js agent**: [`serverUrl`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/ingestion-tools/apm-agent-nodejs/configuration.md#server-url)
* **PHP agent**: [`server_url`](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/configuration-reference.md#config-server-url)
* **Python agent**: [`server_url`](https://www.elastic.co/guide/en/apm/agent/python/current/)
* **Ruby agent**: [`server_url`](asciidocalypse://docs/apm-agent-ruby/docs/reference/ingestion-tools/apm-agent-ruby/configuration.md#config-server-url)
