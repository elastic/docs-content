---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Write your first script [hello-world-script]

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

1. `script` object
2. `script` source


The `script` is a standard JSON object that defines scripts under most APIs in {{es}}. This object requires `source` to define the script itself. The script doesn’t specify a language, so it defaults to Painless.
