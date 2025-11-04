---
navigation_title: Shorten scripts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Shorten your script [script-shorten-syntax]

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

This version of the script removes several components and simplifies the syntax significantly:

* The `lang` declaration. Because Painless is the default language, you don’t need to specify the language if you’re writing a Painless script.
* The `return` keyword. Painless automatically uses the final statement in a script (when possible) to produce a return value in a script context that requires one.
* The `get` method, which is replaced with brackets `[]`. Painless uses a shortcut specifically for the `Map` type that allows us to use brackets instead of the lengthier `get` method.
* The semicolon at the end of the `source` statement. Painless does not require semicolons for the final statement of a block. However, it does require them in other cases to remove ambiguity.

You can use this abbreviated syntax anywhere that {{es}} supports scripts, such as when you’re creating [runtime fields](../../manage-data/data-store/mapping/map-runtime-field.md). Be mindful, however, that the `field` access API is not a direct replacement for `doc`. This shortened version of the original script includes a default value (the `null`) so the script may access both `doc` values and `_source` as underlying structures, depending on the field type.
