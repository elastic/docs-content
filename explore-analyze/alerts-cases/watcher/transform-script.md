---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Script {{watcher-transform}}"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-script.html
---

# Script payload transform [transform-script]

A [{{watcher-transform}}](transform.md) that executes a script on the current payload in the watch execution context and replaces it with a newly generated one. The following snippet shows how a simple script {{watcher-transform}} can be defined on the watch level:

::::{tip}
The `script` {{watcher-transform}} is often useful when used in combination with the [`search`](transform-search.md) {{watcher-transform}}, where the script can extract only the significant data from a search result, and by that, keep the payload minimal. This can be achieved with the [`chain`](transform-chain.md) {{watcher-transform}}.
::::

```js
{
  "transform" : {
    "script" : "return [ 'time' : ctx.trigger.scheduled_time ]" <1>
  }
}
```

1. A simple `painless` script that creates a new payload with a single `time` field holding the scheduled time.
%  NOTCONSOLE

::::{note}
The executed script may either return a valid model that is the equivalent of a Java™ Map or a JSON object (you will need to consult the documentation of the specific scripting language to find out what this construct is). Any other value that is returned will be assigned and accessible to/via the `_value` variable.
::::

## Script settings [transform-script-settings]

The `script` attribute may hold a string value in which case it will be treated as an inline script and the default Elasticsearch script languages will be assumed (as described in [Scripting](../../scripting.md)). You can use the other scripting languages supported by Elasticsearch. For this, you need to set the `script` field to an object describing the script and its language. The following table lists the possible settings that can be configured:

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `inline` | yes | - | When using an inline script, this field holds                                     the script itself. |
| `id` | yes | - | When referring to a stored script, this                                     field holds the id of the script. |
| `lang` | no | `painless` | The script language |
| `params` | no | - | Additional parameters/variables that are                                     accessible by the script |

When using the object notation of the script, one (and only one) of `inline`, or `id` fields must be defined.

::::{note}
In addition to the provided `params`, the scripts also have access to the [standard watch execution context parameters](how-watcher-works.md#watch-execution-context).
::::
