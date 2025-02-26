---
navigation_title: "dissect"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/dissect-processor.html
---

# Dissect strings [dissect-processor]


The `dissect` processor tokenizes incoming strings using defined patterns.


## Example [_example_22]

```yaml
  - dissect:
      tokenizer: "%{key1} %{key2} %{key3|convert_datatype}"
      field: "message"
      target_prefix: "dissect"
```

For a full example, see [Dissect example](#dissect-example).


## Configuration settings [_configuration_settings_27]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `tokenizer` | Yes |  | Field used to define the **dissection** pattern. You can provide an optional convert datatype after the key by using a pipe character (`&#124;`) as a separator to convert the value from `string` to `integer`, `long`, `float`, `double`, `boolean`, or `IP`. |
| `field` | No | `message` | Event field to tokenize. |
| `target_prefix` | No | `dissect` | Name of the field where the values will be extracted. When an empty string is defined, the processor creates the keys at the root of the event. When the target key already exists in the event, the processor won’t replace it and log an error; you need to either drop or rename the key before using dissect, or enable the `overwrite_keys` flag. |
| `ignore_failure` | No | `false` | Whether to return an error if the tokenizer fails to match the message field. If `true`, the processor silently restores the original event, allowing execution of subsequent processors (if any). If `false`, the processor logs an error, preventing execution of other processors. |
| `overwrite_keys` | No | `false` | Whether to overwrite existing keys. If `true`, the processor overwrites existing keys in the event. If `false`, the processor fails if the key already exists. |
| `trim_values` | No | `none` | Enables the trimming of the extracted values. Useful to remove leading and trailing spaces. Possible values are:<br><br>* `none`: no trimming is performed.<br>* `left`: values are trimmed on the left (leading).<br>* `right`: values are trimmed on the right (trailing).<br>* `all`: values are trimmed for leading and trailing.<br> |
| `trim_chars` | No | (`" "`) to trim space characters | Set of characters to trim from values when `trim_values` is enabled. To trim multiple characters, set this value to a string containing all characters to trim. For example, `trim_chars: " \t"` trims spaces and tabs. |

For tokenization to be successful, all keys must be found and extracted. If a key cannot be found, an error is logged, and no modification is done on the original event.

::::{note}
A key can contain any characters except reserved suffix or prefix modifiers:  `/`,`&`, `+`, `#` and `?`.
::::


See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.


## Dissect example [dissect-example]

For this example, imagine that an application generates the following messages:

```sh
"321 - App01 - WebServer is starting"
"321 - App01 - WebServer is up and running"
"321 - App01 - WebServer is scaling 2 pods"
"789 - App02 - Database will be restarted in 5 minutes"
"789 - App02 - Database is up and running"
"789 - App02 - Database is refreshing tables"
```

Use the `dissect` processor to split each message into three fields, for example, `service.pid`, `service.name`, and `service.status`:

```yaml
  - dissect:
      tokenizer: '"%{service.pid|integer} - %{service.name} - %{service.status}"'
      field: "message"
      target_prefix: ""
```

This configuration produces fields like:

```json
"service": {
  "pid": 321,
  "name": "App01",
  "status": "WebServer is up and running"
},
```

`service.name` is an ECS [keyword field](elasticsearch://docs/reference/elasticsearch/mapping-reference/keyword.md), which means that you can use it in {{es}} for filtering, sorting, and aggregations.

When possible, use ECS-compatible field names. For more information, see the [Elastic Common Schema](ecs://docs/reference/index.md) documentation.

