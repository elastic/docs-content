---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html
---

# How to write scripts [modules-scripting-using]

Wherever scripting is supported in the {{es}} APIs, the syntax follows the same pattern; you specify the language of your script, provide the script logic (or source), and add parameters that are passed into the script:

```js
  "script": {
    "lang":   "...",
    "source" | "id": "...",
    "params": { ... }
  }
```
%  NOTCONSOLE

`lang`
:   Specifies the language the script is written in. Defaults to `painless`.

`source`, `id`
:   The script itself, which you specify as `source` for an inline script or `id` for a stored script. Use the [stored script APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-script) to create and manage stored scripts.

`params`
:   Specifies any named parameters that are passed into the script as variables. [Use parameters](#prefer-params) instead of hard-coded values to decrease compile time.


## Write your first script [hello-world-script]

[Painless](modules-scripting-painless.md) is the default scripting language for {{es}}. It is secure, performant, and provides a natural syntax for anyone with a little coding experience.

A Painless script is structured as one or more statements and optionally has one or more user-defined functions at the beginning. A script must always have at least one statement.

The [Painless execute API](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md) provides the ability to test a script with simple user-defined parameters and receive a result. Let’s start with a complete script and review its constituent parts.

First, index a document with a single field so that we have some data to work with:

```console
PUT my-index-000001/_doc/1
{
  "my_field": 5
}
```

We can then construct a script that operates on that field and run evaluate the script as part of a query. The following query uses the [`script_fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#script-fields) parameter of the search API to retrieve a script valuation. There’s a lot happening here, but we’ll break it down the components to understand them individually. For now, you only need to understand that this script takes `my_field` and operates on it.

```console
GET my-index-000001/_search
{
  "script_fields": {
    "my_doubled_field": {
      "script": { <1>
        "source": "doc['my_field'].value * params['multiplier']", <2>
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```
%  TEST[continued]

1. `script` object
2. `script` source


The `script` is a standard JSON object that defines scripts under most APIs in {{es}}. This object requires `source` to define the script itself. The script doesn’t specify a language, so it defaults to Painless.


## Use parameters in your script [prefer-params]

The first time {{es}} sees a new script, it compiles the script and stores the compiled version in a cache. Compilation can be a heavy process. Rather than hard-coding values in your script, pass them as named `params` instead.

For example, in the previous script, we could have just hard coded values and written a script that is seemingly less complex. We could just retrieve the first value for `my_field` and then multiply it by `2`:

```painless
"source": "return doc['my_field'].value * 2"
```

Though it works, this solution is pretty inflexible. We have to modify the script source to change the multiplier, and {{es}} has to recompile the script every time that the multiplier changes.

Instead of hard-coding values, use named `params` to make scripts flexible, and also reduce compilation time when the script runs. You can now make changes to the `multiplier` parameter without {{es}} recompiling the script.

```painless
"source": "doc['my_field'].value * params['multiplier']",
"params": {
  "multiplier": 2
}
```

You can compile up to 150 scripts per 5 minutes by default. For ingest contexts, the default script compilation rate is unlimited.

```js
script.context.field.max_compilations_rate=100/10m
```
%  NOTCONSOLE

::::{important}
If you compile too many unique scripts within a short time, {{es}} rejects the new dynamic scripts with a `circuit_breaking_exception` error.
::::



## Shorten your script [script-shorten-syntax]

Using syntactic abilities that are native to Painless, you can reduce verbosity in your scripts and make them shorter. Here’s a simple script that we can make shorter:

```console
GET my-index-000001/_search
{
  "script_fields": {
    "my_doubled_field": {
      "script": {
        "lang":   "painless",
        "source": "doc['my_field'].value * params.get('multiplier');",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```
%  TEST[s/^/PUT my-index-000001\n/]

Let’s look at a shortened version of the script to see what improvements it includes over the previous iteration:

```console
GET my-index-000001/_search
{
  "script_fields": {
    "my_doubled_field": {
      "script": {
        "source": "field('my_field').get(null) * params['multiplier']",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```
%  TEST[s/^/PUT my-index-000001\n/]

This version of the script removes several components and simplifies the syntax significantly:

* The `lang` declaration. Because Painless is the default language, you don’t need to specify the language if you’re writing a Painless script.
* The `return` keyword. Painless automatically uses the final statement in a script (when possible) to produce a return value in a script context that requires one.
* The `get` method, which is replaced with brackets `[]`. Painless uses a shortcut specifically for the `Map` type that allows us to use brackets instead of the lengthier `get` method.
* The semicolon at the end of the `source` statement. Painless does not require semicolons for the final statement of a block. However, it does require them in other cases to remove ambiguity.

Use this abbreviated syntax anywhere that {{es}} supports scripts, such as when you’re creating [runtime fields](../../manage-data/data-store/mapping/map-runtime-field.md).


## Store and retrieve scripts [script-stored-scripts]

You can store and retrieve scripts from the cluster state using the [stored script APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-script). Stored scripts allow you to reference shared scripts for operations like scoring, aggregating, filtering, and reindexing. Instead of embedding scripts inline in each query, you can reference these shared operations.

Stored scripts can also reduce request payload size. Depending on script size and request frequency, this can help lower latency and data transfer costs.

::::{note}
Unlike regular scripts, stored scripts require that you specify a script language using the `lang` parameter.
::::


To create a script, use the [create stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-put-script). For example, the following request creates a stored script named `calculate-score`.

```console
POST _scripts/calculate-score
{
  "script": {
    "lang": "painless",
    "source": "Math.log(_score * 2) + params['my_modifier']"
  }
}
```

You can retrieve that script by using the [get stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get-script).

```console
GET _scripts/calculate-score
```
%  TEST[continued]

To use the stored script in a query, include the script `id` in the `script` declaration:

```console
GET my-index-000001/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
            "message": "some message"
        }
      },
      "script": {
        "id": "calculate-score", <1>
        "params": {
          "my_modifier": 2
        }
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[continued]

1. `id` of the stored script


To delete a stored script, submit a [delete stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-script) request.

```console
DELETE _scripts/calculate-score
```
%  TEST[continued]


## Update documents with scripts [scripts-update-scripts]

You can use the [update API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update) to update documents with a specified script. The script can update, delete, or skip modifying the document. The update API also supports passing a partial document, which is merged into the existing document.

First, let’s index a simple document:

```console
PUT my-index-000001/_doc/1
{
  "counter" : 1,
  "tags" : ["red"]
}
```

To increment the counter, you can submit an update request with the following script:

```console
POST my-index-000001/_update/1
{
  "script" : {
    "source": "ctx._source.counter += params.count",
    "lang": "painless",
    "params" : {
      "count" : 4
    }
  }
}
```
%  TEST[continued]

Similarly, you can use an update script to add a tag to the list of tags. Because this is just a list, the tag is added even it exists:

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "ctx._source.tags.add(params['tag'])",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```
%  TEST[continued]

You can also remove a tag from the list of tags. The `remove` method of a Java `List` is available in Painless. It takes the index of the element you want to remove. To avoid a possible runtime error, you first need to make sure the tag exists. If the list contains duplicates of the tag, this script just removes one occurrence.

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```
%  TEST[continued]

You can also add and remove fields from a document. For example, this script adds the field `new_field`:

```console
POST my-index-000001/_update/1
{
  "script" : "ctx._source.new_field = 'value_of_new_field'"
}
```
%  TEST[continued]

Conversely, this script removes the field `new_field`:

```console
POST my-index-000001/_update/1
{
  "script" : "ctx._source.remove('new_field')"
}
```
%  TEST[continued]

Instead of updating the document, you can also change the operation that is executed from within the script. For example, this request deletes the document if the `tags` field contains `green`. Otherwise it does nothing (`noop`):

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "if (ctx._source.tags.contains(params['tag'])) { ctx.op = 'delete' } else { ctx.op = 'none' }",
    "lang": "painless",
    "params": {
      "tag": "green"
    }
  }
}
```
%  TEST[continued]




