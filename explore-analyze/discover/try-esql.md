---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/try-esql.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Step-by-step tutorial for querying data with Elasticsearch Query Language (ES|QL) in Discover using piped commands to filter, transform, and aggregate data with sample data and visualizations.
---

# Using ES|QL [try-esql]

Elasticsearch Query Language ({{esql}}) helps you explore and analyze your {{product.elasticsearch}} data directly in **Discover**, without a [data view](discover-get-started.md#find-the-data-you-want-to-use). {{esql}} uses a piped syntax where you chain commands together to filter, transform, and aggregate data without needing to switch between different query interfaces. This tutorial walks you through querying sample data with {{esql}}, from basic field selection to complex filtering and visualization.

## Prerequisites [try-esql-prerequisites]

- The `enableESQL` setting enabled in **Advanced Settings** (enabled by default)
- Have data in {{product.elasticsearch}}.
  The examples on this page use the {{product.kibana}} sample web logs to explore data and create visualizations. You can install sample data by following [Add sample data](../index.md#gs-get-data-into-kibana).

::::{tip}
For the complete {{esql}} documentation, including all supported commands, functions, and operators, refer to the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md). For a more detailed overview of {{esql}} in {{product.kibana}}, refer to [Use {{esql}} in Kibana](../query-filter/languages/esql-kibana.md).
::::


## Use {{esql}} [tutorial-try-esql]

To load the sample data:

1. Go to **Discover**.
2. Select **Try {{esql}}** from the application menu bar.

   :::{tip}
   If you've entered a KQL or Lucene query in the default mode of Discover, it automatically converts to ES|QL.
   :::

   Let’s say we want to find out what operating system users have and how much RAM is on their machine.

3. Set the time range to **Last 7 days**.
4. Copy the following query. To make queries more readable, you can put each processing command on a new line.

    ```esql
    FROM kibana_sample_data_logs <1>
    | KEEP machine.os, machine.ram <2>
    ```

    1. We're specifically looking for data from the sample web logs we installed.
    2. We’re only keeping the `machine.os` and `machine.ram` fields in the results table.
   
   ::::{note}
   {{esql}} keywords are not case sensitive.
   ::::

5. Click **▶Run**.
   ![An image of the query result](/explore-analyze/images/kibana-esql-machine-os-ram.png "")

Let’s add `geo.dest` to our query to find out the geographical destination of the visits and limit the results.

1. Copy the query below:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | LIMIT 10
    ```

2. Click **▶Run** again. You can notice that the table is now limited to 10 results. The visualization also updated automatically based on the query, and broke down the data for you.
   ::::{note}
   When you don’t specify any specific fields to retain using `KEEP`, the visualization isn’t broken down automatically. Instead, an additional option appears above the visualization and lets you select a field manually.
   ::::
   ![An image of the extended query result](/explore-analyze/images/kibana-esql-limit.png "")


We will now take it a step further to sort the data by machine ram and filter out the `GB` destination.

1. Copy the query below:

    ```esql
    FROM kibana_sample_data_logs
    | KEEP machine.os, machine.ram, geo.dest
    | SORT machine.ram desc
    | WHERE geo.dest != "GB"
    | LIMIT 10
    ```

2. Click **▶Run** again. The table and visualization no longer show results for which the `geo.dest` field value is "GB", and the results are now sorted in descending order in the table based on the `machine.ram` field.

    ![An image of the full query result](/explore-analyze/images/kibana-esql-full-query.png "")

3. Click **Save** to save the query and visualization to a dashboard.


### Edit the ES|QL visualization [_edit_the_esql_visualization]

You can make changes to the visualization by clicking the pencil icon. This opens additional settings that let you adjust the chart type, axes, breakdown, colors, and information displayed to your liking. If you’re not sure which route to go, check one of the suggestions available in the visualization editor.

If you’d like to keep the visualization and add it to a dashboard, you can save it using the floppy disk icon.


### ES|QL and time series data [_esql_and_time_series_data]

By default, ES|QL identifies time series data when an index contains a `@timestamp` field. This enables the time range selector and visualization options for your query.

If your index doesn’t have an explicit `@timestamp` field, but has a different time field, you can still enable the time range selector and visualization options by calling the `?_tstart` and `?_tend` parameters in your query.

For example, the eCommerce sample data set doesn’t have a `@timestamp` field, but has an `order_date` field.

By default, when querying this data set, time series capabilities aren’t active. No visualization is generated and the time picker is disabled.

```esql
FROM kibana_sample_data_ecommerce
| KEEP customer_first_name, email, products._id.keyword
```

:::{image} /explore-analyze/images/kibana-esql-no-time-series.png
:alt: ESQL query without time series capabilities enabled
:::

While still querying the same data set, by adding the `?_tstart` and `?_tend` parameters based on the `order_date` field, **Discover** enables times series capabilities.

```esql
FROM kibana_sample_data_ecommerce
| WHERE order_date >= ?_tstart and order_date <= ?_tend
```

:::{image} /explore-analyze/images/kibana-esql-custom-time-series.png
:alt: ESQL query with a custom time field enabled
:::

### Create and edit lookup indices from queries [discover-esql-lookup-join]
```{applies_to}
stack: preview 9.2
serverless: preview
```

In **Discover**, LOOKUP JOIN commands include interactive options that let you create or edit lookup indices directly from the editor.

:::{note}
This section describes how to use the {{kib}} UI to create and edit lookup indices. You can also create and manage indices using the {{es}} APIs for [version 9](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) and [Serverless](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-indices-create).
:::

#### Create a lookup index from the editor [create-lookup-esql]

You can create a lookup index directly from the {{esql}} editor. To populate this index, you can type in data manually or upload a CSV file up to 500 MB.

To create lookup indices, you need the [`create_index`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege on the corresponding pattern.

1. In your {{esql}} query, add a `LOOKUP JOIN` command. For example:
   ```esql
   FROM kibana_sample_data_logs
   | LOOKUP JOIN
   ```
   Add a space after the command. The editor suggests existing lookup indices and offers to create one. You can also type an index name in your query. If it doesn't exist, the editor suggests creating it.

2. Select the **Create lookup index** suggestion that appears in the autocomplete menu.

3. Define a name for the lookup index. The name must: 
   - Not contain spaces or any of the following characters: `\`, `/`, `*`, `?`, `<`, `>`, `|`, `:`, and `#`.
   - Not start with `-`, `_`, or `+`.

4. Provide data for the lookup index. You can either:
   - **Upload a CSV file up to 500 MB**. When you upload a file, you can preview its data, inspect its contents, and review any detected issues before importing it. Refer to [](#esql-lookup-index-from-file) for more details.
   - **Add data manually**. You can add fields and populate data directly. When adding a field, you must set its name and [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md).
     :::{note}
     Some {{es}} data types aren't supported in {{kib}}.
     :::
   - **Using a combination of both methods**. You can upload a file after adding data manually, and edit or expand the data imported from a file.

5. Check your index and its data. You can explore your index using the search field, or open it in a new Discover session by selecting **Open in Discover**. If you choose to open it in Discover, a new browser tab opens with a prefilled {{esql}} query on the index.

6. **Save** any unsaved changes, then **Close** the index editor to return to your query.

Your new index is automatically added to your query. You can then specify the field to join using `ON <field_to_join>`.

##### Load data into a lookup index from a CSV file [esql-lookup-index-from-file]

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

#### View or edit a lookup index from the editor [view-edit-lookup-esql]

You can view and modify existing lookup indices referenced in an {{esql}} query directly from the editor, depending on your privileges:
- To edit lookup indices, you need the [`write`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.
- To view lookup indices in read-only mode, you need the [`view_index_metadata`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) {{es}} privilege.

To view or edit an index:

1. In the {{esql}} query, hover over the lookup index name.

2. Select the **Edit lookup index** or **View lookup index** option that appears. A flyout showing the index appears.

3. Depending on your permissions and needs, explore or edit the index. When editing the index, you have the same options described in [](#create-lookup-esql).

   :::{note}
   Editing a lookup index affects all {{esql}} queries that reference it. Make sure that your changes are compatible with existing queries that use this index.
   :::

4. If you made changes, select **Save** before closing the flyout.

#### Reset the lookup index configuration

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

### Add variable controls to your Discover queries [add-variable-control]
```{applies_to}
stack: preview 9.2
serverless: preview
```

Variable controls help you make your queries more dynamic instead of having to maintain several versions of almost identical queries.

![Variable control in Discover](/explore-analyze/images/variable-control-discover.png " =75%")

You can add them from your Discover {{esql}} query.

:::{include} ../_snippets/variable-control-procedure.md
:::

:::{include} ../_snippets/variable-control-examples.md
:::

#### Allow multi-value selections for {{esql}}-based variable controls [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

#### Edit a variable control

Once a control is active for your query, you can still edit it by hovering over it and by selecting the {icon}`pencil` **Edit** option that appears.

You can edit all of the options described in [](#add-variable-control).

When you save your edits, the control is updated for your query.

#### Import a Discover query along with its controls into a dashboard

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::
