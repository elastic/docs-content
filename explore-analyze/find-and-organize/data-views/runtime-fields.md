---
description: Add runtime fields to a Kibana data view to compute values at query time, without reindexing your data.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Explore your data with runtime fields [runtime-fields]

Runtime fields are fields that you add to documents after you've ingested your data. {{kib}} evaluates them at query time. They are not stored in the index.

Add a runtime field to a data view to define a field for a specific use case, override values returned from index fields, or work with data before you understand its structure, without reindexing.

::::{warning}
Runtime fields can impact {{kib}} performance. When you run a query, {{es}} uses the fields you index first to shorten the response time. Index the fields that you commonly search for and filter on, such as `timestamp`, then use runtime fields to limit the number of fields {{es}} uses to calculate values.
::::

## Before you begin [runtime-fields-prereqs]

You need the same privileges required to [create a data view](create-data-view.md#create-data-view-prereqs).

## Add runtime fields [create-runtime-fields]

Add a runtime field on the data view you want to change by emitting a value with the [Painless scripting language](/explore-analyze/scripting/modules-scripting-painless.md). You can also add runtime fields in [**Discover**](/explore-analyze/discover/discover-get-started.md#add-field-in-discover) and [**Lens**](/explore-analyze/visualize/lens.md#change-the-fields).

Runtime fields created against a data view are not applied to the underlying index mapping in {{es}}.

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that you want to add the runtime field to, then select **Add field**.
3. Enter the field **Name**, then select the **Type**.
4. Select **Set custom label**, then enter the label you want to display where the data view is used, such as **Discover**.
5. Select **Set value**, then define the script. The script must match the **Type**, or the data view fails anywhere it is used.
6. To help you define the script, use the **Preview**:

    * To view the other available fields, use the **Document ID** arrows.
    * To filter the fields list, enter the keyword in **Filter fields**.
    * To pin frequently used fields to the top of the list, hover over the field, then select ![Icon to pin field to the top of the list](/explore-analyze/images/kibana-stackManagement-indexPatterns-pinRuntimeField-7.15.png "").

7. Select **Create field**.

The new field is available anywhere the data view is used, for example in **Discover** or when building a **Lens** visualization.

For detailed information on how to use runtime fields with {{es}}, refer to [Runtime fields](/manage-data/data-store/mapping/runtime-fields.md). Runtime fields are different from unmapped fields, which can be present in documents but not defined in the index mapping. To query unmapped fields in {{esql}}, refer to [Unmapped fields](elasticsearch://reference/query-languages/esql/esql-unmapped-fields.md).

## Runtime field examples [runtime-field-examples]

Try the runtime field examples on your own using the [**Sample web logs**](/explore-analyze/index.md#gs-get-data-into-kibana) data.

### Return a keyword value [simple-hello-world-example]

Return `Hello World!`:

```text
emit("Hello World!");
```

![Runtime field with keyword type](/explore-analyze/images/kibana-runtime_field.png "")

### Perform a calculation on a single field [perform-a-calculation-on-a-single-field]

Calculate kilobytes from bytes:

```text
emit(doc['bytes'].value / 1024)
```

### Return a substring [return-substring]

Return the string that appears after the last slash in the URL:

```text
def path = doc["url.keyword"].value;
if (path != null) {
    int lastSlashIndex = path.lastIndexOf('/');
    if (lastSlashIndex > 0) {
        emit(path.substring(lastSlashIndex+1));
    return;
    }
}
emit("");
```

### Return multiple fields with a composite runtime field [composite-runtime-field]

A single runtime field can also produce multiple subfields when you select the `Composite` type. The script editor provides default types that you can customize for each subfield.

Return `keyword` and `double` type subfields. The first argument for `emit` is the name of the subfield.

```text
emit('subfield_a', 'Hello');
emit('subfield_b', 42);
```

![Runtime field with composite type](/explore-analyze/images/kibana-runtime_field_composite.png "")

### Replace nulls with blanks [replace-nulls-with-blanks]

Replace `null` values with `None`:

```text
def source = doc['referer'].value;
if (source != null) {
  emit(source);
  return;
}
else {
  emit("None");
}
```

Specify the operating system condition:

```text
def source = doc['machine.os.keyword'].value;
if (source != "") {
  emit(source);
}
else {
  emit("None");
}
```

## Manage runtime fields [manage-runtime-fields]

Edit the settings for runtime fields, or remove runtime fields from data views.

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the runtime field you want to manage, then open the runtime field edit options or delete the runtime field.

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
* [Manage scripted fields](scripted-fields.md)
