---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Compare condition"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition-compare.html
---

# Compare condition [condition-compare]

Use the `compare` condition to perform a simple comparison against a value in the watch payload. You can use the `compare` condition without enabling dynamic scripting.

## Compare condition operators [condition-compare-operators]

| Name | Description |
| --- | --- |
| `eq` | Returns `true` when the resolved value equals the given one (applies              to numeric, string, list, object and values) |
| `not_eq` | Returns `true` when the resolved value does not equal the given one              (applies to numeric, string, list, object and null values) |
| `gt` | Returns `true` when the resolved value is greater than the given              one (applies to numeric and string values) |
| `gte` | Returns `true` when the resolved value is greater/equal than/to the              given one (applies to numeric and string values) |
| `lt` | Returns `true` when the resolved value is less than the given one              (applies to numeric and string values) |
| `lte` | Returns `true` when the resolved value is less/equal than/to the              given one (applies to numeric and string values) |

## Using a compare condition [_using_a_compare_condition]

To use the `compare` condition, you specify the value in the execution context that you want to evaluate, a [comparison operator](#condition-compare-operators), and the value you want to compare against. For example, the following `compare` condition returns `true` if the number of the total hits in the [search result](input-search.md) is greater than or equal to 5:

```js
{
  "condition" : {
    "compare" : {
      "ctx.payload.hits.total" : { <1>
        "gte" : 5 <2>
      }
    }
  }
}
```

1. Use dot notation to reference a value in the execution context.
2. Specify a comparison operator and the value you want to compare against.
%  NOTCONSOLE

You can also compare two values in the execution context by specifying the compared value as a path of the form of `{{path}}`. For example, the following condition compares the `ctx.payload.aggregations.status.buckets.error.doc_count` to the `ctx.payload.aggregations.handled.buckets.true.doc_count`:

```js
{
  "condition" : {
    "compare" : {
      "ctx.payload.aggregations.status.buckets.error.doc_count" : {
        "not_eq" : "{{ctx.payload.aggregations.handled.buckets.true.doc_count}}"
      }
    }
  }
}
```
%  NOTCONSOLE

## Using date math in a compare condition [compare-condition-date-math]

When comparing dates and times, you can use date math expressions of the form `<{{expression}}>`. For example, the following expression returns `true` if the watch was executed within the last five minutes:

```js
{
  "condition" : {
    "compare" : {
      "ctx.execution_time" : {
        "gte" : "<{now-5m}>"
      }
    }
  }
}
```
%  NOTCONSOLE

## Accessing values in the execution context [_accessing_values_in_the_execution_context]

You use "dot-notation" to access values in the execution context. Values loaded into the execution context by the input are prefixed by `ctx.payload`.

You can reference entries in arrays using their zero-based array indices. For example, to access the third element of the `ctx.payload.hits.hits` array, use `ctx.payload.hits.hits.2`.

| Name | Description |
| --- | --- |
| `ctx.watch_id` | The id of the watch that is currently executing. |
| `ctx.execution_time` | The time execution of this watch started. |
| `ctx.trigger.triggered_time` | The time this watch was triggered. |
| `ctx.trigger.scheduled_time` | The time this watch was supposed to be triggered. |
| `ctx.metadata.*` | Any metadata associated with the watch. |
| `ctx.payload.*` | The payload data loaded by the watch’s input. |
