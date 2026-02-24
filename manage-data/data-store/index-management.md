---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#view-edit-indices
  - https://www.elastic.co/guide/en/serverless/current/index-management.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Index management [index-management]

Elastic's **Index Management** features are an easy, convenient way to manage your cluster's indices, [data streams](/manage-data/data-store/data-streams.md), [templates](/manage-data/data-store/templates.md), and [enrich policies](/manage-data/ingest/transform-enrich/data-enrichment.md). Practicing good index management ensures your data is stored correctly and in the most cost-effective way possible.

To use these features, go to the **Index management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Required permissions [index-mgm-req-permissions]
```{applies_to}
stack: ga
```

If you use {{es}} {{security-features}}, the following [security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) are required:

* The `monitor` cluster privilege to access {{kib}}'s **Index Management** features.
* The `view_index_metadata` and `manage` index privileges to view a data stream or index's data.
* The `manage_index_templates` cluster privilege to manage index templates.

To add these privileges, go to **Stack Management > Security > Roles** or use the [Create or update roles API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role).

## Manage indices [manage-indices]

Investigate your indices and perform operations from the **Indices** view.

:::::{applies-switch}

::::{applies-item} serverless:

:::{image} /manage-data/images/serverless-index-management-indices.png
:alt: Index Management indices
:screenshot:
:::

* To access details and perform operations on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), and [settings](elasticsearch://reference/elasticsearch/index-settings/index.md). From this view, you can navigate to **Discover** to further explore the documents in the index.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

    Refer to [Perform operations on indices](/manage-data/data-store/perform-index-operations.md) for details about the actions that you can run.

* Enable **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).
::::

::::{applies-item} stack:
:sync: stack

:::{image} /manage-data/images/elasticsearch-reference-management_index_labels.png
:alt: Index Management UI
:screenshot:
:::

* To access details and perform operations on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), [settings](elasticsearch://reference/elasticsearch/index-settings/index.md), and statistics. From this view, you can navigate to **Discover** to further explore the documents in the index, and you can perform operations using the **Manage index** menu.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

    Refer to [Perform operations on indices](/manage-data/data-store/perform-index-operations.md) for details about the actions that you can run.

* Enable **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).
::::
:::::

## Manage data streams

A [data stream](/manage-data/data-store/data-streams.md) lets you store append-only time series data across multiple indices while giving you a single named resource for requests.

Investigate your data streams and address lifecycle management needs in the **Data Streams** view.

:::{image} /manage-data/images/serverless-management-data-stream.png
:alt: Data stream details
:screenshot:
:::

In {{es-serverless}}, indices matching the `logs-*-*` pattern use the logsDB index mode by default. The logsDB index mode creates a [logs data stream](/manage-data/data-store/data-streams/logs-data-stream.md).

* To view information about the stream's backing indices, click the number in the **Indices** column.
* A value in the **Data retention** column indicates that the data stream is managed by a data stream lifecycle policy. This value is the time period for which your data is guaranteed to be stored. Data older than this period can be deleted by {{es}} at a later time.
* To modify the data retention value, select a data stream, open the **Manage**  menu, and click **Edit data retention**. On {{stack}}, this action is only available if your data stream is not managed by an ILM policy.
* To view more information about a data stream including it's lifecycle settings, click the stream's name.

:::{admonition} Streams
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}

Starting with {{stack}} version 9.2, the [**Streams**](/solutions/observability/streams/streams.md) page provides a centralized interface for common data management tasks in {{kib}}, including tasks such as [modifying data retention](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#data-retention-streams) values.
:::

## Manage index templates [index-management-manage-index-templates]

An index template is a type of [template](/manage-data/data-store/templates.md) that tells {{es}} how to configure an index when it is created.

Create, edit, clone, and delete your index templates in the **Index Templates** view. Changes made to an index template do not affect existing indices.

:::{image} /manage-data/images/serverless-index-management-index-templates.png
:alt: Index templates
:screenshot:
:::

* To show details and perform operations, click the template name.
* To view more information about the component templates within an index template, click the value in the **Component templates** column.
* Values in the **Content** column indicate whether a template contains index mappings, settings, and aliases.
* To create new index templates, use the **Create template** wizard.

### Try it: Create an index template [_try_it_create_an_index_template]

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

## Manage component templates [index-management-manage-component-templates]

Component templates are a type of [template](/manage-data/data-store/templates.md) used as reusable building blocks within index templates to configure index settings, mappings, and aliases.

Create, edit, clone, and delete your component templates in the **Component Templates** view.

:::{image} /manage-data/images/serverless-management-component-templates.png
:alt: Component templates
:screenshot:
:::

* To show details and perform operations, click the template name.
* To create new component templates, use the **Create component template** wizard.

## Manage enrich policies [manage-enrich-policies]

An [enrich policy](/manage-data/ingest/transform-enrich/data-enrichment.md#enrich-policy) is a set of configuration options used to add data from your existing indices to incoming documents during ingest. An enrich policy contains:

* The policy type that determines how the policy matches the enrich data to incoming documents
* The source indices that store enrich data as documents
* The fields from the source indices used to match incoming documents
* The enrich fields containing enrich data from the source indices that you want to add to incoming documents
* An optional [query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-all-query.md).

Use the **Enrich Policies** view to add data from your existing indices to incoming documents during ingest.

:::{image} /manage-data/images/serverless-management-enrich-policies.png
:alt: Enrich policies
:screenshot:
:::

* To show details click the policy name.
* To perform operations, click the policy name or use the buttons in the **Actions** column.
* To create new policies, use the **Create enrich policy** wizard.

You must execute a new enrich policy before you can use it with an enrich processor or {{esql}} query. When executed, an enrich policy uses enrich data from the policy's source indices to create a streamlined system index called the enrich index. The policy uses this index to match and enrich incoming documents.

Check out these examples:

* [Example: Enrich your data based on geolocation](/manage-data/ingest/transform-enrich/example-enrich-data-based-on-geolocation.md)
* [Example: Enrich your data based on exact values](/manage-data/ingest/transform-enrich/example-enrich-data-based-on-exact-values.md)
* [Example: Enrich your data by matching a value to a range](/manage-data/ingest/transform-enrich/example-enrich-data-by-matching-value-to-range.md)
