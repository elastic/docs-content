---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-auth.html
applies_to:
  stack: all
---

# APM agent authorization [apm-agent-auth]

::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

Most options in this section are supported by all APM Server deployment methods.

::::


Agent authorization APM Server configuration options.

:::::::{tab-set}

::::::{tab-item} APM Server binary
**Example config file:**

```yaml
apm-server:
  host: "localhost:8200"
  rum:
    enabled: true

output:
  elasticsearch:
    hosts: ElasticsearchAddress:9200

max_procs: 4
```
::::::

::::::{tab-item} Fleet-managed
Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Look for these settings under **Agent authorization**.
::::::

:::::::

## API key authentication options [apm-api-key-auth-settings]

These settings apply to API key communication between the APM Server and APM Agents.

::::{note}
These settings are different from the API key settings used for {{es}} output and monitoring.
::::



### API key for agent authentication [_api_key_for_agent_authentication]

Enable API key authorization by setting `enabled` to `true`. By default, `enabled` is set to `false`, and API key support is disabled. (bool)

|     |     |
| --- | --- |
| APM Server binary | `auth.api_key.enabled` |
| Fleet-managed | `API key for agent authentication` |

::::{tip}
Not using Elastic APM agents? When enabled, third-party APM agents must include a valid API key in the following format: `Authorization: ApiKey <token>`. The key must be the base64 encoded representation of the API key’s `id:name`.
::::



### API key limit [_api_key_limit]

Each unique API key triggers one request to {{es}}. This setting restricts the number of unique API keys are allowed per minute. The minimum value for this setting should be the number of API keys configured in your monitored services. The default `limit` is `100`. (int)

|     |     |
| --- | --- |
| APM Server binary | `auth.api_key.limit` |
| Fleet-managed | `Number of keys` |


### Secret token [_secret_token]

Authorization token for sending APM data. The same token must also be set in each {{apm-agent}}. This token is not used for RUM endpoints. (text)

|     |     |
| --- | --- |
| APM Server binary | `auth.api_key.token` |
| Fleet-managed | `Secret token` |


## `auth.api_key.elasticsearch.*` configuration options [_auth_api_key_elasticsearch_configuration_options]

::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

The below options are only supported by the APM Server binary.

All of the `auth.api_key.elasticsearch.*` configurations are optional. If none are set, configuration settings from the `apm-server.output` section will be reused.

::::



### `elasticsearch.hosts` [_elasticsearch_hosts]

API keys are fetched from {{es}}. This configuration needs to point to a secured {{es}} cluster that is able to serve API key requests.


### `elasticsearch.protocol` [_elasticsearch_protocol]

The name of the protocol {{es}} is reachable on. The options are: `http` or `https`. The default is `http`. If nothing is configured, configuration settings from the `output` section will be reused.


### `elasticsearch.path` [_elasticsearch_path]

An optional HTTP path prefix that is prepended to the HTTP API calls. If nothing is configured, configuration settings from the `output` section will be reused.


### `elasticsearch.proxy_url` [_elasticsearch_proxy_url]

The URL of the proxy to use when connecting to the {{es}} servers. The value may be either a complete URL or a "host[:port]", in which case the "http"scheme is assumed. If nothing is configured, configuration settings from the `output` section will be reused.


### `elasticsearch.timeout` [_elasticsearch_timeout]

The HTTP request timeout in seconds for the {{es}} request. If nothing is configured, configuration settings from the `output` section will be reused.


## `auth.api_key.elasticsearch.ssl.*` configuration options [_auth_api_key_elasticsearch_ssl_configuration_options]

SSL is off by default. Set `elasticsearch.protocol` to `https` if you want to enable `https`.


### `elasticsearch.ssl.enabled` [_elasticsearch_ssl_enabled]

Enable custom SSL settings. Set to false to ignore custom SSL settings for secure communication.


### `elasticsearch.ssl.verification_mode` [_elasticsearch_ssl_verification_mode]

Configure SSL verification mode. If `none` is configured, all server hosts and certificates will be accepted. In this mode, SSL based connections are susceptible to man-in-the-middle attacks. **Use only for testing**. Default is `full`.


### `elasticsearch.ssl.supported_protocols` [_elasticsearch_ssl_supported_protocols]

List of supported/valid TLS versions. By default, all TLS versions from 1.0 to 1.2 are enabled.


### `elasticsearch.ssl.certificate_authorities` [_elasticsearch_ssl_certificate_authorities]

List of root certificates for HTTPS server verifications.


### `elasticsearch.ssl.certificate` [_elasticsearch_ssl_certificate]

The path to the certificate for SSL client authentication.


### `elasticsearch.ssl.key` [_elasticsearch_ssl_key]

The client certificate key used for client authentication. This option is required if certificate is specified.


### `elasticsearch.ssl.key_passphrase` [_elasticsearch_ssl_key_passphrase]

An optional passphrase used to decrypt an encrypted key stored in the configured key file.


### `elasticsearch.ssl.cipher_suites` [_elasticsearch_ssl_cipher_suites]

The list of cipher suites to use. The first entry has the highest priority. If this option is omitted, the Go crypto library’s default suites are used (recommended).


### `elasticsearch.ssl.curve_types` [_elasticsearch_ssl_curve_types]

The list of curve types for ECDHE (Elliptic Curve Diffie-Hellman ephemeral key exchange).


### `elasticsearch.ssl.renegotiation` [_elasticsearch_ssl_renegotiation]

Configure what types of renegotiation are supported. Valid options are `never`, `once`, and `freely`. Default is `never`.

* `never` - Disables renegotiation.
* `once` - Allows a remote server to request renegotiation once per connection.
* `freely` - Allows a remote server to repeatedly request renegotiation.
