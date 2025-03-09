---
navigation_title: Customize deployment components
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-customize-deployment.html
---

% Background and scope note: this document is about the Deployment -> Edit page, how ECE applies changes, and links to other configurable features

# Customize your deployment [ece-customize-deployment]

% TBD, refine this intro after checking the UI
In ECE, you can customize your deployment at any time by selecting **Edit** from the deployment page. This allows you to modify the deployment architecture, adjust configuration settings, availability zones, resources, and enable or disable data tiers.

::::{note}
The configurable components and allowed values available on the Edit page depend on the [deployment template](./deployment-templates.md) and [instance configurations](./ece-configuring-ece-instance-configurations-default.md) associated with the deployment.
::::

To customize your deployment:

1. [Log into the Cloud UI](./log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other [filters](./search-filter-deployments.md). To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.

## Editing deployment

In the deployment edit page, you can change the following settings:

* Enable [autoscaling](../../autoscaling.md) so that the available resources adjust automatically as demands on the deployment change.

* If you don’t want to autoscale your deployment, you can manually increase or decrease capacity by adjusting the size of hot, warm, cold, and frozen [data tiers](../../../manage-data/lifecycle/data-tiers.md) nodes. For example, you might want to add warm or cold tier nodes if you have time series data that is accessed less-frequently and rarely needs to be updated.

    * From the **Size per zone** drop-down menu, select what best fits your requirements.

        :::{image} ../../../images/cloud-enterprise-ec-customize-deployment2.png
        :alt: Customize hot data and content tier nodes
        :::

        Based on the size you select for a tier, ECE automatically calculates the required number of nodes. Before adding additional nodes, the system scales up existing nodes to the maximum size allowed by their instance configuration, as defined in the deployment template. The maximum size for an {{es}} instance using the default templates typically ranges between 58GB and 64GB RAM.
        
        The **Architecture** summary displays the total number of nodes per zone, where each circle color represents a different node type:

        :::{image} ../../../images/cloud-enterprise-ec-number-of-nodes.png
        :alt: Number of nodes per deployment size
        :::

    * Adjust the number of **Availability zones** to increase fault tolerance for the deployment.

* Select **Edit user settings** to add configuration settings to the YML file of any component and further customize its behavior.

  For more information, refer to [](edit-stack-settings.md).

* Enable specific {{es}} plugins which are not enabled by default.
* Enable additional features, such as Machine Learning or coordinating nodes.
* Set specific configuration parameters for your {{es}} nodes or {{kib}} instances.

## Applying changes

When clicking on **Save changes** in the Edit deployment page

% TBD, explain a bit the different type of plans

* Select the method to apply changes
  * Rolling inline
  * Grow and shrink

## Other configuration changes

The following configuration settings are not available within the Edit deployment page:

* Logs and Metrics (monitoring)
* Secure settings (keystore settings)
* Snapshots

