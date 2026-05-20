---
navigation_title: Use parameters
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Use parameters in your script [prefer-params]

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

::::{important}
If you compile too many unique scripts within a short time, {{es}} rejects the new dynamic scripts with a `circuit_breaking_exception` error.
::::
