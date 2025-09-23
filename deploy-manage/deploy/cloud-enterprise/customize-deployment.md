---
navigation_title: Customize deployment components
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-customize-deployment.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

% document scope: this document focuses on the Deployment -> Edit page, how ECE applies changes, and links to other configurable features

# Customize your deployment components [ece-customize-deployment]

In ECE, you can customize your deployment at any time by selecting **Edit** from the deployment page. This allows you to fine-tune its capacity and architecture, adjust configuration settings, availability zones, and enable or disable [data tiers](/manage-data/lifecycle/data-tiers.md).

::::{note}
The configurable components and allowed values available on the Edit page depend on the [deployment template](./deployment-templates.md) and [instance configurations](./ece-configuring-ece-instance-configurations-default.md) associated with the deployment.
::::

To customize your deployment:

1. [Log into the Cloud UI](./log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other [filters](./search-filter-deployments.md). To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.

4. Let the user interface guide you through the cluster configuration for your cluster. Refer to [](#ece-edit-deployment) for more details.

    ::::{tip}
        When updating an existing deployment, you can make multiple changes to your {{es}} cluster with a single configuration update.
    ::::

5. Select a [configuration strategy](#configuration-strategies) and save your changes. The orchestrator will prepare and execute a plan to apply the requested changes.

Review the changes to your configuration on the **Activity** page, with a tab for {{es}} and one for {{kib}}.

## Editing deployment [ece-edit-deployment]

In the deployment edit page, you can configure the following settings and features:

* Enable [autoscaling](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md) so that the available resources adjust automatically as demands on the deployment change.

* If you don’t want to autoscale your deployment, you can manually increase or decrease capacity of each [data tier](../../../manage-data/lifecycle/data-tiers.md) and component. For example, you might add warm or cold tier nodes for time series data that is accessed infrequently, or expand {{kib}} capacity to handle higher workloads.

    * From the **Size per zone** drop-down menu, select what best fits your requirements.

        :::{image} /deploy-manage/images/cloud-enterprise-ec-customize-deployment2.png
        :alt: Customize hot data and content tier nodes
        :::

        Based on the size you select for a tier, ECE automatically calculates the required number of nodes. Before adding additional nodes, the system scales up existing nodes to the maximum size allowed by their instance configuration, as defined in the deployment template. The maximum size for an {{es}} instance using the default templates typically ranges between 58GB and 64GB RAM.
        
        The **Architecture** summary displays the total number of nodes per zone, where each circle color represents a different node type:

        :::{image} /deploy-manage/images/cloud-enterprise-ec-number-of-nodes.png
        :alt: Number of nodes per deployment size
        :::

* Adjust the number of **Availability zones** for each component to enhance [fault tolerance](./ece-ha.md) in your deployment.

* Enable additional components, such as [Machine Learning](../../../explore-analyze/machine-learning.md) nodes or an [Integrations server](./manage-integrations-server.md).

* Select **Manage user settings and extensions** at {{es}} level, or **Edit user settings** for other components, to customize the YML configuration settings and plugin extensions. For more details, refer to [](edit-stack-settings.md) and [](./add-plugins.md).

* Select the **Advanced edit** link at the bottom of the page to access the [](./advanced-cluster-configuration.md) view.

    ::::{warning}
    You can break things when using the advanced cluster configuration editor. Use this functionality only if you know what you are doing or if you are being directed by someone from Elastic.
    ::::

## Configuration strategies [configuration-strategies]

When you select **Save changes** on the **Edit deployment** page, the orchestrator initiates a plan to apply the new configuration to your deployment. You can control how these changes are applied to minimize disruption and ensure a smooth transition.

* **Autodetect strategy** (recommended): Let ECE determine the strategy depending on the type changes to apply.
* **Rolling change per node**: One instance at a time. This strategy performs inline, rolling configuration changes that mutate existing containers. Recommended for most configuration changes. If the required resources are unavailable on the ECE nodes handling the existing instances, it falls back to grow and shrink.
* **Grow and shrink**: The orchestrator creates new instances with the new configuration, then migrates the data, and eventually deletes the original ones. This strategy is automatically selected when adding or removing master-eligible instances.
* **Rolling grow and shrink**: Similar to grow and shrink, but creating one instance at a time. This strategy can take a lot longer than grow and shrink.

The `Extended maintenance` optional flag will make ECE to [stop routing requests](../../maintenance/start-stop-routing-requests.md) to all instances during the plan execution. The cluster will be unavailable for external connections while the configuration changes are in progress.

::::{note}
If you enable the **Extended maintenance** optional flag, ECE will [stop routing requests](../../maintenance/start-stop-routing-requests.md) to all instances during the plan execution, making the cluster unavailable for external connections while configuration changes are in progress.

This option introduces downtime and is rarely needed. Use it only when you need to block all traffic to the cluster during the update.
::::

When executing plans, always review the reported configuration changes and track progress on the **Activity** page of the deployment, which includes separate tabs for {{es}}, {{kib}}, and other {{stack}} components.
