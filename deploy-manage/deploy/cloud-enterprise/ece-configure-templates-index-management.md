---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-templates-index-management.html
---

# Configure index management for templates [ece-configure-templates-index-management]

If you create a deployment template that includes more than one data configuration, you must also specify how Elastic Cloud Enterprise should manage indices for your users when they create their deployments. For time-series use cases such as logging, metrics, and APM, providing a template that enables index management ensures that data is being stored in the most cost-effective way possible as it ages.

In a template that creates a hot-warm architecture, you can use index curation to specify where new indices are created initially and where they are moved to later on. However, index curation has been deprecated in favor of index lifecycle management, which offers additional features and more fine-grained control over indices. For instance, using ILM you can enable automatic roll-over of index aliases to new indices when existing indices become too large or too old, and you can set indices to be deleted when they are no longer useful.


## Before you begin [ece_before_you_begin_4]

Configuring index management is part of the larger task of [creating deployment templates](ece-configuring-ece-create-templates.md) or editing them. The choices you make here determine which index management methods are available to your users when they create deployments.

You should configure all index management methods that you want your users to be able to choose from when they create their deployments from your template. You can configure index curation, index lifecycle management, or both. If you are not sure which index management methods to configure, take a look at how your users are asked to [configure index management](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-index-management.html) when they customize their deployments.


## Steps [ece_steps_2]

To configure index management when you create a deployment template:

1. On the **Index Management** page, configure the index curation methods that you want to be available when your users create deployments:

    Index lifecycle management
    :   Uses the ILM feature of the Elastic Stack that provides an integrated and streamlined way to manage time-based data, making it easier to follow best practices for managing your indices. Compared to index curation, ILM gives you more fine-grained control over the lifecycle of each index.

        To configure index lifecycle management:

        1. Specify the node attributes for your data configurations.

            Node attributes are simple key-value pairs, such as `node_type: hot`, `node_type: warm`, and `node_type: cold`. These node attributes add defining metadata attributes to each data configuration in your template that tell your users what they can be used for. What you define here should help guide your users when they set up their index lifecycle management policy in Kibana, such as a hot-warm policy.

            1. Specify an attribute key-value pair in the **Node attributes** field, with the key and value separated by a colon.
            2. Repeat the previous step until you have added all the node attributes that you want to be available to your users when they create an index lifecycle policy later on.


    Index curation
    :   Creates new indices on hot nodes first and moves them to warm nodes later on, based on the data views (formerly *index patterns*) you specify. Also manages replica counts for you, so that all shards of an index can fit on the right data nodes. Compared to index lifecycle management, index curation for time-based indices supports only one action, to move indices from nodes on one data configuration to another, but it is more straightforward to set up initially and all setup can be done directly from the Cloud UI.

        If your user need to delete indices once they are no longer useful to them, they can run [Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/current/index.html) on-premise to manage indices for Elasticsearch clusters hosted on Elastic Cloud Enterprise.

        To configure index curation:

        1. Select the hot data configuration where new indices get created initially.
        2. Select the warm nodes where older indices get moved to later on when they get curated.
        3. Specify which indices get curated by including at least one data view.

            By default, the pattern is `*`, which means that all indices get curated. For logging use cases, you could specify to curate only the `logstash-*`, `metricbeat-*`, or `filebeat-*` data views, for example.

        4. Specify the time interval after which indices get curated.

2. Select **Next**.

After you have completed these steps, continue with [creating your deployment template](ece-configuring-ece-create-templates.md#ece-configuring-ece-create-templates-ui).

