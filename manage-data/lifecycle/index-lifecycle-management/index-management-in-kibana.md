---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html
---

# Index management in Kibana [index-mgmt]

{{kib}}'s **Index Management** features are an easy, convenient way to manage your cluster’s indices, [data streams](../../data-store/index-types/data-streams.md), [index templates](../../data-store/templates.md), and [enrich policies](../../ingest/transform-enrich/data-enrichment.md). Practicing good index management ensures your data is stored correctly and in the most cost-effective way possible.

To use these features, go to **Stack Management** > **Index Management**.


## Required permissions [index-mgm-req-permissions]

If you use {{es}} {security-features}, the following [security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) are required:

* The `monitor` cluster privilege to access {{kib}}'s **Index Management** features.
* The `view_index_metadata` and `manage` index privileges to view a data stream or index’s data.
* The `manage_index_templates` cluster privilege to manage index templates.

To add these privileges, go to **Stack Management > Security > Roles** or use the [Create or update roles API](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role.html).


## Manage indices [view-edit-indices]

Investigate your indices and perform operations from the **Indices** view.

:::{image} ../../../images/elasticsearch-reference-management_index_labels.png
:alt: Index Management UI
:class: screenshot
:::

* To show details and perform operations such as close, forcemerge, and flush, click the index name.  To perform operations on multiple indices, select their checkboxes and then open the **Manage** menu. For more information on managing indices, refer to [Index APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html).
* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-follow.html), a [rollup index](https://www.elastic.co/guide/en/elasticsearch/reference/current/rollup-get-rollup-index-caps.html), or [frozen](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html).
* To drill down into the index [mappings](../../data-store/mapping.md), [settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-modules-settings), and statistics, click an index name. From this view, you can navigate to **Discover** to further explore the documents in the index.

    :::{image} ../../../images/elasticsearch-reference-management_index_details.png
    :alt: Index Management UI
    :class: screenshot
    :::



## Manage data streams [manage-data-streams]

Investigate your data streams and address lifecycle management needs in the **Data Streams** view.

The value in the **Indices** column indicates the number of backing indices. Click this number to drill down into details.

A value in the data retention column indicates that the data stream is managed by a [data stream lifecycle policy](../data-stream.md). This value is the time period for which your data is guaranteed to be stored. Data older than this period can be deleted by Elasticsearch at a later time.

:::{image} ../../../images/elasticsearch-reference-management-data-stream-fields.png
:alt: Data stream details
:class: screenshot
:::

* To view more information about a data stream, such as its generation or its current index lifecycle policy, click the stream’s name. From this view, you can navigate to **Discover** to further explore data within the data stream.
* [preview]To edit the data retention value, open the **Manage** menu, and then click **Edit data retention**. This action is only available if your data stream is not managed by an ILM policy.


## Manage index templates [manage-index-templates]

Create, edit, clone, and delete your index templates in the **Index Templates** view. Changes made to an index template do not affect existing indices.

:::{image} ../../../images/elasticsearch-reference-management-index-templates.png
:alt: Index templates
:class: screenshot
:::


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

1. Add [component templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-component-template.html) to your index template.

    Component templates are pre-configured sets of mappings, index settings, and aliases you can reuse across multiple index templates. Badges indicate whether a component template contains mappings (**M**), index settings (**S**), aliases (**A**), or a combination of the three.

    Component templates are optional. For this tutorial, do not add any component templates.

    :::{image} ../../../images/elasticsearch-reference-management_index_component_template.png
    :alt: Component templates page
    :class: screenshot
    :::

2. Define index settings. These are optional. For this tutorial, leave this section blank.
3. Define a mapping that contains an [object](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html) field named `geo` with a child [`geo_point`](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) field named `coordinates`:

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

2. Use the [get index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-index.html) to view the configurations for the new indices. The indices were configured using the index template you created earlier.

    ```console
    GET /my-index-000001,my-index-000002
    ```



## Manage enrich policies [manage-enrich-policies]

Use the **Enrich Policies** view to add data from your existing indices to incoming documents during ingest. An enrich policy contains:

* The policy type that determines how the policy matches the enrich data to incoming documents
* The source indices that store enrich data as documents
* The fields from the source indices used to match incoming documents
* The enrich fields containing enrich data from the source indices that you want to add to incoming documents
* An optional [query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html).

:::{image} ../../../images/elasticsearch-reference-management-enrich-policies.png
:alt: Enrich policies
:class: screenshot
:::

When creating an enrich policy, the UI walks you through the configuration setup and selecting the fields. Before you can use the policy with an enrich processor or {{esql}} query, you must execute the policy.

When executed, an enrich policy uses enrich data from the policy’s source indices to create a streamlined system index called the enrich index. The policy uses this index to match and enrich incoming documents.

Check out these examples:

* [Example: Enrich your data based on geolocation](../../ingest/transform-enrich/example-enrich-data-based-on-geolocation.md)
* [Example: Enrich your data based on exact values](../../ingest/transform-enrich/example-enrich-data-based-on-exact-values.md)
* [Example: Enrich your data by matching a value to a range](../../ingest/transform-enrich/example-enrich-data-by-matching-value-to-range.md)

