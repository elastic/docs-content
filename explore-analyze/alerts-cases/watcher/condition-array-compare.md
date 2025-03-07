---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Array compare condition"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition-array-compare.html
---

# Array compare condition [condition-array-compare]

Use `array_compare` to compare an array of values in the execution context to a given value. See [Table 84](condition-compare.md#condition-compare-operators) for the operators you can use.

## Using an array compare condition [_using_an_array_compare_condition]

To use the `array_compare` condition, you specify the array in the execution context that you want to evaluate, a [comparison operator](condition-compare.md#condition-compare-operators), and the value you want to compare against. Optionally, you can specify the path to the field in each array element that you want to evaluate.

For example, the following `array_compare` condition returns `true` if there is at least one bucket in the aggregation that has a `doc_count` greater than or equal to 25:

```js
{
  "condition": {
    "array_compare": {
      "ctx.payload.aggregations.top_tweeters.buckets" : { <1>
        "path": "doc_count", <2>
        "gte": { <3>
          "value": 25 <4>
        }
      }
    }
  }
}
```

1. The path to the array in the execution context that you want to evaluate, specified in dot notation.
2. The path to the field in each array element that you want to evaluate.
3. The [comparison operator](condition-compare.md#condition-compare-operators) to use.
4. The comparison value. Supports date math like the [compare condition](condition-compare.md#compare-condition-date-math).
%  NOTCONSOLE

::::{note}
When using fieldnames that contain a dot this condition will not work, use a [script condition](condition-script.md) instead.
::::

## Array-compare condition attributes [_array_compare_condition_attributes]

| Name | Description |
| --- | --- |
| `<array path>` | The path to the array in the execution                                         context, specified in dot notation.                                         For example, `ctx.payload.aggregations.top_tweeters.buckets`. |
| `<array path>.path` | The path to the field in each array element                                         that you want to evaluate. For example,                                         `doc_count`. Defaults to an empty string. |
| `<array path>.<operator>.quantifier` | How many matches are required for the                                         comparison to evaluate to `true`: `some`                                         or `all`. Defaults to `some`--there must                                         be at least one match. If the array is                                         empty, the comparison evaluates to `true`                                         if the quantifier is set to `all` and                                         `false` if the quantifier is set to                                         `some`. |
| `<array path>.<operator>.value` | The value to compare against. |
