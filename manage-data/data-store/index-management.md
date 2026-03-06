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

# Manage indices in {{kib}} [index-management]

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

* Enable **Include hidden indices** to view the full set of indices, including backing indices for [data streams](/manage-data/data-store/data-streams.md).

* To filter the list of indices, use the search bar or click a badge. Badges indicate if an index is a [follower index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-follow) or a [rollup index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-get-rollup-index-caps).
::::
:::::


## Manage data streams

* [](/manage-data/data-store/data-streams/manage-data-stream.md)

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

* [Learn more about index templates](/manage-data/data-store/templates.md#index-templates)

## Manage component templates [index-management-manage-component-templates]

* [Learn more about component templates](/manage-data/data-store/templates.md#component-templates)

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
