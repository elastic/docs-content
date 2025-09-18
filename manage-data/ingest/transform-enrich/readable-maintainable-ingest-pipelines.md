---
applies_to:
  stack: ga
  serverless: ga
---

# Create readable and maintainable ingest pipelines

There are many ways to achieve similar results when creating ingest pipelines, which can make maintenance and readability difficult. This guide outlines patterns you can follow to make the maintenance and readability of ingest pipelines easier without sacrificing functionality.

:::{note}
This guide does not provide guidance on optimizing for ingest pipeline performance.
:::

## Access fields

When creating ingest pipelines, there are are few options for accessing fields in conditional statements and scripts. All formats can be used to reference fields, so choose the one that makes your pipeline easier to read and maintain.

| Notation                       | Example                                               | Notes                                                                           |
| ------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------------------------- |
| Dot notation                   | `ctx.event.action`                                    | Supported in conditionals and painless scripts.                                 |
| Square bracket notation        | `ctx['event']['action']`                              | Supported in conditionals and painless scripts.                                 |
| Mixed dot and bracket notation | `ctx.event['action']`                                 | Supported in conditionals and painless scripts.                                 |
| Field API  {applies_to}`stack: ga 9.2.0`                    | `field('event.action', '')` or `$('event.action','')` | Supported in conditionals and painless scripts. |
| Field API                      | `field('event.action', '')` or `$('event.action','')` | Supported only in painless scripts.                                             |

Below are some general guidelines for choosing the right option in a situation.

### Field API

```{applies_to}
stack: ga 9.2.0
```

The field API can be used in conditionals (the `if` statement of your processor) in addition to being used in the script processor itself.

:::{note}
This is the preferred way to access fields.
:::

**Benefits**

- Clean and easy to read.
- Handles null values automatically.
- Adds support for additional functions like `isEmpty()` to ease comparisons.
- Handles dots as part of field name.
- Handles dots as dot walking for object notation.
- Handles special characters.

**Limitations**

- Not available in all versions for conditionals.

### Dot notation [dot-notation]

**Benefits**

