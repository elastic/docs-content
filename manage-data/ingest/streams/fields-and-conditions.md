---
navigation_title: Fields and conditions
description: Refer to fields of logs, metrics, traces, and documents in Streams processors and routing rules, and write OTTL conditions that match the records you expect.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Fields and conditions in Streams

Processors and routing rules both need to say which part of a record they mean. A processor names the field it writes or renames, and an optional condition decides which records it acts on. A routing rule's condition decides which records it sends to its target. Streams uses the OpenTelemetry Transformation Language (OTTL) for each of them, so a field is written the same way and a condition behaves the same way in a pipeline and in a router.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## How a record is structured [streams-fields-records]

Streams works on the OpenTelemetry data model. A record is a log record, a span, or a metric data point. Each record sits inside an instrumentation scope, which sits inside a resource, so a field can belong to the record itself, to its scope, or to its resource.

A document from a [Managed _bulk source](sources/elasticsearch-bulk.md) is a record of its own kind. Its fields are the keys of the JSON you sent.

## Locations in processor forms [streams-fields-locations]

When a processor form asks where a field lives, you pick a **Location** and give the field's **Name** or **Path** within it. The default is **Body** in Add fields and **Record** in Rename fields and Set. Each location stands for one part of the record:

| Location | What it is |
| --- | --- |
| **Body** | The log record body. For structured logs, a key inside it such as `message`. Logs only. |
| **Document** | A field of a document from a Managed _bulk source, by its key, such as `order.status`. A dotted key is one key, not a path into nested objects. Offered when the pipeline carries documents. |
| **Resource** | Resource-level fields shared by all records from the same source, such as `service.name` or `deployment.environment.name`. |
| **Scope** | Instrumentation scope fields, such as the library name and version. |
| **Attributes** | The current record's attributes, for example `http.request.method` on a log record or span. |
| **Metadata** | Metadata that travels with a batch of data through the pipeline, for all signals. It isn't sent to the destination with each record. |
| **Record** | The complete current record: a log record, span, or data point. Available in Set and Rename fields, where the path can reach fields such as a log's `severity_text`. |

In the [Set](processors/set.md) processor you can instead select **Use Context** next to **Location** and choose an explicit OTTL context, such as **Resource**, **Scope**, **Log**, **Span**, **Span event**, **Metric**, or **Data point**, or select **Leave unset** and write a full OTTL path, for example `log.severity_text` or `datapoint.attributes["host.name"]`. Locations are portable across signals, so prefer them unless you need something only a context exposes.

The [Filter](processors/filter.md) and [Transform](processors/transform.md) processors have no **Location**. Each of their blocks has a **Context** instead. Leave it as **None** to let Streams infer the context from what you write.

## Refer to fields in OTTL [streams-fields-paths]

Conditions, OTTL values, and Transform statements refer to fields by their OTTL path. These paths are the ones you'll use most:

| Field | OTTL path |
| --- | --- |
| An attribute of the current record | `attributes["http.route"]` |
| A resource attribute | `resource.attributes["service.name"]` |
| A scope attribute | `scope.attributes["key"]` |
| A key in a structured log body | `body["message"]` |
| A field of a document from a Managed _bulk source | `body["order.status"]` |
| A field of the record itself | `severity_text` or `severity_number` on a log record, `name` on a span |

The key inside the brackets is one key, even when it contains dots. `attributes["service.name"]` reads the attribute named `service.name`, not a `name` key nested inside a `service` map.

## Write conditions [streams-fields-conditions]

A condition is an OTTL boolean expression that Streams evaluates against each record. You write one in these places:

* The optional **Condition** of the [Add fields](processors/add-fields.md), [Rename fields](processors/rename-fields.md), and [Set](processors/set.md) processors. The processor acts only on records that match.
* The **Conditions** of a [Filter](processors/filter.md) block. A record that matches any of them is dropped.
* The optional **Conditions** of a [Transform](processors/transform.md) block. The block's statements run only on records that match any of them.
* The **Condition** of a [routing rule](route-data.md). Matching records go to the rule's target. A rule without a condition matches every record that reaches it.

A condition compares fields with `==`, `!=`, `<`, `<=`, `>`, and `>=`, and combines comparisons with `and`, `or`, and `not`. For example:

```text
resource.attributes["deployment.environment.name"] == "production"
attributes["http.route"] == "/healthz" or attributes["http.route"] == "/readyz"
severity_number >= 17 and resource.attributes["service.name"] == "checkout"
```

A field that a record doesn't have evaluates to `nil`, and `nil` isn't equal to any value. As a result, a negative condition such as `attributes["level"] != "info"` also matches every record that has no `level` attribute. A Filter processor would drop those records, and a routing rule would claim them. Rule out the missing case first when that isn't what you want, as in `attributes["level"] != nil and attributes["level"] != "info"`.

Conditions are free text, without autocompletion, so check each one against a record you know should match and one you know shouldn't.

For the full syntax, refer to the [OTTL documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/README.md). For the functions you can use in a condition, such as `IsMatch` or `IsString`, refer to the [OTTL functions reference](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/ottlfuncs/README.md).

## Related pages [streams-fields-related]

* [Process data before it reaches Elasticsearch](process-data.md): Add a pipeline and choose the processors that change or drop records.
* [Route data to different destinations](route-data.md): Add a router whose rules send records to different destinations by condition.
* [Add fields processor](processors/add-fields.md): Add named fields to records, optionally when a condition holds.
* [Filter processor](processors/filter.md): Drop records that match OTTL conditions.
* [Rename fields processor](processors/rename-fields.md): Give fields a new name within their location.
* [Set processor](processors/set.md): Write to any field by its location or full OTTL path.
* [Transform processor](processors/transform.md): Run OTTL statements of your choice on each record.
* [Streams glossary](glossary.md): Look up record, location, context, condition, and the other terms used on this page.
