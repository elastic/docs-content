---
navigation_title: Transform processor
description: Run OTTL statements of your choice on records in a Streams pipeline, optionally guarded by conditions, for anything the other processors don't cover.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
---

# Transform processor

The **Transform** processor runs OpenTelemetry Transformation Language (OTTL) statements on each record. It's the fallback when no other processor does what you need, such as parsing a value out of the body, truncating or hashing a field, replacing a pattern, converting a type, or changing several fields in one step. Each block of statements can be guarded by conditions, and blocks run in order, so a later block sees what an earlier one changed.

Prefer [Add fields](add-fields.md), [Set](set.md), [Rename fields](rename-fields.md), and [Filter](filter.md) when they fit. Their cards in the **Processing** panel are easier to read, and they don't depend on OTTL syntax.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-transform-config]

**Default error mode**
:   What happens when a statement fails. This setting applies to every block that doesn't set its own **Error mode**. **Propagate** stops and reports the error. **Ignore** logs the error and carries on with the next statement. **Silent** carries on with the next statement without logging the error. Leave it as **None** to use the OpenTelemetry Collector's own default, which is **Propagate**.

**Configurations**
:   One or more blocks of statements. Each block has:

    * **Error mode**: overrides the default error mode for this block. **None** means the default applies.
    * **Context**: the OTTL context the statements are written in, such as **Log**, **Span**, or **Resource**. Leave it as **None** to infer the context from the statements.
    * **Conditions**: optional OTTL conditions, one per row. When present, the block's statements run only on records that match any of them.
    * **Statements**: a list of OTTL statements, one per row, run in order.
    * **Shared cache**: off by default. Turn it on to share the OTTL cache between all blocks that have it turned on, so a later block can use a value an earlier one stored.

    Select **Add item** under **Conditions** or **Statements** to add a row, or select the minus icon to remove one. Select **Add item** below the last block to add another block.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Writing statements [streams-transform-statements]

An OTTL statement is a function call on fields of the current record, for example `set(attributes["source"], "streams")`. The functions available are those of the collector's transform processor. The ones you'll use most:

| Function | Example |
| --- | --- |
| `set` | `set(attributes["env"], resource.attributes["deployment.environment.name"])` |
| `delete_key`, `delete_matching_keys` | `delete_key(attributes, "password")` |
| `replace_pattern`, `replace_all_patterns` | `replace_pattern(body, "\\d{4}-\\d{4}-\\d{4}-\\d{4}", "****")` |
| `truncate_all`, `limit` | `truncate_all(attributes, 4096)` |
| `merge_maps` | `merge_maps(attributes, ParseJSON(body), "upsert")` |
| `keep_keys` | `keep_keys(resource.attributes, ["service.name", "host.name"])` |

Converters such as `ParseJSON`, `ExtractPatterns`, `Int`, `String`, `SHA256`, and `Time` produce values you pass to a function. Refer to the [OTTL functions reference](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/ottlfuncs/README.md) for the full list and the [transform processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md) for the contexts.

## Examples [streams-transform-examples]

Parse a JSON log body into attributes and keep the raw body:

```text
merge_maps(attributes, ParseJSON(body), "upsert") where IsMatch(body, "^\\{")
```

Mask card numbers in log bodies before they leave the pipeline:

```text
replace_pattern(body, "\\b\\d{4}[ -]?\\d{4}[ -]?\\d{4}[ -]?\\d{4}\\b", "[redacted]")
```

Extract the request method and path from an access log line:

```text
merge_maps(attributes, ExtractPatterns(body, "^(?P<method>[A-Z]+) (?P<path>\\S+)"), "insert")
```

Drop an attribute from spans of one service, with a block condition:

* **Conditions**: `resource.attributes["service.name"] == "payments"`
* **Statements**: `delete_key(attributes, "db.statement")`

## Related pages [streams-transform-related]

* [Process data](../process-data.md): Learn how pipelines run, what the locations mean, and how to add and manage processors.
* [Add fields](add-fields.md), [Rename fields](rename-fields.md), and [Set](set.md): Prefer these processors when a single add, rename, or assignment does the job.
* [Filter](filter.md): Drop whole records instead of changing them.
