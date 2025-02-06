---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling.html
---

# Deployment autoscaling [ece-autoscaling]

Autoscaling helps you to more easily manage your deployments by adjusting their available resources automatically, and currently supports scaling for both data and machine learning nodes, or machine learning nodes only. Check the following sections to learn more:

* [Overview](../autoscaling.md#ece-autoscaling-intro)
* [When does autoscaling occur?](../autoscaling.md#ece-autoscaling-factors)
* [Notifications](../autoscaling.md#ece-autoscaling-notifications)
* [Restrictions and limitations](../autoscaling.md#ece-autoscaling-restrictions)
* [Enable or disable autoscaling](../autoscaling.md#ece-autoscaling-enable)
* [Update your autoscaling settings](../autoscaling.md#ece-autoscaling-update)

You can also have a look at our [autoscaling example](ece-autoscaling-example.md), as well as a sample request to [create an autoscaled deployment through the API](ece-autoscaling-api-example.md).


## Overview [ece-autoscaling-intro]

When you first create a deployment it can be challenging to determine the amount of storage your data nodes will require. The same is relevant for the amount of memory and CPU that you want to allocate to your machine learning nodes. It can become even more challenging to predict these requirements for weeks or months into the future. In an ideal scenario, these resources should be sized to both ensure efficient performance and resiliency, and to avoid excess costs. Autoscaling can help with this balance by adjusting the resources available to a deployment automatically as loads change over time, reducing the need for monitoring and manual intervention.

::::{note}
Autoscaling is enabled for the Machine Learning tier by default for new deployments.
::::


Currently, autoscaling behavior is as follows:

* **Data tiers**

    * Each Elasticsearch [data tier](../../manage-data/lifecycle/data-tiers.md) scales upward based on the amount of available storage. When we detect more storage is needed, autoscaling will scale up each data tier independently to ensure you can continue and ingest more data to your hot and content tier, or move data to the warm, cold, or frozen data tiers.
    * In addition to scaling up existing data tiers, a new data tier will be automatically added when necessary, based on your [index lifecycle management policies](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-index-management.html).
    * To control the maximum size of each data tier and ensure it will not scale above a certain size, you can use the maximum size per zone field.
    * Autoscaling based on memory or CPU, as well as autoscaling downward, is not currently supported. In case you want to adjust the size of your data tier to add more memory or CPU, or in case you deleted data and want to scale it down, you can set the current size per zone of each data tier manually.

* **Machine learning nodes**

    * Machine learning nodes can scale upward and downward based on the configured machine learning jobs.
    * When a machine learning job is opened, or a machine learning trained model is deployed, if there are no machine learning nodes in your deployment, the autoscaling mechanism will automatically add machine learning nodes. Similarly, after a period of no active machine learning jobs, any enabled machine learning nodes are disabled automatically.
    * To control the maximum size of your machine learning nodes and ensure they will not scale above a certain size, you can use the maximum size per zone field.
    * To control the minimum size of your machine learning nodes and ensure the autoscaling mechanism will not scale machine learning below a certain size, you can use the minimum size per zone field.
    * The determination of when to scale is based on the expected memory and CPU requirements for the currently configured machine learning jobs and trained models.


::::{note}
For any Elastic Cloud Enterprise Elasticsearch component the number of availability zones is not affected by autoscaling. You can always set the number of availability zones manually and the autoscaling mechanism will add or remove capacity per availability zone.
::::



## When does autoscaling occur? [ece-autoscaling-factors]

Several factors determine when data tiers or machine learning nodes are scaled.

For a data tier, an autoscaling event can be triggered in the following cases:

* Based on an assessment of how shards are currently allocated, and the amount of storage and buffer space currently available.

When past behavior on a hot tier indicates that the influx of data can increase significantly in the near future. Refer to [Reactive storage decider](autoscaling-deciders.md) and [Proactive storage decider](autoscaling-deciders.md) for more detail.

* Through ILM  policies. For example, if a deployment has only hot nodes and autoscaling is enabled, it automatically creates warm or cold nodes, if an ILM policy is trying to move data from hot to warm or cold nodes.

On machine learning nodes, scaling is determined by an estimate of the memory and CPU requirements for the currently configured jobs and trained models. When a new machine learning job tries to start, it looks for a node with adequate native memory and CPU capacity. If one cannot be found, it stays in an `opening` state. If this waiting job exceeds the queueing limit set in the machine learning decider, a scale up is requested. Conversely, as machine learning jobs run, their memory and CPU usage might decrease or other running jobs might finish or close. In this case, if the duration of decreased resource usage exceeds the set value for `down_scale_delay`, a scale down is requested. Check [Machine learning decider](autoscaling-deciders.md) for more detail. To learn more about machine learning jobs in general, check [Create anomaly detection jobs](https://www.elastic.co/guide/en/machine-learning/current/create-jobs.html).

On a highly available deployment, autoscaling events are always applied to instances in each availability zone simultaneously, to ensure consistency.


## Notifications [ece-autoscaling-notifications]

In the event that a data tier or machine learning node scales up to its maximum possible size, a notice appears on the deployment overview page prompting you to adjust your autoscaling settings in order to ensure optimal performance.

A warning is also issued in the ECE `service-constructor` logs with the field `labels.autoscaling_notification_type` and a value of `data-tier-at-limit` (for a fully scaled data tier) or `ml-tier-at-limit` (for a fully scaled machine learning node). The warning is indexed in the `logging-and-metrics` deployment, so you can use that event to [configure an email notification](../../explore-analyze/alerts-cases/watcher/actions-email.md).


## Restrictions and limitations [ece-autoscaling-restrictions]

The following are known limitations and restrictions with autoscaling:

* Autoscaling will not run if the cluster is unhealthy or if the last Elasticsearch plan failed.
* In the event that an override is set for the instance size or disk quota multiplier for an instance by means of the [Instance Overrides API](https://www.elastic.co/guide/en/cloud-enterprise/current/set-all-instances-settings-overrides.html), autoscaling will be effectively disabled. It’s recommended to avoid adjusting the instance size or disk quota multiplier for an instance that uses autoscaling, since the setting prevents autoscaling.


## Enable or disable autoscaling [ece-autoscaling-enable]

To enable or disable autoscaling on a deployment:

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In your deployment menu, select **Edit**.
4. Select desired autoscaling configuration for this deployment using **Enable Autoscaling for:** dropdown menu.
5. Select **Confirm** to have the autoscaling change and any other settings take effect. All plan changes are shown on the Deployment **Activity** page.

When autoscaling has been enabled, the autoscaled nodes resize according to the [autoscaling settings](../autoscaling.md#ece-autoscaling-update). Current sizes are shown on the deployment overview page.

When autoscaling has been disabled, you need to adjust the size of data tiers and machine learning nodes manually.


## Update your autoscaling settings [ece-autoscaling-update]

Each autoscaling setting is configured with a default value. You can adjust these if necessary, as follows:

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In your deployment menu, select **Edit**.
4. To update a data tier:

    1. Use the dropdown box to set the **Maximum size per zone** to the largest amount of resources that should be allocated to the data tier automatically. The resources will not scale above this value.
    2. You can also update the **Current size per zone**. If you update this setting to match the **Maximum size per zone**, the data tier will remain fixed at that size.
    3. For a hot data tier you can also adjust the **Forecast window**. This is the duration of time, up to the present, for which past storage usage is assessed in order to predict when additional storage is needed.
    4. Select **Save** to apply the changes to your deployment.

5. To update machine learning nodes:

    1. Use the dropdown box to set the **Minimum size per zone** and **Maximum size per zone** to the smallest and largest amount of resources, respectively, that should be allocated to the nodes automatically. The resources allocated to machine learning will not exceed these values. If you set these two settings to the same value, the machine learning node will remain fixed at that size.
    2. Select **Save** to apply the changes to your deployment.


You can also view our [example](ece-autoscaling-example.md) of how the autoscaling settings work.

::::{note}
On Elastic Cloud Enterprise, system-owned deployment templates include the default values for all deployment autoscaling settings.
::::
