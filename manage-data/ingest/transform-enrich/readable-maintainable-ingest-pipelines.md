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

## Write concise `if` conditional statements

Use `if` statements to ensure that an ingest pipeline processor is only applied when specific conditions are met.

### Accessing fields in conditionals

In an ingest pipeline, when working with `if` statements also known as conditionals inside processors. The topic around error processing is a bit more complex, most importantly any errors that are coming from null values, missing keys, missing values, inside the conditional, will lead to an error that is not captured by the `ignore_failure` handler and will exit the pipeline.

You can access fields in two ways:

- Dot notation
- Square bracket notation

For example:

- `ctx.event.action`

is equivalent to:

- `ctx['event']['action']`

Both notations can be used to reference fields, so choose the one that makes your pipeline easier to read and maintain.

:::{warn}
No support for null safety operations `?`
{warn}

Use the bracket notation when you have special characters such as `@` in the field name, or a `.` in the field name. As an example:

- field_name: `demo.cool.stuff`

using:

`ctx.demo.cool.stuff` it would try to access the field `stuff` in the object `cool` in the object `demo`.

using:

`ctx['demo.cool.stuff']` it can access the field directly.

You can also mix and match both worlds when needed:

- field_name: `my.nested.object.has@!%&chars`

Proper way: `ctx.my.nested.object['has@!%&chars']`

You can even, partially use the `?` operator:

- `ctx.my?.nested?.object['has@!%&chars']`

But it will error if object is `null`. To be a 100% on the safe side you need to write the following statement:

- `ctx.my?.nested?.object != null && ctx.my.nested.object['has@!%&chars'] == ...`

#### Accessing fields in a script

Within a script there are the same two possibilities to access fields as above. As well as the new `getter`. This only works in the painless scripts in an ingest pipeline. Take the following input:

```json
{
  "_source": {
       "user_name": "philipp"
  }
}
```

When you want to set the `user.name` field with a script:

- `ctx.user.name = ctx.user_name`

This works as long as `user_name` is populated. If it is null you will get `null` as value. Additionally, when the `user` object does not exist, it will error because Java needs you to define the `user` object first before adding a key `name` into it. We cover the `new HashMap()` further down.

This is one of the alternatives to get it working when you only want to set it, if it is not null

```painless
if (ctx.user_name != null) {
   ctx.user = new HashMap();
   ctx.user.name = ctx.user_name;
}
```

This works fine, as you now check for null.

However there is also an easier to write and maintain alternative available:

- `ctx.user.name = $('user_name', null);`

This $('field', 'fallback') allows you to specify the field without the `CTX` for walking. You can even supply `$('this.very.nested.field.is.super.far.away', null)` when you need to. The fallback is in case the field is null. This comes in very handy when needing to do certain manipulation of data. Let's say you want to lowercase all the field names, you can simply write this now:

- `ctx.user.name = $('user_name','').toLowerCase();`

You see that I switched up the null value to an empty String. Since the String has the `toLowerCase()` function. This of course works with all types. Bit of a silly thing, since you could simply write `object.abc` as the field value. As an example you can see that we can even create a map, list, array, whatever you want.

- `if ($('object', {}).containsKey('abc')){}`

One common thing I use it for is when dealing with numbers and casting. The field specifies the usage in `%`, however Elasticsearch doesn't like this, or better to say Kibana renders % as `0-1` for `0%-100%` and not `0-100`. `100` is equal to `10.000%`

- field: `cpu_usage = 100.00`
- `ctx.cpu.usage = $('cpu_usage',0.0)/100`

This allows me to always set the `cpu.usage` field and not to worry about it, have an always working division. One other way to leverage this, in a simpler script is like this, but most scripts are rather complex so this is not that often applicable.

```json
{
  "script": {
    "source": "ctx.abc = ctx.def"
    "if": "ctx.def != null"
  }
}
```

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

### Use null safe operators `?`

