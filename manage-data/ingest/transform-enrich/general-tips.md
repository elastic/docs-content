---
mapped_pages:
  - https://www.elastic.co/docs/manage-data/ingest/transform-enrich/general-tips-and-tricks.html
applies_to:
  stack: ga
  serverless: ga
---

# Tips and Tricks

There are various ways to handle data in ingest pipelines, and while they all produce similar results, some methods might be more suitable depending on the specific case. This section provides guidance to ensure that your ingest pipelines are consistent, readable, and maintainable. While we won't focus heavily on performance optimizations, the goal is to create pipelines that are easy to understand and manage.

## Accessing Fields in `if` Statements

In an ingest pipeline, when working with `if` statements inside processors, you can access fields in two ways:

- Dot notation
- Square bracket notation

For example:

- `ctx.event.action`

is equivalent to:

- `ctx['event']['action']`

Both notations can be used to reference fields, so choose the one that makes your pipeline easier to read and maintain.

### Downsides of brackets

- No support for null safety operations `?`

### When to use brackets

When you have special characters such as `@` in the field name, or a `.` in the field name. As an example:

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

## Accessing fields in a script

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

This works as long as `user_name` is populated. If it is null, you get null as value for user.name. Additionally, when the `user` object does not exist, it will error because Java needs you to define the `user` object first before adding a key `name` into it.

This is one of the alternatives to get it working when you only want to set it, if it is not null

```painless
if (ctx.user_name != null) {
   ctx.user.name = ctx.user_name
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

## Check if a value exists and is not null

In simplest case the `ignore_empty_value` parameter is available in most processors to handle fields without values. Or the `ignore_failure` parameter to let the processor fail without impacting the pipeline you  but sometime you will need to use  the [null safe operator `?.`](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator) to check if a field exists and is not `null`.

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

## Check if a key is in a document

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

## Remove empty fields or remove empty fields that match a regular expression

Alex and Honza created a [blog post](https://alexmarquardt.com/2020/11/06/using-elasticsearch-painless-scripting-to-iterate-through-fields/) presenting painless scripts that remove empty fields or fields that match a regular expression. We are already using this in a lot of places. Most of the time in the custom pipeline and in the final pipeline as well.

```json
POST _ingest/pipeline/remove_empty_fields/_simulate
{
  "docs": [
    {
      "_source": {
        "key1": "first value",
        "key2": "some other value",
        "key3": "",
        "sudoc": {
          "a": "abc",
          "b": ""
        }
      }
    },
    {
      "_source": {
        "key1": "",
        "key2": "some other value",
        "list_of_docs": [
          {
            "foo": "abc",
            "bar": ""
          },
          {
            "baz": "",
            "subdoc_in_list": {"child1": "xxx", "child2": ""}
          }
        ]
      }
    }
  ]
}
```

```json
PUT _ingest/pipeline/remove_unwanted_keys
{
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          void iterateAllFields(def x) {
            if (x instanceof List) {
              for (def v: x) {
                iterateAllFields(v);
              }
            }
            if (!(x instanceof Map)) {
              return;
            }
            x.entrySet().removeIf(e -> e.getKey() =~ /unwanted_key_.*/);
// You can also add more lines here. Like checking for emptiness, or null directly.
            x.entrySet().removeIf(e -> e.getKey() == "");
            x.entrySet().removeIf(e -> e.getKey() == null);
            for (def v: x.values()) {
              iterateAllFields(v);
            }
          }
          iterateAllFields(ctx);
      """
      }
    }
  ]
}
```

## Type check of fields in ingest pipelines

If it is required to check the type of a field, this can be done via the Painless method instanceof

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
  {
    "_source": {
      "winlog": {
        "event_data": {
          "param1": "hello"
        }
      }
    }
  }
  ],
  "pipeline": {
    "processors": [
      {
        "rename": {
          "field": "winlog.event_data.param1",
          "target_field": "SysEvent1",
          "if": "ctx.winlog?.event_data?.param1 instanceof String"
        }
      }
    ]
  }
}
```

Yes the `instanceof` also works with the `?` operator.

## Calculate time in other timezone

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

## Work with JSON as value of fields

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

## Script Processor

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

## Remove fields based on their values

When `ignore_malformed`,  null or other mapping parameters are not sufficient, you can use a script like this:

```yaml
- script:
    lang: painless
    params:
      values:
        - ""
        - "-"
        - "N/A"
    source: >-
      ctx?.sophos?.xg.entrySet().removeIf(entry -> params.values.contains(entry.getValue()));
```

## GROK vs Dissects

There can be a very long discussion on whether to choose GROK or dissects. When to choose what, depends on a lot of factors and existing knowledge. Dissects are easier to understand and follow, but are limited in their use. The log should look fairly the same all the times, as opposed to grok which can deal with a lot of different tasks, like optional fields in various positions.

I can only go as far as telling what I like to do, which might not be the best on performance, but definitely the easiest to read and maintain. A log source often has many diverse messages and you might only need to extract certain information that is always on the same position, for example this message

```text
2018-08-14T14:30:02.203151+02:00 linux-sqrz systemd[4179]: Stopped target Basic System.
```

With a dissect we can simply do `%{_tmp.date} %{host.hostname} %{process.name}[%{process.pid}]: %{message}` and call it a day. Now we have extracted the most important information, like the timestamp. If you extract first to `_tmp.date` or directly over `@timestamp` is a discussion for another chapter.

With that extracted we are left with the `message` field to gather information, like user logins etc.
