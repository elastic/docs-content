---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Templates [elasticsearch-templates]

Templates are the mechanism by which {{es}} applies settings, mappings, and other configurations when creating indices or data streams.

You configure templates prior to creating indices or data streams. When an index is created, either manually or by indexing a document, the matching template determines the settings, mappings, and other configurations to apply. When used with a [data stream](/manage-data/data-store/data-streams.md), a template also defines how each backing index is configured as it is created.

There are two types of template:

* An [**index template**](#index-templates) is the main configuration object applied when creating an index or data stream. It matches index names using `index_patterns` and resolves conflicts using a `priority` value. An index template can optionally define settings, mappings, and aliases directly, and refer to a list of component templates that provide reusable configuration blocks. It can also indicate whether it should create a data stream or a regular index.

* A [**component template**](#component-templates) is a reusable building block that defines settings, mappings, and aliases. Component templates are not applied directly; they must be referenced by index templates.

Together, index templates and their referenced component templates form what is known as *composable templates*.

The following conditions apply to using templates:

* Composable index templates take precedence over any [legacy templates](https://www.elastic.co/guide/en/elasticsearch/reference/8.18/indices-templates-v1.html), which were deprecated in {{es}} 7.8. If no composable template matches a given index, a legacy template may still match and be applied.
* If an index is created with explicit settings and also matches an index template, the settings from the [create index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) request take precedence over settings specified in the index template and its component templates.
* Settings specified in the index template itself take precedence over the settings in its component templates.
* When you specify multiple component templates in the `composed_of` field of an index template, the component templates are merged in the order specified, which means that later component templates override earlier component templates.
* If a new data stream or index matches more than one index template, the index template with the highest priority is used.
* When you create an index template, be careful to avoid [naming pattern collisions](#avoid-index-pattern-collisions) with built-in {{es}} index templates.

:::{tip}
For a detailed exploration and examples of setting up composable templates, refer to the Elastic blog [Index templating in Elasticsearch: How to use composable templates](https://www.elastic.co/search-labs/blog/index-composable-templates).
:::

## Index templates [index-templates]

An **index template** is used to configure an index when it is created. [Mappings](/manage-data/data-store/mapping.md), [settings](elasticsearch://reference/elasticsearch/index-settings/index.md), and [aliases](/manage-data/data-store/aliases.md) specified in the index template are inherited by each created index. These can also be specified in the component templates that the index template is composed of.

You can create and manage index templates in {{kib}} or using the {{es}} API. 

:::::{tab-set}
:group: template

::::{tab-item} Kibana
:sync: kibana
To create an index template, complete the following steps:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, select **Create template**.

    ![Create template page](/manage-data/images/elasticsearch-reference-create-template-wizard-my_template.png "")

1. On the **Logistics** page:
    1. Specify a name for the template.
    1. Specify a pattern to match the indices you want to manage with the lifecycle policy. For example, `my-index-*`.
    1. If you're storing continuously generated, append-only data, you can opt to create [data streams](/manage-data/data-store/data-streams.md) instead of indices for more efficient storage.

        :::{note}
        When you enable the data stream option, an option to set **Data retention** also becomes available. Data retention is applicable only if you're using a data stream lifecycle, which is an alternative to index lifecycle management. Refer to the [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) to learn more.
        :::


    1. Configure any other options you'd like, including:
        * The [index mode](elasticsearch://reference/elasticsearch/index-settings/time-series.md) to use for the created indices.
        * The template priority, version, and any metadata.
        * Whether or not to overwrite the `action.auto_create_index` cluster setting.

        Refer to the [create or update index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API documentation for details about these options.

1. On the **Component templates** page, you can use the search and filter tools to select any [component templates](/manage-data/data-store/templates.md#component-templates) to include in the index template. The index template will inherit the settings (**S**), mappings (**M**), and aliases (**A**) defined in the component templates and apply them to indices when they're created.

1. On the **Index settings** page, you can define your index settings directly in the index template. When used together with component templates, the mappings defined on this page will override any conflicting definitions from the associated component templates.

    1. Optional: Add any additional [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md) that should be applied to the indices as they're created. For example, you can set the number of shards and replicas for each index, as well as configure {{ilm-init}} by specifying [ILM settings](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md) to apply to the indices:

        ```js
        {
          "index.lifecycle.name": "my_policy",
          "index.lifecycle.rollover_alias": "test-alias",
          "number_of_shards": 1,
          "number_of_replicas": 1
        }
        ```

1. Optional: On the **Mappings** page, customize the fields and data types used when documents are indexed into {{es}}. When used together with component templates, these mappings override any conflicting definitions from the associated component templates.  Refer to [Mapping](/manage-data/data-store/mapping.md) for details.
    1. For example, you can define a mapping that contains an [object](elasticsearch://reference/elasticsearch/mapping-reference/object.md) field named `geo` with a child [`geo_point`](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) field named `coordinates`.

        Alternatively, you can click the **Load JSON** link and define the mapping as JSON:

        ```js
        {
          "properties": {
            "geo": {
              "properties": {
                "coordinates": {
                  "type": "geo_point"
                }
              }
            }
          }
        }
        ```

1. Optional: On the **Aliases** page, specify an [alias](/manage-data/data-store/aliases.md) for each created index. For example, you can define an alias named `my-index`:
    
     ```js
    {
      "my-index": {}
    }
    ```

    Note that this isn't required when configuring ILM, which instead uses the `index.lifecycle.rollover_alias` setting to access rolling indices.

1. On the **Review** page, confirm your selections and select **Create template**. You can check your selected options, as well as both the format of the index template that will be created and the associated API request.

The newly created index template will be used for all new indices with names that match the specified pattern, and for each of these, the specified ILM policy will be applied.


:::{dropdown} Optional: Create new indices to test your template
To test your newly created template, you can create two new indices, for example `my-index-000001` and `my-index-000002`.

1. Index the following documents, to create new indices:

    ```console
    POST /my-index-000001/_doc
    {
      "@timestamp": "2019-05-18T15:57:27.541Z",
      "ip": "225.44.217.191",
      "extension": "jpg",
      "response": "200",
      "geo": {
        "coordinates": {
          "lat": 38.53146222,
          "lon": -121.7864906
        }
      },
      "url": "https://media-for-the-masses.theacademyofperformingartsandscience.org/uploads/charles-fullerton.jpg"
    }

    POST /my-index-000002/_doc
    {
      "@timestamp": "2019-05-20T03:44:20.844Z",
      "ip": "198.247.165.49",
      "extension": "php",
      "response": "200",
      "geo": {
        "coordinates": {
          "lat": 37.13189556,
          "lon": -76.4929875
        }
      },
      "memory": 241720,
      "url": "https://theacademyofperformingartsandscience.org/people/type:astronauts/name:laurel-b-clark/profile"
    }
    ```

1. Use the [get index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get) to view the configurations for the new indices. The indices were configured using the index template you created earlier.

    ```console
    GET /my-index-000001,my-index-000002
    ```
:::

::::

::::{tab-item} API
:sync: api
Use the [create or update index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API to add an index template to a cluster.

The following request creates an index template that is *composed of* the two component templates shown in the [component templates](#component-templates) example.

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
  "priority": 501,
  "composed_of": ["component_template1", "runtime_component_template"],
  "version": 3,
  "_meta": {
    "description": "my custom"
  }
}
```
::::

:::::

:::{tip}
The following features can be useful when you're setting up index templates:

* You can test the effect of an index template before putting it into use. Refer to [Simulate multi-component templates](/manage-data/data-store/templates/simulate-multi-component-templates.md) to learn more.
* You can create an index template for a component template that does not yet exist. When doing so, you can use the `ignore_missing_component_templates` configuration option in an index template so that the missing component template is ignored. Refer to [Ignore missing component templates](/manage-data/data-store/templates/ignore-missing-component-templates.md) to learn more.
:::

### Avoid index pattern collisions [avoid-index-pattern-collisions]

{{es}} has built-in index templates, each with a priority of `100`, for the following index patterns:

* `.kibana-reporting*`
* `logs-*-*`
* `metrics-*-*`
* `synthetics-*-*`
* `profiling-*`
* `security_solution-*-*`

[{{agent}}](/reference/fleet/index.md) uses these templates to create data streams. Index templates created by {{fleet}} integrations use similar overlapping index patterns and have a priority up to `200`.

If you use {{fleet}} or {{agent}}, assign your index templates a priority lower than `100` to avoid overriding these templates. Otherwise, to avoid accidentally applying the templates, do one or more of the following:

* To disable all built-in index and component templates, set [`stack.templates.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#stack-templates-enabled) to `false` using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Note, however, that this is not recommended, see the [setting documentation](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#stack-templates-enabled) for more information.
* Use a non-overlapping index pattern.
* Assign templates with an overlapping pattern a `priority` higher than `500`. For example, if you don’t use {{fleet}} or {{agent}} and want to create a template for the `logs-*` index pattern, assign your template a priority of `501`. This ensures your template is applied instead of the built-in template for `logs-*-*`.
* To avoid naming collisions with built-in and Fleet-managed index templates, avoid using `@` as part of the name of your own index templates.
* Beginning in {{stack}} version 9.1, {{fleet}} uses indices named `fleet-synced-integrations*` for a feature. Avoid using this name to avoid collisions with built-in indices.

## Component templates [component-templates]

A **component template** is a reusable building block that defines mappings, settings, and aliases. Component templates are not applied directly to indices, but referenced by index templates and used when determining the final configuration of an index.

You can create and manage component templates on the **Index management** page in {{kib}} or by using the [component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) API.

:::::{tab-set}
:group: template

::::{tab-item} Kibana
:sync: kibana
Create, edit, clone, and delete your component templates in the **Component Templates** view.

:::{image} /manage-data/images/serverless-management-component-templates.png
:alt: Component templates
:screenshot:
:::

* To show details and perform operations, click the template name.
* To create new component templates, use the **Create component template** wizard.
::::

::::{tab-item} API
:sync: api
You can create and manage component templates using the [component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) API.
The following request creates the two component templates used in the previous index template example:

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
::::

:::::
