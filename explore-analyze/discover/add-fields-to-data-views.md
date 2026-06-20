---
navigation_title: Add fields
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#add-field-in-discover
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Create runtime fields in Discover to extend your data views without reindexing. Compute values on the fly, combine fields, or extract new data from existing fields.
---

# Add runtime fields to {{data-sources}} from Discover [add-field-in-discover]

Create [runtime fields](../../manage-data/data-store/mapping/runtime-fields.md) directly from **Discover** to extend your {{data-source}} without reindexing your data. Runtime fields are computed on the fly from your source data, allowing you to combine existing fields, extract new values, or perform calculations without modifying your indices.

**Technical summary**: In **Discover**, click **Add a field** from the fields sidebar, select the field type, write a {{product.painless}} script using `emit(value)` to compute the field value from source data, and save to the {{data-source}}. Runtime fields are stored in the {{data-source}} definition and computed at query time.

Use runtime fields when you need to add missing fields, combine data from multiple fields, or create calculated values for analysis and visualization.

## Prerequisites

* You need sufficient privileges to modify the {{data-source}}. Refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).
* You should understand [runtime fields](../../manage-data/data-store/mapping/runtime-fields.md) and the [{{product.painless}} scripting language](../scripting/modules-scripting-painless.md).

## Add a runtime field

1. In **Discover**, open the {{data-source}} you want to modify.
2. In the fields sidebar, select **Add a field**.
3. Select the **Type** of the new field from the dropdown menu (for example, `Keyword`, `Long`, `Boolean`, `Date`, or `IP`).
4. **Name** the field. Choose a name that corresponds to the naming convention of other fields in the {{data-source}}. 
5. Optionally, set a **Custom label** and **Description** for the field to make it more recognizable in your {{data-source}}. The custom label appears in **Discover** and other applications, while the field name is used in queries.
6. Define the field value using one of these options:
   
   * **Set value**: Define a script that determines the value to show for the field. This is required for computed fields.
   * **Set format**: Set your preferred format for displaying the value. Changing the format can affect the value and prevent highlighting in **Discover**.

   By default, if you don't enable **Set value**, the field value is retrieved from the source data if it already contains a field with the same name.

7. In the **Advanced settings**, you can adjust the field popularity to make it appear higher or lower in the fields list. By default, **Discover** orders popular fields from most selected to least selected.
8. Select **Save** to add the field to your {{data-source}}.

The new field now appears in the fields list and can be added to the document table, used in queries, and visualized like any other field.

## Usage examples

### Example 1: Simple "Hello World" field

This example creates a simple static text field:

* **Name**: `hello`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

```ts
emit("Hello World!");
```

### Example 2: Combine and convert fields

This example combines first and last name fields from the ecommerce sample data, creating a "Last, First Initial" format:

* **Name**: `customer`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

```ts
String str = doc['customer_first_name.keyword'].value;
char ch1 = str.charAt(0);
emit(doc['customer_last_name.keyword'].value + ", " + ch1);
```

This creates a computed field that displays as "Smith, J" for a customer named John Smith.

## Edit or remove a runtime field

To modify or remove a runtime field you created:

1. Find the field in the fields list in **Discover**.
2. Hover over the field name and select the gear icon.
3. Choose to edit the field definition or remove it from the {{data-source}}.

Changes to runtime fields affect all applications using the same {{data-source}}.

## Learn more

* For more information on adding fields and {{product.painless}} scripting language examples, refer to [Explore your data with runtime fields](../find-and-organize/data-views.md#runtime-fields).
* For advanced runtime field concepts, see [Runtime fields](../../manage-data/data-store/mapping/runtime-fields.md).
* To learn about {{product.painless}} scripting, refer to [{{product.painless}} scripting language](../scripting/modules-scripting-painless.md).

