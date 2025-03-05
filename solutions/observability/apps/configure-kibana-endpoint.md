---
navigation_title: "{{kib}} endpoint"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-setup-kibana-endpoint.html
applies_to:
  stack: all
---



# Configure the Kibana endpoint [apm-setup-kibana-endpoint]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

You must configure the {{kib}} endpoint when running the APM Server binary with a non-{{es}} output. Configuring the {{kib}} endpoint allows the APM Server to communicate with {{kib}} and ensure that the APM integration was properly set up. It is also required for APM agent configuration when using an output other than {{es}}.

For all other use-cases, starting in version 8.7.0, APM agent configurations is fetched directly from {{es}}. Configuring and enabling the {{kib}} endpoint is only used as a fallback. Please see [APM agent central configuration](configure-apm-agent-central-configuration.md) instead.

::::


Here’s a sample configuration:

```yaml
apm-server.kibana.enabled: true
apm-server.kibana.host: "http://localhost:5601"
```


## {{kib}} endpoint configuration options [_kib_endpoint_configuration_options]

You can specify the following options in the `apm-server.kibana` section of the `apm-server.yml` config file. These options are not required for a Fleet-managed APM Server.


### `apm-server.kibana.enabled` [apm-kibana-enabled]

Defaults to `false`. Must be `true` to use APM Agent configuration.


### `apm-server.kibana.host` [apm-kibana-host]

The {{kib}} host that APM Server will communicate with. The default is `127.0.0.1:5601`. The value of `host` can be a `URL` or `IP:PORT`. For example: `http://192.15.3.2`, `192:15.3.2:5601` or `http://192.15.3.2:6701/path`. If no port is specified, `5601` is used.

::::{note}
When a node is defined as an `IP:PORT`, the *scheme* and *path* are taken from the [apm-server.kibana.protocol](#apm-kibana-protocol-option) and [apm-server.kibana.path](#apm-kibana-path-option) config options.
::::


IPv6 addresses must be defined using the following format: `https://[2001:db8::1]:5601`.


### `apm-server.kibana.protocol` [apm-kibana-protocol-option]

The name of the protocol {{kib}} is reachable on. The options are: `http` or `https`. The default is `http`. However, if you specify a URL for host, the value of `protocol` is overridden by whatever scheme you specify in the URL.

Example config:

```yaml
apm-server.kibana.host: "192.0.2.255:5601"
apm-server.kibana.protocol: "http"
apm-server.kibana.path: /kibana
```


### `apm-server.kibana.username` [_apm_server_kibana_username]

The basic authentication username for connecting to {{kib}}.


### `apm-server.kibana.password` [_apm_server_kibana_password]

The basic authentication password for connecting to {{kib}}.


### `apm-server.kibana.api_key` [_apm_server_kibana_api_key]

Authentication with an API key. Formatted as `id:api_key`


### `apm-server.kibana.path` [apm-kibana-path-option]

An HTTP path prefix that is prepended to the HTTP API calls. This is useful for the cases where {{kib}} listens behind an HTTP reverse proxy that exports the API under a custom prefix.


### `apm-server.kibana.ssl.enabled` [_apm_server_kibana_ssl_enabled]

Enables APM Server to use SSL settings when connecting to {{kib}} via HTTPS. If you configure APM Server to connect over HTTPS, this setting defaults to `true` and APM Server uses the default SSL settings.

Example configuration:

```yaml
apm-server.kibana.host: "https://192.0.2.255:5601"
apm-server.kibana.ssl.enabled: true
apm-server.kibana.ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
apm-server.kibana.ssl.certificate: "/etc/pki/client/cert.pem"
apm-server.kibana.ssl.key: "/etc/pki/client/cert.key"
```

For information on the additional SSL configuration options, see [SSL/TLS output settings](ssltls-output-settings.md).

