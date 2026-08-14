---
description: Scripted fields compute values at query time from a Kibana data view. Deprecated in favor of runtime fields and ES|QL.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Scripted fields

::::{admonition} Deprecated in 7.13, creation removed in 9.0.
:class: warning

Use [runtime fields](runtime-fields.md) instead of scripted fields. Runtime fields support Painless scripting and provide greater flexibility. You can also use the [Elasticsearch Query Language (ES|QL)](elasticsearch://reference/query-languages/esql.md) to compute values directly at query time.
::::

Scripted fields compute data on the fly from your {{es}} indices. The values appear in **Discover** as part of the document data. You can use scripted fields in visualizations, query them with the [{{kib}} query language](/explore-analyze/query-filter/languages/kql.md), and filter them in the filter bar. The values are computed at query time, so they aren't indexed and can't be searched using the {{kib}} default query language.

Computing scripted fields at query time can be resource intensive and can slow {{kib}}. {{kib}} doesn't validate scripted fields. If a script contains errors, you get exceptions when you view the generated data.

When you define a scripted field in {{kib}}, you have a choice of the [Lucene expressions](/explore-analyze/scripting/modules-scripting-expression.md) or the [Painless](/explore-analyze/scripting/modules-scripting-painless.md) scripting language.

You can reference any single value numeric field in your expressions, for example:

```
doc['field_name'].value
```

For more information on scripted fields and additional examples, refer to [Using Painless in {{kib}} scripted fields](https://www.elastic.co/blog/using-painless-kibana-scripted-fields)

## Migrate to runtime fields or {{esql}} queries [migrate-off-scripted-fields]

The following examples migrate a scripted field called `computed_values` on the Kibana Sample Data Logs data view to a runtime field and to an {{esql}} query.

### Scripted field [scripted-field-example]

In the scripted field example, variables track every value the script needs to access or return. Scripted fields can return only a single value, so the variables must be returned together as an array at the end of the script.

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

Unlike scripted fields, runtime fields don't need to return a single value. They can emit values at any point in the script. {{kib}} combines those values and returns them as a multi-value field. That removes the need to manage an array of values yourself.

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

Alternatively, you can use {{esql}} to compute the values you need at query time, without managing a data view. {{esql}} can compute multiple field values in a single query, use those values with its commands and functions, and aggregate against them. That approach fits one-off queries and real-time analysis.

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

You need a role with the **Data View Management** {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

### Edit or delete a scripted field [update-scripted-field-steps]

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the scripted field you want to manage.
3. Select the **Scripted fields** tab, then open the scripted field edit options or delete the scripted field.

Your change takes effect immediately anywhere the data view is used.

For more information about scripted fields in {{es}}, refer to [Scripting](/explore-analyze/scripting.md).

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
* [Explore your data with runtime fields](runtime-fields.md)
