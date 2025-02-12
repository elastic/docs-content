# Full disk on multiple-nodes deployment [ech-multiple-node-deployment-disk-used]

**Health check**

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the {{es}} Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} ../../../images/cloud-heroku-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. On your deployment page, scroll down to **Instances** and check if the disk allocation for any of your {{es}} instances is over 90%.

    :::{image} ../../../images/cloud-heroku-ec-full-disk-multiple-nodes.png
    :alt: Full disk on multiple-nodes deployment
    :::


**Possible cause**

* The available storage is insufficient for the amount of ingested data.

**Resolution**

* [Delete unused data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
* Increase the disk size (scale up).

::::{note}
If your {{es}} cluster is unhealthy and reports a status of red, the scale up configuration change to increasing disk size on the affected data tiers may fail. You might need to delete some data so the configuration can be edited. If you want to increase your disk size without deleting data, then [reach out to Elastic support](../../../deploy-manage/deploy/elastic-cloud/ech-get-help.md) and we will assist you with scaling up.
::::


**Preventions**

* Increase the disk size (scale up).

    1. On your deployment page, scroll down to **Instances** and identify the node attribute of the instances that are running out of disk space.

        :::{image} ../../../images/cloud-heroku-ec-node-attribute.png
        :alt: Instance node attribute
        :::

    2. Use the node types identified at step 1 to find out the corresponding data tier.

        :::{image} ../../../images/cloud-heroku-ec-node-types-data-tiers.png
        :alt: Node type and corresponding attribute
        :::

    3. From your deployment menu, go to the **Edit** page and increase the **Size per zone** for the data tiers identified at step 2.

        :::{image} ../../../images/cloud-heroku-ec-increase-size-per-zone.png
        :alt: Increase size per zone
        :::

* Enable [autoscaling](../../../deploy-manage/autoscaling.md) to grow your cluster automatically when it runs out of space.
* Configure (ILM) policies to automatically delete unused data.
* Enable [data tiers](../../../manage-data/lifecycle/data-tiers.md) to move older data that you don’t query often to more cost-effective storage.

