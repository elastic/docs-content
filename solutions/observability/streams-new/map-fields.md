---
navigation_title: Map fields
description: Map Streams fields to define how Elasticsearch stores and indexes your data, balancing query performance and storage cost.
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Map fields in Streams [streams-schema]

Field mappings define how {{es}} stores and indexes your data, balancing storage efficiency against query performance. You can map fields from the [**Processing** tab](#streams-map-fields-processing) or the [**Schema** tab](#streams-map-fields-processing).

## Mapped versus runtime fields [streams-mapped-vs-runtime]

Unmapped fields can still be searched using [runtime fields](../../../manage-data/data-store/mapping/runtime-fields.md), but at a higher query cost. Use this table to decide which approach fits your use case:

| | Mapped fields | Runtime fields |
|---|---|---|
| **Storage** | Higher — field is indexed at ingest | None — calculated at query time |
| **Query performance** | Fast | Slower |
| **Aggregations and sorting** | Fully supported | Supported, but slower |
| **Schema changes** | Require re-indexing | No re-indexing needed |
| **Best for** | Fields you query, filter, or aggregate regularly | Exploratory queries, infrequent lookups, or schema still in flux |

For most fields, use mapped fields. The performance benefit outweighs the extra storage for any field you use regularly — especially fields used in dashboards, filters, and aggregations. Use runtime fields when you're still exploring your data structure or for fields you rarely query.

For more background on field types and mapping, refer to the [mapping](../../../manage-data/data-store/mapping.md) overview.

## Map fields from the Processing tab [streams-map-fields-processing]

After you create a [processor](./parse-and-process.md), open the **Detected fields** tab to view any fields it extracted. Streams automatically attempts to map these fields so you can use them in queries.

From here, you can:

- Accept the suggested field mapping.
- Change an incorrect field mapping to the correct type.
- Remove the mapping from a field.

## Map fields from the Schema tab [streams-map-fields-processing]

The **Schema** tab provides an overview of how fields are defined within your stream.

- **Classic streams:** the **Schema** tab lists all fields found in the underlying index or index template. Each field shows its mapping status and type, either **Mapped** or **Unmapped**.

- **Wired streams:** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` the **Schema** tab determines field mappings by combining information from the current stream’s index and its parent streams. Fields with a type defined in a parent stream have the **Inherited** status. You can navigate to that parent stream to view or edit the mapping (except for fields defined in the root logs stream, which you can't modify).

  When you add a mapping to a wired stream, all of its child streams automatically inherit it.

### Edit mappings from the Schema tab

To edit field mappings from the **Schema** tab:
1. Open the **Field actions** menu by selecting the {icon}`boxes_vertical` icon.
1. Select **Map field**.
1. From the **Type** menu, select the field type.
1. Select **Stage changes** to save your updates.