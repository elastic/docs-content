---
description: Manage and migrate off scripted fields on a Kibana data view. Deprecated in favor of runtime fields and ES|QL.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Manage scripted fields [scripted-fields]

::::{admonition} Deprecated in 7.13, creation removed in 9.0.
:class: warning

Use [runtime fields](runtime-fields.md) instead of scripted fields. Runtime fields support Painless scripting and provide greater flexibility. You can also use the [Elasticsearch Query Language (ES|QL)](elasticsearch://reference/query-languages/esql.md) to compute values directly at query time.
::::

Scripted fields compute data on the fly from the data in your {{es}} indices. The data is shown on the Discover tab as part of the document data, and you can use scripted fields in your visualizations. You query scripted fields with the [{{kib}} query language](/explore-analyze/query-filter/languages/kql.md), and can filter them using the filter bar. The scripted field values are computed at query time, so they aren't indexed and cannot be searched using the {{kib}} default query language.

::::{warning}
Computing data on the fly with scripted fields can be very resource intensive and can have a direct impact on {{kib}} performance. Keep in mind that there's no built-in validation of a scripted field. If your scripts are buggy, you'll get exceptions whenever you try to view the dynamically generated data.
::::

When you define a scripted field in {{kib}}, you have a choice of the [Lucene expressions](/explore-analyze/scripting/modules-scripting-expression.md) or the [Painless](/explore-analyze/scripting/modules-scripting-painless.md) scripting language.

You can reference any single value numeric field in your expressions, for example:

```
doc['field_name'].value
```

For more information on scripted fields and additional examples, refer to [Using Painless in {{kib}} scripted fields](https://www.elastic.co/blog/using-painless-kibana-scripted-fields)

## Migrate to runtime fields or {{esql}} queries [migrate-off-scripted-fields]

The following code snippets demonstrate how an example scripted field called `computed_values` on the Kibana Sample Data Logs data view could be migrated to either a runtime field or an {{esql}} query, highlighting the differences between each approach.

### Scripted field [scripted-field-example]

In the scripted field example, variables are created to track all values the script will need to access or return. Since scripted fields can only return a single value, the created variables must be returned together as an array at the end of the script.

```text
def hour_of_day = $('@timestamp', ZonedDateTime.parse('1970-01-01T00:00:00Z')).getHour();
def time_of_day = '';

if (hour_of_day >= 22 || hour_of_day < 5)
  time_of_day = 'Night';
else if (hour_of_day < 12)
  time_of_day = 'Morning';
else if (hour_of_day < 18)
  time_of_day = 'Afternoon';
else
  time_of_day = 'Evening';

def response_int = Integer.parseInt($('response.keyword', '200'));
def response_category = '';

if (response_int < 200)
  response_category = 'Informational';
else if (response_int < 300)
  response_category = 'Successful';
else if (response_int < 400)
  response_category = 'Redirection';
else if (response_int < 500)
  response_category = 'Client Error';
else
  response_category = 'Server Error';

return [time_of_day, response_category];
```

### Runtime field [runtime-field-example]

Unlike scripted fields, runtime fields do not need to return a single value and can emit values at any point in the script, which will be combined and returned as a multi-value field. This allows for more flexibility in the script logic and removes the need to manually manage an array of values.

```text
def hour_of_day = $('@timestamp', ZonedDateTime.parse('1970-01-01T00:00:00Z')).getHour();

if (hour_of_day >= 22 || hour_of_day < 5)
  emit('Night');
else if (hour_of_day < 12)
  emit('Morning');
else if (hour_of_day < 18)
  emit('Afternoon');
else
  emit('Evening');

def response_int = Integer.parseInt($('response.keyword', '200'));

if (response_int < 200)
  emit('Informational');
else if (response_int < 300)
  emit('Successful');
else if (response_int < 400)
  emit('Redirection');
else if (response_int < 500)
  emit('Client Error');
else
  emit('Server Error');
```

### ES|QL query [esql-example]

Alternatively, ES|QL can be used to skip the need for data view management entirely and compute the values you need directly at query time. ES|QL supports computing multiple field values in a single query, using computed values with its rich set of commands and functions, and even aggregations against computed values. This makes it an excellent solution for one-off queries and realtime data analysis.

```esql
FROM kibana_sample_data_logs
  | EVAL hour_of_day = DATE_EXTRACT("HOUR_OF_DAY", @timestamp)
  | EVAL time_of_day = CASE(
      hour_of_day >= 22 OR hour_of_day < 5, "Night",
      hour_of_day < 12, "Morning",
      hour_of_day < 18, "Afternoon",
      "Evening"
    )
  | EVAL response_int = TO_INTEGER(response)
  | EVAL response_category = CASE(
      response_int < 200, "Informational",
      response_int < 300, "Successful",
      response_int < 400, "Redirection",
      response_int < 500, "Client Error",
      "Server Error"
    )
  | EVAL computed_values = MV_APPEND(time_of_day, response_category)
  | DROP hour_of_day, time_of_day, response_int, response_category
```

## Existing scripted fields [update-scripted-field]

::::{warning}
The ability to create new scripted fields has been removed from the **Data Views** management page in 9.0. Existing scripted fields can still be edited or deleted, and the creation UI can be accessed by navigating directly to `/app/management/kibana/dataViews/dataView/{{dataViewId}}/create-field`, but we recommend migrating to runtime fields or ES|QL queries instead to prepare for removal.
::::

### Before you begin [scripted-fields-prereqs]

You need the same privileges required to [create a data view](create-data-view.md#create-data-view-prereqs).

### Edit or delete a scripted field [update-scripted-field-steps]

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the scripted field you want to manage.
3. Select the **Scripted fields** tab, then open the scripted field edit options or delete the scripted field.

Your change takes effect immediately anywhere the data view is used.

For more information about scripted fields in {{es}}, refer to [Scripting](/explore-analyze/scripting.md).

::::{warning}
Built-in validation is unsupported for scripted fields. When your scripts contain errors, you receive exceptions when you view the dynamically generated data.
::::

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
* [Explore your data with runtime fields](runtime-fields.md)
