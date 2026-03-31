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

# Manage indices in {{kib}}

$$$manage-indices$$$

Practicing good index management ensures your data is stored efficiently and cost-effectively. {{kib}}'s index management features offer a convenient way to view and [perform operations on](/manage-data/data-store/index-operations-reference.md) your cluster’s [indices](/manage-data/data-store/index-basics.md), [data streams](/manage-data/data-store/data-streams.md), [index and component templates](/manage-data/data-store/templates.md), and [enrich policies](/manage-data/ingest/transform-enrich/data-enrichment.md).

:::{tip}
All operations available on the **{{index-manage-app}}** page can also be performed using the {{es}} REST API. Refer to [Manage data from the command line](/manage-data/data-store/manage-data-from-the-command-line.md) for examples, or browse the [{{es}} index APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-indices) directly.
:::

## Required permissions [required-permissions]
```{applies_to}
stack: ga
```

If you use {{es}} {{security-features}}, the following [security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) are required:

* The `monitor` cluster privilege to access {{kib}}'s **{{index-manage-app}}** features.
* The `view_index_metadata` and `manage` index privileges to view a data stream or index's data.
* The `manage_index_templates` cluster privilege to manage index templates.

To add these privileges, go to **{{stack-manage-app}} > Security > Roles** or use the [Create or update roles](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) API.

## Navigate the Index Management page

To open the **{{index-manage-app}}** page, use the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


:::::{applies-switch}

::::{applies-item} serverless:

:::{image} /manage-data/images/serverless-index-management-indices.png
:alt: Index Management indices
:screenshot:
:::

* To access details and [perform operations](/manage-data/data-store/index-operations-reference.md) on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), and [settings](elasticsearch://reference/elasticsearch/index-settings/index.md). From this view, you can navigate to **Discover** to further explore the documents in the index.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

* Turn on **Include hidden indices** to view the full set of indices, including backing indices for data streams.

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).

* To view and [manage](/manage-data/data-store/data-streams/manage-data-stream.md) your data streams, including backing indices and retention settings, go to the **Data Streams** tab.

* To create, edit, clone, or delete [index templates](/manage-data/data-store/templates.md) and [component templates](/manage-data/data-store/templates.md#component-templates) that define how {{es}} configures new indices or data streams, go the **Index Templates** or **Component Templates** tab.

* To create, execute, or delete [enrich policies](/manage-data/ingest/transform-enrich/data-enrichment.md) that add data from existing indices to incoming documents during ingest, open the **Enrich Policies** tab.

::::

::::{applies-item} stack:
:sync: stack

:::{image} /manage-data/images/elasticsearch-reference-management_index_labels.png
:alt: Index Management UI
:screenshot:
:::

* To access details and [perform operations](/manage-data/data-store/index-operations-reference.md) on indices:

    * For a single index, click the index name to drill down into the index overview, [mappings](/manage-data/data-store/mapping.md), [settings](elasticsearch://reference/elasticsearch/index-settings/index.md), and statistics. From this view, you can navigate to **Discover** to further explore the documents in the index, and you can perform operations using the **Manage index** menu.

    * For multiple indices, select their checkboxes and then open the **Manage indices** menu. 

* Turn on **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).

* To view and [manage](/manage-data/data-store/data-streams/manage-data-stream.md) your data streams, including backing indices and retention settings, go to the **Data Streams** tab.

* To create, edit, clone, or delete [index templates](/manage-data/data-store/templates.md) and [component templates](/manage-data/data-store/templates.md#component-templates) that define how {{es}} configures new indices or data streams, go the **Index Templates** or **Component Templates** tab.

* To create, execute, or delete [enrich policies](/manage-data/ingest/transform-enrich/data-enrichment.md) that add data from existing indices to incoming documents during ingest, open the **Enrich Policies** tab.
::::
:::::