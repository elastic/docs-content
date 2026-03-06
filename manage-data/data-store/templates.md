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
* If a new data stream or index matches more than one index template, the index template with the highest priority is used.
* When you create an index template, be careful to avoid [naming pattern collisions](#avoid-index-pattern-collisions) with built-in {{es}} index templates.

:::{tip}
For a detailed exploration and examples of setting up composable templates, refer to the Elastic blog [Index templating in Elasticsearch: How to use composable templates](https://www.elastic.co/search-labs/blog/index-composable-templates).
:::

## Index templates [index-templates]

An **index template** is used to configure an index when it is created. [Mappings](/manage-data/data-store/mapping.md), [settings](elasticsearch://reference/elasticsearch/index-settings/index.md), and [aliases](/manage-data/data-store/aliases.md) specified in the index template are inherited by each created index. These can also be specified in the component templates that the index template is composed of.

You can create and manage index templates on the **Index management** page in {{kib}} or by using the [index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API.

:::::{tab-set}
:group: template

::::{tab-item} Kibana
:sync: kibana
In this tutorial, you'll create an index template and use it to configure two new indices.

#### Step 1. Add a name and index pattern

1. In the **Index Templates** view, open the **Create template** wizard.

    :::{image} /manage-data/images/elasticsearch-reference-management_index_create_wizard.png
    :alt: Create wizard
    :screenshot:
    :::

2. In the **Name** field, enter `my-index-template`.
3. Set **Index pattern** to `my-index-*` so the template matches any index with that index pattern.
4. Leave **Data Stream**, **Priority**, **Version**, and **_meta field** blank or as-is.

#### Step 2. Add settings, mappings, and aliases

When creating an index template, you can define settings, mappings, and aliases directly in the template or include them through one or more component templates.

A [component template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) is a type of [template](/manage-data/data-store/templates.md) used as a building block for constructing index templates. {{kib}} displays badges indicating whether a component template contains mappings (**M**), index settings (**S**), aliases (**A**), or a combination of the three.

1. Add component templates to your index template.

    Component templates are optional. For this tutorial, do not add any component templates.

    :::{image} /manage-data/images/elasticsearch-reference-management_index_component_template.png
    :alt: Component templates page
    :screenshot:
    :::

2. Define index settings directly in the index template. When used in conjunction with component templates, settings defined directly in the index template override any conflicting settings from the associated component templates.

    This step is optional. For this tutorial, leave this section blank.
3. Define mappings directly in the index template. When used in conjunction with component templates, these mappings override any conflicting definitions from the associated component templates.

    Define a mapping that contains an [object](elasticsearch://reference/elasticsearch/mapping-reference/object.md) field named `geo` with a child [`geo_point`](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) field named `coordinates`:

    :::{image} /manage-data/images/elasticsearch-reference-management-index-templates-mappings.png
    :alt: Mapped fields page
    :screenshot:
    :::

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

    You can create additional mapping configurations in the **Dynamic templates** and **Advanced options** tabs. For this tutorial, do not create any additional mappings.

4. Define an alias named `my-index`:

    ```js
    {
      "my-index": {}
    }
    ```

5. On the review page, check the summary. If everything looks right, click **Create template**.

#### Step 3. Create new indices

You're now ready to create new indices using your index template.

1. Index the following documents to create two indices: `my-index-000001` and `my-index-000002`.

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

2. Use the [get index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get) to view the configurations for the new indices. The indices were configured using the index template you created earlier.

    ```console
    GET /my-index-000001,my-index-000002
    ```

::::

::::{tab-item} API
:sync: api
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
* `$.logs`
* `$.logs.*`
* `logs.otel`
* `logs.otel.*`
* `logs.ecs`
* `logs.ecs.*`

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
