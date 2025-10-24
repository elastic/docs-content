---
navigation_title: Customize built-in {{ilm-init}} policies
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/example-using-index-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Customize built-in {{ilm-init}} policies for {{agent}} data streams

{{es}} includes a set of built-in {{ilm-init}} policies that govern how managed indices transition as they age. This guide demonstrates how you can customize the lifecycle of a managed index, to adjust how the index transitions across [data tiers](/manage-data/lifecycle/data-tiers.md) and what [actions](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-actions), such as downsampling or shrinking, are performed on the index during each lifecycle phase.

Setting a custom {{ilm-init}} policy is useful when you have a specific set of indices, for example a set of Kubernetes logs which can grow to be quite large in volume, for which you don't want to use the default data retention duration and other {{ilm-init}} settings.

[{{agent}}](/reference/fleet/index.md) uses the following set of built-in {{ilm-init}} policies to manage backing indices for its data streams:

* `logs@lifecycle`
* `logs-otel@lifecycle`
* `metrics@lifecycle`
* `metrics-otel@lifecycle`
* `synthetics@lifecycle`
* `traces@lifecycle`
* `traces-otel@lifecycle`

This tutorial covers customizing the way ingested logging data is managed. Rather than use the default lifecycle settings from the built-in `logs@lifecycle` {{ilm-init}} policy, you can use the **Index Lifecycle Policies** feature in {{kib}} to tailor a new policy based on your application’s specific performance, resilience, and retention requirements. This involves three main steps:
 1. [Create a duplicate of the `logs@lifecycle` policy](#example-using-index-lifecycle-policy-duplicate-ilm-policy).
 2. [Modify the new policy to suit your requirements](#ilm-ex-modify-policy).
 3. [Apply the new policy to your log data using a `logs@custom` component template](#example-using-index-lifecycle-policy-apply-policy).

:::{tip}
* If you're using [Elastic integrations](https://docs.elastic.co/en/integrations) and are not yet familiar with which data streams are associated with them, refer to [Manage the lifecycle policy for integrations data](/manage-data/lifecycle/index-lifecycle-management/manage-lifecycle-integrations-data.md).

* If you're looking for a more advanced use case, such as customizing an ILM policy for a selected set of data streams in one or more integrations or namespaces, check the set of tutorials in [Customize data retention policies](/reference/fleet/data-streams-ilm-tutorial.md) in the {{fleet}} and {{agent}} reference documentation.

    These tutorials go into greater depth about creating and using `@custom` component templates. For example, the tutorial [Apply an ILM policy to all data streams generated from {{fleet}} integrations across all namespaces](/reference/fleet/data-streams-scenario1.md) shows how to create and use the `logs@custom` and `metrics@custom` component templates to customize {{ilm-init}} policies associated with data streams in integrations.
:::

## Scenario [example-using-index-lifecycle-policy-scenario]

You want to send log files to an {{es}} cluster so you can visualize and analyze the data. This data has the following retention requirements:

* When the primary shard size of the write index reaches 50GB or the index is 30 days old, roll over to a new index.
* After rollover, keep indices in the hot data tier for 30 days.
* 30 days after rollover:

    * Move indices to the warm data tier.
    * Set replica shards to 1.
    * [Force merge](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) multiple index segments to free up the space used by deleted documents.

* Delete indices 90 days after rollover.


## Prerequisites [example-using-index-lifecycle-policy-prerequisites]

To complete this tutorial, you’ll need:

* An {{es}} cluster with hot and warm data tiers.

    * {{ech}}: Elastic Stack deployments on {{ecloud}} include a hot tier by default. To add a warm tier, edit your deployment and click **Add capacity** for the warm data tier.

        :::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-ess-add-warm-data-tier.png
        :alt: Add a warm data tier to your deployment
        :screenshot:
        :::

    * Self-managed cluster: Assign `data_hot` and `data_warm` roles to nodes as described in [*Data tiers*](../data-tiers.md).

        For example, include the `data_warm` node role in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file of each node in the warm tier:

        ```yaml
        node.roles: [ data_warm ]
        ```

* A host with {{agent}} installed and configured to send logs to your {{es}} cluster.


## Duplicate the policy [example-using-index-lifecycle-policy-duplicate-ilm-policy]

{{agent}} uses data streams with an index pattern of `logs-*-*` to store log monitoring data. The managed `logs@lifecycle` {{ilm-init}} policy automatically manages backing indices for these data streams.

If you don’t want to use the policy defaults, then you can customize the managed policy and then save it as a new policy. You can then use the new policy in related component templates and index templates.

::::{warning}
You should never edit managed policies directly. Changes to managed policies might be rolled back or overwritten.
::::


To save the `logs@lifecycle` policy as a new policy in {{kib}}:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Toggle **Include managed system policies**.
3. Select the `logs@lifecycle` policy.
4. On the **Edit policy logs** page, toggle **Save as new policy**, and then provide a new name for the policy, for example, `logs-custom`.

The `logs@lifecycle` policy uses the recommended rollover defaults: Start writing to a new index when the primary shard size of the current write index reaches 50GB or the index becomes 30 days old.

To view or change the rollover settings, click **Advanced settings** for the hot phase. Then disable **Use recommended defaults** to display the rollover settings.

:::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-hotphaserollover-default.png
:alt: View rollover defaults
:screenshot:
:::


## Modify the policy [ilm-ex-modify-policy]

The default `logs@lifecycle` policy is designed to prevent the creation of many tiny daily indices. You can modify your copy of the policy to meet your performance requirements and manage resource usage.

1. Activate the warm phase and click **Advanced settings**.

    1. Set **Move data into phase when** to **30 days old**. This moves indices to the warm tier 30 days after rollover.
    2. Enable **Set replicas** and change **Number of replicas** to **1**.
    3. Enable **Force merge data** and set **Number of segments** to **1**.

    :::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-modify-default-warm-phase-rollover.png
    :alt: Add a warm phase with custom settings
    :screenshot:
    :::

2. In the warm phase, click the trash icon to enable the delete phase.

    :::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-enable-delete-phase.png
    :alt: Enable the delete phase
    :screenshot:
    :::

    In the delete phase, set **Move data into phase when** to **90 days old**. This deletes indices 90 days after rollover.

    :::{image} /manage-data/images/elasticsearch-reference-tutorial-ilm-delete-rollover.png
    :alt: Add a delete phase
    :screenshot:
    :::

3. Click **Save as new policy**.

::::{tip}
Copies of managed {{ilm-init}} policies are also marked as **Managed**. You can use the [Create or update lifecycle policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) to update the `_meta.managed` parameter to `false`.
::::



## Apply the policy [example-using-index-lifecycle-policy-apply-policy]

To apply your new {{ilm-init}} policy to the `logs` index template, create or edit the `logs@custom` component template.


:::::{admonition} Using @custom component templates
A `@custom` component template allows you to customize the mappings and settings of the managed index templates, without having to override them or their main component templates.

Many {{es}} managed index templates include one or more `@custom` component templates. A `@custom` component template must first be created before it can be used, and its name must exactly match the name specified in the managed index template in order to be applied automatically to indices as they're created.

For example, if you're ingesting OpenTelemetry (OTel) logs, any OTel log data streams and their backing indices are configured by the `logs-otel@template` managed index template. That index template automatically applies settings defined in the `logs@custom` and the `logs-otel@custom` template when they exist.

Go to **Index Management > Index Templates** and select any managed index to view the `@custom` component templates associated with it. 

:::{image} /manage-data/images/elasticsearch-reference-tutorial-custom-policies-otel-template.png
:alt: A screenshot showing the logs@custom and logs-otel@custom component templates associated with the logs-otel@template index template.
:::
:::::

:::{tip}
If you want your {{ilm-init}} changes to apply only to specific indices, you can create a custom index template directly instead of modifying the custom component template. Use the **Index management** page in {{kib}} or the [index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API to create a new template.
:::

1. Click on the **Component Template** tab and click **Create component template**.
2. Under **Logistics**, name the component template `logs@custom`.
3. Under **Index settings**, set the {{ilm-init}} policy name created in the previous step:

    ```JSON
    {
        "index": {
            "lifecycle": {
                "name": "logs-custom"
            }
        }
    }
    ```

4. Continue to **Review**, and then click **Save component template**.
5. Click the **Index Templates**, tab, and then select the `logs` index template.
6. In the summary, view the **Component templates** list. `logs@custom` should be listed.
