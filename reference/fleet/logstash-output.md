---
navigation_title: "{{ls}}"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/logstash-output.html
products:
  - id: fleet
  - id: elastic-agent
---

# {{ls}} output [logstash-output]


The {{ls}} output uses an internal protocol to send events directly to {{ls}} over TCP. {{ls}} provides additional parsing, transformation, and routing of data collected by {{agent}}.

**Compatibility:** This output works with all compatible versions of {{ls}}. Refer to the [Elastic Support Matrix](https://www.elastic.co/support/matrix#matrix_compatibility).

This example configures a {{ls}} output called `default` in the `elastic-agent.yml` file:

```yaml
outputs:
  default:
    type: logstash
    hosts: ["127.0.0.1:5044"] <1>
```

1. The {{ls}} server and the port (`5044`) where {{ls}} is configured to listen for incoming {{agent}} connections.


To receive the events in {{ls}}, you also need to create a {{ls}} configuration pipeline. The {{ls}} configuration pipeline listens for incoming {{agent}} connections, processes received events, and then sends the events to {{es}}.

Be aware that the structure of the documents sent from {{agent}} to {{ls}} must not be modified by the pipeline. We recommend that the pipeline doesn’t edit or remove the fields and their contents. Editing the structure of the documents coming from {{agent}} can prevent the {{es}} ingest pipelines associated to the integrations in use to work correctly. We cannot guarantee that the {{es}} ingest pipelines associated to the integrations using {{agent}} can work with missing or modified fields.

The following {{ls}} pipeline definition example configures a pipeline that listens on port `5044` for incoming {{agent}} connections and routes received events to {{es}}.

```yaml
input {
  elastic_agent {
    port => 5044
    enrich => none <1>
    ssl_enabled => true
    ssl_certificate_authorities => ["<ca_path>"]
    ssl_certificate => "<server_cert_path>"
    ssl_key => "<server_cert_key_in_pkcs8>"
    ssl_client_authentication => "required"
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"] <2>
    # cloud_id => "..."
    data_stream => "true"
    api_key => "<api_key>" <3>
    data_stream => true
    ssl_enabled => true
    ssl_certificate_authorities => "<elasticsearch_ca_path>"
  }
}
```

1. Do not modify the events' schema.
2. The {{es}} server and the port (`9200`) where {{es}} is running.
3. The API Key used by {{ls}} to ship data to the destination data streams.


For more information about configuring {{ls}}, refer to [Configuring {{ls}}](logstash://reference/creating-logstash-pipeline.md) and [{{agent}} input plugin](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md).

## {{ls}} output configuration settings [_ls_output_configuration_settings]

The `logstash` output supports the following settings, grouped by category. Many of these settings have sensible defaults that allow you to run {{agent}} with minimal configuration.

* [Commonly used settings](#output-logstash-commonly-used-settings)
* [Authentication settings](#output-logstash-authentication-settings)
* [Memory queue settings](#output-logstash-memory-queue-settings)
* [Performance tuning settings](#output-logstash-performance-tuning-settings)


## Commonly used settings [output-logstash-commonly-used-settings]

`enabled` $$$output-logstash-enabled-setting$$$
:   (boolean) Enables or disables the output. If set to `false`, the output is disabled.

`escape_html` $$$output-logstash-escape_html-setting$$$
:   (boolean) Configures escaping of HTML in strings. Set to `true` to enable escaping.

    **Default:** `false`

`hosts` $$$output-logstash-hosts-setting$$$
:   (list) The list of known {{ls}} servers to connect to. If load balancing is disabled, but multiple hosts are configured, one host is selected randomly (there is no precedence). If one host becomes unreachable, another one is selected randomly.

    All entries in this list can contain a port number. If no port is specified, `5044` is used.

`proxy_url` $$$output-logstash-proxy_url-setting$$$
:   (string) The URL of the SOCKS5 proxy to use when connecting to the {{ls}} servers. The value must be a URL with a scheme of `socks5://`. The protocol used to communicate to {{ls}} is not based on HTTP, so you cannot use a web proxy.

    If the SOCKS5 proxy server requires client authentication, embed a username and password in the URL as shown in the example.

    When using a proxy, hostnames are resolved on the proxy server instead of on the client. To change this behavior, set `proxy_use_local_resolver`.

    ```yaml
    outputs:
      default:
        type: logstash
        hosts: ["remote-host:5044"]
        proxy_url: socks5://user:password@socks5-proxy:2233
    ```

`proxy_use_local_resolver` $$$output-logstash-proxy_use_local_resolver-setting$$$
:   (boolean) Determines whether {{ls}} hostnames are resolved locally when using a proxy. If `false` and a proxy is used, name resolution occurs on the proxy server.

    **Default:** `false`


## Authentication settings [output-logstash-authentication-settings]

When sending data to a secured cluster through the `logstash` output, {{agent}} can use SSL/TLS. For a list of available settings, refer to [SSL/TLS](/reference/fleet/elastic-agent-ssl-configuration.md), specifically the settings under [Table 7, Common configuration options](/reference/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/fleet/elastic-agent-ssl-configuration.md#client-ssl-options).

::::{note}
To use SSL/TLS, you must also configure the [{{agent}} input plugin for {{ls}}](logstash-docs-md://lsr/plugins-inputs-beats.md) to use SSL/TLS.
::::


For more information, refer to [Configure SSL/TLS for the {{ls}} output](/reference/fleet/secure-logstash-connections.md).


## Memory queue settings [output-logstash-memory-queue-settings]

The memory queue keeps all events in memory.

The memory queue waits for the output to acknowledge or drop events. If the queue is full, no new events can be inserted into the memory queue. Only after the signal from the output will the queue free up space for more events to be accepted.

The memory queue is controlled by the parameters `flush.min_events` and `flush.timeout`. `flush.min_events` gives a limit on the number of events that can be included in a single batch, and `flush.timeout` specifies how long the queue should wait to completely fill an event request. If the output supports a `bulk_max_size` parameter, the maximum batch size will be the smaller of `bulk_max_size` and `flush.min_events`.

`flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`.

In synchronous mode, an event request is always filled as soon as events are available, even if there are not enough events to fill the requested batch. This is useful when latency must be minimized. To use synchronous mode, set `flush.timeout` to 0.

For backwards compatibility, synchronous mode can also be activated by setting `flush.min_events` to 0 or 1. In this case, batch size will be capped at 1/2 the queue capacity.

In asynchronous mode, an event request will wait up to the specified timeout to try and fill the requested batch completely. If the timeout expires, the queue returns a partial batch with all available events. To use asynchronous mode, set `flush.timeout` to a positive duration, for example 5s.

This sample configuration forwards events to the output when there are enough events to fill the output’s request (usually controlled by `bulk_max_size`, and limited to at most 512 events by `flush.min_events`), or when events have been waiting for 5s without filling the requested size:f 512 events are available or the oldest available event has been waiting for 5s in the queue:

```yaml
  queue.mem.events: 4096
  queue.mem.flush.min_events: 512
  queue.mem.flush.timeout: 5s
```

`queue.mem.events` $$$output-logstash-queue.mem.events-setting$$$
:   The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.

    **Default:** `3200 events`

`queue.mem.flush.min_events` $$$output-logstash-queue.mem.flush.min_events-setting$$$
:   `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`

    **Default:** `1600 events`

`queue.mem.flush.timeout` $$$output-logstash-queue.mem.flush.timeout-setting$$$
:   (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.

    **Default:** `10s`


## Performance tuning settings [output-logstash-performance-tuning-settings]

Settings that may affect performance.


`backoff.init` $$$output-logstash-backoff.init-setting$$$
:   (string) The number of seconds to wait before trying to reconnect to {{ls}} after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.

    **Default:** `1s`

`backoff.max` $$$output-logstash-backoff.max-setting$$$
:   (string) The maximum number of seconds to wait before attempting to connect to {{es}} after a network error.

    **Default:** `60s`

`bulk_max_size` $$$output-logstash-bulk_max_size-setting$$$
:   (int) The maximum number of events to bulk in a single {{ls}} request.

    Events can be collected into batches. {{agent}} will split batches larger than `bulk_max_size` into multiple batches.

    Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.

    Set this value to `0` to turn off the splitting of batches. When splitting is turned off, the queue determines the number of events to be contained in a batch.

    **Default:** `2048`

`compression_level` $$$output-logstash-compression_level-setting$$$
:   (int) The gzip compression level. Set this value to `0` to disable compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).

    Increasing the compression level reduces network usage but increases CPU usage.

    **Default:** `3`

`loadbalance` $$$output-logstash-loadbalance-setting$$$
:   If `true` and multiple {{ls}} hosts are configured, the output plugin load balances published events onto all {{ls}} hosts. If `false`, the output plugin sends all events to one host (determined at random) and switches to another host if the selected one becomes unresponsive.

    With `loadbalance` enabled:
    * {{agent}} reads batches of events and sends each batch to one {{ls}} worker dynamically, based on a work-queue shared between the outputs.
    * If a connection drops, {{agent}} takes the disconnected {{ls}} worker out of its pool.
    * {{agent}} tries to reconnect. If it succeeds, it re-adds the {{ls}} worker to the pool.
    * If one of the {{ls}} nodes is slow but "healthy", it sends a keep-alive signal until the full batch of data is processed. This prevents {{agent}} from sending further data until it receives an acknowledgement signal back from {{ls}}. {{agent}} keeps all events in memory until after that acknowledgement occurs.

    Without `loadbalance` enabled:
    * {{agent}} picks a random {{ls}} host and sends batches of events to it. Due to the random algorithm, the load on the {{ls}} nodes should be roughly equal.
    * In case of any errors, {{agent}} picks another {{ls}} node, also at random. If a connection to a host fails, the host is retried only if there are errors on the new connection.

    **Default:** `false`

    Example:

    ```yaml
    outputs:
      default:
        type: logstash
        hosts: ["localhost:5044", "localhost:5045"]
        loadbalance: true
    ```

`max_retries` $$$output-logstash-max_retries-setting$$$
:   (int) The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.

    Set `max_retries` to a value less than 0 to retry until all events are published.

    **Default:** `3`

`pipelining` $$$output-logstash-pipelining-setting$$$
:   (int) The number of batches to send asynchronously to {{ls}} while waiting for an ACK from {{ls}}. The output becomes blocking after the specified number of batches are written. Specify `0` to turn off pipelining.

    **Default:** `2`

`slow_start` $$$output-logstash-slow_start-setting$$$
:   (boolean) If `true`, only a subset of events in a batch of events is transferred per transaction. The number of events to be sent increases up to `bulk_max_size` if no error is encountered. On error, the number of events per transaction is reduced again.

    **Default:** `false`

`timeout` $$$output-logstash-timeout-setting$$$
:   (string) The number of seconds to wait for responses from the {{ls}} server before timing out.

    **Default:** `30s`

`ttl` $$$output-logstash-ttl-setting$$$
:   (string) Time to live for a connection to {{ls}} after which the connection will be reestablished. This setting is useful when {{ls}} hosts represent load balancers. Because connections to {{ls}} hosts are sticky, operating behind load balancers can lead to uneven load distribution across instances. Specify a TTL on the connection to achieve equal connection distribution across instances.

    **Default:** `0` (turns off the feature)

    ::::{note}
    The `ttl` option is not yet supported on an asynchronous {{ls}} client (one with the `pipelining` option set).
    ::::

`worker` $$$output-logstash-worker-setting$$$
:   (int) The number of workers per configured host publishing events. Example: If you have two hosts and three workers, in total six workers are started (three for each host).

    **Default:** `1`


