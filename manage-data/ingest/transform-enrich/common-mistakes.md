---
mapped_pages:
  - https://www.elastic.co/docs/manage-data/ingest/transform-enrich/common-mistakes.html
applies_to:
  stack: ga
  serverless: ga
---

# Create readable and maintainable ingest pipelines

There are many ways to achieve similar results when creating ingest pipelines, which can make maintenance and readability difficult. This guide outlines patterns you can follow to make the maintenance and readability of ingest pipelines easier without sacrificing functionality.

:::{note}
This guide does not provide guidance on optimizing for ingest pipeline performance.
:::

## If Statements

`if` statements are frequently used in ingest pipeline processors to ensure that a processor only runs when specific conditions are met. By adding an `if` condition, you can control when a processor is applied, making your pipelines more flexible and robust.

### Avoiding Excessive OR Conditions

When using the [boolean OR operator](elasticsearch://reference/scripting-languages/painless/painless-operators-boolean.md#boolean-or-operator) (`||`), it's easy for `if` conditions to become overly complex and difficult to maintain, especially when chaining many OR checks. Instead, consider using array-based checks like `.contains()` to simplify your logic and improve readability.

#### ![don't](../../images/icon-cross.svg) **Don't**: Run many ORs

```painless
"if": "ctx?.kubernetes?.container?.name == 'admin' || ctx?.kubernetes?.container?.name == 'def'
|| ctx?.kubernetes?.container?.name == 'demo' || ctx?.kubernetes?.container?.name == 'acme'
|| ctx?.kubernetes?.container?.name == 'wonderful'
```

#### ![do](../../images/icon-check.svg) **Do**: Use contains to compare

```painless
["admin","def", ...].contains(ctx.kubernetes?.container?.name)
```

A key implication is that using `["admin", "def", ...].contains(ctx.kubernetes?.container?.name)` checks for exact matches only. For example, `"admin".contains("admin")` returns `true`, but `"demo-admin-demo".contains("admin")` would not match unless you explicitly check for partial matches using something like `ctx.kubernetes.container.name.contains('admin') || ...`.

Also, the null safe operator (`?.`) works as expected here—if the value is `null`, the `contains` method simply returns `false` without causing an error.

### Null safe operator

Anticipate potential problems with the data, and use the [null safe operator](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator) (`?.`) to prevent data from being processed incorrectly.

:::{tip}
It is not necessary to use a null safe operator for first level objects
(for example, use `ctx.openshift` instead of `ctx?.openshift`).
`ctx` will only ever be `null` if the entire `_source` is empty.
:::

For example, if you only want data that has a valid string in a `ctx.openshift.origin.threadId` field:

#### ![don't](../../images/icon-cross.svg) **Don't**: Leave the condition vulnerable to failures and use redundant checks

```painless
ctx.openshift.origin != null <1>
&& ctx.openshift.origin.threadId != null <2>
```

1. It's unnecessary to check both `openshift.origin` and `openshift.origin.threadId`.
2. This will fail if `openshift` is not properly set because it assumes that `ctx.openshift` and `ctx.openshift.origin` both exist.

#### ![do](../../images/icon-check.svg) **Do**: Use the null safe operator

```painless
ctx.openshift?.origin?.threadId instanceof String <1>
```

1. Only if there's a `ctx.openshift` and a `ctx.openshift.origin` will it check for a `ctx.openshift.origin.threadId` and make sure it is a string.

### Use null safe operators when checking type

If you're using a null safe operator, it will return the value if it is not `null` so there is no reason to check whether a value is not `null` before checking the type of that value.

For example, if you only want data when the value of the `ctx.openshift.origin.eventPayload` field is a string:

#### ![don't](../../images/icon-cross.svg) **Don't**: Use redundant checks

```painless
ctx?.openshift?.eventPayload != null && ctx.openshift.eventPayload instanceof String
```

#### ![do](../../images/icon-check.svg) **Do**: Use the null safe operator with the type check

```painless
ctx.openshift?.eventPayload instanceof String
```

### Use null safe operator with boolean OR operator

When using the [boolean OR operator](elasticsearch://reference/scripting-languages/painless/painless-operators-boolean.md#boolean-or-operator) (`||`), you need to use the null safe operator for both conditions being checked.

For example, if you want to include data when the value of the `ctx.event.type` field is either `null` or `'0'`:

#### ![don't](../../images/icon-cross.svg) **Don't**: Leave the conditions vulnerable to failures

```painless
ctx.event.type == null || ctx.event.type == '0' <1>
```

1. This will fail if `ctx.event` is not properly set because it assumes that `ctx.event` exists. If it fails on the first condition it won't even try the second condition.

#### ![do](../../images/icon-check.svg) **Do**: Use the null safe operator in both conditions

```painless
"if": "ctx.event?.type == null || ctx.event?.type == '0'"
```

1. Both conditions will be checked.

### Avoiding Redundant Null Checks

It is often unnecessary to use the `?` (null safe operator) multiple times when you have already traversed the object path.

#### ![don't](../../images/icon-cross.svg) **Don't**: Use redundant null safe operators

```painless
"if": "ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor?.ddos?.command_line != null"
```

#### ![do](../../images/icon-check.svg) **Do**: Use the null safe operator only where needed

Since the `if` condition is evaluated left to right, once `ctx.arbor?.ddos?.subsystem == 'CLI'` passes, you know `ctx.arbor.ddos` exists. You can safely omit the second `?`.

```painless
"if": "ctx.arbor?.ddos?.subsystem == 'CLI' && ctx.arbor.ddos.command_line != null"
```

This improves readability and avoids redundant checks.

### Checking for emptiness

When checking if a field is not empty, avoid redundant null safe operators and use clear, concise conditions.

#### ![don't](../../images/icon-cross.svg) **Don't**: Use redundant null safe operators

```painless
"if": "ctx?.user?.geo?.region != null && ctx?.user?.geo?.region != ''"
```

#### ![do](../../images/icon-check.svg) **Do**: Use the null safe operator only where needed

Once you've checked `ctx.user?.geo?.region != null`, you can safely access `ctx.user.geo.region` in the next condition.

```painless
"if": "ctx.user?.geo?.region != null && ctx.user.geo.region != ''"
```

#### ![do](../../images/icon-check.svg) **Do**: Use `.isEmpty()` for strings

% TO DO: Find link to `isEmpty()` method
To check if a string field is not empty, use the `isEmpty()` method in your condition. For example:

```painless
"if": "ctx.user?.geo?.region instanceof String && ctx.user.geo.region.isEmpty() == false"
```

This ensures the field exists, is a string, and is not empty.

:::{tip}
For such checks you can also ommit the `instanceof String` and use an [`Elvis`](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#elvis-operator) such as `if: ctx.user?.geo?.region?.isEmpty() ?: false`. This will only work when region is a String. If it is a double, object or any other type that does not have an `isEmpty()`function it will fail with a `Java Function not found` error.
:::

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

## Converting mb/gb values to bytes

When working with data sizes, it's best practice to store all values as bytes (using a `long` type) in Elasticsearch. This ensures consistency and allows you to leverage advanced formatting in Kibana Data Views to display human-readable sizes.

### ![don't](../../images/icon-cross.svg) **Don't**: Use multiple `gsub` processors for unit conversion

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

### ![do](../../images/icon-check.svg) **Do**: Use the `bytes` processor for automatic conversion

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

## Rename processor

The rename processor renames a field. There are two flags:

- ignore_missing
- ignore_failure

Ignore missing is useful when you are not sure that the field you want to rename from exist. Ignore_failure will help you with any failure encountered. The rename processor can only rename to non-existing fields. If you already have the field `abc` and you want to rename `def` to `abc` then the operation fails. The `ignore_failure` helps you in this case.

## Script processor

Sometimes, you may need to use a script processor in your ingest pipeline when no built-in processor can achieve your goal. However, it's important to write scripts that are clear, concise, and maintainable.

### Calculating `event.duration` in a complex manner

#### ![don't](../../images/icon-cross.svg) **Don't**: Use verbose and error-prone scripting patterns

The following example demonstrates several common mistakes:

- Accessing fields using square brackets (e.g., `ctx['temp']['duration']`) instead of dot notation.
- Using multiple `!= null` checks instead of the null safe operator (`?.`).
- Parsing substrings manually instead of leveraging date/time parsing utilities.
- Accessing `event.duration` directly without ensuring `event` exists.
- Calculating `event.duration` in milliseconds, when it should be in nanoseconds.

```json
{
  "script": {
    "source": """
       String timeString = ctx['temp']['duration'];
       ctx['event']['duration'] = Integer.parseInt(timeString.substring(0,2))*360000 + Integer.parseInt(timeString.substring(3,5))*60000 + Integer.parseInt(timeString.substring(6,8))*1000 + Integer.parseInt(timeString.substring(9,12));
     """,
    "if": "ctx.temp != null && ctx.temp.duration != null"
  }
}
```

This approach is hard to read, error-prone, and doesn't take advantage of the powerful date/time features available in Painless.

#### ![do](../../images/icon-check.svg) **Do**: Use null safe operators and built-in date/time utilities

A better approach is to:

- Use the null safe operator to check for field existence.
- Ensure the `event` object exists before assigning to it.
- Use `DateTimeFormatter` and `LocalTime` to parse the duration string.
- Store the duration in nanoseconds, as expected by ECS.

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
             if (ctx.event == null) {
               ctx.event = [:];
             }
             DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss.SSS");
             LocalTime time = LocalTime.parse(ctx.temp.duration, formatter);
             ctx.event.duration = time.toNanoOfDay();
           """,
          "if": "ctx.temp?.duration != null"
        }
      }
    ]
  }
}
```

This version is more robust, easier to maintain, and leverages the full capabilities of Painless and Java's date/time APIs. Always prefer built-in utilities and concise, readable code when writing script processors.

## Stitching together IP addresses in a script processor

When reconstructing or normalizing IP addresses in ingest pipelines, avoid unnecessary complexity and redundant operations.

### ![don't](../../images/icon-cross.svg) **Don't**: Use verbose and error-prone scripting patterns

- No check if `destination` is available as an object.
- Uses square bracket notation for field access.
- Unnecessary casting to `Integer` when parsing string segments.
- Allocates an extra variable for the IP string instead of setting the field directly.

```json
{
  "script": {
    "source": """
        String[] ipSplit = ctx['destination']['ip'].splitOnToken('.');
        String ip = Integer.parseInt(ipSplit[0]) + '.' + Integer.parseInt(ipSplit[1]) + '.' + Integer.parseInt(ipSplit[2]) + '.' + Integer.parseInt(ipSplit[3]);
        ctx['destination']['ip'] = ip;
    """,
    "if": "(ctx['destination'] != null) && (ctx['destination']['ip'] != null)"
  }
}
```

### ![do](../../images/icon-check.svg) **Do**: Use concise, readable, and safe scripting

- Use dot notation for field access.
- Use the null safe operator (`?.`) to check for field existence.
- Avoid unnecessary casting and extra variables.

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
            def temp = ctx.destination.ip.splitOnToken('.');
            ctx.destination.ip = temp[0] + "." + temp[1] + "." + temp[2] + "." + temp[3];
          """,
          "if": "ctx.destination?.ip != null"
        }
      }
    ]
  }
}
```

This approach is more maintainable, avoids unnecessary operations, and ensures your pipeline scripts are robust and easy to understand.

## ![don't](../../images/icon-cross.svg) **Don't**: Remove `@timestamp` before using the date processor

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

#### ![do](../../images/icon-check.svg) **Do**: Use array index notation in Mustache templates

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
