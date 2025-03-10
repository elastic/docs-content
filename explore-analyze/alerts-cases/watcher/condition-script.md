---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Script condition"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition-script.html
---

# Script condition [condition-script]

A watch [condition](condition.md) that evaluates a script. The default scripting language is `painless`. You can use any of the scripting languages supported by Elasticsearch as long as the language supports evaluating expressions to Boolean values. Note that the `mustache` and `expression` languages are too limited to be used by this condition. For more information, see [Scripting](../../scripting.md).

## Using a script condition [_using_a_script_condition]

The following snippet configures an inline `script` condition that always returns `true`:

```js
"condition" : {
  "script" : "return true"
}
```
%  NOTCONSOLE

This example defines a script as a simple string. This format is actually a shortcut for defining an [inline](#condition-script-inline) script. The formal definition of a script is an object that specifies the script type and optional language and parameter values. If the `lang` attribute is omitted, the language defaults to `painless`. Elasticsearch supports two types of scripts, [inline](#condition-script-inline) and [stored](#condition-script-stored).

For example, the following snippet shows a formal definition of an `inline` script that explicitly specifies the language and defines a single script parameter, `result`:

```js
"condition" : {
  "script" : {
    "source" : "return params.result",
    "lang" : "painless",
    "params" : {
      "result" : true
    }
  }
}
```
%  NOTCONSOLE

## Inline scripts [condition-script-inline]

Inline scripts are scripts that are defined in the condition itself. The following snippet shows the formal configuration of a simple painless script that always returns `true`.

```js
"condition" : {
  "script" : {
    "source" : "return true"
  }
}
```
%  NOTCONSOLE

## Stored scripts [condition-script-stored]

Stored scripts refer to scripts that were [stored](../../scripting/modules-scripting-using.md) in Elasticsearch. The following snippet shows how to refer to a script by its `id`:

```js
"condition" : {
  "script" : {
    "id" : "my_script"
  }
}
```
%  NOTCONSOLE

As with [inline](#condition-script-inline) scripts, you can also specify the script language and parameters:

```js
"condition" : {
  "script" : {
    "id" : "my_script",
    "lang" : "javascript",
    "params" : { "color" : "red" }
  }
}
```
%  NOTCONSOLE

## Accessing the watch payload [accessing-watch-payload]

A script can access the current watch execution context, including the payload data, as well as any parameters passed in through the condition definition.

For example, the following snippet defines a watch that uses a [`search` input](input-search.md) and uses a `script` condition to check if the number of hits is above a specified threshold:

```js
{
  "input" : {
    "search" : {
      "request": {
        "indices" : "log-events",
        "body" : {
          "size" : 0,
          "query" : { "match" : { "status" : "error" } }
        }
      }
    }
  },
  "condition" : {
    "script" : {
      "source" : "return ctx.payload.hits.total > params.threshold",
      "params" : {
        "threshold" : 5
      }
    }
  }
}
```
%  NOTCONSOLE

When you’re using a scripted condition to evaluate an Elasticsearch response, keep in mind that the fields in the response are no longer in their native data types. For example, the `@timestamp` in the response is a string, rather than a `DateTime`. To compare the response `@timestamp` against the `ctx.execution_time`, you need to parse the `@timestamp` string into a `ZonedDateTime`. For example:

```js
java.time.ZonedDateTime.parse(@timestamp)
```
%  NOTCONSOLE

You can reference the following variables in the watch context:

| Name | Description |
| --- | --- |
| `ctx.watch_id` | The id of the watch that is currently executing. |
| `ctx.execution_time` | The time execution of this watch started. |
| `ctx.trigger.triggered_time` | The time this watch was triggered. |
| `ctx.trigger.scheduled_time` | The time this watch was supposed to be triggered. |
| `ctx.metadata.*` | Any metadata associated with the watch. |
| `ctx.payload.*` | The payload data loaded by the watch’s input. |
