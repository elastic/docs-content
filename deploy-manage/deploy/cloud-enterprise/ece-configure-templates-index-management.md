---
navigation_title: Configure index management
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-templates-index-management.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure index management for deployment templates [ece-configure-templates-index-management]

If you create a deployment template that includes more than one data configuration, you must also specify how {{ece}} should manage indices for your users when they create their deployments. For time-series use cases such as logging, metrics, and APM, providing a template that enables index management ensures that data is being stored in the most cost-effective way possible as it ages.

Configuring index management is part of the larger task of [creating deployment templates](ece-configuring-ece-create-templates.md) or editing them. The choices you make here determine which index management methods are available to your users when they create deployments.

You should configure all index management methods that you want your users to be able to choose from when they create their deployments from your template. You can configure index curation, index lifecycle management, or both.


## Available index management strategies 

Index lifecycle management
:   Uses the [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) feature of the {{stack}} that provides an integrated and streamlined way to manage time-based data, making it easier to follow best practices for managing your indices. Compared to index curation, ILM gives you more fine-grained control over the lifecycle of each index.

Index curation (Curator) {applies_to}`stack: deprecated 6.7`
:   Creates new indices on hot nodes first and moves them to warm nodes later on, based on the data views (formerly *index patterns*) you specify. Also manages replica counts for you, so that all shards of an index can fit on the right data nodes. Compared to index lifecycle management, index curation for time-based indices supports only one action, to move indices from nodes on one data configuration to another, but it is more straightforward to set up initially and all setup can be done directly from the Cloud UI. 

    If your users need to delete indices once they are no longer useful to them, they can run [Curator](curator://reference/index.md) on-premise to manage indices for {{es}} clusters hosted on {{ece}}.

    ::::{note}
    Index curation has been deprecated in favor of [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md). For {{stack}} version 6.7 and later, any deployments using index curation will be prompted to [migrate to ILM](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md).
    ::::


## Configure {{ilm}}

To configure {{ilm}} as part of your deployment template:

On the **Index Management** page, under **{{ilm}} ({{ilm-init}})**, specify the node attributes for your data configurations. 

Node attributes are simple key-value pairs, such as `node_type: hot`, `node_type: warm`, and `node_type: cold`. These node attributes add defining metadata attributes to each data configuration in your template that tell your users what they can be used for. What you define here should help guide your users when they set up their index lifecycle management policy in {{kib}}, such as a hot-warm policy.

For each data tier, specify an attribute key-value pair in the **Node attributes** field, with the key and value separated by a colon. Repeat this process until you have added all the node attributes that you want to be available to your users when they create an index lifecycle policy later on.

## Configure index curation
```{applies_to}
stack: deprecated 6.7
```

::::{note}
Index curation has been deprecated in favor of [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md). For {{stack}} version 6.7 and later, any deployments using index curation will be prompted to [migrate to ILM](/manage-data/lifecycle/index-lifecycle-management/migrate-index-management.md).
::::

To configure index curation as part of your deployment template:

1. On the **Index Management** page, under **Index curation**, click **Configure**.

2. Configure index curation by adding an index pattern:

    1. Select the hot data configuration where new indices get created initially.
    2. Select the warm nodes where older indices get moved to later on when they get curated.
    3. Specify which indices get curated by including at least one index pattern.

        By default, the pattern is `*`, which means that all indices get curated. For logging use cases, you could specify to curate only the `logstash-*`, `metricbeat-*`, or `filebeat-*` data views, for example.

    4. Specify the time interval after which indices get curated.

## Next steps

After you have completed these steps, continue with [creating your deployment template](ece-configuring-ece-create-templates.md#ece-configuring-ece-create-templates-ui).

