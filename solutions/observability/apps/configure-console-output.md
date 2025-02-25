---
navigation_title: "Console"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-console-output.html
applies_to:
  stack: all
---



# Configure the Console output [apm-console-output]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

The Console output is not yet supported by {{fleet}}-managed APM Server.

::::


The Console output writes events in JSON format to stdout.

::::{warning}
The Console output should be used only for debugging issues as it can produce a large amount of logging data.
::::


To use this output, edit the APM Server configuration file to disable the {{es}} output by commenting it out, and enable the console output by adding `output.console`.

Example configuration:

```yaml
output.console:
  pretty: true
```


## Configuration options [_configuration_options_7]

You can specify the following `output.console` options in the `apm-server.yml` config file:


### `enabled` [_enabled_6]

The enabled config is a boolean setting to enable or disable the output. If set to false, the output is disabled.

The default value is `true`.


### `pretty` [_pretty]

If `pretty` is set to true, events written to stdout will be nicely formatted. The default is false.


### `codec` [_codec_3]

Output codec configuration. If the `codec` section is missing, events will be JSON encoded using the `pretty` option.

See [Change the output codec](#apm-configuration-output-codec) for more information.


### `bulk_max_size` [_bulk_max_size_4]

The maximum number of events to buffer internally during publishing. The default is 2048.

Specifying a larger batch size may add some latency and buffering during publishing. However, for Console output, this setting does not affect how events are published.

Setting `bulk_max_size` to values less than or equal to 0 disables the splitting of batches. When splitting is disabled, the queue decides on the number of events to be contained in a batch.


## Change the output codec [apm-configuration-output-codec]

For outputs that do not require a specific encoding, you can change the encoding by using the codec configuration. You can specify either the `json` or `format` codec. By default the `json` codec is used.

**`json.pretty`**: If `pretty` is set to true, events will be nicely formatted. The default is false.

**`json.escape_html`**: If `escape_html` is set to true, HTML symbols will be escaped in strings. The default is false.

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