- Clean and easy to read.
- Supports null safe operations `?`. Read more in [Use null safe operators (`?.`)](#null-safe-operators).

**Limitations**

- Does not support field names that contain a `.` or any special characters such as `@`.
  Use [Bracket notation](#bracket-notation) instead.

### Bracket notation [bracket-notation]

**Benefits**

- Supports special characters such as `@` in the field name.
  For example, if there's a field name called `has@!%&chars`, you would use `ctx['has@!%&chars']`.
- Supports field names that contain `.`.
  For example, if there's a field named `foo.bar`, if you used `ctx.foo.bar` it will try to access the field `bar` in the object `foo` in the object `ctx`. If you used `ctx['foo.bar']` it can access the field directly.

**Limitations**

- Slightly more verbose than dot notation.
- No support for null safe operations `?`.
  Use [Dot notation](#dot-notation) instead.

### Mixed dot and bracket notation

**Benefits**

- You can also mix dot notation and bracket notation to take advantage of the benefits of both formats.
  For example, you could use `ctx.my.nested.object['has@!%&chars']`. Then you can use the `?` operator on the fields using dot notation while still accessing a field with a name that contains special characters: `ctx.my?.nested?.object['has@!%&chars']`.

**Limitations**

- Slightly more difficult to read.

## Write concise conditionals (`if` statements) [conditionals]

Use conditionals (`if` statements) to ensure that an ingest pipeline processor is only applied when specific conditions are met.

% In an ingest pipeline, when working with conditionals inside processors. The topic around error processing is a bit more complex, most importantly any errors that are coming from null values, missing keys, missing values, inside the conditional, will lead to an error that is not captured by the `ignore_failure` handler and will exit the pipeline.

### Use null safe operators (`?.`) [null-safe-operators]

Anticipate potential problems with the data, and use the [null safe operator](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator) (`?.`) to prevent data from being processed incorrectly.

:::{tip}
It is not necessary to use a null safe operator for first level objects
(for example, use `ctx.openshift` instead of `ctx?.openshift`).
`ctx` will only ever be `null` if the entire `_source` is empty.
:::

For example, if you only want data that has a valid string in a `ctx.openshift.origin.threadId` field:

#### ![ ](../../images/icon-cross.svg) **Don't**: Leave the condition vulnerable to failures and use redundant checks

```painless
ctx.openshift.origin != null <1>
&& ctx.openshift.origin.threadId != null <2>
```

1. It's unnecessary to check both `openshift.origin` and `openshift.origin.threadId`.
2. This will fail if `openshift` is not properly set because it assumes that `ctx.openshift` and `ctx.openshift.origin` both exist.

#### ![ ](../../images/icon-check.svg) **Do**: Use the null safe operator

```painless
ctx.openshift?.origin?.threadId instanceof String <1>
```

1. Only if there's a `ctx.openshift` and a `ctx.openshift.origin` will it check for a `ctx.openshift.origin.threadId` and make sure it is a string.

### Use null safe operators when checking type

If you're using a null safe operator, it will return the value if it is not `null` so there is no reason to check whether a value is not `null` before checking the type of that value.

For example, if you only want data when the value of the `ctx.openshift.origin.eventPayload` field is a string:

#### ![ ](../../images/icon-cross.svg) **Don't**: Use redundant checks

```painless
ctx?.openshift?.eventPayload != null && ctx.openshift.eventPayload instanceof String
```

#### ![ ](../../images/icon-check.svg) **Do**: Use the null safe operator with the type check

```painless
ctx.openshift?.eventPayload instanceof String
```

### Use null safe operator with boolean OR operator

When using the [boolean OR operator](elasticsearch://reference/scripting-languages/painless/painless-operators-boolean.md#boolean-or-operator) (`||`), you need to use the null safe operator for both conditions being checked.

For example, if you want to include data when the value of the `ctx.event.type` field is either `null` or `'0'`:

#### ![ ](../../images/icon-cross.svg) **Don't**: Leave the conditions vulnerable to failures

```painless
ctx.event.type == null || ctx.event.type == '0' <1>
```

1. This will fail if `ctx.event` is not properly set because it assumes that `ctx.event` exists. If it fails on the first condition it won't even try the second condition.

#### ![ ](../../images/icon-check.svg) **Do**: Use the null safe operator in both conditions

```painless
ctx.event?.type == null || ctx.event?.type == '0' <1>
```

1. Both conditions will be checked.

### Avoid redundant null checks

It is often unnecessary to use the null safe operator (`.?`) multiple times when you have already traversed the object path.

For example, if you're checking the value of two different child properties of `ctx.arbor.ddos`:

#### ![ ](../../images/icon-cross.svg) **Don't**: Use redundant null safe operators

```painless
ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor?.ddos?.command_line != null
```

#### ![ ](../../images/icon-check.svg) **Do**: Use the null safe operator only where needed

```painless
ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor.ddos.command_line != null <1>
```

1. Since the `if` condition is evaluated left to right, once `ctx.arbor?.ddos?.subsystem == 'CLI'` passes, you know `ctx.arbor.ddos` exists so you can safely omit the second `?`.

### Check for emptiness

When checking if a field is not empty, avoid redundant null safe operators and use clear, concise conditions.

#### ![ ](../../images/icon-cross.svg) **Don't**: Use redundant null safe operators

```painless
ctx?.user?.geo?.region != null && ctx?.user?.geo?.region != ''
```

#### ![ ](../../images/icon-check.svg) **Do**: Use the null safe operator only where needed

Once you've checked `ctx.user?.geo?.region != null`, you can safely access `ctx.user.geo.region` in the next condition.

```painless
ctx.user?.geo?.region != null && ctx.user.geo.region != ''
```

#### ![ ](../../images/icon-check.svg) **Do**: Use `.isEmpty()` for strings

% TO DO: Find link to `isEmpty()` method
To check if a string field is not empty, use the `isEmpty()` method in your condition. For example:

```painless
ctx.user?.geo?.region instanceof String && ctx.user.geo.region.isEmpty() == false <1>
```

1. This ensures the field exists, is a string, and is not empty.

:::{tip}
For such checks you can also omit the `instanceof String` and use an [`Elvis`](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#elvis-operator) such as `if: ctx.user?.geo?.region?.isEmpty() ?: false`. This will only work when `region` is a `String`. If it is a `double`, `object`, or any other type that does not have an `isEmpty()` function, it will fail with a `Java Function not found` error.
:::

:::{dropdown} Full example

Here is a full reproducible example:

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "user": {
          "geo": {
            "region": "123"
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": {
            "region": ""
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": {
            "region": null
          }
        }
      }
    },
    {
      "_source": {
        "user": {
          "geo": null
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "demo",
          "value": true,
          "if": "if": "ctx.user?.geo?.region != null && ctx.user.geo.region != ''"
        }
      }
    ]
  }
}
```

:::

### Avoid excessive OR conditions

When using the [boolean OR operator](elasticsearch://reference/scripting-languages/painless/painless-operators-boolean.md#boolean-or-operator) (`||`), `if` conditions can become unnecessarily complex and difficult to maintain, especially when chaining many OR checks. Instead, consider using array-based checks like `.contains()` to simplify your logic and improve readability.

#### ![ ](../../images/icon-cross.svg) **Don't**: Run many ORs

```painless
"if": "ctx?.kubernetes?.container?.name == 'admin' || ctx?.kubernetes?.container?.name == 'def'
|| ctx?.kubernetes?.container?.name == 'demo' || ctx?.kubernetes?.container?.name == 'acme'
|| ctx?.kubernetes?.container?.name == 'wonderful'
```

#### ![ ](../../images/icon-check.svg) **Do**: Use contains to compare

```painless
["admin","def","demo","acme","wonderful"].contains(ctx.kubernetes?.container?.name)
```

:::{tip}
This example only checks for exact matches. Do not use this approach if you need to check for partial matches.
:::

## Convert mb/gb values to bytes

When working with data sizes, store all values as bytes (using a `long` type) in Elasticsearch. This ensures consistency and allows you to leverage advanced formatting in Kibana Data Views to display human-readable sizes.

### ![ ](../../images/icon-cross.svg) **Don't**: Use multiple `gsub` processors for unit conversion

Avoid chaining several `gsub` processors to strip units and manually convert values. This approach is error-prone, hard to maintain, and can easily miss edge cases.

```json
{
  "gsub": {
    "field": "document.size",
    "pattern": "M",
    "replacement": "",
    "ignore_missing": true,
    "if": "ctx?.document?.size != null && ctx.document.size.endsWith(\"M\")"
  }
},
{
  "gsub": {
    "field": "document.size",
    "pattern": "(\\d+)\\.(\\d+)G",
    "replacement": "$1$200",
    "ignore_missing": true,
    "if": "ctx?.uws?.size != null && ctx.document.size.endsWith(\"G\")"
  }
},
{
  "gsub": {
    "field": "document.size",
    "pattern": "G",
    "replacement": "000",
    "ignore_missing": true,
    "if": "ctx?.uws?.size != null && ctx.document.size.endsWith(\"G\")"
  }
}
```

### ![ ](../../images/icon-check.svg) **Do**: Use the `bytes` processor for automatic conversion

The [`bytes` processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/bytes-processor.html) automatically parses and converts strings like `"100M"` or `"2.5GB"` into their byte values. This is more reliable, easier to maintain, and supports a wide range of units.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "document": {
          "size": "100M"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "bytes": {
          "field": "document.size"
        }
      }
    ]
  }
}
```

:::{tip}
After storing values as bytes, you can use Kibana's field formatting to display them in a human-friendly format (KB, MB, GB, etc.) without changing the underlying data.
:::

## Rename fields

The [rename processor](elasticsearch://reference/enrich-processor/rename-processor.md) renames a field. There are two flags:

- `ignore_missing`: Useful when you are not sure that the field you want to rename exists.
- `ignore_failure`: Helps with any failures encountered. For example, the rename processor can only rename to non-existing fields. If you already have the field `abc` and you want to rename `def` to `abc`, the operation will fail.

## Script processor

If no built-in processor can achieve your goal, you may need to use a [script processor](elasticsearch://reference/enrich-processor/script-processor.md) in your ingest pipeline. Be sure to write scripts that are clear, concise, and maintainable.

### Add new fields

All of the above discussed ways to [access fields](#access-fields) and retrieve their values is applicable within the script context. [Null handling](#null-safe-operators) is still an important aspect when accessing the fields.

:::{tip}
The fields API is the recommended way to add new fields.
:::

For example, add a new `system.cpu.total.norm.pct` field based on the value of the `cpu.usage` field. The value of the existing `cpu.usage` field is a number on a scale of 0-100. The value of the new `system.cpu.total.norm.pct` field will be on a scale from 0-1.0 where 1 is the equivalent of 100 in the `cpu.usage` field.

**Option 1: Fields API (preferred)**
Create a new `system.cpu.total.norm.pct` field and set the value to the value of the `cpu.usage` field divided by `100.0`.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "cpu": {
          "usage": 90 <1>
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "script": {
          "source": """
            field('system.cpu.total.norm.pct').set($('cpu.usage',0.0)/100.0) <2>
          """
        }
      }
    ]
  }
}
```
1. This field expects 0-1 and not 0-100. When renaming the field, divide this value by 100 to get the correct value.
2. The `field` API is exposed as `field(<field name>)`. The `set(<value>)` is responsible for setting the value. Inside we use the `$(<field name>, fallback)` to read the value out of the existing field. Lastly we divide by `100.0`. The `.0` is important, otherwise it will perform an integer only division and return just 0 instead of 0.9.

**Option 2: Without the fields API**
Without the field API, there is much more code involved to ensure that you can walk the full path of `system.cpu.total.norm.pct`.

```json
{
  "script": {
    "source": "
      if(ctx.system == null){ <1>
        ctx.system = new HashMap(); <2>
      }
      if(ctx.system.cpu == null){
        ctx.system.cpu = [:]; <3>
      }
      if(ctx.system.cpu.total == null){
        ctx.system.cpu.total = [:];
      }
      if(ctx.system.cpu.total.norm == null){
        ctx.system.cpu.total.norm = [:];
      }
      ctx.system.cpu.total.norm.pct = $('cpu.usage', 0.0)/100.0; <4>
      "
  }
}
```
1. Check whether the objects are null or not and then create them.
2. Create a new `HashMap` to store all the objects in it.
3. Instead of writing `new HashMap()`, use the shortcut `[:]`.
4. Perform the same calculation as above and set the value.

### Calculate `event.duration` in a complex manner

#### ![ ](../../images/icon-cross.svg) **Don't**: Use verbose and error-prone scripting patterns

```json
{
  "script": {
    "source": """
       String timeString = ctx['temp']['duration']; <1>
       ctx['event']['duration'] = Integer.parseInt(timeString.substring(0,2))*360000 + Integer.parseInt(timeString.substring(3,5))*60000 + Integer.parseInt(timeString.substring(6,8))*1000 + Integer.parseInt(timeString.substring(9,12)); <2> <3> <4>
     """,
    "if": "ctx.temp != null && ctx.temp.duration != null" <5>
  }
}
```

1. Avoid accessing fields using square brackets instead of dot notation.
2. `ctx['event']['duration']`: Do not attempt to access child properties without ensuring the parent property exists.
3. `timeString.substring(0,2)`: Avoid parsing substrings manually instead of leveraging date/time parsing utilities.
4. `event.duration` should be in nanoseconds, as expected by ECS, instead of milliseconds.
5. Avoid redundant null checks instead of the null safe operator (`?.`).

This approach is hard to read, error-prone, and doesn't take advantage of the powerful date/time features available in Painless.

#### ![ ](../../images/icon-check.svg) **Do**: Use null safe operators and built-in date/time utilities

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "temp": {
          "duration": "00:00:06.448"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "script": {
          "source": """
             if (ctx.event == null) { <1>
               ctx.event = [:];
             }
             DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss.SSS"); <2>
             LocalTime time = LocalTime.parse(ctx.temp.duration, formatter);
             ctx.event.duration = time.toNanoOfDay(); <3>
           """,
          "if": "ctx.temp?.duration != null" <4>
        }
      }
    ]
  }
}
```

1. Ensure the `event` object exists before assigning to it.
2. Use `DateTimeFormatter` and `LocalTime` to parse the duration string.
3. Store the duration in nanoseconds, as expected by ECS.
4. Use the null safe operator to check for field existence.

### Stitch together IP addresses in a script processor

When reconstructing or normalizing IP addresses in ingest pipelines, avoid unnecessary complexity and redundant operations.

#### ![ ](../../images/icon-cross.svg) **Don't**: Use verbose and error-prone scripting patterns

```json
{
  "script": {
    "source": """
        String[] ipSplit = ctx['destination']['ip'].splitOnToken('.'); <1>
        String ip = Integer.parseInt(ipSplit[0]) + '.' + Integer.parseInt(ipSplit[1]) + '.' + Integer.parseInt(ipSplit[2]) + '.' + Integer.parseInt(ipSplit[3]); <2>
        ctx['destination']['ip'] = ip; <3>
    """,
    "if": "(ctx['destination'] != null) && (ctx['destination']['ip'] != null)" <4>
  }
}
```

1. Uses square bracket notation for field access instead of dot notation.
2. Unnecessary casting to `Integer` when parsing string segments.
3. Allocates an extra variable for the IP string instead of setting the field directly.
4. Does not check if `destination` is available as an object.

#### ![ ](../../images/icon-check.svg) **Do**: Use concise, readable, and safe scripting

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "destination": {
          "ip": "192.168.0.1.3.4.5.6.4"
        }
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "script": {
          "source": """
            def temp = ctx.destination.ip.splitOnToken('.'); <1>
            ctx.destination.ip = temp[0] + "." + temp[1] + "." + temp[2] + "." + temp[3]; <2>
          """,
          "if": "ctx.destination?.ip != null" <3>
        }
      }
    ]
  }
}
```

1. Uses dot notation for field access.
2. Avoids unnecessary casting and extra variables.
3. Uses the null safe operator (`?.`) to check for field existence.

This approach is more maintainable, avoids unnecessary operations, and ensures your pipeline scripts are robust and easy to understand.

## ![ ](../../images/icon-cross.svg) **Don't**: Remove `@timestamp` before using the date processor

It's a common mistake to explicitly remove the `@timestamp` field before running a date processor, as shown below:

```json
{
  "set": {
    "field": "openshift.timestamp",
    "value": "{{openshift.date}} {{openshift.time}}",
    "if": "ctx?.openshift?.date != null && ctx?.openshift?.time != null && ctx?.openshift?.timestamp == null"
  }
},
{
  "remove": {
    "field": "@timestamp",
    "ignore_missing": true,
    "if": "ctx?.openshift?.timestamp != null || ctx?.openshift?.timestamp1 != null"
  }
},
{
  "date": {
    "field": "openshift.timestamp",
    "formats": [
      "yyyy-MM-dd HH:mm:ss",
      "ISO8601"
    ],
    "timezone": "Europe/Vienna",
    "if": "ctx?.openshift?.timestamp != null"
  }
}
```

This removal step is unnecessary and can even be counterproductive. The `date` processor will automatically overwrite the value in `@timestamp` with the parsed date from your source field, unless you explicitly set a different `target_field`. There's no need to remove `@timestamp` beforehand—the processor will handle updating it for you.

Removing `@timestamp` can also introduce subtle bugs, especially if the date processor is skipped or fails, leaving your document without a timestamp.

## Mustache tips and tricks

Mustache is a simple templating language used in Elasticsearch ingest pipelines to dynamically insert field values into strings. You can use double curly braces (`{{ }}`) to reference fields from your document, enabling flexible and dynamic value assignment in processors like `set`, `rename`, and others.

For example, `{{host.hostname}}` will be replaced with the value of the `host.hostname` field at runtime. Mustache supports accessing nested fields, arrays, and even provides some basic logic for conditional rendering.

### Accessing values in an array

When you need to reference a specific element in an array using Mustache templates, you can use dot notation with the zero-based index. For example, to access the first value in the `tags` array, use `.0` after the array field name.

#### ![ ](../../images/icon-check.svg) **Do**: Use array index notation in Mustache templates

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "host": {
          "hostname": "abc"
        },
        "tags": [
          "cool-host"
        ]
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "host.alias",
          "value": "{{tags.0}}"
        }
      }
    ]
  }
}
```

In this example, `{{tags.0}}` retrieves the first element of the `tags` array (`"cool-host"`) and assigns it to the `host.alias` field. This approach is necessary when you want to extract a specific value from an array for use elsewhere in your document. Using the correct index ensures you get the intended value, and this pattern works for any array field in your source data.

### Transform into a JSON string

Whenever you need to store the original `_source` within a field `event.original`, use mustache function `{{#toJson}}<field>{{/toJson}}`.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "foo": "bar",
        "key": 123
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "event.original",
          "value": "{{#toJson}}_source{{/toJson}}"
        }
      }
    ]
  }
}
```
