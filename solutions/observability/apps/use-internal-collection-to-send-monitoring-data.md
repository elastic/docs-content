---
navigation_title: "Use internal collection"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-monitoring-internal-collection.html
applies_to:
  stack: all
---

# Use internal collection to send monitoring data [apm-monitoring-internal-collection]


Use internal collectors to send {{beats}} monitoring data directly to your monitoring cluster. Or as an alternative to internal collection, use [Use {{metricbeat}} collection](use-metricbeat-to-send-monitoring-data.md). The benefit of using internal collection instead of {{metricbeat}} is that you have fewer pieces of software to install and maintain.

1. Create an API key or user that has appropriate authority to send system-level monitoring data to {{es}}. For example, you can use the built-in `apm_system` user or assign the built-in `apm_system` role to another user. For more information on the required privileges, see [Create a *monitoring* role](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-to-publish-monitoring). For more information on how to use API keys, see [Grant access using API keys](grant-access-using-api-keys.md).
2. Add the `monitoring` settings in the APM Server configuration file. If you configured the {{es}} output and want to send APM Server monitoring events to the same {{es}} cluster, specify the following minimal configuration:

    ```yaml
    monitoring:
      enabled: true
      elasticsearch:
        api_key:  id:api_key <1>
        username: apm_system
        password: somepassword
    ```

    1. Specify one of `api_key` or `username`/`password`.


    If you want to send monitoring events to an [{{ecloud}}](https://cloud.elastic.co/) monitoring cluster, you can use two simpler settings. When defined, these settings overwrite settings from other parts in the configuration. For example:

    ```yaml
    monitoring:
      enabled: true
      cloud.id: 'staging:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyRjZWM2ZjI2MWE3NGJmMjRjZTMzYmI4ODExYjg0Mjk0ZiRjNmMyY2E2ZDA0MjI0OWFmMGNjN2Q3YTllOTYyNTc0Mw=='
      cloud.auth: 'elastic:{pwd}'
    ```

    If you configured a different output, such as {{ls}} or you want to send APM Server monitoring events to a separate {{es}} cluster (referred to as the *monitoring cluster*), you must specify additional configuration options. For example:

    ```yaml
    monitoring:
      enabled: true
      cluster_uuid: PRODUCTION_ES_CLUSTER_UUID <1>
      elasticsearch:
        hosts: ["https://example.com:9200", "https://example2.com:9200"] <2>
        api_key:  id:api_key <3>
        username: apm_system
        password: somepassword
    ```

    1. This setting identifies the {{es}} cluster under which the monitoring data for this APM Server instance will appear in the {{stack-monitor-app}} UI. To get a cluster’s `cluster_uuid`, call the `GET /` API against that cluster.
    2. This setting identifies the hosts and port numbers of {{es}} nodes that are part of the monitoring cluster.
    3. Specify one of `api_key` or `username`/`password`.


    If you want to use PKI authentication to send monitoring events to {{es}}, you must specify a different set of configuration options. For example:

    ```yaml
    monitoring:
      enabled: true
      cluster_uuid: PRODUCTION_ES_CLUSTER_UUID
      elasticsearch:
        hosts: ["https://example.com:9200", "https://example2.com:9200"]
        username: ""
        ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
        ssl.certificate: "/etc/pki/client/cert.pem"
        ssl.key: "/etc/pki/client/cert.key"
    ```

    You must specify the `username` as `""` explicitly so that the username from the client certificate (`CN`) is used. See [SSL/TLS output settings](ssltls-output-settings.md) for more information about SSL settings.

3. Start APM Server.
4. [View the monitoring data in {{kib}}](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md).


## Settings for internal collection [apm-configuration-monitor]

Use the following settings to configure internal collection when you are not using {{metricbeat}} to collect monitoring data.

You specify these settings in the X-Pack monitoring section of the `apm-server.yml` config file:


### `monitoring.enabled` [_monitoring_enabled]

The `monitoring.enabled` config is a boolean setting to enable or disable {{monitoring}}. If set to `true`, monitoring is enabled.

The default value is `false`.


### `monitoring.elasticsearch` [_monitoring_elasticsearch]

The {{es}} instances that you want to ship your APM Server metrics to. This configuration option contains the following fields:


#### `api_key` [_api_key_3]

The detail of the API key to be used to send monitoring information to {{es}}. See [Grant access using API keys](grant-access-using-api-keys.md) for more information.


#### `bulk_max_size` [_bulk_max_size_5]

The maximum number of metrics to bulk in a single {{es}} bulk API index request. The default is `50`. For more information, see [{{es}}](configure-elasticsearch-output.md).


#### `backoff.init` [_backoff_init_5]

The number of seconds to wait before trying to reconnect to {{es}} after a network error. After waiting `backoff.init` seconds, APM Server tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset. The default is `1s`.


#### `backoff.max` [_backoff_max_5]

The maximum number of seconds to wait before attempting to connect to {{es}} after a network error. The default is `60s`.


#### `compression_level` [_compression_level_4]

The gzip compression level. Setting this value to `0` disables compression. The compression level must be in the range of `1` (best speed) to `9` (best compression). The default value is `0`. Increasing the compression level reduces the network usage but increases the CPU usage.


#### `headers` [_headers_2]

Custom HTTP headers to add to each request. For more information, see [{{es}}](configure-elasticsearch-output.md).


#### `hosts` [_hosts_4]

The list of {{es}} nodes to connect to. Monitoring metrics are distributed to these nodes in round robin order. For more information, see [{{es}}](configure-elasticsearch-output.md).


#### `max_retries` [_max_retries_5]

The number of times to retry sending the monitoring metrics after a failure. After the specified number of retries, the metrics are typically dropped. The default value is `3`. For more information, see [{{es}}](configure-elasticsearch-output.md).


#### `parameters` [_parameters_2]

Dictionary of HTTP parameters to pass within the URL with index operations.


#### `password` [_password_4]

The password that APM Server uses to authenticate with the {{es}} instances for shipping monitoring data.


#### `metrics.period` [_metrics_period]

The time interval (in seconds) when metrics are sent to the {{es}} cluster. A new snapshot of APM Server metrics is generated and scheduled for publishing each period. The default value is 10 * time.Second.


#### `state.period` [_state_period]

The time interval (in seconds) when state information are sent to the {{es}} cluster. A new snapshot of APM Server state is generated and scheduled for publishing each period. The default value is 60 * time.Second.


#### `protocol` [_protocol]

The name of the protocol to use when connecting to the {{es}} cluster. The options are: `http` or `https`. The default is `http`. If you specify a URL for `hosts`, however, the value of protocol is overridden by the scheme you specify in the URL.


#### `proxy_url` [_proxy_url_4]

The URL of the proxy to use when connecting to the {{es}} cluster. For more information, see [{{es}}](configure-elasticsearch-output.md).


#### `timeout` [_timeout_5]

The HTTP request timeout in seconds for the {{es}} request. The default is `90`.


#### `ssl` [_ssl_5]

Configuration options for Transport Layer Security (TLS) or Secure Sockets Layer (SSL) parameters like the certificate authority (CA) to use for HTTPS-based connections. If the `ssl` section is missing, the host CAs are used for HTTPS connections to {{es}}. For more information, see [SSL/TLS output settings](ssltls-output-settings.md).


#### `username` [_username_3]

The user ID that APM Server uses to authenticate with the {{es}} instances for shipping monitoring data.

