---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html
applies_to:
  stack: ga
  serverless: ga
---

# Templates [index-templates]

::::{note}
This topic describes the composable index templates introduced in {{es}} 7.8. For information about how index templates worked previously, see the [legacy template documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-template).
::::


$$$getting$$$
An index template is a way to tell {{es}} how to configure an index when it is created. For data streams, the index template configures the stream’s backing indices as they are created. Templates are configured **prior to index creation**. When an index is created - either manually or through indexing a document - the template settings are used as a basis for creating the index.

There are two types of templates: index templates and [component templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template). Component templates are reusable building blocks that configure mappings, settings, and aliases. While you can use component templates to construct index templates, they aren’t directly applied to a set of indices. Index templates can contain a collection of component templates, as well as directly specify settings, mappings, and aliases.

The following conditions apply to index templates:

* Composable templates take precedence over legacy templates. If no composable template matches a given index, a legacy template may still match and be applied.
* If an index is created with explicit settings and also matches an index template, the settings from the [create index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request take precedence over settings specified in the index template and its component templates.
* Settings specified in the index template itself take precedence over the settings in its component templates.
* If a new data stream or index matches more than one index template, the index template with the highest priority is used.

::::{admonition} Avoid index pattern collisions
:name: avoid-index-pattern-collisions

{{es}} has built-in index templates, each with a priority of `100`, for the following index patterns:

* `.kibana-reporting*`
* `logs-*-*`
* `metrics-*-*`
* `synthetics-*-*`
* `profiling-*`
* `security_solution-*-*`

[{{agent}}](/reference/ingestion-tools/fleet/index.md) uses these templates to create data streams. Index templates created by {{fleet}} integrations use similar overlapping index patterns and have a priority up to `200`.

If you use {{fleet}} or {{agent}}, assign your index templates a priority lower than `100` to avoid overriding these templates. Otherwise, to avoid accidentally applying the templates, do one or more of the following:

* To disable all built-in index and component templates, set [`stack.templates.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#stack-templates-enabled) to `false` using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Note, however, that this is not recommended, see the [setting documentation](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#stack-templates-enabled) for more information.
* Use a non-overlapping index pattern.
* Assign templates with an overlapping pattern a `priority` higher than `500`. For example, if you don’t use {{fleet}} or {{agent}} and want to create a template for the `logs-*` index pattern, assign your template a priority of `500`. This ensures your template is applied instead of the built-in template for `logs-*-*`.
* To avoid naming collisions with built-in and Fleet-managed index templates, avoid using `@` as part of the name of your own index templates.
* Beginning in {{stack}} version 9.1, {{fleet}} uses indices named `fleet-synced-integrations*` for a feature. Avoid using this name to avoid collisions with built-in indices.

::::



## Create index template [create-index-templates]

Use the [index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) and [put component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) APIs to create and update index templates. You can also [manage index templates](../lifecycle/index-lifecycle-management/index-management-in-kibana.md) from Stack Management in {{kib}}.

The following requests create two component templates.

```console
PUT _component_template/component_template1
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        }
      }
    }
  }
}

PUT _component_template/runtime_component_template
{
  "template": {
    "mappings": {
      "runtime": { <1>
        "day_of_week": {
          "type": "keyword",
          "script": {
            "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ENGLISH))"
          }
        }
      }
    }
  }
}
```

1. This component template adds a [runtime field](mapping/map-runtime-field.md) named `day_of_week` to the mappings when a new index matches the template.


The following request creates an index template that is *composed of* these component templates.

```console
PUT _index_template/template_1
{
  "index_patterns": ["te*", "bar*"],
  "template": {
    "settings": {
      "number_of_shards": 1
    },
    "mappings": {
      "_source": {
        "enabled": true
      },
      "properties": {
        "host_name": {
          "type": "keyword"
        },
        "created_at": {
          "type": "date",
          "format": "EEE MMM dd HH:mm:ss Z yyyy"
        }
      }
    },
    "aliases": {
      "mydata": { }
    }
  },
  "priority": 500,
  "composed_of": ["component_template1", "runtime_component_template"],
  "version": 3,
  "_meta": {
    "description": "my custom"
  }
}
```
