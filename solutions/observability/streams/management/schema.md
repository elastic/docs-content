---
navigation_title: Map fields
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Map fields [streams-schema]

Mappings define how {{es}} stores and indexes your data, balancing storage efficiency against query capability and performance.

Unmapped fields can still be searched using [runtime fields](../../../../manage-data/data-store/mapping/runtime-fields.md), but these incur higher query costs. Runtime fields are useful for exploring your data and experimenting with different query types before finalizing a schema.

Once you know which fields you query most often, you can map them to improve performance, at the cost of additional storage. For a general overview, refer to the [Mapping](../../../../manage-data/data-store/mapping.md) documentation.

Streams gives you options for mapping fields and editing field mappings, either after creating a processor or from the **Schema** tab.

## Processing tab

After creating a [processor](./extract.md), open the **Detected fields** tab to find any fields that the processor has extracted. Streams automatically attempts to map these fields so you can use them in queries.

From here, you can:

- Accept the suggested field mapping.
- Change the field mapping to a different type.
- Remove the mapping from these fields.

## Schema tab

The **Schema** tab provides an overview of how fields are defined within your stream.

**Classic streams:** the **Schema** tab lists all fields found in the underlying index or index template. Each field shows its mapping status and type. Fields are labelled with either a **Mapped** or **Unmapped** status accordingly.

**Wired streams:** :applies_to: {"stack": "preview 9.2", "serverless": "preview"} the **Schema** tab determines field mappings by combining information from the current stream’s index and its parent streams. Fields whose type is defined in a parent stream have the status of **Inherited**. You can navigate to that parent stream to view or edit the mapping (except for fields defined in the root logs stream, which cannot be modified).

When you add a mapping to a wired stream, its child streams inherit the mapping.

### Edit mappings from the Schema tab

To edit field mappings from the **Schema** tab:
1. Open the **Field actions** menu by selecting the {icon}`boxes_vertical` icon.
1. Select **Map field**
1. From the **Type** dropdown, select the desired field type.
1. Select **Stage changes**.

% need to add permissions ## Permissions to edit and add fields [streams-schema-permissions]