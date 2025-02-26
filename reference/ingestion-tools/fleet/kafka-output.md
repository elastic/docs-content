---
navigation_title: "Kafka"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kafka-output.html
---

# Kafka output [kafka-output]


The Kafka output sends events to Apache Kafka.

**Compatibility:** This output can connect to Kafka version 0.8.2.0 and later. Older versions might work as well, but are not supported.

This example configures a Kafka output called `kafka-output` in the {{agent}} `elastic-agent.yml` file, with settings as described further in:

```yaml
outputs:
  kafka-output:
    type: kafka
    hosts:
      - 'kafka1:9092'
      - 'kafka2:9092'
      - 'kafka3:9092'
    client_id: Elastic
    version: 1.0.0
    compression: gzip
    compression_level: 4
    username: <my-kafka-username>
    password: <my-kakfa-password>
    sasl:
      mechanism: SCRAM-SHA-256
    partition:
      round_robin:
        group_events: 1
    topic: 'elastic-agent'
    headers: []
    timeout: 30
    broker_timeout: 30
    required_acks: 1
    ssl:
      verification_mode: full
```

## Kafka output and using {{ls}} to index data to {{es}} [_kafka_output_and_using_ls_to_index_data_to_es]

If you are considering using {{ls}} to ship the data from `kafka` to {{es}}, please be aware the structure of the documents sent from {{agent}} to `kafka` must not be modified by {{ls}}. We suggest disabling `ecs_compatibility` on both the `kafka` input and the `json` codec in order to make sure the input doesn’t edit the fields and their contents.

The data streams set up by the integrations expect to receive events having the same structure and field names as they were sent directly from an {{agent}}.

Refer to [{{ls}} output for {{agent}}](/reference/ingestion-tools/fleet/logstash-output.md) documentation for more details.

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


## Kafka output configuration settings [_kafka_output_configuration_settings]

The `kafka` output supports the following settings, grouped by category. Many of these settings have sensible defaults that allow you to run {{agent}} with minimal configuration.

