---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/example-using-index-lifecycle-policy.html
applies_to:
  stack: ga
  serverless: ga
---

# Tutorial: Customize built-in policies

{{es}} includes the following built-in {{ilm-init}} policies:

* `logs@lifecycle`
* `metrics@lifecycle`
* `synthetics@lifecycle`

{{agent}} uses these policies to manage backing indices for its data streams. This tutorial shows you how to use {{kib}}’s **Index Lifecycle Policies** to customize these policies based on your application’s performance, resilience, and retention requirements.


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

        :::{image} ../../../images/elasticsearch-reference-tutorial-ilm-ess-add-warm-data-tier.png
        :alt: Add a warm data tier to your deployment
        :class: screenshot
        :::

    * Self-managed cluster: Assign `data_hot` and `data_warm` roles to nodes as described in [*Data tiers*](../data-tiers.md).

        For example, include the `data_warm` node role in the `elasticsearch.yml` file of each node in the warm tier:

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

1. Open the menu and go to **Stack Management** > **Index Lifecycle Policies**.
2. Toggle **Include managed system policies**.
3. Select the `logs@lifecycle` policy.
4. On the **Edit policy logs** page, toggle **Save as new policy**, and then provide a new name for the policy, for example, `logs-custom`.

The `logs@lifecycle` policy uses the recommended rollover defaults: Start writing to a new index when the primary shard size of the current write index reaches 50GB or the index becomes 30 days old.

To view or change the rollover settings, click **Advanced settings** for the hot phase. Then disable **Use recommended defaults** to display the rollover settings.

:::{image} ../../../images/elasticsearch-reference-tutorial-ilm-hotphaserollover-default.png
:alt: View rollover defaults
:class: screenshot
:::


## Modify the policy [ilm-ex-modify-policy]

The default `logs@lifecycle` policy is designed to prevent the creation of many tiny daily indices. You can modify your copy of the policy to meet your performance requirements and manage resource usage.

1. Activate the warm phase and click **Advanced settings**.

    1. Set **Move data into phase when** to **30 days old**. This moves indices to the warm tier 30 days after rollover.
    2. Enable **Set replicas** and change **Number of replicas** to **1**.
    3. Enable **Force merge data** and set **Number of segments** to **1**.

    :::{image} ../../../images/elasticsearch-reference-tutorial-ilm-modify-default-warm-phase-rollover.png
    :alt: Add a warm phase with custom settings
    :class: screenshot
    :::

2. In the warm phase, click the trash icon to enable the delete phase.

    :::{image} ../../../images/elasticsearch-reference-tutorial-ilm-enable-delete-phase.png
    :alt: Enable the delete phase
    :class: screenshot
    :::

    In the delete phase, set **Move data into phase when** to **90 days old**. This deletes indices 90 days after rollover.

    :::{image} ../../../images/elasticsearch-reference-tutorial-ilm-delete-rollover.png
    :alt: Add a delete phase
    :class: screenshot
    :::

3. Click **Save as new policy**.

::::{tip}
Copies of managed {{ilm-init}} policies are also marked as **Managed**. You can use the [Create or update lifecycle policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) to update the `_meta.managed` parameter to `false`.
::::



## Apply the policy [example-using-index-lifecycle-policy-apply-policy]

To apply your new {{ilm-init}} policy to the `logs` index template, create or edit the `logs@custom` component template.

A `*@custom` component template allows you to customize the mappings and settings of managed index templates, without having to override managed index templates or component templates. This type of component template is automatically picked up by the index template. [Learn more](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template).

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
