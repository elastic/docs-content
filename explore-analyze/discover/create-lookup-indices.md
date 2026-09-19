---
navigation_title: Create lookup indices
applies_to:
  stack: preview 9.2
  serverless: preview
products:
  - id: kibana
type: how-to
description: Create and edit lookup indices from the ES|QL editor in Discover. Add data from a CSV file or by hand, then join it in your query.
---

# Create lookup indices from Discover queries

In **Discover**, [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/esql-lookup-join.md) commands include interactive options that let you create or edit lookup indices directly from the editor. You can type in rows, upload a CSV file, and join the new index in the same query.

This page describes the {{kib}} editor. You can also create and manage indices using the {{es}} APIs for [version 9]({{es-apis}}operation/operation-indices-create) and [Serverless]({{es-serverless-apis}}operation/operation-indices-create).

## Before you begin

- To create lookup indices, you need the [`create_index`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege on the corresponding pattern.
- To edit lookup indices, you need the [`write`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.
- To view lookup indices in read-only mode, you need the [`view_index_metadata`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.
- You need an {{esql}} query in **Discover**. If you are new to that editor, start with [Get started with Discover using {{esql}}](try-esql.md).

## Create and edit lookup indices from queries [discover-esql-lookup-join]

### Create a lookup index from the editor [create-lookup-esql]

You can create a lookup index directly from the {{esql}} editor. To populate this index, you can type in data manually or upload a CSV file up to 500 MB.

1. In your {{esql}} query, add a `LOOKUP JOIN` command. For example:
   ```esql
   FROM kibana_sample_data_logs
   | LOOKUP JOIN
   ```
   Add a space after the command. The editor suggests existing lookup indices and offers to create one. You can also type an index name in your query. If it doesn't exist, the editor suggests creating it.

2. Select the **Create lookup index** suggestion that appears in the autocomplete menu.

3. Define a name for the lookup index.
   - The name must not contain spaces or any of the following characters: `\`, `/`, `*`, `?`, `<`, `>`, `|`, `:`, and `#`.
   - The name must not start with `-`, `_`, or `+`.

4. Provide data for the lookup index. You can either:
   - **Upload a CSV file up to 500 MB**. When you upload a file, you can preview its data, inspect its contents, and review any detected issues before importing it. Refer to [](#esql-lookup-index-from-file) for more details.
   - **Add data manually**. You can add fields and populate data directly. When adding a field, you must set its name and [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md).
     :::{note}
     Some {{es}} data types aren't supported in {{kib}}.
     :::
   - **Using a combination of both methods**. You can upload a file after adding data manually, and edit or expand the data imported from a file.

5. Check your index and its data. You can explore your index using the search field, or open it in a new Discover session by selecting **Open in Discover**. If you choose to open it in Discover, a new browser tab opens with a prefilled {{esql}} query on the index.

   :::{tip}
   :applies_to: {"stack": "preview 9.5", "serverless": "preview"}
   The search field supports free text and [KQL](/explore-analyze/query-filter/languages/kql.md) syntax, with autocomplete for field names and values. Newly added columns appear as autocomplete suggestions only after you save the index, and the filter doesn't match unsaved values.
   :::

6. **Save** any unsaved changes, then **Close** the index editor to return to your query.

Your new index is automatically added to your query. You can then specify the field to join using `ON <field_to_join>`.

### Load data into a lookup index from a CSV file [esql-lookup-index-from-file]

When you are editing a lookup index from the {{esql}} editor, you can add data to it by uploading CSV files up to 500 MB.

:::::{applies-switch}

::::{applies-item} { serverless:, stack: ga 9.3+ }
1. Drag the files you want to upload from your computer. You can add several files at a time and can repeat the operation multiple times.

   :::{note}
   If your index has unsaved changes, a message informs you that these changes will be lost. To keep those changes, cancel the upload and save your index, then start a new upload.
   :::

2. Preview the data for each file you're importing, then select **Continue**. If issues are detected, a message appears with more details. Typical issues include differences between the fields of the index and those of the imported files.
   - New fields coming from imported files will be added to the index.
   - Fields that exist in the index but are missing from the imported file will be kept but not filled with any data.

3. Review and adjust the field names and data types to match the needs of your lookup index. After the import, you can no longer edit them.

4. Select **Import** to validate the configuration and proceed with the import, then **Finish** to finalize the operation and return to the lookup index.

Data coming from the files is appended to the index, and the index is automatically saved.
::::

::::{applies-item} stack: ga =9.2
1. Select {icon}`download` **Upload file**.

2. Select the CSV file to import on your machine. You can select several files to import at once.

   :::{note}
   If your index has unsaved changes, a message informs you that these changes will be lost. To keep those changes, cancel the upload and save your index, then select {icon}`download` **Upload file** again.
   :::

3. Preview the data for each file you're importing. Field data types are automatically detected and set. If issues are detected, a **File issues** tab with more details appears before you validate the import. Common issues include differences between the fields in the index and in the imported files.
   - New fields coming from imported files will be added to the index.
   - Fields that exist in the index but are missing from the imported file will be kept but not filled with any data.

4. Select **Import** to finalize the operation.

Data coming from the files is appended to the index, and the index is automatically saved.
::::

:::::

### View or edit a lookup index from the editor [view-edit-lookup-esql]

You can view and modify existing lookup indices referenced in an {{esql}} query directly from the editor, depending on your privileges.

To view or edit an index:

1. In the {{esql}} query, hover over the lookup index name.

2. Select the **Edit lookup index** or **View lookup index** option that appears. A flyout showing the index appears.

3. Depending on your permissions and needs, explore or edit the index. When editing the index, you have the same options described in [](#create-lookup-esql).

   :::{note}
   Editing a lookup index affects all {{esql}} queries that reference it. Make sure that your changes are compatible with existing queries that use this index.
   :::

4. If you made changes, select **Save** before closing the flyout.

### Reset the lookup index configuration

At any time, you can delete all the index data and fields.

:::::{applies-switch}

::::{applies-item} { serverless:, stack: ga 9.3+ }
1. Select all the index data using the checkbox in the header of the table.

2. Select **Delete selected** from the contextual menu that appears upon selecting entries.

3. Once all entries are deleted, a **Reset index** button appears. Select it to remove all fields configured in the index.

The lookup index is fully reset and saved automatically.
::::

::::{applies-item} stack: ga =9.2
In this version, you cannot fully reset the index configuration. For example, you can't remove columns. However, you can delete the index data. To do that, select the entries to delete, then select **Delete selected** from the contextual menu that appears.
::::

:::::

### Limitations [discover-esql-lookup-editor-limitations]

The following limitations apply to the lookup index editor in {{kib}}. For general limitations of the `LOOKUP JOIN` command, refer to [Join data from multiple indices with LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md#limitations).

Row display limit
:   The lookup index editor displays up to 1,000 rows. To find a specific row when the index contains more than 1,000 entries, use the search field: it searches the full index. The `LIMIT` command in your {{esql}} query has no effect on the data shown here.

    {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` The search field accepts KQL syntax for precise filtering. Unsaved rows and values aren't matched until you save the index.

## Related pages

- [Use Discover with ES|QL](use-esql.md)
- [Join data from multiple indices with LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md)
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md)
