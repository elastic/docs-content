---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
description: Run an ingest pipeline processor only when a condition is true, and apply other pipelines to documents based on their contents.
type: how-to
---

# Conditionally run processors and pipelines

Use conditions to apply a processor or a pipeline only to the documents that need it. For example, you can drop documents from a guest network, or send documents from different services through different pipelines.

## Conditionally run a processor [conditionally-run-processor]

Each processor supports an optional `if` condition, written as a [Painless script](elasticsearch://reference/scripting-languages/painless/painless.md). If provided, the processor only runs when the `if` condition is `true`.

`if` condition scripts run in Painless's [ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md). In `if` conditions, `ctx` values are read-only.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents with 'network.name' of 'Guest'",
        "if": "ctx?.network?.name == 'Guest'"
      }
    }
  ]
}
```

You can use regular expressions in your `if` condition scripts when the [`script.painless.regex.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#script-painless-regex-enabled) cluster setting allows them. The default value, `limited`, allows regular expressions but limits their complexity. For supported syntax, refer to [Painless regular expressions](elasticsearch://reference/scripting-languages/painless/painless-regexes.md).

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "If 'url.scheme' is 'http', set 'url.insecure' to true",
        "if": "ctx.url?.scheme =~ /^http$/",
        "field": "url.insecure",
        "value": true
      }
    }
  ]
}
```

You must specify `if` conditions as valid JSON on a single line. However, you can use the [{{kib}} console](/explore-analyze/query-filter/tools/console.md#configuring-console)'s triple quote syntax to write and debug larger scripts.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that don't contain 'prod' tag",
        "if": """
            Collection tags = ctx.tags;
            if(tags != null){
              for (String tag : tags) {
                if (tag.toLowerCase().contains('prod')) {
                  return false;
                }
              }
            }
            return true;
        """
      }
    }
  ]
}
```

You can also specify a [stored script](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md) as the `if` condition.

```console
PUT _scripts/my-prod-tag-script
{
  "script": {
    "lang": "painless",
    "source": """
      Collection tags = ctx.tags;
      if(tags != null){
        for (String tag : tags) {
          if (tag.toLowerCase().contains('prod')) {
            return false;
          }
        }
      }
      return true;
    """
  }
}

PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that don't contain 'prod' tag",
        "if": { "id": "my-prod-tag-script" }
      }
    }
  ]
}
```

::::{tip}
Expensive regular expressions and complex `if` condition scripts can slow indexing speeds. If possible, avoid them.
::::

Incoming documents often contain object fields. If a processor script attempts to access a field whose parent object doesn't exist, {{es}} returns a `NullPointerException`. To avoid these exceptions, use [null safe operators](elasticsearch://reference/scripting-languages/painless/painless-operators-reference.md#null-safe-operator), such as `?.`, and write your scripts to be null safe. For more patterns, refer to [Write concise conditionals](/manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md#conditionals).

For example, `ctx.network?.name.equalsIgnoreCase('Guest')` is not null safe. `ctx.network?.name` can return null. Rewrite the script as `'Guest'.equalsIgnoreCase(ctx.network?.name)`, which is null safe because `Guest` is always non-null.

If you can't rewrite a script to be null safe, include an explicit null check.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "drop": {
        "description": "Drop documents that contain 'network.name' of 'Guest'",
        "if": "ctx.network?.name != null && ctx.network.name.contains('Guest')"
      }
    }
  ]
}
```

## Conditionally apply pipelines [conditionally-apply-pipelines]

Combine an `if` condition with the [`pipeline`](elasticsearch://reference/ingest-processor/pipeline-processor.md) processor to apply other pipelines to documents based on your criteria. You can use this pipeline as the [default pipeline](/manage-data/ingest/transform-enrich/apply-ingest-pipelines.md#set-default-pipeline) in an [index template](/manage-data/data-store/templates.md) used to configure multiple data streams or indices.

```console
PUT _ingest/pipeline/one-pipeline-to-rule-them-all
{
  "processors": [
    {
      "pipeline": {
        "description": "If 'service.name' is 'apache_httpd', use 'httpd_pipeline'",
        "if": "ctx.service?.name == 'apache_httpd'",
        "name": "httpd_pipeline"
      }
    },
    {
      "pipeline": {
        "description": "If 'service.name' is 'syslog', use 'syslog_pipeline'",
        "if": "ctx.service?.name == 'syslog'",
        "name": "syslog_pipeline"
      }
    },
    {
      "fail": {
        "description": "If 'service.name' is not 'apache_httpd' or 'syslog', return a failure message",
        "if": "ctx.service?.name != 'apache_httpd' && ctx.service?.name != 'syslog'",
        "message": "This pipeline requires service.name to be either `syslog` or `apache_httpd`"
      }
    }
  ]
}
```

## Related pages

* [Create readable and maintainable ingest pipelines](/manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md)
* [Access data in processors](/manage-data/ingest/transform-enrich/access-data-in-processors.md)
* [Error handling](/manage-data/ingest/transform-enrich/error-handling.md)
