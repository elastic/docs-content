---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-customize-deployment.html
---

# Customize your deployment [ece-customize-deployment]

You can either customize a new deployment, or customize an existing one. On the **Create a deployment** page, select **Edit settings** to change the cloud provider, region, hardware profile, and stack version; or select **Advanced settings** for more complex configuration settings.

On the **Advanced settings** page, you can change the following settings:

* Enable [autoscaling](../../autoscaling.md) so that the available resources adjust automatically as demands on the deployment change.
* If you don’t want to autoscale your deployment, you can manually increase or decrease capacity by adjusting the size of hot, warm, cold, and frozen [data tiers](../../../manage-data/lifecycle/data-tiers.md) nodes. For example, you might want to add warm tier nodes if you have time series data that is accessed less-frequently and rarely needs to be updated. Alternatively, you might need cold tier nodes if you have time series data that is accessed occasionally and not normally updated.

    * From the **Size per zone** drop-down menu, select what best fits your requirements.

        :::{image} ../../../images/cloud-enterprise-ec-customize-deployment2.png
        :alt: Customize hot data and content tier nodes
        :::

        Tiers increase in size before they increase the number of nodes. Based on the size that you select, the number of nodes is calculated for you automatically. Each node can be scaled up to 58GB RAM for Azure or 64GB RAM for GCP and AWS. The **Architecture** summary displays the total number of nodes per zone, where each circle color represents a different node type.

        :::{image} ../../../images/cloud-enterprise-ec-number-of-nodes.png
        :alt: Number of nodes per deployment size
        :::

    * Adjust the number of **Availability zones** to increase fault tolerance for the deployment.

* Open **Edit user settings**  to change the  YML configuration file to further customize how you run {{es}}.

For more information, refer to [Editing your user settings](edit-stack-settings.md).

* Enable specific {{es}} plugins which are not enabled by default.
* Enable additional features, such as Machine Learning or coordinating nodes.
* Set specific configuration parameters for your {{es}} nodes or {{kib}} instances.

That’s it! Now that you are up and running, [start exploring with {{kib}}](create-deployment.md), our open-source visualization tool. If you’re not familiar with adding data, yet, {{kib}} can show you how to index your data into {{es}}.
