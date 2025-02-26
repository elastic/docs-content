---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/ls-output-settings.html
---

# Logstash output settings [ls-output-settings]

Specify these settings to send data over a secure connection to {{ls}}. You must also configure a {{ls}} pipeline that reads encrypted data from {{agent}}s and sends the data to {{es}}. Follow the in-product steps to configure the {{ls}} pipeline.

In the {{fleet}} [Output settings](/reference/ingestion-tools/fleet/fleet-settings.md#output-settings), make sure that the {{ls}} output type is selected.

Before using the {{ls}} output, you need to make sure that for any integrations that have been [added to your {{agent}} policy](/reference/ingestion-tools/fleet/add-integration-to-policy.md), the integration assets have been installed on the destination cluster. Refer to [Install and uninstall {{agent}} integration assets](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md) for the steps to add integration assets.

To learn how to generate certificates, refer to [Configure SSL/TLS for the {{ls}} output](/reference/ingestion-tools/fleet/secure-logstash-connections.md).

To receive the events in {{ls}}, you also need to create a {{ls}} configuration pipeline. The {{ls}} configuration pipeline listens for incoming {{agent}} connections, processes received events, and then sends the events to {{es}}.

The following example configures a {{ls}} pipeline that listens on port `5044` for incoming {{agent}} connections and routes received events to {{es}}.

The {{ls}} pipeline definition below is an example. Please refer to the `Additional Logstash configuration required` steps when creating the {{ls}} output in the Fleet outputs page.

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
2. The API Key obtained from the {{ls}} output creation steps in Fleet.


|     |     |
| --- | --- |
| $$$ls-logstash-hosts$$$<br>**{{ls}} hosts**<br> | The addresses your {{agent}}s will use to connect to {{ls}}. Use the format `host:port`. Click **add** row to specify additional {{ls}} addresses.<br><br>**Examples:**<br><br>* `192.0.2.0:5044`<br>* `mylogstashhost:5044`<br><br>Refer to the [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) documentation for default ports and other configuration details.<br> |
| $$$ls-server-ssl-certificate-authorities-setting$$$<br>**Server SSL certificate authorities**<br> | The CA certificate to use to connect to {{ls}}. This is the CA used to generate the certificate and key for {{ls}}. Copy and paste in the full contents for the CA certificate.<br><br>This setting is optional.<br> |
| $$$ls-client-ssl-certificate-setting$$$<br>**Client SSL certificate**<br> | The certificate generated for the client. Copy and paste in the full contents of the certificate. This is the certificate that all the agents will use to connect to {{ls}}.<br><br>In cases where each client has a unique certificate, the local path to that certificate can be placed here. The agents will pick the certificate in that location when establishing a connection to {{ls}}.<br> |
| $$$ls-client-ssl-certificate-key-setting$$$<br>**Client SSL certificate key**<br> | The private key generated for the client. This must be in PKCS 8 key. Copy and paste in the full contents of the certificate key. This is the certificate key that all the agents will use to connect to {{ls}}.<br><br>In cases where each client has a unique certificate key, the local path to that certificate key can be placed here. The agents will pick the certificate key in that location when establishing a connection to {{ls}}.<br><br>To prevent unauthorized access the certificate key is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the key as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher.<br><br>Note that this setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://docs/reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.<br> |
| $$$ls-agent-proxy-output$$$<br>**Proxy**<br> | Select a proxy URL for {{agent}} to connect to {{ls}}. To learn about proxy configuration, refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md).<br> |
| $$$ls-output-advanced-yaml-setting$$$<br>**Advanced YAML configuration**<br> | YAML settings that will be added to the {{ls}} output section of each policy that uses this output. Make sure you specify valid YAML. The UI does not currently provide validation.<br><br>See [Advanced YAML configuration](#ls-output-settings-yaml-config) for descriptions of the available settings.<br> |
| $$$ls-agent-integrations-output$$$<br>**Make this output the default for agent integrations**<br> | When this setting is on, {{agent}}s use this output to send data if no other output is set in the [agent policy](/reference/ingestion-tools/fleet/agent-policy.md).<br><br>Output to {{ls}} is not supported for agent integrations in a policy used by {{fleet-server}} or APM.<br> |
| $$$ls-agent-monitoring-output$$$<br>**Make this output the default for agent monitoring**<br> | When this setting is on, {{agent}}s use this output to send [agent monitoring data](/reference/ingestion-tools/fleet/monitor-elastic-agent.md) if no other output is set in the [agent policy](/reference/ingestion-tools/fleet/agent-policy.md).<br><br>Output to {{ls}} is not supported for agent monitoring in a policy used by {{fleet-server}} or APM.<br> |

## Advanced YAML configuration [ls-output-settings-yaml-config]

| Setting | Description |
| --- | --- |
| $$$output-logstash-fleet-settings-backoff.init-setting$$$<br>`backoff.init`<br> | (string) The number of seconds to wait before trying to reconnect to {{ls}} after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.<br><br>**Default:** `1s`<br> |
| $$$output-logstash-fleet-settings-backoff.max-setting$$$<br>`backoff.max`<br> | (string) The maximum number of seconds to wait before attempting to connect to {{es}} after a network error.<br><br>**Default:** `60s`<br> |
| $$$output-logstash-fleet-settings-bulk_max_size-setting$$$<br>`bulk_max_size`<br> | (int) The maximum number of events to bulk in a single {{ls}} request.<br><br>Events can be collected into batches. {{agent}} will split batches larger than `bulk_max_size` into multiple batches.<br><br>Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.<br><br>Set this value to `0` to turn off the splitting of batches. When splitting is turned off, the queue determines the number of events to be contained in a batch.<br><br>**Default:** `2048`<br> |
| $$$output-logstash-fleet-settings-compression_level-setting$$$<br>`compression_level`<br> | (int) The gzip compression level. Set this value to `0` to disable compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).<br><br>Increasing the compression level reduces network usage but increases CPU usage.<br> |
| $$$output-logstash-fleet-settings-escape_html-setting$$$<br>`escape_html`<br> | (boolean) Configures escaping of HTML in strings. Set to `true` to enable escaping.<br><br>**Default:** `false`<br> |
| $$$output-logstash-fleet-settings-index-setting$$$<br>`index`<br> | (string) The index root name to write events to.<br> |
| $$$output-logstash-fleet-settings-loadbalance-setting$$$<br>`loadbalance`<br> | If `true` and multiple {{ls}} hosts are configured, the output plugin load balances published events onto all {{ls}} hosts. If `false`, the output plugin sends all events to one host (determined at random) and switches to another host if the selected one becomes unresponsive.<br><br>With `loadbalance` enabled:<br><br>* {{agent}} reads batches of events and sends each batch to one {{ls}} worker dynamically, based on a work-queue shared between the outputs.<br>* If a connection drops, {{agent}} takes the disconnected {{ls}} worker out of its pool.<br>* {{agent}} tries to reconnect. If it succeeds, it re-adds the {{ls}} worker to the pool.<br>* If one of the {{ls}} nodes is slow but "healthy", it sends a keep-alive signal until the full batch of data is processed. This prevents {{agent}} from sending further data until it receives an acknowledgement signal back from {{ls}}. {{agent}} keeps all events in memory until after that acknowledgement occurs.<br><br>Without `loadbalance` enabled:<br><br>* {{agent}} picks a random {{ls}} host and sends batches of events to it. Due to the random algorithm, the load on the {{ls}} nodes should be roughly equal.<br>* In case of any errors, {{agent}} picks another {{ls}} node, also at random. If a connection to a host fails, the host is retried only if there are errors on the new connection.<br><br>**Default:** `false`<br><br>Example:<br><br>```yaml<br>outputs:<br>  default:<br>    type: logstash<br>    hosts: ["localhost:5044", "localhost:5045"]<br>    loadbalance: true<br>```<br> |
| $$$output-logstash-fleet-settings-max_retries-setting$$$<br>`max_retries`<br> | (int) The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.<br><br>Set `max_retries` to a value less than 0 to retry until all events are published.<br><br>**Default:** `3`<br> |
| $$$output-logstash-fleet-settings-pipelining-setting$$$<br>`pipelining`<br> | (int) The number of batches to send asynchronously to {{ls}} while waiting for an ACK from {{ls}}. The output becomes blocking after the specified number of batches are written. Specify `0` to turn off pipelining.<br><br>**Default:** `2`<br> |
| $$$output-logstash-fleet-settings-proxy_use_local_resolver-setting$$$<br>`proxy_use_` `local_resolver`<br> | (boolean) Determines whether {{ls}} hostnames are resolved locally when using a proxy. If `false` and a proxy is used, name resolution occurs on the proxy server.<br><br>**Default:** `false`<br> |
| $$$output-logstash-fleet-settings-queue.mem.events-setting$$$<br>`queue.mem.events`<br> | The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.<br><br>**Default:** `3200 events`<br> |
| $$$output-logstash-fleet-settings-queue.mem.flush.min_events-setting$$$<br>`queue.mem.flush.min_events`<br> | `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`<br><br>**Default:** `1600 events`<br> |
| $$$output-logstash-fleet-settings-queue.mem.flush.timeout-setting$$$<br>`queue.mem.flush.timeout`<br> | (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.<br><br>**Default:** `10s`<br> |
| $$$output-logstash-fleet-settings-slow_start-setting$$$<br>`slow_start`<br> | (boolean) If `true`, only a subset of events in a batch of events is transferred per transaction. The number of events to be sent increases up to `bulk_max_size` if no error is encountered. On error, the number of events per transaction is reduced again.<br><br>**Default:** `false`<br> |
| $$$output-logstash-fleet-settings-timeout-setting$$$<br>`timeout`<br> | (string) The number of seconds to wait for responses from the {{ls}} server before timing out.<br><br>**Default:** `30s`<br> |
| $$$output-logstash-fleet-settings-ttl-setting$$$<br>`ttl`<br> | (string) Time to live for a connection to {{ls}} after which the connection will be reestablished. This setting is useful when {{ls}} hosts represent load balancers. Because connections to {{ls}} hosts are sticky, operating behind load balancers can lead to uneven load distribution across instances. Specify a TTL on the connection to achieve equal connection distribution across instances.<br><br>**Default:** `0` (turns off the feature)<br><br>::::{note} <br>The `ttl` option is not yet supported on an asynchronous {{ls}} client (one with the `pipelining` option set).<br>::::<br><br> |
| $$$output-logstash-fleet-settings-worker-setting$$$<br>`worker`<br> | (int) The number of workers per configured host publishing events. Example: If you have two hosts and three workers, in total six workers are started (three for each host).<br><br>**Default:** `1`<br> |
