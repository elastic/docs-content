---
navigation_title: Map fields
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Map fields in Streams [streams-schema]

After selecting a stream, map fields either after creating a processor on the **Processing** tab or from the **Schema** tab.

Field mappings define how {{es}} stores and indexes your data, balancing storage efficiency against query performance.

Unmapped fields can still be searched using [runtime fields](../../../../manage-data/data-store/mapping/runtime-fields.md), but these incur higher query costs.

After identifying which fields you query most often, you can map them to improve performance, at the cost of additional storage. For more background, refer to the [Mapping](../../../../manage-data/data-store/mapping.md) overview.

## Map fields from the Processing tab

After you create a [processor](./extract.md), open the **Detected fields** tab to view any fields it extracted. Streams automatically attempts to map these fields so you can use them in queries.

From here, you can:

- Accept the suggested field mapping.
- Change an incorrect field mapping to the correct type.
- Remove the mapping from a field.

## Map fields from the Schema tab

The **Schema** tab provides an overview of how fields are defined within your stream.

- **Classic streams:** the **Schema** tab lists all fields found in the underlying index or index template. Each field shows its mapping status and type, either **Mapped** or **Unmapped**.

- **Wired streams:** {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` the **Schema** tab determines field mappings by combining information from the current stream’s index and its parent streams. Fields with a type defined in a parent stream have the **Inherited** status. You can navigate to that parent stream to view or edit the mapping (except for fields defined in the root logs stream, which you can't modify).

  When you add a mapping to a wired stream, all of its child streams automatically inherit it.

### Edit mappings from the Schema tab

To edit field mappings from the **Schema** tab:
1. Open the **Field actions** menu by selecting the {icon}`boxes_vertical` icon.
1. Select **Map field**.
1. From the **Type** dropdown, select the desired field type.
1. Select **Stage changes** to save your updates.