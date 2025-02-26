---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#manage-index-templates
  - https://www.elastic.co/guide/en/serverless/current/index-management.html#index-management-manage-index-templates
applies_to:
  stack: ga
  serverless: ga
---

# Manage index templates [manage-index-templates]

Create, edit, clone, and delete your index templates in the **Index Templates** view. Changes made to an index template do not affect existing indices.

:::{image} ../../../images/elasticsearch-reference-management-index-templates.png
:alt: Index templates
:class: screenshot
:::

In {{serverless-full}}, the default **logs** template uses the logsDB index mode to create a [logs data stream](../data-streams/logs-data-stream.md).

If you don’t have any templates, you can create one using the **Create template** wizard.

### Try it: Create an index template [_try_it_create_an_index_template]

In this tutorial, you’ll create an index template and use it to configure two new indices.

**Step 1. Add a name and index pattern**

1. In the **Index Templates** view, open the **Create template** wizard.

    :::{image} ../../../images/elasticsearch-reference-management_index_create_wizard.png
    :alt: Create wizard
    :class: screenshot
    :::

2. In the **Name** field, enter `my-index-template`.
3. Set **Index pattern** to `my-index-*` so the template matches any index with that index pattern.
4. Leave **Data Stream**, **Priority**, **Version**, and **_meta field** blank or as-is.

**Step 2. Add settings, mappings, and aliases**

1. Add [component templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) to your index template.

    Component templates are pre-configured sets of mappings, index settings, and aliases you can reuse across multiple index templates. Badges indicate whether a component template contains mappings (**M**), index settings (**S**), aliases (**A**), or a combination of the three.

    Component templates are optional. For this tutorial, do not add any component templates.

    :::{image} ../../../images/elasticsearch-reference-management_index_component_template.png
    :alt: Component templates page
    :class: screenshot
    :::

2. Define index settings. These are optional. For this tutorial, leave this section blank.
3. Define a mapping that contains an [object](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/object.md) field named `geo` with a child [`geo_point`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/geo-point.md) field named `coordinates`:

    :::{image} ../../../images/elasticsearch-reference-management-index-templates-mappings.png
    :alt: Mapped fields page
    :class: screenshot
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

**Step 3. Create new indices**

You’re now ready to create new indices using your index template.

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
