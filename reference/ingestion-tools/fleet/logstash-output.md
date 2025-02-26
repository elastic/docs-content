---
navigation_title: "{{ls}}"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/logstash-output.html
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

The following {{ls}} pipeline definition example configures a pipeline that listens on port `5044` for incoming {{agent}} connections and routes received events to {{es}}.

```yaml
input {
  elastic_agent {
    port => 5044
    enrich => none <1>
    ssl => true
    ssl_certificate_authorities => ["<ca_path>"]
    ssl_certificate => "<server_cert_path>"
    ssl_key => "<server_cert_key_in_pkcs8>"
    ssl_verify_mode => "force_peer"
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"] <2>
    # cloud_id => "..."
    data_stream => "true"
    api_key => "<api_key>" <3>
    data_stream => true
    ssl => true
    # cacert => "<elasticsearch_ca_path>"
  }
}
```

1. Do not modify the events' schema.
2. The {{es}} server and the port (`9200`) where {{es}} is running.
3. The API Key used by {{ls}} to ship data to the destination data streams.


For more information about configuring {{ls}}, refer to [Configuring {{ls}}](logstash://docs/reference/creating-logstash-pipeline.md) and [{{agent}} input plugin](logstash://docs/reference/plugins-inputs-elastic_agent.md).

## {{ls}} output configuration settings [_ls_output_configuration_settings]

The `logstash` output supports the following settings, grouped by category. Many of these settings have sensible defaults that allow you to run {{agent}} with minimal configuration.

* [Commonly used settings](#output-logstash-commonly-used-settings)
* [Authentication settings](#output-logstash-authentication-settings)
* [Memory queue settings](#output-logstash-memory-queue-settings)
* [Performance tuning settings](#output-logstash-performance-tuning-settings)


## Commonly used settings [output-logstash-commonly-used-settings]

| Setting | Description |
| --- | --- |
| $$$output-logstash-enabled-setting$$$<br>`enabled`<br> | (boolean) Enables or disables the output. If set to `false`, the output is disabled.<br> |
| $$$output-logstash-escape_html-setting$$$<br>`escape_html`<br> | (boolean) Configures escaping of HTML in strings. Set to `true` to enable escaping.<br><br>**Default:** `false`<br> |
| $$$output-logstash-hosts-setting$$$<br>`hosts`<br> | (list) The list of known {{ls}} servers to connect to. If load balancing is disabled, but multiple hosts are configured, one host is selected randomly (there is no precedence). If one host becomes unreachable, another one is selected randomly.<br><br>All entries in this list can contain a port number. If no port is specified, `5044` is used.<br> |
| $$$output-logstash-proxy_url-setting$$$<br>`proxy_url`<br> | (string) The URL of the SOCKS5 proxy to use when connecting to the {{ls}} servers. The value must be a URL with a scheme of `socks5://`. The protocol used to communicate to {{ls}} is not based on HTTP, so you cannot use a web proxy.<br><br>If the SOCKS5 proxy server requires client authentication, embed a username and password in the URL as shown in the example.<br><br>When using a proxy, hostnames are resolved on the proxy server instead of on the client. To change this behavior, set `proxy_use_local_resolver`.<br><br>```yaml<br>outputs:<br>  default:<br>    type: logstash<br>    hosts: ["remote-host:5044"]<br>    proxy_url: socks5://user:password@socks5-proxy:2233<br>```<br> |
| $$$output-logstash-proxy_use_local_resolver-setting$$$<br>`proxy_use_` `local_resolver`<br> | (boolean) Determines whether {{ls}} hostnames are resolved locally when using a proxy. If `false` and a proxy is used, name resolution occurs on the proxy server.<br><br>**Default:** `false`<br> |


## Authentication settings [output-logstash-authentication-settings]

When sending data to a secured cluster through the `logstash` output, {{agent}} can use SSL/TLS. For a list of available settings, refer to [SSL/TLS](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md), specifically the settings under [Table 7, Common configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#client-ssl-options).

::::{note}
To use SSL/TLS, you must also configure the [{{agent}} input plugin for {{ls}}](logstash://docs/reference/plugins-inputs-beats.md) to use SSL/TLS.
::::


For more information, refer to [Configure SSL/TLS for the {{ls}} output](/reference/ingestion-tools/fleet/secure-logstash-connections.md).


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

| Setting | Description |
| --- | --- |
| $$$output-logstash-queue.mem.events-setting$$$<br>`queue.mem.events`<br> | The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.<br><br>**Default:** `3200 events`<br> |
| $$$output-logstash-queue.mem.flush.min_events-setting$$$<br>`queue.mem.flush.min_events`<br> | `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`<br><br>**Default:** `1600 events`<br> |
| $$$output-logstash-queue.mem.flush.timeout-setting$$$<br>`queue.mem.flush.timeout`<br> | (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.<br><br>**Default:** `10s`<br> |


## Performance tuning settings [output-logstash-performance-tuning-settings]

Settings that may affect performance.

| Setting | Description |
| --- | --- |
| $$$output-logstash-backoff.init-setting$$$<br>`backoff.init`<br> | (string) The number of seconds to wait before trying to reconnect to {{ls}} after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.<br><br>**Default:** `1s`<br> |
| $$$output-logstash-backoff.max-setting$$$<br>`backoff.max`<br> | (string) The maximum number of seconds to wait before attempting to connect to {{es}} after a network error.<br><br>**Default:** `60s`<br> |
| $$$output-logstash-bulk_max_size-setting$$$<br>`bulk_max_size`<br> | (int) The maximum number of events to bulk in a single {{ls}} request.<br><br>Events can be collected into batches. {{agent}} will split batches larger than `bulk_max_size` into multiple batches.<br><br>Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.<br><br>Set this value to `0` to turn off the splitting of batches. When splitting is turned off, the queue determines the number of events to be contained in a batch.<br><br>**Default:** `2048`<br> |
| $$$output-logstash-compression_level-setting$$$<br>`compression_level`<br> | (int) The gzip compression level. Set this value to `0` to disable compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).<br><br>Increasing the compression level reduces network usage but increases CPU usage.<br><br>**Default:** `3`<br> |
| $$$output-logstash-loadbalance-setting$$$<br>`loadbalance`<br> | If `true` and multiple {{ls}} hosts are configured, the output plugin load balances published events onto all {{ls}} hosts. If `false`, the output plugin sends all events to one host (determined at random) and switches to another host if the selected one becomes unresponsive.<br><br>With `loadbalance` enabled:<br><br>* {{agent}} reads batches of events and sends each batch to one {{ls}} worker dynamically, based on a work-queue shared between the outputs.<br>* If a connection drops, {{agent}} takes the disconnected {{ls}} worker out of its pool.<br>* {{agent}} tries to reconnect. If it succeeds, it re-adds the {{ls}} worker to the pool.<br>* If one of the {{ls}} nodes is slow but "healthy", it sends a keep-alive signal until the full batch of data is processed. This prevents {{agent}} from sending further data until it receives an acknowledgement signal back from {{ls}}. {{agent}} keeps all events in memory until after that acknowledgement occurs.<br><br>Without `loadbalance` enabled:<br><br>* {{agent}} picks a random {{ls}} host and sends batches of events to it. Due to the random algorithm, the load on the {{ls}} nodes should be roughly equal.<br>* In case of any errors, {{agent}} picks another {{ls}} node, also at random. If a connection to a host fails, the host is retried only if there are errors on the new connection.<br><br>**Default:** `false`<br><br>Example:<br><br>```yaml<br>outputs:<br>  default:<br>    type: logstash<br>    hosts: ["localhost:5044", "localhost:5045"]<br>    loadbalance: true<br>```<br> |
| $$$output-logstash-max_retries-setting$$$<br>`max_retries`<br> | (int) The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.<br><br>Set `max_retries` to a value less than 0 to retry until all events are published.<br><br>**Default:** `3`<br> |
| $$$output-logstash-pipelining-setting$$$<br>`pipelining`<br> | (int) The number of batches to send asynchronously to {{ls}} while waiting for an ACK from {{ls}}. The output becomes blocking after the specified number of batches are written. Specify `0` to turn off pipelining.<br><br>**Default:** `2`<br> |
| $$$output-logstash-slow_start-setting$$$<br>`slow_start`<br> | (boolean) If `true`, only a subset of events in a batch of events is transferred per transaction. The number of events to be sent increases up to `bulk_max_size` if no error is encountered. On error, the number of events per transaction is reduced again.<br><br>**Default:** `false`<br> |
| $$$output-logstash-timeout-setting$$$<br>`timeout`<br> | (string) The number of seconds to wait for responses from the {{ls}} server before timing out.<br><br>**Default:** `30s`<br> |
| $$$output-logstash-ttl-setting$$$<br>`ttl`<br> | (string) Time to live for a connection to {{ls}} after which the connection will be reestablished. This setting is useful when {{ls}} hosts represent load balancers. Because connections to {{ls}} hosts are sticky, operating behind load balancers can lead to uneven load distribution across instances. Specify a TTL on the connection to achieve equal connection distribution across instances.<br><br>**Default:** `0` (turns off the feature)<br><br>::::{note} <br>The `ttl` option is not yet supported on an asynchronous {{ls}} client (one with the `pipelining` option set).<br>::::<br><br> |
| $$$output-logstash-worker-setting$$$<br>`worker`<br> | (int) The number of workers per configured host publishing events. Example: If you have two hosts and three workers, in total six workers are started (three for each host).<br><br>**Default:** `1`<br> |


