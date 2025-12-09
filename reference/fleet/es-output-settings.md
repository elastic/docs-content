---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/es-output-settings.html
products:
  - id: fleet
  - id: elastic-agent
---

# Elasticsearch output settings [es-output-settings]

Specify these settings to send data over a secure connection to {{es}}. In the {{fleet}} [Output settings](/reference/fleet/fleet-settings.md#output-settings), make sure that {{es}} output type is selected.

|     |     |
| --- | --- |

**Hosts** $$$es-output-hosts-setting$$$
:   The {{es}} URLs where {{agent}}s will send data. By default, {{es}} is exposed on the following ports:

    `9200`
    :   Default {{es}} port for self-managed clusters

    `443`
    :   Default {{es}} port for {{ecloud}}

    **Examples:**
    * `https://192.0.2.0:9200`
    * `https://1d7a52f5eb344de18ea04411fe09e564.fleet.eu-west-1.aws.qa.cld.elstc.co:443`
    * `https://[2001:db8::1]:9200`

    Refer to the [{{fleet-server}}](/reference/fleet/fleet-server.md) documentation for default ports and other configuration details.

**{{es}} CA trusted fingerprint** $$$es-trusted-fingerprint-yaml-setting$$$
:   HEX encoded SHA-256 of a CA certificate. If this certificate is present in the chain during the handshake, it will be added to the `certificate_authorities` list and the handshake will continue normally. To learn more about trusted fingerprints, refer to the [{{es}} security documentation](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).

**Proxy** $$$es-agent-proxy-output$$$
:   Select a proxy URL for {{agent}} to connect to {{es}}. To learn about proxy configuration, refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/fleet/fleet-agent-proxy-support.md).

**Advanced YAML configuration** $$$es-output-advanced-yaml-setting$$$
:   YAML settings that will be added to the {{es}} output section of each policy that uses this output. Make sure you specify valid YAML. The UI does not currently provide validation.
    See [Advanced YAML configuration](#es-output-settings-yaml-config) for descriptions of the available settings.

**Make this output the default for agent integrations** $$$es-agent-integrations-output$$$
:   When this setting is on, {{agent}}s use this output to send data if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).

**Make this output the default for agent monitoring** $$$es-agent-monitoring-output$$$
:   When this setting is on, {{agent}}s use this output to send [agent monitoring data](/reference/fleet/monitor-elastic-agent.md) if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).

