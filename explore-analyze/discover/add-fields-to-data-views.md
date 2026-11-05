---
navigation_title: Add a runtime field
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Add a runtime field to a data view from Discover when your data lacks a value you need, then use it in the table and in visualizations.
---

# Add a runtime field to a data view from Discover

When your data doesn't have a field you need, such as a value that is part of another field or a combination of two fields, you can add a [runtime field](../../manage-data/data-store/mapping/runtime-fields.md) to your [data view](../find-and-organize/data-views.md) without leaving **Discover**. You can then use the new field for analysis and visualizations the same way you use other fields.

## Before you begin

- Open **Discover** in classic mode, select the data view that you want to add the field to, and run a search so the fields list appears. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- Have a role with the **Data View Management** {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

## Add a runtime field

1. Start from either location:

   - In the sidebar, select **Add a field**.
   - In the data view menu, select **Add a field to this data view**.

2. Select the **Type** of value that the field holds:

   - **Keyword** for text, such as names or labels.
   - **Long** for whole numbers and **Double** for numbers with decimals.
   - **Date** for dates and times.
   - **IP** for IP addresses.
   - **Boolean** for true or false.
   - **Geo point** for locations.
   - **Composite** to produce several fields from one script. Refer to [Return multiple fields with a composite runtime field](../find-and-organize/data-views/runtime-fields.md#composite-runtime-field).

3. **Name** the field. Name it in a way that corresponds to the way other fields of the data view are named. You can set a custom label and description for the field to make it more recognizable in your data view.
4. Define the value that you want the field to show. By default, the field value is retrieved from the source data if it already contains a field with the same name. You can customize this with the following options:
   - **Set value**: Define a script that determines the value to show for the field. The script must return a value of the **Type** you selected, or the data view fails wherever it's used. For more information on adding fields and Painless scripting language examples, refer to [Explore your data with runtime fields](../find-and-organize/data-views/runtime-fields.md).
   - **Set format**: Set your preferred format for displaying the value. Changing the format can affect the value and prevent highlighting in Discover.

5. To check what your script returns before you save, use the **Preview**. Select the **Document ID** arrows to see the value for other documents.
6. In the advanced settings, you can adjust the field popularity to make it appear higher or lower in the fields list. By default, Discover orders popular fields from most selected to least selected.
7. Select **Save** to save your new field.

**Result:** The new field appears in the list of fields, and you can add it to the table. It's available wherever the data view is used. It doesn't change the index mapping in {{es}}.

## Examples

The following examples use the [sample ecommerce data](/manage-data/ingest/sample-data.md). The first adds a "Hello world" field. The second combines the `customer_first_name` and `customer_last_name` fields into a single "customer" field.

**Hello world field example**:

* **Name**: `hello`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

    ```painless
    emit("Hello World!");
    ```

**Customer field example**:

* **Name**: `customer`
* **Type**: `Keyword`
* **Set value**: enabled
* **Script**:

    ```painless
    String str = doc['customer_first_name.keyword'].value;
    char ch1 = str.charAt(0);
    emit(doc['customer_last_name.keyword'].value + ", " + ch1);
    ```

## Related pages

- [Use Discover in classic mode](use-classic-mode.md)
- [Explore your data with runtime fields](../find-and-organize/data-views/runtime-fields.md)
