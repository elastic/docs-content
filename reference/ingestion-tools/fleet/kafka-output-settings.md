---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kafka-output-settings.html
---

# Kafka output settings [kafka-output-settings]

Specify these settings to send data over a secure connection to Kafka. In the {{fleet}} [Output settings](/reference/ingestion-tools/fleet/fleet-settings.md#output-settings), make sure that the Kafka output type is selected.

::::{note}
If you plan to use {{ls}} to modify {{agent}} output data before it’s sent to Kafka, please refer to our [guidance](#kafka-output-settings-ls-warning) for doing so, further in on this page.
::::



### General settings [_general_settings]

|     |     |
| --- | --- |
| $$$kafka-output-version$$$<br>**Kafka version**<br> | The Kafka protocol version that {{agent}} will request when connecting. Defaults to `1.0.0`. Currently Kafka versions from `0.8.2.0` to `2.6.0` are supported, however the latest Kafka version (`3.x.x`) is expected to be compatible when version `2.6.0` is selected. When using Kafka 4.0 and newer, the version must be set to at least `2.1.0`.<br> |
| $$$kafka-output-hosts$$$<br>**Hosts**<br> | The addresses your {{agent}}s will use to connect to one or more Kafka brokers. Use the format `host:port` (without any protocol `http://`). Click **Add row** to specify additional addresses.<br><br>**Examples:**<br><br>* `localhost:9092`<br>* `mykafkahost:9092`<br><br>Refer to the [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) documentation for default ports and other configuration details.<br> |


### Authentication settings [_authentication_settings]

Select the mechanism that {{agent}} uses to authenticate with Kafka.

|     |     |
| --- | --- |
| $$$kafka-output-authentication-none$$$<br>**None**<br> | No authentication is used between {{agent}} and Kafka. This is the default option. In production, it’s recommended to have an authentication method selected.<br><br>Plaintext<br>:   Set this option for traffic between {{agent}} and Kafka to be sent as plaintext, without any transport layer security.<br><br>    This is the default option when no authentication is set.<br><br><br>Encryption<br>:   Set this option for traffic between {{agent}} and Kafka to use transport layer security.<br><br>    When **Encryption*** is selected, the ***Server SSL certificate authorities** and **Verification mode** mode options become available.<br><br> |
| $$$kafka-output-authentication-basic$$$<br>**Username / Password**<br> | Connect to Kafka with a username and password.<br><br>Provide your username and password, and select a SASL (Simple Authentication and Security Layer) mechanism for your login credentials.<br><br>When SCRAM is enabled, {{agent}} uses the [SCRAM](https://en.wikipedia.org/wiki/Salted_Challenge_Response_Authentication_Mechanism) mechanism to authenticate the user credential. SCRAM is based on the IETF RFC5802 standard which describes a challenge-response mechanism for authenticating users.<br><br>* Plain - SCRAM is not used to authenticate<br>* SCRAM-SHA-256 - uses the SHA-256 hashing function<br>* SCRAM-SHA-512 - uses the SHA-512 hashing function<br><br>To prevent unauthorized access your Kafka password is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher.<br><br>Note that this setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://docs/reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.<br> |
| $$$kafka-output-authentication-ssl$$$<br>**SSL**<br> | Authenticate using the Secure Sockets Layer (SSL) protocol. Provide the following details for your SSL certificate:<br><br>Client SSL certificate<br>:   The certificate generated for the client. Copy and paste in the full contents of the certificate. This is the certificate that all the agents will use to connect to Kafka.<br><br>    In cases where each client has a unique certificate, the local path to that certificate can be placed here. The agents will pick the certificate in that location when establishing a connection to Kafka.<br><br><br>Client SSL certificate key<br>:   The private key generated for the client. This must be in PKCS 8 key. Copy and paste in the full contents of the certificate key. This is the certificate key that all the agents will use to connect to Kafka.<br><br>    In cases where each client has a unique certificate key, the local path to that certificate key can be placed here. The agents will pick the certificate key in that location when establishing a connection to Kafka.<br><br>    To prevent unauthorized access the certificate key is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the key as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher.<br><br>    Note that this setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://docs/reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.<br><br> |
| **Server SSL certificate authorities**<br> | The CA certificate to use to connect to Kafka. This is the CA used to generate the certificate and key for Kafka. Copy and paste in the full contents for the CA certificate.<br><br>This setting is optional. This setting is not available when the authentication `None` and `Plaintext` options are selected.<br><br>Click **Add row** to specify additional certificate authories.<br> |
| **Verification mode**<br> | Controls the verification of server certificates. Valid values are:<br><br>`Full`<br>:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.<br><br>`None`<br>:   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.<br><br>`Strict`<br>:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.<br><br>`Certificate`<br>:   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.<br><br>The default value is `Full`. This setting is not available when the authentication `None` and `Plaintext` options are selected.<br> |


### Partitioning settings [_partitioning_settings]

The number of partitions created is set automatically by the Kafka broker based on the list of topics. Records are then published to partitions either randomly, in round-robin order, or according to a calculated hash.

|     |     |
| --- | --- |
| $$$kafka-output-partitioning-random$$$<br>**Random**<br> | Publish records to Kafka output broker event partitions randomly. Specify the number of events to be published to the same partition before the partitioner selects a new partition.<br> |
| $$$kafka-output-partitioning-roundrobin$$$<br>**Round robin**<br> | Publish records to Kafka output broker event partitions in a round-robin fashion. Specify the number of events to be published to the same partition before the partitioner selects a new partition.<br> |
| $$$kafka-output-partitioning-hash$$$<br>**Hash**<br> | Publish records to Kafka output broker event partitions based on a hash computed from the specified list of fields. If a field is not specified, the Kafka event key value is used.<br> |


### Topics settings [_topics_settings]

Use this option to set the Kafka topic for each {{agent}} event.

|     |     |
| --- | --- |
| $$$kafka-output-topics-default$$$<br>**Default topic**<br> | Set a default topic to use for events sent by {{agent}} to the Kafka output.<br><br>You can set a static topic, for example `elastic-agent`, or you can choose to set a topic dynamically based on an [Elastic Common Scheme (ECS)][Elastic Common Schema (ECS)](ecs://docs/reference/index.md)) field. Available fields include:<br><br>* `data_stream_type`<br>* `data_stream.dataset`<br>* `data_stream.namespace`<br>* `@timestamp`<br>* `event-dataset`<br><br>You can also set a custom field. This is useful if you’re using the [`add_fields` processor](/reference/ingestion-tools/fleet/add_fields-processor.md) as part of your {{agent}} input. Otherwise, setting a custom field is not recommended.<br> |


### Header settings [_header_settings]

A header is a key-value pair, and multiple headers can be included with the same key. Only string values are supported. These headers will be included in each produced Kafka message.

|     |     |
| --- | --- |
| $$$kafka-output-headers-key$$$<br>**Key**<br> | The key to set in the Kafka header.<br> |
| $$$kafka-output-headers-value$$$<br>**Value**<br> | The value to set in the Kafka header.<br><br>Click **Add header** to configure additional headers to be included in each Kafka message.<br> |
| $$$kafka-output-headers-clientid$$$<br>**Client ID**<br> | The configurable ClientID used for logging, debugging, and auditing purposes. The default is `Elastic`. The Client ID is part of the protocol to identify where the messages are coming from.<br> |


### Compression settings [_compression_settings]

You can enable compression to reduce the volume of Kafka output.

|     |     |
| --- | --- |
| $$$kafka-output-compression-codec$$$<br>**Codec**<br> | Select a compression codec to use. Supported codecs are `snappy`, `lz4` and `gzip`.<br> |
| $$$kafka-output-compression-level$$$<br>**Level**<br> | For the `gzip` codec you can choose a compression level. The level must be in the range of `1` (best speed) to `9` (best compression).<br><br>Increasing the compression level reduces the network usage but increases the CPU usage. The default value is 4.<br> |


### Broker settings [_broker_settings]

Configure timeout and buffer size values for the Kafka brokers.

|     |     |
| --- | --- |
| $$$kafka-output-broker-timeout$$$<br>**Broker timeout**<br> | The maximum length of time a Kafka broker waits for the required number of ACKs before timing out (see the `ACK reliability` setting further in). The default is 30 seconds.<br> |
| $$$kafka-output-broker-reachability-timeout$$$<br>**Broker reachability timeout**<br> | The maximum length of time that an {{agent}} waits for a response from a Kafka broker before timing out. The default is 30 seconds.<br> |
| $$$kafka-output-broker-ack-reliability$$$<br>**ACK reliability**<br> | The ACK reliability level required from broker. Options are:<br><br>* Wait for local commit<br>* Wait for all replicas to commit<br>* Do not wait<br><br>The default is `Wait for local commit`.<br><br>Note that if ACK reliability is set to `Do not wait` no ACKs are returned by Kafka. Messages might be lost silently in the event of an error.<br> |


### Other settings [_other_settings]

|     |     |
| --- | --- |
| $$$kafka-output-other-key$$$<br>**Key**<br> | An optional formatted string specifying the Kafka event key. If configured, the event key can be extracted from the event using a format string.<br><br>See the [Kafka documentation](https://kafka.apache.org/intro#intro_topics) for the implications of a particular choice of key; by default, the key is chosen by the Kafka cluster.<br> |
| $$$kafka-output-other-proxy$$$<br>**Proxy**<br> | Select a proxy URL for {{agent}} to connect to Kafka. To learn about proxy configuration, refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md).<br> |
| $$$kafka-output-advanced-yaml-setting$$$<br>**Advanced YAML configuration**<br> | YAML settings that will be added to the Kafka output section of each policy that uses this output. Make sure you specify valid YAML. The UI does not currently provide validation.<br><br>See [Advanced YAML configuration](#kafka-output-settings-yaml-config) for descriptions of the available settings.<br> |
| $$$kafka-output-agent-integrations$$$<br>**Make this output the default for agent integrations**<br> | When this setting is on, {{agent}}s use this output to send data if no other output is set in the [agent policy](/reference/ingestion-tools/fleet/agent-policy.md).<br> |
| $$$kafka-output-agent-monitoring$$$<br>**Make this output the default for agent monitoring**<br> | When this setting is on, {{agent}}s use this output to send [agent monitoring data](/reference/ingestion-tools/fleet/monitor-elastic-agent.md) if no other output is set in the [agent policy](/reference/ingestion-tools/fleet/agent-policy.md).<br> |

## Advanced YAML configuration [kafka-output-settings-yaml-config]

|   Setting  | Description  |
| --- | --- |
| $$$output-kafka-fleet-settings-backoff.init-setting$$$<br>`backoff.init`<br> | (string) The number of seconds to wait before trying to reconnect to Kafka after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.<br><br>**Default:** `1s`<br> |
| $$$output-kafka-fleet-settings-backoff.max-setting$$$<br>`backoff.max`<br> | (string) The maximum number of seconds to wait before attempting to connect to Kafka after a network error.<br><br>**Default:** `60s`<br> |
| $$$output-kafka-fleet-settings-bulk_max_size-setting$$$<br>`bulk_max_size`<br> | (int) The maximum number of events to bulk in a single Kafka request.<br><br>**Default:** `2048`<br> |
| $$$output-kafka-fleet-settings-flush_frequency-setting$$$<br>`bulk_flush_frequency`<br> | (int) Duration to wait before sending bulk Kafka request. `0` is no delay.<br><br>**Default:** `0`<br> |
| $$$output-kafka-fleet-settings-channel_buffer_size-setting$$$<br>`channel_buffer_size`<br> | (int) Per Kafka broker number of messages buffered in output pipeline.<br><br>**Default:** `256`<br> |
| $$$output-kafka-fleet-settings-client_id-setting$$$<br>`client_id`<br> | (string) The configurable ClientID used for logging, debugging, and auditing purposes.<br><br>**Default:** `Elastic Agent`<br> |
| $$$output-kafka-fleet-settings-codec-setting$$$<br>`codec`<br> | Output codec configuration. You can specify either the `json` or `format` codec. By default the `json` codec is used.<br><br>**`json.pretty`**: If `pretty` is set to true, events will be nicely formatted. The default is false.<br><br>**`json.escape_html`**: If `escape_html` is set to true, html symbols will be escaped in strings. The default is false.<br><br>Example configuration that uses the `json` codec with pretty printing enabled to write events to the console:<br><br>```yaml<br>output.console:<br>  codec.json:<br> pretty: true<br>  escape_html: false<br>```<br><br>**`format.string`**: Configurable format string used to create a custom formatted message.<br><br>Example configurable that uses the `format` codec to print the events timestamp and message field to console:<br><br>```yaml<br>output.console:<br> codec.format:<br> string: '%{[@timestamp]} %{[message]}'<br>```<br><br>**Default:** `json`<br> |
| $$$output-kafka-fleet-settings-keep_alive-setting$$$<br>`keep_alive`<br> | (string) The keep-alive period for an active network connection. If `0s`, keep-alives are disabled.<br><br>**Default:** `0s`<br> |
| $$$output-kafka-fleet-settings-max_message_bytes-setting$$$<br>`max_message_bytes`<br> | (int) The maximum permitted size of JSON-encoded messages. Bigger messages will be dropped. This value should be equal to or less than the broker’s `message.max.bytes`.<br><br>**Default:** `1000000` (bytes)<br> |
| $$$output-kafka-fleet-settings-metadata-setting$$$<br>`metadata`<br> | Kafka metadata update settings. The metadata contains information about brokers, topics, partition, and active leaders to use for publishing.<br><br>**`refresh_frequency`**<br>:   Metadata refresh interval. Defaults to 10 minutes.<br><br>**`full`**<br>:   Strategy to use when fetching metadata. When this option is `true`, the client will maintain a full set of metadata for all the available topics. When set to `false` it will only refresh the metadata for the configured topics. The default is false.<br><br>**`retry.max`**<br>:   Total number of metadata update retries. The default is 3.<br><br>**`retry.backoff`**<br>:   Waiting time between retries. The default is 250ms.<br> |
| $$$output-kafka-fleet-settings-queue.mem.events-setting$$$<br>`queue.mem.events`<br> | The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.<br><br>**Default:** `3200 events`<br> |
| $$$output-kafka-fleet-settings-queue.mem.flush.min_events-setting$$$<br>`queue.mem.flush.min_events`<br> | `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`<br><br>**Default:** `1600 events`<br> |
| $$$output-kafka-fleet-settings-queue.mem.flush.timeout-setting$$$<br>`queue.mem.flush.timeout`<br> | (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.<br><br>**Default:** `10s`<br> |


## Kafka output and using {{ls}} to index data to {{es}} [kafka-output-settings-ls-warning]

If you are considering using {{ls}} to ship the data from `kafka` to {{es}}, please be aware the structure of the documents sent from {{agent}} to `kafka` must not be modified by {{ls}}. We suggest disabling `ecs_compatibility` on both the `kafka` input and the `json` codec in order to make sure the input doesn’t edit the fields and their contents.

The data streams setup by the integrations expect to receive events having the same structure and field names as they were sent directly from an {{agent}}.

The structure of the documents sent from {{agent}} to `kafka` must not be modified by {{ls}}. We suggest disabling `ecs_compatibility` on both the `kafka` input and the `json` codec.

Refer to the [{{ls}} output for {{agent}}](/reference/ingestion-tools/fleet/ls-output-settings.md) documentation for more details.

```yaml
inputs {
  kafka {
    ...
    ecs_compatibility => "disabled"
    codec => json { ecs_compatibility => "disabled" }
    ...
  }
}
...
```
