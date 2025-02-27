---
navigation_title: "{{es}}"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-elasticsearch-output.html
applies_to:
  stack: all
---



# Configure the Elasticsearch output [apm-elasticsearch-output]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

This documentation only applies to APM Server binary users. Fleet-managed users should see [Configure the {{es}} output](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/elasticsearch-output.md).

::::


The {{es}} output sends events directly to {{es}} using the {{es}} HTTP API.

Example configuration:

```yaml
output.elasticsearch:
  hosts: ["https://myEShost:9200"] <1>
```

1. To enable SSL, add `https` to all URLs defined under *hosts*.


When sending data to a secured cluster through the `elasticsearch` output, APM Server can use any of the following authentication methods:

* Basic authentication credentials (username and password).
* Token-based (API key) authentication.
* Public Key Infrastructure (PKI) certificates.

**Basic authentication:**

```yaml
output.elasticsearch:
  hosts: ["https://myEShost:9200"]
  username: "apm_writer"
  password: "{pwd}"
```

**API key authentication:**

```yaml
output.elasticsearch:
  hosts: ["https://myEShost:9200"]
  api_key: "ZCV7VnwBgnX0T19fN8Qe:KnR6yE41RrSowb0kQ0HWoA" <1>
```

1.  You *must* set the API key to be configured to **Beats**. Base64 encoded API keys are not currently supported in this configuration. For details on how to create and configure a compatible API key, refer to [Create an API key for writing events](grant-access-using-api-keys.md#apm-beats-api-key-publish).


**PKI certificate authentication:**

```yaml
output.elasticsearch:
  hosts: ["https://myEShost:9200"]
  ssl.certificate: "/etc/pki/client/cert.pem"
  ssl.key: "/etc/pki/client/cert.key"
```

See [Secure communication with {{es}}](#apm-securing-communication-elasticsearch) for details on each authentication method.


## Compatibility [_compatibility]

This output works with all compatible versions of {{es}}. See the [Elastic Support Matrix](https://www.elastic.co/support/matrix#matrix_compatibility).


## Configuration options [_configuration_options_3]

You can specify the following options in the `elasticsearch` section of the `apm-server.yml` config file:


### `enabled` [_enabled_2]

The enabled config is a boolean setting to enable or disable the output. If set to `false`, the output is disabled.

The default value is `true`.


### `hosts` [apm-hosts-option]

The list of {{es}} nodes to connect to. The events are distributed to these nodes in round robin order. If one node becomes unreachable, the event is automatically sent to another node. Each {{es}} node can be defined as a `URL` or `IP:PORT`. For example: `http://192.15.3.2`, `https://es.found.io:9230` or `192.24.3.2:9300`. If no port is specified, `9200` is used.

::::{note}
When a node is defined as an `IP:PORT`, the *scheme* and *path* are taken from the [`protocol`](#apm-protocol-option) and [`path`](#apm-path-option) config options.
::::


```yaml
output.elasticsearch:
  hosts: ["10.45.3.2:9220", "10.45.3.1:9230"]
  protocol: https
  path: /elasticsearch
```

In the previous example, the {{es}} nodes are available at `https://10.45.3.2:9220/elasticsearch` and `https://10.45.3.1:9230/elasticsearch`.


### `compression_level` [_compression_level]

The gzip compression level. Setting this value to `0` disables compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).

Increasing the compression level will reduce the network usage but will increase the CPU usage.

The default value is `0`.


### `escape_html` [_escape_html]

Configure escaping of HTML in strings. Set to `true` to enable escaping.

The default value is `false`.


### `api_key` [_api_key_2]

Instead of using a username and password, you can use API keys to secure communication with {{es}}. The value must be the ID of the API key and the API key joined by a colon: `id:api_key`.

You *must* set the API key to be configured to **Beats**. Base64 encoded API keys are not currently supported in this configuration. For details on how to create and configure a compatible API key, refer to [Create an API key for writing events](grant-access-using-api-keys.md#apm-beats-api-key-publish).

:::{image} ../../../images/observability-apm-api-key-beats.png
:alt: API key dropdown highlighting the Beats option
:::


### `username` [_username]

The basic authentication username for connecting to {{es}}.

This user needs the privileges required to publish events to {{es}}. To create a user like this, see [Create a *writer* role](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-to-publish-events).


### `password` [_password]

The basic authentication password for connecting to {{es}}.


### `parameters` [_parameters]

Dictionary of HTTP parameters to pass within the URL with index operations.


### `protocol` [apm-protocol-option]

The name of the protocol {{es}} is reachable on. The options are: `http` or `https`. The default is `http`. However, if you specify a URL for [`hosts`](#apm-hosts-option), the value of `protocol` is overridden by whatever scheme you specify in the URL.


### `path` [apm-path-option]

An HTTP path prefix that is prepended to the HTTP API calls. This is useful for the cases where {{es}} listens behind an HTTP reverse proxy that exports the API under a custom prefix.


### `headers` [_headers]

Custom HTTP headers to add to each request created by the {{es}} output. Example:

```yaml
output.elasticsearch.headers:
  X-My-Header: Header contents
```

It is possible to specify multiple header values for the same header name by separating them with a comma.


### `proxy_url` [_proxy_url]

The URL of the proxy to use when connecting to the {{es}} servers. The value may be either a complete URL or a "host[:port]", in which case the "http" scheme is assumed. If a value is not specified through the configuration file then proxy environment variables are used. See the [Go documentation](https://golang.org/pkg/net/http/#ProxyFromEnvironment) for more information about the environment variables.


### `max_retries` [_max_retries]

The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.

Set `max_retries` to a value less than 0 to retry until all events are published.

The default is 3.


### `flush_bytes` [_flush_bytes]

The bulk request size threshold, in bytes, before flushing to {{es}}. The value must have a suffix, e.g. `"2MB"`. The default is `1MB`.


### `flush_interval` [_flush_interval]

The maximum duration to accumulate events for a bulk request before being flushed to {{es}}. The value must have a duration suffix, e.g. `"5s"`. The default is `1s`.


### `backoff.init` [_backoff_init]

The number of seconds to wait before trying to reconnect to {{es}} after a network error. After waiting `backoff.init` seconds, APM Server tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset. The default is `1s`.


### `backoff.max` [_backoff_max]

The maximum number of seconds to wait before attempting to connect to {{es}} after a network error. The default is `60s`.


### `timeout` [_timeout]

The HTTP request timeout in seconds for the {{es}} request. The default is 90.


### `ssl` [_ssl]

Configuration options for SSL parameters like the certificate authority to use for HTTPS-based connections. If the `ssl` section is missing, the host CAs are used for HTTPS connections to {{es}}.

See the [secure communication with {{es}}](#apm-securing-communication-elasticsearch) guide or [SSL configuration reference](ssltls-output-settings.md) for more information.


## Secure communication with {{es}} [apm-securing-communication-elasticsearch]

When sending data to a secured cluster through the `elasticsearch` output, APM Server can use any of the following authentication methods:

* Basic authentication credentials (username and password).
* Token-based API authentication.
* A client certificate.

Authentication is specified in the APM Server configuration file:

* To use **basic authentication**, specify the `username` and `password` settings under `output.elasticsearch`. For example:

    ```yaml
    output.elasticsearch:
      hosts: ["https://myEShost:9200"]
      username: "apm_writer" <1>
      password: "{pwd}"
    ```

    1. This user needs the privileges required to publish events to {{es}}. To create a user like this, see [Create a *writer* role](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-to-publish-events).

* To use token-based **API key authentication**, specify the `api_key` under `output.elasticsearch`. For example:

    ```yaml
    output.elasticsearch:
      hosts: ["https://myEShost:9200"]
      api_key: "KnR6yE41RrSowb0kQ0HWoA" <1>
    ```

    1. This API key must have the privileges required to publish events to {{es}}. You *must* set the API key to be configured to **Beats**. Base64 encoded API keys are not currently supported in this configuration. For details on how to create and configure a compatible API key, refer to [Create an API key for writing events](grant-access-using-api-keys.md#apm-beats-api-key-publish).


* To use **Public Key Infrastructure (PKI) certificates** to authenticate users, specify the `certificate` and `key` settings under `output.elasticsearch`. For example:

    ```yaml
    output.elasticsearch:
      hosts: ["https://myEShost:9200"]
      ssl.certificate: "/etc/pki/client/cert.pem" <1>
      ssl.key: "/etc/pki/client/cert.key" <2>
    ```

    1. The path to the certificate for SSL client authentication
    2. The client certificate key


    These settings assume that the distinguished name (DN) in the certificate is mapped to the appropriate roles in the `role_mapping.yml` file on each node in the {{es}} cluster. For more information, see [Using role mapping files](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file).

    By default, APM Server uses the list of trusted certificate authorities (CA) from the operating system where APM Server is running. If the certificate authority that signed your node certificates is not in the host system’s trusted certificate authorities list, you need to add the path to the `.pem` file that contains your CA’s certificate to the APM Server configuration. This will configure APM Server to use a specific list of CA certificates instead of the default list from the OS.

    Here is an example configuration:

    ```yaml
    output.elasticsearch:
      hosts: ["https://myEShost:9200"]
      ssl.certificate_authorities: <1>
        - /etc/pki/my_root_ca.pem
        - /etc/pki/my_other_ca.pem
      ssl.certificate: "/etc/pki/client.pem" <2>
      ssl.key: "/etc/pki/key.pem" <3>
    ```

    1. Specify the path to the local `.pem` file that contains your Certificate Authority’s certificate. This is needed if you use your own CA to sign your node certificates.
    2. The path to the certificate for SSL client authentication
    3. The client certificate key


    ::::{note}
    For any given connection, the SSL/TLS certificates must have a subject that matches the value specified for `hosts`, or the SSL handshake fails. For example, if you specify `hosts: ["foobar:9200"]`, the certificate MUST include `foobar` in the subject (`CN=foobar`) or as a subject alternative name (SAN). Make sure the hostname resolves to the correct IP address. If no DNS is available, then you can associate the IP address with your hostname in `/etc/hosts` (on Unix) or `C:\Windows\System32\drivers\etc\hosts` (on Windows).
    ::::




### Learn more about secure communication [apm-securing-communication-learn-more]

More information on sending data to a secured cluster is available in the configuration reference:

* [SSL/TLS output settings](ssltls-output-settings.md)
