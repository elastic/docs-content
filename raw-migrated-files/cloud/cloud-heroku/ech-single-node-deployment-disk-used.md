# Full disk on single-node deployment [ech-single-node-deployment-disk-used]

**Health check**

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the Elasticsearch Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} ../../../images/cloud-heroku-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. On your deployment page, scroll down to **Instances** and check if the disk allocation for your {{es}} instance is over 90%.

    :::{image} ../../../images/cloud-heroku-ec-full-disk-single-node.png
    :alt: Full disk on single-node deployment
    :::


**Possible cause**

* The available storage is insufficient for the amount of ingested data.

**Resolution**

* [Delete unused data](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-delete-index.html).
* Increase the disk size on your Hot data and Content tier (scale up).

::::{note}
If your {{es}} cluster is unhealthy and reports a status of red, then increasing the disk size of your Hot data and Content tier may fail. You might need to delete some data so the configuration can be edited. If you want to increase your disk size without deleting data, then [reach out to Elastic support](../../../deploy-manage/deploy/elastic-cloud/ech-get-help.md) and we will assist you with scaling up.
::::


**Preventions**

* Increase the disk size on your Hot data and Content tier (scale up).

    From your deployment menu, go to the **Edit** page and increase the **Size per zone** for your Hot data and Content tiers.

    :::{image} ../../../images/cloud-heroku-ec-increase-size-per-zone.png
    :alt: Increase size per zone
    :::

* Enable [autoscaling](../../../deploy-manage/autoscaling.md) to grow your cluster automatically when it runs out of space.
* Configure (ILM) policies to automatically delete unused data.
* Add nodes to your {{es}} cluster and enable [data tiers](../../../manage-data/lifecycle/data-tiers.md) to move older data that you don’t query often to more cost-effective storage.