**Performance tuning** $$$es-agent-performance-tuning$$$
:   Choose one of the menu options to tune your {{agent}} performance when sending data to an {{es}} output. You can optimize for throughput, scale, latency, or you can choose a balanced (the default) set of performance specifications. Refer to [Performance tuning settings](#es-output-settings-performance-tuning-settings) for details about the setting values and their potential impact on performance.

    You can also use the [Advanced YAML configuration](#es-output-settings-yaml-config) field to set custom values. Note that if you adjust any of the performance settings described in the following **Advanced YAML configuration** section, the **Performance tuning** option automatically changes to `Custom` and cannot be changed.

    Performance tuning preset values take precedence over any settings that may be defined separately. If you want to change any setting, you need to use the `Custom` **Performance tuning** option and specify the settings in the **Advanced YAML configuration** field.

    For example, if you would like to use the balanced preset values except that you prefer a higher compression level, you can do so as follows:
    1. In {{fleet}}, open the **Settings** tab.
    2. In the **Outputs** section, select **Add output** to create a new output, or select the edit icon to edit an existing output.
    3. In the **Add new output** or the **Edit output** flyout, set **Performance tuning** to `Custom`.
    4. Refer to the list of [performance tuning preset values](#es-output-settings-performance-tuning-settings), and add the settings you prefer into the **Advanced YAML configuration** field. For the `balanced` presets, the yaml configuration would be as shown:

      ```yaml
      bulk_max_size: 1600
      worker: 1
      queue.mem.events: 3200
      queue.mem.flush.min_events: 1600
      queue.mem.flush.timeout: 10s
      compression_level: 1
      idle_connection_timeout: 3s
      ```

    5. Adjust any settings as preferred. For example, you can update the `compression_level` setting to `4`.
    When you create an {{agent}} policy using this output, the output will use the balanced preset options except with the higher compression level, as specified.

**Write to logs streams** {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2`
:   When this setting is on, `logs` and `logs.*` are added to the output streams configuration in the agent policy using this output. Enabling this setting is only part of the process for allowing {{agent}} to send data to [wired streams](/solutions/observability/streams/streams.md#streams-wired-streams). For additional required steps, refer to [Ship data to streams > {{fleet}}](/solutions/observability/streams/wired-streams.md#streams-wired-streams-ship).

## Advanced YAML configuration [es-output-settings-yaml-config]

`allow_older_versions` $$$output-elasticsearch-fleet-settings-allow_older_versions-setting$$$
:   Allow {{agent}} to connect and send output to an {{es}} instance that is running an earlier version than the agent version.
    This setting does not affect {{agent}}'s ability to connect to {{fleet-server}}. {{fleet-server}} will not accept a connection from an agent at a later major or minor version. It will accept a connection from an agent at a later patch version. For example, an {{agent}} at version 8.14.3 can connect to a {{fleet-server}} on version 8.14.0, but an agent at version 8.15.0 or later is not able to connect.

    **Default:** `true`

`backoff.init` $$$output-elasticsearch-fleet-settings-backoff.init-setting$$$
:   (string) The number of seconds to wait before trying to reconnect to {{es}} after a network error. After waiting `backoff.init` seconds, {{agent}} tries to reconnect. If the attempt fails, the backoff timer is increased exponentially up to `backoff.max`. After a successful connection, the backoff timer is reset.

    **Default:** `1s`

`backoff.max` $$$output-elasticsearch-fleet-settings-backoff.max-setting$$$
:   (string) The maximum number of seconds to wait before attempting to connect to {{es}} after a network error.

    **Default:** `60s`

`bulk_max_size` $$$output-elasticsearch-fleet-settings-bulk_max_size-setting$$$
:   (int) The maximum number of events to bulk in a single {{es}} bulk API index request.
    Events can be collected into batches. {{agent}} will split batches larger than `bulk_max_size` into multiple batches.
    Specifying a larger batch size can improve performance by lowering the overhead of sending events. However big batch sizes can also increase processing times, which might result in API errors, killed connections, timed-out publishing requests, and, ultimately, lower throughput.
    Setting `bulk_max_size` to values less than or equal to 0 turns off the splitting of batches. When splitting is disabled, the queue decides on the number of events to be contained in a batch.

    **Default:** `1600`

`compression_level` $$$output-elasticsearch-fleet-settings-compression_level-setting$$$
:   (int) The gzip compression level. Set this value to `0` to disable compression. The compression level must be in the range of `1` (best speed) to `9` (best compression).
    Increasing the compression level reduces network usage but increases CPU usage.

`max_retries` $$$output-elasticsearch-fleet-settings-max_retries-setting$$$
:   (int) The number of times to retry publishing an event after a publishing failure. After the specified number of retries, the events are typically dropped.
    Set `max_retries` to a value less than 0 to retry until all events are published.

    **Default:** `3`

`queue.mem.events` $$$output-elasticsearch-fleet-settings-queue.mem.events-setting$$$
:   The number of events the queue can store. This value should be evenly divisible by the smaller of `queue.mem.flush.min_events` or `bulk_max_size` to avoid sending partial batches to the output.

    **Default:** `3200 events`

`queue.mem.flush.min_events` $$$output-elasticsearch-fleet-settings-queue.mem.flush.min_events-setting$$$
:   `flush.min_events` is a legacy parameter, and new configurations should prefer to control batch size with `bulk_max_size`. As of 8.13, there is never a performance advantage to limiting batch size with `flush.min_events` instead of `bulk_max_size`

    **Default:** `1600 events`

`queue.mem.flush.timeout` $$$output-elasticsearch-fleet-settings-queue.mem.flush.timeout-setting$$$
:   (int) The maximum wait time for `queue.mem.flush.min_events` to be fulfilled. If set to 0s, events are available to the output immediately.

    **Default:** `10s`

`timeout` $$$output-elasticsearch-fleet-settings-timeout-setting$$$
:   (string) The HTTP request timeout in seconds for the {{es}} request.

    **Default:** `90s`

`worker` $$$output-elasticsearch-fleet-settings-worker-setting$$$
:   (int) The number of workers per configured host publishing events. Example: If you have two hosts and three workers, in total six workers are started (three for each host).

    **Default:** `1`

`status_reporting.enabled` $$$output-elasticsearch-fleet-settings-status_reporting.enabled-setting$$$
:   (boolean) Whether status reporting is enabled for this output. When disabled, the output does not change its health status if there is a connectivity problem.

    **Default:** `true`

## Performance tuning settings [es-output-settings-performance-tuning-settings]

| Configuration | Balanced | Optimized for Throughput | Optimized for Scale | Optimized for Latency |
| --- | --- | --- | --- | --- |
| `bulk_max_size` | 1600 | 1600 | 1600 | 50 |
| `worker` | 1 | 4 | 1 | 1 |
| `queue.mem.events` | 3200 | 12800 | 3200 | 4100 |
| `queue.mem.flush.min_events` | 1600 | 1600 | 1600 | 2050 |
| `queue.mem.flush.timeout` | 10 | 5 | 20 | 1 |
| `compression_level` | 1 | 1 | 1 | 1 |
| `idle_connection_timeout` | 3 | 15 | 1 | 60 |

For descriptions of each setting, refer to [Advanced YAML configuration](#es-output-settings-yaml-config). For the  `queue.mem.events`, `queue.mem.flush.min_events` and `queue.mem.flush.timeout` settings, refer to the [internal queue configuration settings](beats://reference/filebeat/configuring-internal-queue.md) in the {{filebeat}} documentation.

`Balanced` represents the new default setting (out of the box behavior). Relative to `Balanced`, `Optimized for throughput` setting will improve EPS by 4 times, `Optimized for Scale` will perform on par and `Optimized for Latency` will show a 20% degredation in EPS (Events Per Second). These relative performance numbers were calculated from a performance testbed which operates in a controlled setting ingesting a large log file.

As mentioned, the `custom` preset allows you to input your own set of parameters for a finer tuning of performance. The following table is a summary of a few data points and how the resulting EPS compares to the `Balanced` setting mentioned above.

These presets apply only to agents on version 8.12.0 or later.

| worker | bulk_max_size | queue.mem.events | queue.mem.flush.min_events | queue.mem.flush.timeout | idle_connection_timeout | Relative EPS |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1600 | 3200 | 1600 | 5 | 15 | 1x |
| 1 | 2048 | 4096 | 2048 | 5 | 15 | 1x |
| 1 | 4096 | 8192 | 4096 | 5 | 15 | 1x |
| 2 | 1600 | 6400 | 1600 | 5 | 15 | 2x |
| 2 | 2048 | 8192 | 2048 | 5 | 15 | 2x |
| 2 | 4096 | 16384 | 4096 | 5 | 15 | 2x |
| 4 | 1600 | 12800 | 1600 | 5 | 15 | 3.6x |
| 4 | 2048 | 16384 | 2048 | 5 | 15 | 3.6x |
| 4 | 4096 | 32768 | 4096 | 5 | 15 | 3.6x |
| 8 | 1600 | 25600 | 1600 | 5 | 15 | 5.3x |
| 8 | 2048 | 32768 | 2048 | 5 | 15 | 5.1x |
| 8 | 4096 | 65536 | 4096 | 5 | 15 | 5.2x |
| 16 | 1600 | 51200 | 1600 | 5 | 15 | 5.3x |
| 16 | 2048 | 65536 | 2048 | 5 | 15 | 5.2x |
| 16 | 4096 | 131072 | 4096 | 5 | 15 | 5.3x |
