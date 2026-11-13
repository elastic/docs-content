---
navigation_title: Create lookup indices
applies_to:
  serverless: preview
  stack: preview 9.2
products:
  - id: kibana
type: how-to
description: Create and edit lookup indices from the ES|QL editor in Discover. Add data from a CSV file or by hand, then join it in your query.
---

# Create lookup indices from Discover queries

If you want to enrich your query results with extra data, such as a team name for each host, you can create a small lookup index and join it to your query without leaving **Discover**. A lookup index is an {{es}} index that a [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/esql-lookup-join.md) command matches against your results. You can fill it by hand or from a CSV file.

To create a lookup index outside **Discover**, use the create index API for [{{stack}}]({{es-apis}}operation/operation-indices-create) or [{{serverless-full}}]({{es-serverless-apis}}operation/operation-indices-create). Set the `index.mode` index setting to `lookup`, because `LOOKUP JOIN` requires it.

## Before you begin

- To create lookup indices, you need the [`create_index`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege on the corresponding pattern. To add data to the new index, you also need the `write` privilege.
- To edit lookup indices, you need the [`write`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.
- To view lookup indices in read-only mode, you need the [`read`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.
- To reset the configuration of a lookup index, you need the `delete_index` and `create_index` {{es}} privileges.
- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

## Create and edit lookup indices from queries [discover-esql-lookup-join]

### Create a lookup index from the editor [create-lookup-esql]

You can create a lookup index directly from the {{esql}} editor and fill it by hand or from a CSV file.

1. In your {{esql}} query, add a `LOOKUP JOIN` command. For example:

   ```esql
   FROM kibana_sample_data_logs
   | LOOKUP JOIN
   ```

   Add a space after the command. The editor suggests existing lookup indices and offers to create one. You can also enter an index name in your query. If it doesn't exist, the editor suggests creating it.

2. Select the **Create lookup index** suggestion from the autocomplete menu.

3. Enter a name for the lookup index. Use a lowercase name with no spaces and none of these characters: `\`, `/`, `*`, `?`, `<`, `>`, `|`, `:`, `#`. The name can't start with `-`, `_`, `+`, or `.`, and it can't match an existing index.

4. Provide data for the lookup index in one of these ways, or combine them:
   - **Upload a CSV file**. The default size limit is 500 MB, or 100 MB in 9.2 and 9.3. On {{stack}}, the [`fileUpload:maxFileSize`](kibana://reference/advanced-settings.md#kibana-general-settings) advanced setting changes the limit. When you upload a file, you can preview its data, inspect its contents, and review any detected issues before importing it. Refer to [](#esql-lookup-index-from-file) for more details.
   - **Add data manually**. You can add fields and populate data directly. When you add a field:
     - {applies_to}`serverless: preview` {applies_to}`stack: preview 9.3+` Set its name and [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). You can't change the data type after you save the lookup index. The type list offers only some {{es}} data types. If a type isn't in the list, the editor doesn't support it. For example, you can't select `object`, `nested`, `alias`, or `scaled_float`.
     - {applies_to}`stack: preview =9.2` Set its name. {{es}} sets the data type from the values you enter.

   You can upload a file after adding data manually, and edit or expand the data imported from a file.

5. Check your index and its data. The search field and **Open in Discover** become available after you save the index for the first time, so save it first if you want to use them. The search field filters the rows of the index. **Open in Discover** opens the index with a prefilled {{esql}} query. From 9.3, it opens in a new Discover tab, after the editor closes and asks you about any unsaved changes. In 9.2, it opens in a new browser tab.

   :::{tip}
   :applies_to: { serverless: preview, stack: preview 9.5+ }
   The search field supports free text and [Kibana Query Language (KQL)](/explore-analyze/query-filter/languages/kql.md) syntax, with autocomplete for field names and values. Newly added columns appear as autocomplete suggestions only after you save the index, and the search doesn't match unsaved values.
   :::

6. Select **Save** (or **Save and close**) for any unsaved changes. The editor creates the index the first time you save. Then select **Close** to return to your query.

**Result:** The editor adds the new index to your query. To finish the join, name the field to match with `ON <field_to_join>`.

### Load data into a lookup index from a CSV file [esql-lookup-index-from-file]

When you are editing a lookup index from the {{esql}} editor, you can add data to it by uploading CSV files. The default size limit is 500 MB, or 100 MB in 9.2 and 9.3. Refer to [](#create-lookup-esql) for how to change it.

:::::{applies-switch}

::::{applies-item} { serverless: preview, stack: preview 9.3+ }
1. Drag the files you want to upload from your computer, or select the **uploading** link in the empty index prompt to browse for them. You can add several files at a time and can repeat the operation multiple times.

   :::{note}
   If your index has unsaved changes, a message tells you that you lose these changes. To keep these changes, cancel the upload and save your index, then start a new upload.
   :::

2. Preview the data for each file you're importing, then select **Continue**. If the editor detects issues, a message appears with more details. Typical issues include differences between the fields of the index and those of the imported files.
   - The editor adds new fields from the imported files to the index.
   - The editor keeps fields that exist in the index but not in the imported file, and leaves them empty.

3. Review and adjust the field names and data types to match the needs of your lookup index. After the import, you can no longer edit them.

4. Select **Import** to validate the configuration and proceed with the import, then **Finish** to finalize the operation and return to the lookup index.

Data coming from the files is appended to the index, and the index is automatically saved.
::::

::::{applies-item} stack: preview =9.2
1. Select {icon}`download` **Upload file**.

2. Select the CSV file to import on your machine. You can select several files to import at once.

   :::{note}
   If your index has unsaved changes, a message tells you that you lose these changes. To keep these changes, cancel the upload and save your index, then select {icon}`download` **Upload file** again.
   :::

3. Preview the data for each file you're importing. The editor detects and sets the field data types. If it detects issues, a **File issues** tab with more details appears before you validate the import. Common issues include differences between the fields in the index and in the imported files.
   - The editor adds new fields from the imported files to the index.
   - The editor keeps fields that exist in the index but not in the imported file, and leaves them empty.

4. Select **Import** to finalize the operation.

Data coming from the files is appended to the index, and the index is automatically saved.
::::

:::::

### View or edit a lookup index from the editor [view-edit-lookup-esql]

You can view and edit existing lookup indices referenced in an {{esql}} query directly from the editor, depending on your privileges.

To view or edit an index:

1. In the {{esql}} query, hover over the lookup index name.

2. Select the **Edit lookup index** or **View lookup index** option. The editor offers **Edit lookup index** if you have the `write` privilege, and **View lookup index** if you only have the `read` privilege. A flyout showing the index opens.

3. Depending on your permissions and needs, explore or edit the index. When editing the index, you have the same options described in [](#create-lookup-esql).

   :::{note}
   Editing a lookup index affects all {{esql}} queries that reference it. Make sure that your changes are compatible with existing queries that use this index.
   :::

4. If you made changes, select **Save** before closing the flyout.

### Reset the lookup index configuration [reset-the-lookup-index-configuration]

At any time, you can delete all the index data and fields. A reset deletes the index and creates it again as an empty lookup index, so it needs the `delete_index` and `create_index` privileges.

:::::{applies-switch}

::::{applies-item} { serverless: preview, stack: preview 9.3+ }
1. Select all the index data using the checkbox in the header of the table.

2. Select **Delete selected** from the contextual menu.

3. After you delete all entries, a **Reset index** button appears if you have the privileges for a reset. Select it, then confirm, to remove all fields configured in the index.

The lookup index is fully reset and saved automatically.
::::

::::{applies-item} stack: preview =9.2
In this version, you can't fully reset the index configuration. For example, you can't remove columns. However, you can delete the index data. To do that, select the entries to delete, then select **Delete selected** from the contextual menu.
::::

:::::

### Limitations [discover-esql-lookup-editor-limitations]

The following limitations apply to the lookup index editor in {{kib}}. For general limitations of the `LOOKUP JOIN` command, refer to [Join data from multiple indices with LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md#limitations).

Row display limit
:   The lookup index editor displays up to 1,000 rows. To find a specific row when the index contains more than 1,000 entries, use the search field: it searches the full index. The `LIMIT` command in your {{esql}} query has no effect on the data shown here.

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [Join data from multiple indices with LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md)
- [](../query-filter/languages/esql-kibana.md)
