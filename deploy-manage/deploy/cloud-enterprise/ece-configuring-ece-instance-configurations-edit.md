---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-instance-configurations-edit.html
---

# Edit instance configurations [ece-configuring-ece-instance-configurations-edit]

Instance configurations enable components of the Elastic Stack to be matched to allocators for a specific use case. The matching is accomplished by defining a query that filters possible allocators based on their tags. For existing instance configurations, you can edit the query to change how allocators get matched, which in turn changes what components of the Elastic Stack get hosted on the matching allocators when creating or changing a deployment.

You might need to edit instance configurations under the following circumstances:

* After you upgrade to or install Elastic Cloud Enterprise 2.0 or later and [have tagged your allocators](ece-configuring-ece-tag-allocators.md), to indicate how you want to use these tagged allocators.
* If tagged allocators in your ECE installation are not being used as expected when you create or change deployments. Editing an instance configuration affects all deployments that depend on it, and tagged allocators that do not get matched by an instance configuration will not be used. If this happens, you can edit your instance configurations to create less restrictive queries.

::::{tip}
If you edit instance configurations, so that they match fewer allocators, instances of the Elastic Stack that were previously matched to those allocators might be relocated. Keep this in mind when making queries more restrictive.
::::



## Steps [ece_steps]

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Templates**.
3. Select the **Instance configurations** tab to check the default instance configurations that ship with ECE.
4. Choose one of the instance configurations and select **Edit instance configuration**.

    For example: Select to edit the `data.default` default instance configuration, so that you can specify where Elasticsearch data nodes for incoming data should be deployed. In a hot-warm architecture, this will determine where your hot data gets sent to.

5. In the **Input** section, construct a query that filters on specific allocator tags.

    The following steps assume that no query exists, as is the case when you edit the default instance configurations for the first time after installing ECE version 2.0 or later. You can also edit an existing query by modifying the inner and outer clauses.

    ::::{tip}
    An *outer clause* ANDs or ORs your main filtering criteria. You use outer clauses to find the allocators that you tagged earlier. An *inner clause* modifies an outer clause and let’s you refine your filtering criteria further. If you are unsure how the process works, try searching on some of the allocator tags that you added and check how the query results change. If you are editing the `data.default` default instance configuration, you want your query to return all allocators on which Elasticsearch data nodes for incoming data can be placed.
    ::::


    1. Select **And** or **Or** to add a first outer clause.
    2. Enter a key-value pair in the **Key** and **Value** fields that you previously [tagged your allocators](ece-configuring-ece-tag-allocators.md) with.

        For example: Enter `SSD` and `true`, if you tagged your allocators with this tag, or enter whatever tag you are using to identify allocators that can host Elasticsearch data nodes for incoming data.

        :::{image} ../../../images/cloud-enterprise-ece-query-ui.png
        :alt: Creating a query that filters on allocator tags
        :::

    3. Check the list of allocators that get matched by your query:

        * If you are satisfied that your query matches all the allocators where the component(s) of the Elastic Stack can be deployed, move on to the next step. For the `data.default` default instance configuration, this means all the allocators where Elasticsearch data nodes for incoming data should be deployed, for example.
        * If you need to refine your query further, continue to adjust your outer or inner clauses. If you are unsure what to do, keep your initial query simple. You can always refine the query later on by re-editing the instance configuration.

6. Select **Save changes**.
7. If you are configuring the default instance configurations for the hot-warm template: Repeat steps 4 through 6 for the `data.highstorage`, `master`, `coordinating`, `kibana`, and `ml` instance configurations.

    For example: For the `data.highstorage` instance configuration, your query should filter for allocators that use spindle-based storage. If you are using our [sample tags](ece-configuring-ece-tag-allocators.md#allocator-sample-tags), you could filter on either `SSD: false` or `highstorage: true`, depending on which tag you decided to use. For the `master` and `kibana` configurations, some multi-purpose hardware might work well. The `ml` instance configuration can benefit from hardware that provides higher CPU (`highCPU: true` in our sample tags).


After you have saved your changes, the updated instance configurations will be used whenever you create or edit deployments that use deployment templates based on these instance configurations.

