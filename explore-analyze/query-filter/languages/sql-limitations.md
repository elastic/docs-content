---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-limitations.html
---

# SQL Limitations [sql-limitations]


## Large queries may throw `ParsingException` [large-parsing-trees]

Extremely large queries can consume too much memory during the parsing phase, in which case the Elasticsearch SQL engine will abort parsing and throw an error. In such cases, consider reducing the query to a smaller size by potentially simplifying it or splitting it into smaller queries.


## Nested fields in `SYS COLUMNS` and `DESCRIBE TABLE` [sys-columns-describe-table-nested-fields]

{{es}} has a special type of relationship fields called `nested` fields. In Elasticsearch SQL they can be used by referencing their inner sub-fields. Even though `SYS COLUMNS` in non-driver mode (in the CLI and in REST calls) and `DESCRIBE TABLE` will still display them as having the type `NESTED`, they cannot be used in a query. One can only reference its sub-fields in the form:

```sql
[nested_field_name].[sub_field_name]
```

For example:

```sql
SELECT dep.dep_name.keyword FROM test_emp GROUP BY languages;
```


## Scalar functions on nested fields are not allowed in `WHERE` and `ORDER BY` clauses [_scalar_functions_on_nested_fields_are_not_allowed_in_where_and_order_by_clauses]

Elasticsearch SQL doesn’t support the usage of scalar functions on top of nested fields in `WHERE` and `ORDER BY` clauses with the exception of comparison and logical operators.

For example:

```sql
SELECT * FROM test_emp WHERE LENGTH(dep.dep_name.keyword) > 5;
```

and

```sql
SELECT * FROM test_emp ORDER BY YEAR(dep.start_date);
```

are not supported but:

```sql
SELECT * FROM test_emp WHERE dep.start_date >= CAST('2020-01-01' AS DATE) OR dep.dep_end_date IS NULL;
```

is supported.


## Multi-nested fields [_multi_nested_fields]

Elasticsearch SQL doesn’t support multi-nested documents, so a query cannot reference more than one nested field in an index. This applies to multi-level nested fields, but also multiple nested fields defined on the same level. For example, for this index:

```sql
       column         |     type      |    mapping
----------------------+---------------+-------------
nested_A              |STRUCT         |NESTED
nested_A.nested_X     |STRUCT         |NESTED
nested_A.nested_X.text|VARCHAR        |KEYWORD
nested_A.text         |VARCHAR        |KEYWORD
nested_B              |STRUCT         |NESTED
nested_B.text         |VARCHAR        |KEYWORD
```

`nested_A` and `nested_B` cannot be used at the same time, nor `nested_A`/`nested_B` and `nested_A.nested_X` combination. For such situations, Elasticsearch SQL will display an error message.


## Paginating nested inner hits [_paginating_nested_inner_hits]

When SELECTing a nested field, pagination will not work as expected, Elasticsearch SQL will return *at least* the page size records. This is because of the way nested queries work in {{es}}: the root nested field will be returned and it’s matching inner nested fields as well, pagination taking place on the **root nested document and not on its inner hits**.


## Normalized `keyword` fields [normalized-keyword-fields]

`keyword` fields in {{es}} can be normalized by defining a `normalizer`. Such fields are not supported in Elasticsearch SQL.


## Array type of fields [_array_type_of_fields]

Array fields are not supported due to the "invisible" way in which {{es}} handles an array of values: the mapping doesn’t indicate whether a field is an array (has multiple values) or not, so without reading all the data, Elasticsearch SQL cannot know whether a field is a single or multi value. When multiple values are returned for a field, by default, Elasticsearch SQL will throw an exception. However, it is possible to change this behavior through `field_multi_value_leniency` parameter in REST (disabled by default) or `field.multi.value.leniency` in drivers (enabled by default).


## Sorting by aggregation [_sorting_by_aggregation]

When doing aggregations (`GROUP BY`) Elasticsearch SQL relies on {{es}}'s `composite` aggregation for its support for paginating results. However this type of aggregation does come with a limitation: sorting can only be applied on the key used for the aggregation’s buckets. Elasticsearch SQL overcomes this limitation by doing client-side sorting however as a safety measure, allows only up to **65535** rows.

It is recommended to use `LIMIT` for queries that use sorting by aggregation, essentially indicating the top N results that are desired:

```sql
SELECT * FROM test GROUP BY age ORDER BY COUNT(*) LIMIT 100;
```

It is possible to run the same queries without a `LIMIT` however in that case if the maximum size (**10000**) is passed, an exception will be returned as Elasticsearch SQL is unable to track (and sort) all the results returned.

