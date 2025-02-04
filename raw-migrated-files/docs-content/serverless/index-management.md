# Index management [index-management]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

Elastic’s index management features are an easy, convenient way to manage your cluster’s indices, data streams, index templates, and enrich policies. Practicing good index management ensures your data is stored correctly and in the most cost-effective way possible.


## Manage indices [index-management-manage-indices]

Go to **{{project-settings}} → {{manage-app}} → {{index-manage-app}}**:

:::{image} ../../../images/serverless-index-management-indices.png
:alt: {{index-manage-app}} UI
:class: screenshot
:::

The **{{index-manage-app}}** page contains an overview of your indices.

* To show details or perform operations, such as delete, click the index name. To perform operations on multiple indices, select their checkboxes and then open the **Manage** menu.
* To filter the list of indices, use the search bar.
* To drill down into the index mappings, settings, and statistics, click an index name. From this view, you can navigate to **Discover** to further explore the documents in the index.


## Manage data streams [index-management-manage-data-streams]

Investigate your data streams and address lifecycle management needs in the **Data Streams** view.

In {{es-serverless}}, indices matching the `logs-*-*` pattern use the logsDB index mode by default. The logsDB index mode creates a [logs data stream](../../../manage-data/data-store/index-types/logsdb.md).

The value in the **Indices** column indicates the number of backing indices. Click this number to drill down into details.

A value in the data retention column indicates that the data stream is managed by a data stream lifecycle policy.

This value is the time period for which your data is guaranteed to be stored. Data older than this period can be deleted by {{es}} at a later time.

:::{image} ../../../images/serverless-management-data-stream.png
:alt: Data stream details
:class: screenshot
:::

To view information about the stream’s backing indices, click the number in the **Indices** column.

* To view more information about a data stream, such as its generation or its current index lifecycle policy, click the stream’s name. From this view, you can navigate to **Discover** to further explore data within the data stream.
* [preview] To modify the data retention value, select an index, open the **Manage**  menu, and click **Edit data retention**.


## Manage index templates [index-management-manage-index-templates]

Create, edit, clone, and delete your index templates in the **Index Templates** view. Changes made to an index template do not affect existing indices.

:::{image} ../../../images/serverless-index-management-index-templates.png
:alt: Index templates
:class: screenshot
:::

The default **logs** template uses the logsDB index mode to create a [logs data stream](../../../manage-data/data-store/index-types/logsdb.md).

If you don’t have any templates, you can create one using the **Create template** wizard.


## Manage enrich policies [index-management-manage-enrich-policies]

Use the **Enrich Policies** view to add data from your existing indices to incoming documents during ingest. An [enrich policy](../../../manage-data/ingest/transform-enrich/data-enrichment.md) contains:

* The policy type that determines how the policy matches the enrich data to incoming documents
* The source indices that store enrich data as documents
* The fields from the source indices used to match incoming documents
* The enrich fields containing enrich data from the source indices that you want to add to incoming documents
* An optional query.

:::{image} ../../../images/serverless-management-enrich-policies.png
:alt: Enrich policies
:class: screenshot
:::

When creating an enrich policy, the UI walks you through the configuration setup and selecting the fields. Before you can use the policy with an enrich processor, you must execute the policy.

When executed, an enrich policy uses enrich data from the policy’s source indices to create a streamlined system index called the enrich index. The policy uses this index to match and enrich incoming documents.

Check out these examples:

* [Example: Enrich your data based on geolocation](../../../manage-data/ingest/transform-enrich/example-enrich-data-based-on-geolocation.md)
* [Example: Enrich your data based on exact values](../../../manage-data/ingest/transform-enrich/example-enrich-data-based-on-exact-values.md)
* [Example: Enrich your data by matching a value to a range](../../../manage-data/ingest/transform-enrich/example-enrich-data-by-matching-value-to-range.md)
