---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-expression.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Lucene expressions language [modules-scripting-expression]

Lucene’s expressions compile a `javascript` expression to bytecode. They are designed for high-performance custom ranking and sorting functions and are enabled for `inline` and `stored` scripting by default.


## Performance [_performance] 

Expressions were designed to have competitive performance with custom Lucene code. This performance is due to having low per-document overhead as opposed to other scripting engines: expressions do more "up-front".

This allows for very fast execution, even faster than if you had written a `native` script.


## Syntax [_syntax] 

Expressions support a subset of javascript syntax: a single expression.

See the [expressions module documentation](https://lucene.apache.org/core/10_0_0/expressions/index.html?org/apache/lucene/expressions/js/package-summary.md) for details on what operators and functions are available.

Variables in `expression` scripts are available to access:

* document fields, e.g. `doc['myfield'].value`
* variables and methods that the field supports, e.g. `doc['myfield'].empty`
* Parameters passed into the script, e.g. `mymodifier`
* The current document’s score, `_score` (only available when used in a `script_score`)

You can use Expressions scripts for `script_score`, `script_fields`, sort scripts, and numeric aggregation scripts, simply set the `lang` parameter to `expression`.


## Numeric field API [_numeric_field_api] 

| Expression | Description |
| --- | --- |
| `doc['field_name'].value` | The value of the field, as a `double` |
| `doc['field_name'].empty` | A boolean indicating if the field has novalues within the doc. |
| `doc['field_name'].length` | The number of values in this document. |
| `doc['field_name'].min()` | The minimum value of the field in this document. |
| `doc['field_name'].max()` | The maximum value of the field in this document. |
| `doc['field_name'].median()` | The median value of the field in this document. |
| `doc['field_name'].avg()` | The average of the values in this document. |
| `doc['field_name'].sum()` | The sum of the values in this document. |

When a document is missing the field completely, by default the value will be treated as `0`. You can treat it as another value instead, e.g. `doc['myfield'].empty ? 100 : doc['myfield'].value`

When a document has multiple values for the field, by default the minimum value is returned. You can choose a different value instead, e.g. `doc['myfield'].sum()`.

When a document is missing the field completely, by default the value will be treated as `0`.

Boolean fields are exposed as numerics, with `true` mapped to `1` and `false` mapped to `0`. For example: `doc['on_sale'].value ? doc['price'].value * 0.5 : doc['price'].value`


## Date field API [_date_field_api] 

Date fields are treated as the number of milliseconds since January 1, 1970 and support the Numeric Fields API above, plus access to some date-specific fields:

| Expression | Description |
| --- | --- |
| `doc['field_name'].date.centuryOfEra` | Century (1-2920000) |
| `doc['field_name'].date.dayOfMonth` | Day (1-31), e.g. `1` for the first of the month. |
| `doc['field_name'].date.dayOfWeek` | Day of the week (1-7), e.g. `1` for Monday. |
| `doc['field_name'].date.dayOfYear` | Day of the year, e.g. `1` for January 1. |
| `doc['field_name'].date.era` | Era: `0` for BC, `1` for AD. |
| `doc['field_name'].date.hourOfDay` | Hour (0-23). |
| `doc['field_name'].date.millisOfDay` | Milliseconds within the day (0-86399999). |
| `doc['field_name'].date.millisOfSecond` | Milliseconds within the second (0-999). |
| `doc['field_name'].date.minuteOfDay` | Minute within the day (0-1439). |
| `doc['field_name'].date.minuteOfHour` | Minute within the hour (0-59). |
| `doc['field_name'].date.monthOfYear` | Month within the year (1-12), e.g. `1` for January. |
| `doc['field_name'].date.secondOfDay` | Second within the day (0-86399). |
| `doc['field_name'].date.secondOfMinute` | Second within the minute (0-59). |
| `doc['field_name'].date.year` | Year (-292000000 - 292000000). |
| `doc['field_name'].date.yearOfCentury` | Year within the century (1-100). |
| `doc['field_name'].date.yearOfEra` | Year within the era (1-292000000). |

The following example shows the difference in years between the `date` fields date0 and date1:

`doc['date1'].date.year - doc['date0'].date.year`


## `geo_point` field API [geo-point-field-api] 

| Expression | Description |
| --- | --- |
| `doc['field_name'].empty` | A boolean indicating if the field has novalues within the doc. |
| `doc['field_name'].lat` | The latitude of the geo point. |
| `doc['field_name'].lon` | The longitude of the geo point. |

The following example computes distance in kilometers from Washington, DC:

`haversin(38.9072, 77.0369, doc['field_name'].lat, doc['field_name'].lon)`

In this example the coordinates could have been passed as parameters to the script, e.g. based on geolocation of the user.


## Limitations [_limitations_5] 

There are a few limitations relative to other script languages:

* Only numeric, `boolean`, `date`, and `geo_point` fields may be accessed
* Stored fields are not available