* [Kafka output configuration settings](#output-kafka-commonly-used-settings)
* [Authentication settings](#output-kafka-authentication-settings)
* [Memory queue settings](#output-kafka-memory-queue-settings)
* [Topics settings](#output-kafka-topics-settings)
* [Partition settings](#output-kafka-partition-settings)
* [Header settings](#output-kafka-header-settings)
* [Other configuration settings](#output-kafka-configuration-settings)

## Commonly used settings [output-kafka-commonly-used-settings]

| Setting | Description |
| --- | --- |
| $$$output-kafka-enabled-setting$$$<br>`enabled`<br> | (boolean) Enables or disables the output. If set to `false`, the output is disabled.<br> |
| $$$kafka-hosts-setting$$$<br>`hosts`<br> | The addresses your {{agent}}s will use to connect to one or more Kafka brokers.<br><br>Following is an example `hosts` setting with three hosts defined:<br><br>```yaml<br>    hosts:<br>      - 'localhost:9092'<br>      - 'mykafkahost01:9092'<br>      - 'mykafkahost02:9092'<br>```<br> |
| $$$kafka-version-setting$$$<br>`version`<br> | Kafka protocol version that {{agent}} will request when connecting. Defaults to 1.0.0.<br><br>The protocol version controls the Kafka client features available to {{agent}}; it does not prevent {{agent}} from connecting to Kafka versions newer than the protocol version.<br> |


## Authentication settings [output-kafka-authentication-settings]

| Setting | Description |
| --- | --- |
| $$$kafka-username-setting$$$<br>`username`<br> | The username for connecting to Kafka. If username is configured, the password must be configured as well.<br> |
| $$$kafka-password-setting$$$<br>`password`<br> | The password for connecting to Kafka.<br> |
| $$$kafka-sasl.mechanism-setting$$$<br>`sasl.mechanism`<br> | The SASL mechanism to use when connecting to Kafka. It can be one of:<br><br>* `PLAIN` for SASL/PLAIN.<br>* `SCRAM-SHA-256` for SCRAM-SHA-256.<br>* `SCRAM-SHA-512` for SCRAM-SHA-512. If `sasl.mechanism` is not set, `PLAIN` is used if `username` and `password` are provided. Otherwise, SASL authentication is disabled.<br> |
| $$$kafka-ssl-setting$$$<br>`ssl`<br> | When sending data to a secured cluster through the `kafka` output, {{agent}} can use SSL/TLS. For a list of available settings, refer to [SSL/TLS](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md), specifically the settings under [Table 7, Common configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md#client-ssl-options).<br> |


## Memory queue settings [output-kafka-memory-queue-settings]

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
| $$$output-kafka-queue.mem.events-setting$$$<br>`queue.mem.events`<br> | The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.<br><br>**Default:** `3200 events`<br> |
| $$$output-kafka-queue.mem.flush.min_events-setting$$$<br>`queue.mem.flush.min_events`<br> | `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`<br><br>**Default:** `1600 events`<br> |
| $$$output-kafka-queue.mem.flush.timeout-setting$$$<br>`queue.mem.flush.timeout`<br> | (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.<br><br>**Default:** `10s`<br> |


## Topics settings [output-kafka-topics-settings]

Use these options to set the Kafka topic for each {{agent}} event.

| Setting | Description |
| --- | --- |
| $$$kafka-topic-setting$$$<br>`topic`<br> | The default Kafka topic used for produced events.<br> |


## Partition settings [output-kafka-partition-settings]

The number of partitions created is set automatically by the Kafka broker based on the list of topics. Records are then published to partitions either randomly, in round-robin order, or according to a calculated hash.

In the following example, after each event is published to a partition, the partitioner selects the next partition in round-robin fashion.

```yaml
    partition:
      round_robin:
        group_events: 1
```

| Setting | Description |
| --- | --- |
| $$$kafka-random.group-events-setting$$$<br>`random.group_events`<br> | Sets the number of events to be published to the same partition, before the partitioner selects a new partition by random. The default value is 1 meaning after each event a new partition is picked randomly.<br> |
| $$$kafka-round_robin.group_events-setting$$$<br>`round_robin.group_events`<br> | Sets the number of events to be published to the same partition, before the partitioner selects the next partition. The default value is 1 meaning after each event the next partition will be selected.<br> |
| $$$kafka-hash.hash-setting$$$<br>`hash.hash`<br> | List of fields used to compute the partitioning hash value from. If no field is configured, the events key value will be used.<br> |
| $$$kafka-hash.random-setting$$$<br>`hash.random`<br> | Randomly distribute events if no hash or key value can be computed.<br> |


## Header settings [output-kafka-header-settings]

A header is a key-value pair, and multiple headers can be included with the same key. Only string values are supported. These headers will be included in each produced Kafka message.

| Setting | Description |
| --- | --- |
| $$$kafka-key-setting$$$<br>`key`<br> | The key to set in the Kafka header.<br> |
| $$$kafka-value-setting$$$<br>`value`<br> | The value to set in the Kafka header.<br> |
| $$$kafka-client_id-setting$$$<br>`client_id`<br> | The configurable ClientID used for logging, debugging, and auditing purposes. The default is `Elastic`. The Client ID is part of the protocol to identify where the messages are coming from.<br> |


## Other configuration settings [output-kafka-configuration-settings]

You can specify these various other options in the `kafka-output` section of the agent configuration file.

| Setting | Description |
| --- | --- |
| $$$output-kafka-backoff.init-setting$$$<br>`backoff.init`<br> | (string) The number of seconds to wait before trying to reconnect to Kafka after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.<br><br>**Default:** `1s`<br> |
| $$$kafka-backoff.max-setting$$$<br>`backoff.max`<br> | (string) The maximum number of seconds to wait before attempting to connect to Kafka after a network error.<br><br>**Default:** `60s`<br> |
| $$$kafka-broker_timeout-setting$$$<br>`broker_timeout`<br> | The maximum length of time a Kafka broker waits for the required number of ACKs before timing out (see the `required_acks` setting further in).<br><br>**Default:** `30` (seconds)<br> |
| $$$kafka-bulk_flush_frequency-setting$$$<br>`bulk_flush_frequency`<br> | (int) Duration to wait before sending bulk Kafka request. `0`` is no delay.<br><br>**Default:** `0`<br> |
| $$$kafka-bulk_max_size-setting$$$<br>`bulk_max_size`<br> | (int) The maximum number of events to bulk in a single Kafka request.<br><br>**Default:** `2048`<br> |
| $$$kafka-channel_buffer_size-setting$$$<br>`channel_buffer_size`<br> | (int) Per Kafka broker number of messages buffered in output pipeline.<br><br>**Default:** `256`<br> |
| $$$kafka-codec-setting$$$<br>`codec`<br> | Output codec configuration. You can specify either the `json` or `format` codec. By default the `json` codec is used.<br><br>**`json.pretty`**: If `pretty` is set to true, events will be nicely formatted. The default is false.<br><br>**`json.escape_html`**: If `escape_html` is set to true, html symbols will be escaped in strings. The default is false.<br><br>Example configuration that uses the `json` codec with pretty printing enabled to write events to the console:<br><br>```yaml<br>output.console:<br>  codec.json:<br>    pretty: true<br>    escape_html: false<br>```<br><br>**`format.string`**: Configurable format string used to create a custom formatted message.<br><br>Example configurable that uses the `format` codec to print the events timestamp and message field to console:<br><br>```yaml<br>output.console:<br>  codec.format:<br>    string: '%{[@timestamp]} %{[message]}'<br>```<br> |
| $$$kafka-compression-setting$$$<br>`compression`<br> | Select a compression codec to use. Supported codecs are `snappy`, `lz4` and `gzip`.<br> |
| $$$kafka-compression_level-setting$$$<br>`compression_level`<br> | For the `gzip` codec you can choose a compression level. The level must be in the range of `1` (best speed) to `9` (best compression).<br><br>Increasing the compression level reduces the network usage but increases the CPU usage.<br><br>**Default:** `4`.<br> |
| $$$kafka-keep_alive-setting$$$<br>`keep_alive`<br> | (string) The keep-alive period for an active network connection. If `0s`, keep-alives are disabled.<br><br>**Default:** `0s`<br> |
| $$$kafka-max_message_bytes-setting$$$<br>`max_message_bytes`<br> | (int) The maximum permitted size of JSON-encoded messages. Bigger messages will be dropped. This value should be equal to or less than the broker’s `message.max.bytes`.<br><br>**Default:** `1000000` (bytes)<br> |
| $$$kafka-metadata-setting$$$<br>`metadata`<br> | Kafka metadata update settings. The metadata contains information about brokers, topics, partition, and active leaders to use for publishing.<br><br>**`refresh_frequency`**<br>:   Metadata refresh interval. Defaults to 10 minutes.<br><br>**`full`**<br>:   Strategy to use when fetching metadata. When this option is `true`, the client will maintain a full set of metadata for all the available topics. When set to `false` it will only refresh the metadata for the configured topics. The default is false.<br><br>**`retry.max`**<br>:   Total number of metadata update retries. The default is 3.<br><br>**`retry.backoff`**<br>:   Waiting time between retries. The default is 250ms.<br> |
| $$$kafka-required_acks-setting$$$<br>`required_acks`<br> | The ACK reliability level required from broker. 0=no response, 1=wait for local commit, -1=wait for all replicas to commit. The default is 1.<br><br>Note: If set to 0, no ACKs are returned by Kafka. Messages might be lost silently on error.<br><br>**Default:** `1` (wait for local commit)<br> |
| $$$kafka-timeout-setting$$$<br>`timeout`<br> | The number of seconds to wait for responses from the Kafka brokers before timing out. The default is 30 (seconds).<br><br>**Default:** `1000000` (bytes)<br> |