Moreover, the aggregation(s) used in the `ORDER BY` must be only plain aggregate functions. No scalar functions or operators can be used, and therefore no complex columns that combine two ore more aggregate functions can be used for ordering. Here are some examples of queries that are **not allowed**:

```sql
SELECT age, ROUND(AVG(salary)) AS avg FROM test GROUP BY age ORDER BY avg;

SELECT age, MAX(salary) - MIN(salary) AS diff FROM test GROUP BY age ORDER BY diff;
```


## Using a sub-select [_using_a_sub_select]

Using sub-selects (`SELECT X FROM (SELECT Y)`) is **supported to a small degree**: any sub-select that can be "flattened" into a single `SELECT` is possible with Elasticsearch SQL. For example:

```sql
SELECT * FROM (SELECT first_name, last_name FROM emp WHERE last_name NOT LIKE '%a%') WHERE first_name LIKE 'A%' ORDER BY 1;

  first_name   |   last_name
---------------+---------------
 Alejandro     |McAlpine
 Anneke        |Preusig
 Anoosh        |Peyn
 Arumugam      |Ossenbruggen
```

The query above is possible because it is equivalent with:

```sql
SELECT first_name, last_name FROM emp WHERE last_name NOT LIKE '%a%' AND first_name LIKE 'A%' ORDER BY 1;
```

But, if the sub-select would include a `GROUP BY` or `HAVING` or the enclosing `SELECT` would be more complex than `SELECT X FROM (SELECT ...) WHERE [simple_condition]`, this is currently **un-supported**.


## Using [`FIRST`](sql-functions-aggs.md#sql-functions-aggs-first)/[`LAST`](sql-functions-aggs.md#sql-functions-aggs-last) aggregation functions in `HAVING` clause [first-last-agg-functions-having-clause]

Using `FIRST` and `LAST` in the `HAVING` clause is not supported. The same applies to [`MIN`](sql-functions-aggs.md#sql-functions-aggs-min) and [`MAX`](sql-functions-aggs.md#sql-functions-aggs-max) when their target column is of type [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) or [`unsigned_long`](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html) as they are internally translated to `FIRST` and `LAST`.


## Using TIME data type in GROUP BY or [`HISTOGRAM`](sql-functions-grouping.md#sql-functions-grouping-histogram) [group-by-time]

Using `TIME` data type as a grouping key is currently not supported. For example:

```sql
SELECT count(*) FROM test GROUP BY CAST(date_created AS TIME);
```

On the other hand, it can still be used if it’s wrapped with a scalar function that returns another data type, for example:

```sql
SELECT count(*) FROM test GROUP BY MINUTE((CAST(date_created AS TIME));
```

`TIME` data type is also currently not supported in histogram grouping function. For example:

```sql
SELECT HISTOGRAM(CAST(birth_date AS TIME), INTERVAL '10' MINUTES) as h, COUNT(*) FROM t GROUP BY h
```


## Geo-related functions [geo-sql-limitations]

Since `geo_shape` fields don’t have doc values these fields cannot be used for filtering, grouping or sorting.

By default,`geo_points` fields are indexed and have doc values. However only latitude and longitude are stored and indexed with some loss of precision from the original values (4.190951585769653E-8 for the latitude and 8.381903171539307E-8 for longitude). The altitude component is accepted but not stored in doc values nor indexed. Therefore calling `ST_Z` function in the filtering, grouping or sorting will return `null`.


## Retrieving using the `fields` search parameter [using-fields-api]

Elasticsearch SQL retrieves column values using the [search API’s `fields` parameter](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-param). Any limitations on the `fields` parameter also apply to Elasticsearch SQL queries. For example, if `_source` is disabled for any of the returned fields or at index level, the values cannot be retrieved.


## Aggregations in the [`PIVOT`](sql-syntax-select.md#sql-syntax-pivot) clause [aggs-in-pivot]

The aggregation expression in [`PIVOT`](sql-syntax-select.md#sql-syntax-pivot) will currently accept only one aggregation. It is thus not possible to obtain multiple aggregations for any one pivoted column.


## Using a subquery in [`PIVOT`](sql-syntax-select.md#sql-syntax-pivot)'s `IN`-subclause [subquery-in-pivot]

The values that the [`PIVOT`](sql-syntax-select.md#sql-syntax-pivot) query could pivot must be provided in the query as a list of literals; providing a subquery instead to build this list is not currently supported. For example, in this query:

```sql
SELECT * FROM test_emp PIVOT (SUM(salary) FOR languages IN (1, 2))
```

the `languages` of interest must be listed explicitly: `IN (1, 2)`. On the other hand, this example would **not work**:

```sql
SELECT * FROM test_emp PIVOT (SUM(salary) FOR languages IN (SELECT languages FROM test_emp WHERE languages <=2 GROUP BY languages))
```
