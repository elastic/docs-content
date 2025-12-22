---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kafka-output-settings.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Kafka output settings [kafka-output-settings]

Specify these settings to send data over a secure connection to Kafka. In the {{fleet}} [Output settings](/reference/fleet/fleet-settings.md#output-settings), make sure that the Kafka output type is selected.

::::{note}
If you plan to use {{ls}} to modify {{agent}} output data before it’s sent to Kafka, refer to our [guidance](#kafka-output-settings-ls-warning) for doing so, further in on this page.
::::



### General settings [_general_settings]

**Kafka version** $$$kafka-output-version$$$
:   The Kafka protocol version that {{agent}} will request when connecting. Defaults to `1.0.0`. Currently Kafka versions from `0.8.2.0` to `2.6.0` are supported, however the latest Kafka version (`3.x.x`) is expected to be compatible when version `2.6.0` is selected. When using Kafka 4.0 and newer, the version must be set to at least `2.1.0`.

**Hosts** $$$kafka-output-hosts$$$
:   The addresses your {{agent}}s will use to connect to one or more Kafka brokers. Use the format `host:port` (without any protocol `http://`). Click **Add row** to specify additional addresses.

    **Examples:**
    * `localhost:9092`
    * `mykafkahost:9092`

    Refer to the [{{fleet-server}}](/reference/fleet/fleet-server.md) documentation for default ports and other configuration details.


### Authentication settings [_authentication_settings]

Select the mechanism that {{agent}} uses to authenticate with Kafka.

**None** $$$kafka-output-authentication-none$$$
:   No authentication is used between {{agent}} and Kafka. This is the default option. In production, it’s recommended to have an authentication method selected.

    Plaintext
    :   Set this option for traffic between {{agent}} and Kafka to be sent as plaintext, without any transport layer security.

        This is the default option when no authentication is set.


    Encryption
    :   Set this option for traffic between {{agent}} and Kafka to use transport layer security.

        When **Encryption** is selected, the **Server SSL certificate authorities** and **Verification mode** mode options become available.


**Username / Password** $$$kafka-output-authentication-basic$$$
:   Connect to Kafka with a username and password.

    Provide your username and password, and select a SASL (Simple Authentication and Security Layer) mechanism for your login credentials.

    When SCRAM is enabled, {{agent}} uses the [SCRAM](https://en.wikipedia.org/wiki/Salted_Challenge_Response_Authentication_Mechanism) mechanism to authenticate the user credential. SCRAM is based on the IETF RFC5802 standard which describes a challenge-response mechanism for authenticating users.

    * Plain - SCRAM is not used to authenticate
    * SCRAM-SHA-256 - uses the SHA-256 hashing function
    * SCRAM-SHA-512 - uses the SHA-512 hashing function

    To prevent unauthorized access your Kafka password is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher.

    Note that this setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.

**SSL** $$$kafka-output-authentication-ssl$$$
:   Authenticate using the Secure Sockets Layer (SSL) protocol. Provide the following details for your SSL certificate:

    Client SSL certificate
    :   The certificate generated for the client. Copy and paste in the full contents of the certificate. This is the certificate that all the agents will use to connect to Kafka.

        In cases where each client has a unique certificate, the local path to that certificate can be placed here. The agents will pick the certificate in that location when establishing a connection to Kafka.


    Client SSL certificate key
    :   The private key generated for the client. This must be in PKCS 8 key. Copy and paste in the full contents of the certificate key. This is the certificate key that all the agents will use to connect to Kafka.

        In cases where each client has a unique certificate key, the local path to that certificate key can be placed here. The agents will pick the certificate key in that location when establishing a connection to Kafka.

        To prevent unauthorized access the certificate key is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the key as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher.

        Note that this setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.

**Server SSL certificate authorities**
:   The CA certificate to use to connect to Kafka. This is the CA used to generate the certificate and key for Kafka. Copy and paste in the full contents for the CA certificate.

    This setting is optional. This setting is not available when the authentication `None` and `Plaintext` options are selected.

    Click **Add row** to specify additional certificate authories.

**Verification mode**
:   Controls the verification of server certificates. Valid values are:

    `Full`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.

    `None`
    :   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.

    `Strict`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.

    `Certificate`
    :   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.

    The default value is `Full`. This setting is not available when the authentication `None` and `Plaintext` options are selected.


### Partitioning settings [_partitioning_settings]

The number of partitions created is set automatically by the Kafka broker based on the list of topics. Records are then published to partitions either randomly, in round-robin order, or according to a calculated hash.

**Random** $$$kafka-output-partitioning-random$$$
:   Publish records to Kafka output broker event partitions randomly. Specify the number of events to be published to the same partition before the partitioner selects a new partition.

**Round robin** $$$kafka-output-partitioning-roundrobin$$$
:   Publish records to Kafka output broker event partitions in a round-robin fashion. Specify the number of events to be published to the same partition before the partitioner selects a new partition.

**Hash** $$$kafka-output-partitioning-hash$$$
:   Publish records to Kafka output broker event partitions based on a hash computed from the specified list of fields. If a field is not specified, the Kafka event key value is used.


### Topics settings [_topics_settings]

Use this option to set the Kafka topic for each {{agent}} event.

**Default topic** $$$kafka-output-topics-default$$$
:   Set the default Kafka topic used for events sent by {{agent}}.

    You can set a static topic, for example `elastic-agent`, or you can choose to set a topic dynamically based on an [Elastic Common Schema (ECS)](ecs://reference/index.md) field. Available fields include:

    * `data_stream.type`
    * `data_stream.dataset`
    * `data_stream.namespace`
    * `@timestamp`
    * `event.dataset`

    You can also set a custom field. This is useful if you need to construct a more complex or structured topic name. For example, you can use the `fields.kafka_topic` custom field to set a dynamic topic for each event.
    
    To set a dynamic topic value for outputting {{agent}} data to Kafka, you can add the [`add_fields` processor](/reference/fleet/add_fields-processor.md) to any integration policies on your {{fleet}}-managed {{agents}}.
    
    For example, the following `add_fields` processor creates a dynamic topic value for the `fields.kafka_topic` field by interpolating multiple [data stream fields](ecs://reference/ecs-data_stream.md):

    ```yaml
    - add_fields:
        target: ''
        fields: 
          kafka_topic: '${data_stream.type}-${data_stream.dataset}-${data_stream.namespace}' <1>
    ```
    1. Depending on the values of the data stream fields, this generates topic names such as `logs-nginx.access-production` or `metrics-system.cpu-staging` as the value of the custom `kafka_topic` field.

    For more information, refer to [](/reference/fleet/agent-processors.md).


### Header settings [_header_settings]

A header is a key-value pair, and multiple headers can be included with the same key. Only string values are supported. These headers will be included in each produced Kafka message.

**Key** $$$kafka-output-headers-key$$$
:   The key to set in the Kafka header.

**Value** $$$kafka-output-headers-value$$$
:   The value to set in the Kafka header.

    Click **Add header** to configure additional headers to be included in each Kafka message.

**Client ID** $$$kafka-output-headers-clientid$$$
:   The configurable ClientID used for logging, debugging, and auditing purposes. The default is `Elastic`. The Client ID is part of the protocol to identify where the messages are coming from.


### Compression settings [_compression_settings]

You can enable compression to reduce the volume of Kafka output.

**Codec** $$$kafka-output-compression-codec$$$
:   Select a compression codec to use. Supported codecs are `snappy`, `lz4` and `gzip`.

**Level** $$$kafka-output-compression-level$$$
:   For the `gzip` codec you can choose a compression level. The level must be in the range of `1` (best speed) to `9` (best compression).

    Increasing the compression level reduces the network usage but increases the CPU usage. The default value is 4.


### Broker settings [_broker_settings]

Configure timeout and buffer size values for the Kafka brokers.

**Broker timeout** $$$kafka-output-broker-timeout$$$
:   The maximum length of time a Kafka broker waits for the required number of ACKs before timing out (see the `ACK reliability` setting further in). The default is 30 seconds.

**Broker reachability timeout** $$$kafka-output-broker-reachability-timeout$$$
:   The maximum length of time that an {{agent}} waits for a response from a Kafka broker before timing out. The default is 30 seconds.

**ACK reliability** $$$kafka-output-broker-ack-reliability$$$
:   The ACK reliability level required from broker. Options are:

    * Wait for local commit
    * Wait for all replicas to commit
    * Do not wait

    The default is `Wait for local commit`.

    Note that if ACK reliability is set to `Do not wait` no ACKs are returned by Kafka. Messages might be lost silently in the event of an error.


### Other settings [_other_settings]

**Key** $$$kafka-output-other-key$$$
:   An optional formatted string specifying the Kafka event key. If configured, the event key can be extracted from the event using a format string.

    See the [Kafka documentation](https://kafka.apache.org/intro#intro_topics) for the implications of a particular choice of key; by default, the key is chosen by the Kafka cluster.

**Proxy** $$$kafka-output-other-proxy$$$
:   Select a proxy URL for {{agent}} to connect to Kafka. To learn about proxy configuration, refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/fleet/fleet-agent-proxy-support.md).

**Advanced YAML configuration** $$$kafka-output-advanced-yaml-setting$$$
:   YAML settings that will be added to the Kafka output section of each policy that uses this output. Make sure you specify valid YAML. The UI does not currently provide validation.

    See [Advanced YAML configuration](#kafka-output-settings-yaml-config) for descriptions of the available settings.

**Make this output the default for agent integrations** $$$kafka-output-agent-integrations$$$
:   When this setting is on, {{agent}}s use this output to send data if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).

**Make this output the default for agent monitoring** $$$kafka-output-agent-monitoring$$$
:   When this setting is on, {{agent}}s use this output to send [agent monitoring data](/reference/fleet/monitor-elastic-agent.md) if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).

## Advanced YAML configuration [kafka-output-settings-yaml-config]

`backoff.init` $$$output-kafka-fleet-settings-backoff.init-setting$$$
:   (string) The number of seconds to wait before trying to reconnect to Kafka after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.

    **Default:** `1s`

`backoff.max` $$$output-kafka-fleet-settings-backoff.max-setting$$$
:   (string) The maximum number of seconds to wait before attempting to connect to Kafka after a network error.

    **Default:** `60s`

`bulk_max_size` $$$output-kafka-fleet-settings-bulk_max_size-setting$$$
:   (int) The maximum number of events to bulk in a single Kafka request.

    **Default:** `2048`

`bulk_flush_frequency` $$$output-kafka-fleet-settings-flush_frequency-setting$$$
:   (int) Duration to wait before sending bulk Kafka request. `0` is no delay.

    **Default:** `0`

`channel_buffer_size` $$$output-kafka-fleet-settings-channel_buffer_size-setting$$$
:   (int) Per Kafka broker number of messages buffered in output pipeline.

    **Default:** `256`

`client_id` $$$output-kafka-fleet-settings-client_id-setting$$$
:   (string) The configurable ClientID used for logging, debugging, and auditing purposes.

    **Default:** `Elastic Agent`

`codec` $$$output-kafka-fleet-settings-codec-setting$$$
:   Output codec configuration. You can specify either the `json` or `format` codec. By default the `json` codec is used.

    **`json.pretty`**: If `pretty` is set to true, events will be nicely formatted. The default is false.

    **`json.escape_html`**: If `escape_html` is set to true, html symbols will be escaped in strings. The default is false.

    Example configuration that uses the `json` codec with pretty printing enabled to write events to the console:

    ```yaml
    output.console:
      codec.json:
     pretty: true
      escape_html: false
    ```

    **`format.string`**: Configurable format string used to create a custom formatted message.

    Example configurable that uses the `format` codec to print the events timestamp and message field to console:

    ```yaml
    output.console:
     codec.format:
     string: '%{[@timestamp]} %{[message]}'
    ```

    **Default:** `json`

`keep_alive` $$$output-kafka-fleet-settings-keep_alive-setting$$$
:   (string) The keep-alive period for an active network connection. If `0s`, keep-alives are disabled.

    **Default:** `0s`

`max_message_bytes` $$$output-kafka-fleet-settings-max_message_bytes-setting$$$
:   (int) The maximum permitted size of JSON-encoded messages. Bigger messages will be dropped. This value should be equal to or less than the broker’s `message.max.bytes`.

    **Default:** `1000000` (bytes)

`metadata` $$$output-kafka-fleet-settings-metadata-setting$$$
:   Kafka metadata update settings. The metadata contains information about brokers, topics, partition, and active leaders to use for publishing.

    **`refresh_frequency`**
    :   Metadata refresh interval. Defaults to 10 minutes.

    **`full`**
    :   Strategy to use when fetching metadata. When this option is `true`, the client will maintain a full set of metadata for all the available topics. When set to `false` it will only refresh the metadata for the configured topics. The default is false.

    **`retry.max`**
    :   Total number of metadata update retries. The default is 3.

    **`retry.backoff`**
    :   Waiting time between retries. The default is 250ms.

`queue.mem.events` $$$output-kafka-fleet-settings-queue.mem.events-setting$$$
:   The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.

    **Default:** `3200 events`

`queue.mem.flush.min_events` $$$output-kafka-fleet-settings-queue.mem.flush.min_events-setting$$$
:   `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`

    **Default:** `1600 events`

`queue.mem.flush.timeout` $$$output-kafka-fleet-settings-queue.mem.flush.timeout-setting$$$
:   (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.

    **Default:** `10s`


## Kafka output and using {{ls}} to index data to {{es}} [kafka-output-settings-ls-warning]

If you are considering using {{ls}} to ship the data from `kafka` to {{es}}, be aware the structure of the documents sent from {{agent}} to `kafka` must not be modified by {{ls}}. We suggest disabling `ecs_compatibility` on both the `kafka` input and the `json` codec in order to make sure the input doesn’t edit the fields and their contents.

The data streams setup by the integrations expect to receive events having the same structure and field names as they were sent directly from an {{agent}}.

The structure of the documents sent from {{agent}} to `kafka` must not be modified by {{ls}}. We suggest disabling `ecs_compatibility` on both the `kafka` input and the `json` codec.

Refer to the [{{ls}} output for {{agent}}](/reference/fleet/ls-output-settings.md) documentation for more details.

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
