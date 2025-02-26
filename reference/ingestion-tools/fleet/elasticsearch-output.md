---
navigation_title: "{{es}}"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elasticsearch-output.html
---

# Configure the {{es}} output [elasticsearch-output]


The {{es}} output sends events directly to {{es}} by using the {{es}} HTTP API.

**Compatibility:** This output works with all compatible versions of {{es}}. See the [Elastic Support Matrix](https://www.elastic.co/support/matrix#matrix_compatibility).

This example configures an {{es}} output called `default` in the `elastic-agent.yml` file:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: [127.0.0.1:9200]
    username: elastic
    password: changeme
```

This example is similar to the previous one, except that it uses the recommended [token-based (API key) authentication](#output-elasticsearch-apikey-authentication-settings):

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: [127.0.0.1:9200]
    api_key: "my_api_key"
```

::::{note}
Token-based authentication is required in an [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment.
::::


## {{es}} output configuration settings [_es_output_configuration_settings]

The `elasticsearch` output type supports the following settings, grouped by category. Many of these settings have sensible defaults that allow you to run {{agent}} with minimal configuration.

* [Commonly used settings](#output-elasticsearch-commonly-used-settings)
* [Authentication settings](#output-elasticsearch-authentication-settings)
* [Compatibility setting](#output-elasticsearch-compatibility-setting)
* [Data parsing, filtering, and manipulation settings](#output-elasticsearch-data-parsing-settings)
* [HTTP settings](#output-elasticsearch-http-settings)
* [Memory queue settings](#output-elasticsearch-memory-queue-settings)
* [Performance tuning settings](#output-elasticsearch-performance-tuning-settings)


## Commonly used settings [output-elasticsearch-commonly-used-settings]

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-enabled-setting$$$<br>`enabled`<br> | (boolean) Enables or disables the output. If set to `false`, the output is disabled.<br><br>**Default:** `true`<br> |
| $$$output-elasticsearch-hosts-setting$$$<br>`hosts`<br> | (list) The list of {{es}} nodes to connect to. The events are distributed to these nodes in round robin order. If one node becomes unreachable, the event is automatically sent to another node. Each {{es}} node can be defined as a `URL` or `IP:PORT`. For example: `http://192.15.3.2`, `https://es.found.io:9230` or `192.24.3.2:9300`. If no port is specified, `9200` is used.<br><br>::::{note} <br>When a node is defined as an `IP:PORT`, the *scheme* and *path* are taken from the `protocol` and `path` settings.<br>::::<br><br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearch<br>    hosts: ["10.45.3.2:9220", "10.45.3.1:9230"] <1><br>    protocol: https<br>    path: /elasticsearch<br>```<br><br>1. In this example, the {{es}} nodes are available at `https://10.45.3.2:9220/elasticsearch` and `https://10.45.3.1:9230/elasticsearch`.<br><br><br>Note that Elasticsearch Nodes in the [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment are exposed on port 443.<br> |
| $$$output-elasticsearch-protocol-setting$$$<br>`protocol`<br> | (string) The name of the protocol {{es}} is reachable on. The options are: `http` or `https`. The default is `http`. However, if you specify a URL for `hosts`, the value of `protocol` is overridden by whatever scheme you specify in the URL.<br> |
| $$$output-elasticsearch-proxy_disable-setting$$$<br>`proxy_disable`<br> | (boolean) If set to `true`, all proxy settings, including `HTTP_PROXY` and `HTTPS_PROXY` variables, are ignored.<br><br>**Default:** `false`<br> |
| $$$output-elasticsearch-proxy_headers-setting$$$<br>`proxy_headers`<br> | (string) Additional headers to send to proxies during CONNECT requests.<br> |
| $$$output-elasticsearch-proxy_url-setting$$$<br>`proxy_url`<br> | (string) The URL of the proxy to use when connecting to the {{es}} servers. The value may be either a complete URL or a `host[:port]`, in which case the `http` scheme is assumed. If a value is not specified through the configuration file then proxy environment variables are used. See the [Go documentation](https://golang.org/pkg/net/http/#ProxyFromEnvironment) for more information about the environment variables.<br> |


## Authentication settings [output-elasticsearch-authentication-settings]

When sending data to a secured cluster through the `elasticsearch` output, {{agent}} can use any of the following authentication methods:

* [Basic authentication credentials](#output-elasticsearch-basic-authentication-settings)
* [Token-based (API key) authentication](#output-elasticsearch-apikey-authentication-settings)
* [Public Key Infrastructure (PKI) certificates](#output-elasticsearch-pki-certs-authentication-settings)
* [Kerberos](#output-elasticsearch-kerberos-authentication-settings)

### Basic authentication credentials [output-elasticsearch-basic-authentication-settings]

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["https://myEShost:9200"]
    username: "your-username"
    password: "your-password"
```

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-password-setting$$$<br>`password`<br> | (string) The basic authentication password for connecting to {{es}}.<br> |
| $$$output-elasticsearch-username-setting$$$<br>`username`<br> | (string) The basic authentication username for connecting to {{es}}.<br><br>This user needs the privileges required to publish events to {{es}}.<br><br>Note that in an [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment you need to use [token-based (API key) authentication](#output-elasticsearch-apikey-authentication-settings).<br> |


### Token-based (API key) authentication [output-elasticsearch-apikey-authentication-settings]

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["https://myEShost:9200"]
    api_key: "KnR6yE41RrSowb0kQ0HWoA"
```

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-api_key-setting$$$<br>`api_key`<br> | (string) Instead of using a username and password, you can use [API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md) to secure communication with {{es}}. The value must be the ID of the API key and the API key joined by a colon: `id:api_key`. Token-based authentication is required in an [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment.<br> |


### Public Key Infrastructure (PKI) certificates [output-elasticsearch-pki-certs-authentication-settings]

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["https://myEShost:9200"]
    ssl.certificate: "/etc/pki/client/cert.pem"
    ssl.key: "/etc/pki/client/cert.key"
```

For a list of available settings, refer to [SSL/TLS](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md), specifically the settings under [Table 7, Common configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#client-ssl-options).


### Kerberos [output-elasticsearch-kerberos-authentication-settings]

The following encryption types are supported:

* aes128-cts-hmac-sha1-96
* aes128-cts-hmac-sha256-128
* aes256-cts-hmac-sha1-96
* aes256-cts-hmac-sha384-192
* des3-cbc-sha1-kd
* rc4-hmac

Example output config with Kerberos password-based authentication:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["http://my-elasticsearch.elastic.co:9200"]
    kerberos.auth_type: password
    kerberos.username: "elastic"
    kerberos.password: "changeme"
    kerberos.config_path: "/etc/krb5.conf"
    kerberos.realm: "ELASTIC.CO"
```

The service principal name for the {{es}} instance is constructed from these options. Based on this configuration, the name would be:

`HTTP/my-elasticsearch.elastic.co@ELASTIC.CO`

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-kerberos.auth_type-setting$$$<br>`kerberos.auth_type`<br> | (string) The type of authentication to use with Kerberos KDC:<br><br>`password`<br>:   When specified, also set `kerberos.username` and `kerberos.password`.<br><br>`keytab`<br>:   When specified, also set `kerberos.username` and `kerberos.keytab`. The keytab must contain the keys of the selected principal, or authentication fails.<br><br>**Default:** `password`<br> |
| $$$output-elasticsearch-kerberos.config_path$$$<br>`kerberos.config_path`<br> | (string) Path to the `krb5.conf`. {{agent}} uses this setting to find the Kerberos KDC to retrieve a ticket.<br> |
| $$$output-elasticsearch-kerberos.enabled-setting$$$<br>`kerberos.enabled`<br> | (boolean) Enables or disables the Kerberos configuration.<br><br>::::{note} <br>Kerberos settings are disabled if either `enabled` is set to `false` or the `kerberos` section is missing.<br>::::<br><br> |
| $$$output-elasticsearch-kerberos.enable_krb5_fast$$$<br>`kerberos.enable_krb5_fast`<br> | (boolean) If `true`, enables Kerberos FAST authentication. This may conflict with some Active Directory installations.<br><br>**Default:** `false`<br> |
| $$$output-elasticsearch-kerberos.keytab$$$<br>`kerberos.keytab`<br> | (string) If `kerberos.auth_type` is `keytab`, provide the path to the keytab of the selected principal.<br> |
| $$$output-elasticsearch-kerberos.password$$$<br>`kerberos.password`<br> | (string) If `kerberos.auth_type` is `password`, provide a password for the selected principal.<br> |
| $$$output-elasticsearch-kerberos.realm$$$<br>`kerberos.realm`<br> | (string) Name of the realm where the output resides.<br> |
| $$$output-elasticsearch-kerberos.username$$$<br>`kerberos.username`<br> | (string) Name of the principal used to connect to the output.<br> |


### Compatibility setting [output-elasticsearch-compatibility-setting]

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-allow_older_versions-setting$$$<br>`allow_older_versions`<br> | Allow {{agent}} to connect and send output to an {{es}} instance that is running an earlier version than the agent version.<br><br>Note that this setting does not affect {{agent}}'s ability to connect to {{fleet-server}}. {{fleet-server}} will not accept a connection from an agent at a later major or minor version. It will accept a connection from an agent at a later patch version. For example, an {{agent}} at version 8.14.3 can connect to a {{fleet-server}} on version 8.14.0, but an agent at version 8.15.0 or later is not able to connect.<br><br>**Default:** `true`<br> |


### Data parsing, filtering, and manipulation settings [output-elasticsearch-data-parsing-settings]

Settings used to parse, filter, and transform data.

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-escape_html-setting$$$<br>`escape_html`<br> | (boolean) Configures escaping of HTML in strings. Set to `true` to enable escaping.<br><br>**Default:** `false`<br> |
| $$$output-elasticsearch-pipeline-setting$$$<br>`pipeline`<br> | (string) A format string value that specifies the [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) to write events to.<br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearchoutput.elasticsearch:<br>    hosts: ["http://localhost:9200"]<br>    pipeline: my_pipeline_id<br>```<br><br>You can set the ingest pipeline dynamically by using a format string to access any event field. For example, this configuration uses a custom field, `fields.log_type`, to set the pipeline for each event:<br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearch  hosts: ["http://localhost:9200"]<br>    pipeline: "%{[fields.log_type]}_pipeline"<br>```<br><br>With this configuration, all events with `log_type: normal` are sent to a pipeline named `normal_pipeline`, and all events with `log_type: critical` are sent to a pipeline named `critical_pipeline`.<br><br>::::{tip} <br>To learn how to add custom fields to events, see the `fields` option.<br>::::<br><br><br>See the `pipelines` setting for other ways to set the ingest pipeline dynamically.<br> |
| $$$output-elasticsearch-pipelines-setting$$$<br>`pipelines`<br> | An array of pipeline selector rules. Each rule specifies the [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) to use for events that match the rule. During publishing, {{agent}} uses the first matching rule in the array. Rules can contain conditionals, format string-based fields, and name mappings. If the `pipelines` setting is missing or no rule matches, the `pipeline` setting is used.<br><br>Rule settings:<br><br>**`pipeline`**<br>:   The pipeline format string to use. If this string contains field references, such as `%{[fields.name]}`, the fields must exist, or the rule fails.<br><br>**`mappings`**<br>:   A dictionary that takes the value returned by `pipeline` and maps it to a new name.<br><br>**`default`**<br>:   The default string value to use if `mappings` does not find a match.<br><br>**`when`**<br>:   A condition that must succeed in order to execute the current rule.<br><br>All the conditions supported by processors are also supported here.<br><br>The following example sends events to a specific pipeline based on whether the `message` field contains the specified string:<br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearch  hosts: ["http://localhost:9200"]<br>    pipelines:<br>      - pipeline: "warning_pipeline"<br>        when.contains:<br>          message: "WARN"<br>      - pipeline: "error_pipeline"<br>        when.contains:<br>          message: "ERR"<br>```<br><br>The following example sets the pipeline by taking the name returned by the `pipeline` format string and mapping it to a new name that’s used for the pipeline:<br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearch<br>    hosts: ["http://localhost:9200"]<br>    pipelines:<br>      - pipeline: "%{[fields.log_type]}"<br>        mappings:<br>          critical: "sev1_pipeline"<br>          normal: "sev2_pipeline"<br>        default: "sev3_pipeline"<br>```<br><br>With this configuration, all events with `log_type: critical` are sent to `sev1_pipeline`, all events with `log_type: normal` are sent to a `sev2_pipeline`, and all other events are sent to `sev3_pipeline`.<br> |



## HTTP settings [output-elasticsearch-http-settings]

Settings that modify the HTTP requests sent to {{es}}.

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-headers-setting$$$<br>`headers`<br> | Custom HTTP headers to add to each request created by the {{es}} output.<br><br>Example:<br><br>```yaml<br>outputs:<br>  default:<br>    type: elasticsearch<br>    headers:<br>      X-My-Header: Header contents<br>```<br><br>Specify multiple header values for the same header name by separating them with a comma.<br> |
| $$$output-elasticsearch-parameters-setting$$$<br>`parameters`<br> | Dictionary of HTTP parameters to pass within the URL with index operations.<br> |
| $$$output-elasticsearch-path-setting$$$<br>`path`<br> | (string) An HTTP path prefix that is prepended to the HTTP API calls. This is useful for the cases where {{es}} listens behind an HTTP reverse proxy that exports the API under a custom prefix.<br> |


## Memory queue settings [output-elasticsearch-memory-queue-settings]

The memory queue keeps all events in memory.

The memory queue waits for the output to acknowledge or drop events. If the queue is full, no new events can be inserted into the memory queue. Only after the signal from the output will the queue free up space for more events to be accepted.

The memory queue is controlled by the parameters `flush.min_events` and `flush.timeout`. `flush.min_events` gives a limit on the number of events that can be included in a single batch, and `flush.timeout` specifies how long the queue should wait to completely fill an event request. If the output supports a `bulk_max_size` parameter, the maximum batch size will be the smaller of `bulk_max_size` and `flush.min_events`.

`flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`.

In synchronous mode, an event request is always filled as soon as events are available, even if there are not enough events to fill the requested batch. This is useful when latency must be minimized. To use synchronous mode, set `flush.timeout` to 0.

For backwards compatibility, synchronous mode can also be activated by setting `flush.min_events` to 0 or 1. In this case, batch size will be capped at 1/2 the queue capacity.

In asynchronous mode, an event request will wait up to the specified timeout to try and fill the requested batch completely. If the timeout expires, the queue returns a partial batch with all available events. To use asynchronous mode, set `flush.timeout` to a positive duration, for example 5s.

This sample configuration forwards events to the output when there are enough events to fill the output’s request (usually controlled by `bulk_max_size`, and limited to at most 512 events by `flush.min_events`), or when events have been waiting for

```yaml
  queue.mem.events: 4096
  queue.mem.flush.min_events: 512
  queue.mem.flush.timeout: 5s
```

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-queue.mem.events-setting$$$<br>`queue.mem.events`<br> | The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.<br><br>**Default:** `3200 events`<br> |
| $$$output-elasticsearch-queue.mem.flush.min_events-setting$$$<br>`queue.mem.flush.min_events`<br> | `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`<br><br>**Default:** `1600 events`<br> |
| $$$output-elasticsearch-queue.mem.flush.timeout-setting$$$<br>`queue.mem.flush.timeout`<br> | (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.<br><br>**Default:** `10s`<br> |


## Performance tuning settings [output-elasticsearch-performance-tuning-settings]

Settings that may affect performance when sending data through the {{es}} output.

Use the `preset` option to automatically configure the group of performance tuning settings to optimize for `throughput`, `scale`, `latency`, or you can select a `balanced` set of performance specifications.

The performance tuning `preset` values take precedence over any settings that may be defined separately. If you want to change any setting, set `preset` to `custom` and specify the performance tuning settings individually.

| Setting | Description |
| --- | --- |
| $$$output-elasticsearch-backoff.init-setting$$$<br>`backoff.init`<br> | (string) The number of seconds to wait before trying to reconnect to {{es}} after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.<br><br>**Default:** `1s`<br> |
| $$$output-elasticsearch-backoff.max-setting$$$<br>`backoff.max`<br> | (string) The maximum number of seconds to wait before attempting to connect to {{es}} after a network error.<br><br>**Default:** `60s`<br> |
| $$$output-elasticsearch-bulk_max_size-setting$$$<br>`bulk_max_size`<br> | (int) The maximum number of events to bulk in a single {{es}} bulk API index request.<br><br>Events can be collected into batches. {{agent}} will split batches larger than `bulk_max_size` into multiple batches.<br><br>Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.<br><br>Setting `bulk_max_size` to values less than or equal to 0 turns off the splitting of batches. When splitting is disabled, the queue decides on the number of events to be contained in a batch.<br><br>**Default:** `1600`<br> |
| $$$output-elasticsearch-compression_level-setting$$$<br>`compression_level`<br> | (int) The gzip compression level. Set this value to `0` to disable compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).<br><br>Increasing the compression level reduces network usage but increases CPU usage.<br><br>**Default:** `1`<br> |
| $$$output-elasticsearch-max_retries-setting$$$<br>`max_retries`<br> | (int) The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.<br><br>Set `max_retries` to a value less than 0 to retry until all events are published.<br><br>**Default:** `3`<br> |
| $$$output-elasticsearch-preset-setting$$$<br>`preset`<br> | Configures the full group of [performance tuning settings](#output-elasticsearch-performance-tuning-settings) to optimize your {{agent}} performance when sending data to an {{es}} output.<br><br>Refer to [Performance tuning settings](/reference/ingestion-tools/fleet/es-output-settings.md#es-output-settings-performance-tuning-settings) for a table showing the group of values associated with any preset, and another table showing EPS (events per second) results from testing the different preset options.<br><br>Performance tuning preset settings:<br><br>**`balanced`**<br>:   Configure the default tuning setting values for "out-of-the-box" performance.<br><br>**`throughput`**<br>:   Optimize the {{es}} output for throughput.<br><br>**`scale`**<br>:   Optimize the {{es}} output for scale.<br><br>**`latency`**<br>:   Optimize the {{es}} output to reduce latence.<br><br>**`custom`**<br>:   Use the `custom` option to fine-tune the performance tuning settings individually.<br><br>**Default:** `balanced`<br> |
| $$$output-elasticsearch-timeout-setting$$$<br>`timeout`<br> | (string) The HTTP request timeout in seconds for the {{es}} request.<br><br>**Default:** `90s`<br> |
| $$$output-elasticsearch-worker-setting$$$<br>`worker`<br> | (int) The number of workers per configured host publishing events. Example: If you have two hosts and three workers, in total six workers are started (three for each host).<br><br>**Default:** `1`<br> |


