---
navigation_title: "{{ls}}"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-logstash-output.html
applies_to:
  stack: all
---



# Configure the Logstash output [apm-logstash-output]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

The {{ls}} output is not yet supported by {{fleet}}-managed APM Server.

::::


{{ls}} allows for additional processing and routing of APM events. The {{ls}} output sends events directly to {{ls}} using the lumberjack protocol, which runs over TCP.


## Send events to {{ls}} [_send_events_to_ls]

To send events to {{ls}}, you must:

1. [Enable the {{ls}} output in APM Server](#apm-ls-output-config)
2. [Create a {{ls}} configuration pipeline in {{ls}}](#apm-ls-config-pipeline)


### {{ls}} output configuration [apm-ls-output-config]

To enable the {{ls}} output in APM Server, edit the `apm-server.yml` file to:

1. Disable the {{es}} output by commenting it out and
2. Enable the {{ls}} output by uncommenting the {{ls}} section and setting `enabled` to `true`:

    ```yaml
    output.logstash:
      enabled: true
      hosts: ["localhost:5044"] <1>
    ```

    1. The `hosts` option specifies the {{ls}} server and the port (`5044`) where {{ls}} is configured to listen for incoming APM Server connections.



### {{ls}} configuration pipeline [apm-ls-config-pipeline]

Finally, you must create a {{ls}} configuration pipeline that listens for incoming APM Server connections and indexes received events into {{es}}.

1. Use the [Elastic Agent input plugin](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-elastic_agent.md) to configure {{ls}} to receive events from the APM Server. A minimal `input` config might look like this:

    ```json
    input {
      elastic_agent {
        port => 5044
      }
    }
    ```

2. Use the [{{es}} output plugin](asciidocalypse://docs/logstash/docs/reference/plugins-outputs-elasticsearch.md) to send events to {{es}} for indexing. A minimal `output` config might look like this:

    ```json
    output {
      elasticsearch {
        data_stream => "true" <1>
        cloud_id => "YOUR_CLOUD_ID_HERE" <2>
        cloud_auth => "YOUR_CLOUD_AUTH_HERE" <2>
      }
    }
    ```

    1. Enables indexing into {{es}} data streams.
    2. This example assumes you’re sending data to {{ecloud}}. If you’re using a self-hosted version of {{es}}, use `hosts` instead. See [{{es}} output plugin](asciidocalypse://docs/logstash/docs/reference/plugins-outputs-elasticsearch.md) for more information.


Here’s what your basic {{ls}} configuration file will look like when we put everything together:

```json
input {
  elastic_agent {
    port => 5044
  }
}

output {
  elasticsearch {
    data_stream => "true"
    cloud_id => "YOUR_CLOUD_ID_HERE"
    cloud_auth => "YOUR_CLOUD_AUTH_HERE"
  }
}
```


## Accessing the @metadata field [_accessing_the_metadata_field]

Every event sent to {{ls}} contains a special field called [`@metadata`](asciidocalypse://docs/logstash/docs/reference/event-dependent-configuration.md#metadata) that you can use in {{ls}} for conditionals, filtering, indexing and more. APM Server sends the following `@metadata` to {{ls}}:

```json
{
    ...
    "@metadata": {
      "beat": "apm-server", <1>
      "version": "9.0.0-beta1" <2>
    }
}
```

1. To change the default `apm-server` value, set the [`index`](#apm-logstash-index) option in the APM Server config file.
2. The current version of APM Server.


In addition to `@metadata`, APM Server provides other potentially useful fields, like the `data_stream` field, which can be used to conditionally operate on [event types](learn-about-application-data-types.md), namespaces, or datasets.

As an example, you might want to use {{ls}} to route all `metrics` events to the same custom metrics data stream, rather than to service-specific data streams.

However, if when you combine all `metrics` events there are events that have the `data_stream.dataset` field set to different values, indexing will fail with a message stating that the field does not accept any other values. For example, the error might say something like `failed to parse field [data_stream.dataset] of type [constant_keyword]` or `[constant_keyword] field [data_stream.dataset] only accepts values that are equal to the value defined in the mappings`. This is because the `data_stream.dataset` field’s mapping is set to `constant_keyword`, which expects all values of the fields in the index to be the same.

To prevent losing data due to failed indexing, add a [Logstash mutate filter](asciidocalypse://docs/logstash/docs/reference/plugins-filters-mutate.md) to update the value of `data_stream.dataset`. Then, you can send all metrics events to one custom metrics data stream:

```json
filter {
  if [@metadata][beat] == "apm-server" { <1>
    if [data_stream][type] == "metrics" { <2>
      mutate {
        update => { "[data_stream][dataset]" => "custom" } <3>
      }
    }
  }
}
output {
  elasticsearch {
    data_stream => "true"
    cloud_id => "${CLOUD_ID}" <4>
    cloud_auth => "${CLOUD_AUTH}" <4>
  }
}
```

1. Only apply this output if the data is being sent from the APM Server.
2. Determine if the event type is `metrics`.
3. Add a Logstash mutate filter to update the value of `data_stream.dataset`.
4. In this example, `cloud_id` and `cloud_auth` are stored as [environment variables](asciidocalypse://docs/logstash/docs/reference/environment-variables.md).



### Compatibility [_compatibility_2]

This output works with all compatible versions of {{ls}}. See the [Elastic Support Matrix](https://www.elastic.co/support/matrix#matrix_compatibility).


### Configuration options [_configuration_options_4]

You can specify the following options in the `logstash` section of the `apm-server.yml` config file:


#### `enabled` [_enabled_3]

The enabled config is a boolean setting to enable or disable the output. If set to false, the output is disabled.

The default value is `false`.


#### `hosts` [apm-hosts]

The list of known {{ls}} servers to connect to. If load balancing is disabled, but multiple hosts are configured, one host is selected randomly (there is no precedence). If one host becomes unreachable, another one is selected randomly.

All entries in this list can contain a port number. The default port number 5044 will be used if no number is given.


#### `compression_level` [_compression_level_2]

The gzip compression level. Setting this value to 0 disables compression. The compression level must be in the range of 1 (best speed) to 9 (best compression).

Increasing the compression level will reduce the network usage but will increase the CPU usage.

The default value is 3.


#### `escape_html` [_escape_html_2]

Configure escaping of HTML in strings. Set to `true` to enable escaping.

The default value is `false`.


#### `worker` [_worker]

The number of workers per configured host publishing events to {{ls}}. This is best used with load balancing mode enabled. Example: If you have 2 hosts and 3 workers, in total 6 workers are started (3 for each host).


#### `loadbalance` [apm-loadbalance]

If set to true and multiple {{ls}} hosts are configured, the output plugin load balances published events onto all {{ls}} hosts. If set to false, the output plugin sends all events to only one host (determined at random) and will switch to another host if the selected one becomes unresponsive. The default value is false.

```yaml
output.logstash:
  hosts: ["localhost:5044", "localhost:5045"]
  loadbalance: true
  index: apm-server
```


#### `ttl` [_ttl]

Time to live for a connection to {{ls}} after which the connection will be re-established. Useful when {{ls}} hosts represent load balancers. Since the connections to {{ls}} hosts are sticky, operating behind load balancers can lead to uneven load distribution between the instances. Specifying a TTL on the connection allows to achieve equal connection distribution between the instances.  Specifying a TTL of 0 will disable this feature.

The default value is 0.

::::{note}
The "ttl" option is not yet supported on an asynchronous {{ls}} client (one with the "pipelining" option set).
::::



#### `pipelining` [_pipelining]

Configures the number of batches to be sent asynchronously to {{ls}} while waiting for ACK from {{ls}}. Output only becomes blocking once number of `pipelining` batches have been written. Pipelining is disabled if a value of 0 is configured. The default value is 2.


#### `proxy_url` [_proxy_url_2]

The URL of the SOCKS5 proxy to use when connecting to the {{ls}} servers. The value must be a URL with a scheme of `socks5://`. The protocol used to communicate to {{ls}} is not based on HTTP so a web-proxy cannot be used.

If the SOCKS5 proxy server requires client authentication, then a username and password can be embedded in the URL as shown in the example.

When using a proxy, hostnames are resolved on the proxy server instead of on the client. You can change this behavior by setting the [`proxy_use_local_resolver`](#apm-logstash-proxy-use-local-resolver) option.

```yaml
output.logstash:
  hosts: ["remote-host:5044"]
  proxy_url: socks5://user:password@socks5-proxy:2233
```


#### `proxy_use_local_resolver` [apm-logstash-proxy-use-local-resolver]

The `proxy_use_local_resolver` option determines if {{ls}} hostnames are resolved locally when using a proxy. The default value is false, which means that when a proxy is used the name resolution occurs on the proxy server.


#### `index` [apm-logstash-index]

The index root name to write events to. The default is `apm-server`. For example `"apm"` generates `"[apm-]9.0.0-beta1-YYYY.MM.DD"` indices (for example, `"apm-9.0.0-beta1-2017.04.26"`).

::::{note}
This parameter’s value will be assigned to the `metadata.beat` field. It can then be accessed in {{ls}}'s output section as `%{[@metadata][beat]}`.
::::



#### `ssl` [_ssl_2]

Configuration options for SSL parameters like the root CA for {{ls}} connections. See [SSL/TLS output settings](ssltls-output-settings.md) for more information. To use SSL, you must also configure the [{{beats}} input plugin for {{ls}}](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-beats.md) to use SSL/TLS.


#### `timeout` [_timeout_2]

The number of seconds to wait for responses from the {{ls}} server before timing out. The default is 30 (seconds).


#### `max_retries` [_max_retries_2]

The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.

Set `max_retries` to a value less than 0 to retry until all events are published.

The default is 3.


#### `bulk_max_size` [_bulk_max_size]

The maximum number of events to bulk in a single {{ls}} request. The default is 2048.

If the Beat sends single events, the events are collected into batches. If the Beat publishes a large batch of events (larger than the value specified by `bulk_max_size`), the batch is split.

Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.

Setting `bulk_max_size` to values less than or equal to 0 disables the splitting of batches. When splitting is disabled, the queue decides on the number of events to be contained in a batch.


#### `slow_start` [_slow_start]

If enabled, only a subset of events in a batch of events is transferred per transaction. The number of events to be sent increases up to `bulk_max_size` if no error is encountered. On error, the number of events per transaction is reduced again.

The default is `false`.


#### `backoff.init` [_backoff_init_2]

The number of seconds to wait before trying to reconnect to {{ls}} after a network error. After waiting `backoff.init` seconds, APM Server tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset. The default is `1s`.


#### `backoff.max` [_backoff_max_2]

The maximum number of seconds to wait before attempting to connect to {{ls}} after a network error. The default is `60s`.


## Secure communication with {{ls}} [apm-configuring-ssl-logstash]

You can use SSL mutual authentication to secure connections between APM Server and {{ls}}. This ensures that APM Server sends encrypted data to trusted {{ls}} servers only, and that the {{ls}} server receives data from trusted APM Server clients only.

To use SSL mutual authentication:

1. Create a certificate authority (CA) and use it to sign the certificates that you plan to use for APM Server and {{ls}}. Creating a correct SSL/TLS infrastructure is outside the scope of this document. There are many online resources available that describe how to create certificates.

    ::::{tip}
    If you are using {{security-features}}, you can use the [`elasticsearch-certutil` tool](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/certutil.md) to generate certificates.
    ::::

2. Configure APM Server to use SSL. In the `apm-server.yml` config file, specify the following settings under `ssl`:

    * `certificate_authorities`: Configures APM Server to trust any certificates signed by the specified CA. If `certificate_authorities` is empty or not set, the trusted certificate authorities of the host system are used.
    * `certificate` and `key`: Specifies the certificate and key that APM Server uses to authenticate with {{ls}}.

        For example:

        ```yaml
        output.logstash:
          hosts: ["logs.mycompany.com:5044"]
          ssl.certificate_authorities: ["/etc/ca.crt"]
          ssl.certificate: "/etc/client.crt"
          ssl.key: "/etc/client.key"
        ```

        For more information about these configuration options, see [SSL/TLS output settings](ssltls-output-settings.md).

3. Configure {{ls}} to use SSL. In the {{ls}} config file, specify the following settings for the [{{beats}} input plugin for {{ls}}](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-beats.md):

    * `ssl`: When set to true, enables {{ls}} to use SSL/TLS.
    * `ssl_certificate_authorities`: Configures {{ls}} to trust any certificates signed by the specified CA.
    * `ssl_certificate` and `ssl_key`: Specify the certificate and key that {{ls}} uses to authenticate with the client.
    * `ssl_verify_mode`: Specifies whether the {{ls}} server verifies the client certificate against the CA. You need to specify either `peer` or `force_peer` to make the server ask for the certificate and validate it. If you specify `force_peer`, and APM Server doesn’t provide a certificate, the {{ls}} connection will be closed. If you choose not to use [`certutil`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/certutil.md), the certificates that you obtain must allow for both `clientAuth` and `serverAuth` if the extended key usage extension is present.

        For example:

        ```json
        input {
          beats {
            port => 5044
            ssl => true
            ssl_certificate_authorities => ["/etc/ca.crt"]
            ssl_certificate => "/etc/server.crt"
            ssl_key => "/etc/server.key"
            ssl_verify_mode => "force_peer"
          }
        }
        ```

        For more information about these options, see the [documentation for the {{beats}} input plugin](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-beats.md).



### Validate the {{ls}} server’s certificate [apm-testing-ssl-logstash]

Before running APM Server, you should validate the {{ls}} server’s certificate. You can use `curl` to validate the certificate even though the protocol used to communicate with {{ls}} is not based on HTTP. For example:

```shell
curl -v --cacert ca.crt https://logs.mycompany.com:5044
```

If the test is successful, you’ll receive an empty response error:

```shell
* Rebuilt URL to: https://logs.mycompany.com:5044/
*   Trying 192.168.99.100...
* Connected to logs.mycompany.com (192.168.99.100) port 5044 (#0)
* TLS 1.2 connection using TLS_DHE_RSA_WITH_AES_256_CBC_SHA
* Server certificate: logs.mycompany.com
* Server certificate: mycompany.com
> GET / HTTP/1.1
> Host: logs.mycompany.com:5044
> User-Agent: curl/7.43.0
> Accept: */*
>
* Empty reply from server
* Connection #0 to host logs.mycompany.com left intact
curl: (52) Empty reply from server
```

The following example uses the IP address rather than the hostname to validate the certificate:

```shell
curl -v --cacert ca.crt https://192.168.99.100:5044
```

Validation for this test fails because the certificate is not valid for the specified IP address. It’s only valid for the `logs.mycompany.com`, the hostname that appears in the Subject field of the certificate.

```shell
* Rebuilt URL to: https://192.168.99.100:5044/
*   Trying 192.168.99.100...
* Connected to 192.168.99.100 (192.168.99.100) port 5044 (#0)
* WARNING: using IP address, SNI is being disabled by the OS.
* SSL: certificate verification failed (result: 5)
* Closing connection 0
curl: (51) SSL: certificate verification failed (result: 5)
```

See the [troubleshooting docs](../../../troubleshoot/observability/apm/common-problems.md#apm-ssl-client-fails) for info about resolving this issue.

### Test the APM Server to {{ls}} connection [_test_the_apm_server_to_ls_connection]

If you have APM Server running as a service, first stop the service. Then test your setup by running APM Server in the foreground so you can quickly see any errors that occur:

```sh
apm-server -c apm-server.yml -e -v
```

Any errors will be printed to the console. See the [troubleshooting docs](../../../troubleshoot/observability/apm/common-problems.md#apm-ssl-client-fails) for info about resolving common errors.

