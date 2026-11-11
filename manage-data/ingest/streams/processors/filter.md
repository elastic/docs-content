---
navigation_title: Filter processor
description: Drop records that match OTTL conditions in a Streams pipeline, before they reach any destination.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Filter processor

The **Filter** processor drops every record that matches any of its conditions. Use it to stop paying to ship and store data you'll never look at, such as debug logs, health-check requests, metrics from a noisy library, or spans from a synthetic monitor. A dropped record never reaches any destination downstream of the pipeline, including an Amazon S3 copy.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

Filter decides per record. To send unwanted data somewhere cheaper instead of dropping it, use a [router](../route-data.md) with a copy rule that sends everything to S3 and a move rule with a condition for {{es}}.

:::{warning}
A Filter processor acts on live data as soon as you select **Save and apply**, and dropped records can't be recovered. Before you save a condition, check it against a record you know should match and one you know shouldn't.
:::

## Configuration [streams-filter-config]

**Default error mode**
:   What happens when evaluating a condition fails, for example because a function receives a value of the wrong type. This setting applies to every block that doesn't set its own **Error mode**. **Propagate** stops and reports the error, and the payload is dropped. **Ignore** logs the error and carries on with the next condition. **Silent** carries on with the next condition without logging the error. Leave it as **None** to use the OpenTelemetry Collector's own default, which is **Propagate**.

**Configurations**
:   One or more blocks of conditions. A record is dropped when it matches any condition of any block. Each block has:

    * **Error mode**: overrides the default error mode for this block. **None** means the default applies.
    * **Context**: the OTTL context the conditions are written in, such as **Log**, **Span**, or **Resource**. Leave it as **None** to infer the context from the conditions.
    * **Conditions**: a list of OTTL conditions, one per row. Matching any of them drops the record. Select **Add item** to add a condition, drag a row by its handle to reorder, or select the minus icon to remove it.

    Select **Add item** below the last block to add another block.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Writing conditions [streams-filter-conditions]

A condition is an OTTL boolean expression over the fields of the current record, for example `attributes["http.route"] == "/healthz"`.

It's safer to describe the records to drop than the records to keep. These two conditions look similar but behave differently on a record that has no `level` attribute:

* `attributes["level"] == "debug"` drops only records whose `level` is `debug`.
* `attributes["level"] != "info"` drops every record whose `level` isn't `info`, including every record that has no `level` at all.

This is because a missing field evaluates to `nil` in OTTL, and `nil` is not equal to any value. If you do need a negative condition, rule out the missing case first, as in `attributes["level"] != nil and attributes["level"] != "info"`.

For the functions you can use in a condition, such as `IsMatch` or `IsString`, refer to the [OTTL functions reference](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/ottlfuncs/README.md).

## Examples [streams-filter-examples]

Drop debug and trace logs, but keep logs that have no severity at all (`severity_number` is `0` on those):

```text
severity_number > 0 and severity_number < 9
```

Drop health-check requests, in logs and spans:

```text
attributes["http.route"] == "/healthz"
attributes["url.path"] == "/healthz"
```

Drop everything from one noisy service, by the resource:

```text
resource.attributes["service.name"] == "load-generator"
```

Drop metrics from a library you don't chart:

```text
IsMatch(name, "^process\\.runtime\\.jvm\\.buffer.*")
```

Each line is one condition. Put them in the same block to drop a record that matches any of them.

## Related pages [streams-filter-related]

* [Process data](../process-data.md): Learn how pipelines run, what the locations mean, and how to add and manage processors.
* [Route data](../route-data.md): Keep unwanted data by sending it to a cheaper destination instead of dropping it.
* [Transform](transform.md): Remove or mask individual fields instead of dropping the whole record.
* [Add fields](add-fields.md), [Rename fields](rename-fields.md), and [Set](set.md): Change the fields of a record instead of dropping it.