In simplest case the `ignore_missing` parameter is available in most processors to handle fields without values. Or the `ignore_failure` parameter to let the processor fail without impacting the pipeline you  but sometime you will need to use  the [null safe operator `?.`](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator) to check if a field exists and is not `null`.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "host": {
          "hostname": "test"
        },
        "ip": "127.0.0.1"
      }
    },
    {
      "_source": {
        "ip": "127.0.0.1"
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "a",
          "value": "b",
          "if": "ctx.host?.hostname == 'test'"
        }
      }
    ]
  }
}
```

This pipeline will work in both cases because `host?` checks if `host` exists and if not returns `null`. Removing `?` from the `if` condition will fail the second document with an error message: `cannot access method/field [hostname] from a null def reference`

The null operator `?`  is actually doing this behind the scene:

Imagine you write this:

- `ctx.windows?.event?.data?.user?.name == "philipp"`

Then the ? will transform this simple if statement to this:

```painless
ctx.windows != null &&
ctx.windows.event != null &&
ctx.windows.event.data != null &&
ctx.windows.event.data.user != null &&
ctx.windows.event.data.user.name == "philipp"
```

You can use the null safe operator with function too:

- `ctx.message?.startsWith('shoe')`

An [elvis](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-operators-reference.html#elvis-operator) might be useful in your script to handle these  maybe null value:

- `ctx.message?.startsWith('shoe') ?: false`

Most safest and secure option is to write:

- `ctx.message instanceof String && ctx.message.startsWith('shoe')`
- `ctx.event?.category instanceof String && ctx.event.category.startsWith('shoe')`

The reason for that is, if `event.category`  is a number, object or anything other than a `String` then it does not have the `startsWith` function and therefore will error with function `startsWith` not available on type object.

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

#### Use the `containsKey`

The `containsKey` can be used to check if a map contains a specific key.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "ip": "127.0.0.1"
      }
    },
    {
      "_source": {
        "test": "asd"
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "a",
          "value": "b",
          "if": "ctx.containsKey('test')"
        }
      }
    ]
  }
}
```

:::{warn}
This is more complex then it seems, since you will end up writing `ctx.kubernetes.containsKey('namespace')`. If `kubernetes` is null, or comes in as a String it will break processing. Stick to the null safe operator `?` for most work.
{warn}

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

## Use a script processor

If no built-in processor can achieve your goal, you may need to use a [script processor](elasticsearch://reference/enrich-processor/script-processor.md) in your ingest pipeline. Be sure to write scripts that are clear, concise, and maintainable.

### Setting the value of a field

Sometimes it is needed to write to a field and this field does not exist yet. Whenever the object above it exists, this can be done immediately.

`ctx.abc = “cool”` works without any issue as we are adding a root field called `abc`.

Creating something like `ctx.abc.def = “cool”` does not work unless you create the `abc` object beforehand or it already exists. There are multiple ways to do it. What we always or usually want to create is a Map. We can do it in a couple of ways:

```painless
ctx.abc = new HashMap();
ctx.abc = [:];
```

Both options are valid and do the same thing. However there is a big caveat and that is, that if `abc` already exists, it will be overwritten and empty. Validating if `abc` already exists can be done by:

```painless
if(ctx.abc == null) {
  ctx.abc = [:];
}
```

With a simple `if ctx.abc == null` we know that `abc` does not exist and we can create it. Alternatively you can use the shorthand which is super helpful when you need to go 2,3,4 levels deep. You can use either version with the `HashMap()` or with the `[:]`.

```painless
ctx.putIfAbsent("abc", new HashMap());
ctx.putIfAbsent("abc", [:]);
```

Now assuming you want to create this structure:

```json
{
  "user": {
    "geo": {
      "city": "Amsterdam"
   }
  }
}
```

The `putIfAbsent` will help a ton here:

```painless
ctx.putIfAbsent("user", [:]);
ctx.user.putIfAbsent("geo", [:]);
ctx.user.geo = "Amsterdam"
```

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

#### Calculate time in other timezone

When you cannot use the date and its timezone parameter, you can use `datetime` in Painless

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "@timestamp": "2021-08-13T09:06:00.000Z"
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "script": {
          "source": """
            ZonedDateTime zdt = ZonedDateTime.parse(ctx['@timestamp']);
            ZonedDateTime zdt_local = zdt.withZoneSameInstant(ZoneId.of('Europe/Berlin'));
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy - HH:mm:ss Z");
            ctx.localtime = zdt_local.format(formatter);
          """
        }
      }
    ]
  }
}
```

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

#### Work with JSON as value of fields

It is possible to work with json string as value of a field for example to set the `original` field value with the json of `_source`: We are leveraging a `mustache`  function here.

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
          "field": "original",
          "value": "{{#toJson}}_source{{/toJson}}"
        }
      }
    ]
  }
}
```
