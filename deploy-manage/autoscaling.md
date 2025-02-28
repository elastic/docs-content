---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-autoscaling.html
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-autoscaling.html
applies_to:
  deployment:
    ece: ga
    ess: ga
    eck: ga
---

# Autoscaling

::::{note} 
{{cloud-only}}
::::

The autoscaling feature allows an operator to create tiers of nodes. These nodes monitor themselves to decide if they need to scale, based on an operator-defined policy. An Elasticsearch cluster can use the autoscaling API to report if it needs more resources to meet the policy. For example, an operator could define a policy that a warm tier should scale on available disk space. Elasticsearch monitors disk space in the warm tier. If it predicts low disk space for current and future shard copies, the autoscaling API will report that the cluster needs to scale. It remains the responsibility of the operator to add the additional resources that the cluster signals it requires.

:::{{tip}} - Serverless handles autoscaling for you
By default, {{serverless-full}} automatically scales your {{es}} resources based on your usage. You don't need to enable autoscaling.
:::

A policy is composed of a list of roles and a list of deciders. The policy governs the nodes matching the roles. The deciders provide independent estimates of the capacity required. See [Autoscaling deciders](../deploy-manage/autoscaling/autoscaling-deciders.md) for details on available deciders.

Autoscaling supports:
* Scaling machine learning nodes up and down.
* Scaling data nodes up based on storage.

::::{note} 
Autoscaling is not supported on Debian 8.
::::

To learn more about configuring and managing autoscaling, check the following sections:

* [Overview](#ec-autoscaling-intro)
* [When does autoscaling occur?](#ec-autoscaling-factors)
* [Notifications](#ec-autoscaling-notifications)
* [Restrictions and limitations](#ec-autoscaling-restrictions)
* [Enable or disable autoscaling](#ec-autoscaling-enable)
* [Update your autoscaling settings](#ec-autoscaling-update)

::::{tab-set}

:::{tab-item} {{ech}}
You can also have a look at our [autoscaling example](./autoscaling/ece-autoscaling-example.md), as well as a sample request to [create an autoscaled deployment through the API](./autoscaling/ec-hosted-autoscaling-api-example.md).
:::

:::{tab-item} {{ece}}
You can also have a look at our [autoscaling example](./autoscaling/ece-autoscaling-example.md), as well as a sample request to [create an autoscaled deployment through the API](./autoscaling/ece-autoscaling-api-example.md).
:::

:::{tab-item} {{ecloud}} - Heroku
You can also have a look at our [autoscaling example](./autoscaling/ece-autoscaling-example.md).
:::

::::

## Overview [ec-autoscaling-intro]
$$$ece-autoscaling-intro$$$$$$ech-autoscaling-intro$$$When you first create a deployment it can be challenging to determine the amount of storage your data nodes will require. The same is relevant for the amount of memory and CPU that you want to allocate to your machine learning nodes. It can become even more challenging to predict these requirements for weeks or months into the future. In an ideal scenario, these resources should be sized to both ensure efficient performance and resiliency, and to avoid excess costs. Autoscaling can help with this balance by adjusting the resources available to a deployment automatically as loads change over time, reducing the need for monitoring and manual intervention.

::::{note}
Autoscaling is enabled for the Machine Learning tier by default for new deployments.
::::

Currently, autoscaling behavior is as follows:

* **Data tiers**

    * Each Elasticsearch [data tier](../manage-data/lifecycle/data-tiers.md) scales upward based on the amount of available storage. When we detect more storage is needed, autoscaling will scale up each data tier independently to ensure you can continue and ingest more data to your hot and content tier, or move data to the warm, cold, or frozen data tiers.
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
For any Elasticsearch component the number of availability zones is not affected by autoscaling. You can always set the number of availability zones manually and the autoscaling mechanism will add or remove capacity per availability zone.
::::

## When does autoscaling occur?[ec-autoscaling-factors]

$$$ece-autoscaling-factors$$$$$$ech-autoscaling-factors$$$Several factors determine when data tiers or machine learning nodes are scaled.

For a data tier, an autoscaling event can be triggered in the following cases:

* Based on an assessment of how shards are currently allocated, and the amount of storage and buffer space currently available.

* When past behavior on a hot tier indicates that the influx of data can increase significantly in the near future. Refer to [Reactive storage decider](../deploy-manage/autoscaling/autoscaling-deciders.md) and [Proactive storage decider](../deploy-manage/autoscaling/autoscaling-deciders.md) for more detail.

* Through ILM  policies. For example, if a deployment has only hot nodes and autoscaling is enabled, it automatically creates warm or cold nodes, if an ILM policy is trying to move data from hot to warm or cold nodes.

On machine learning nodes, scaling is determined by an estimate of the memory and CPU requirements for the currently configured jobs and trained models. When a new machine learning job tries to start, it looks for a node with adequate native memory and CPU capacity. If one cannot be found, it stays in an `opening` state. If this waiting job exceeds the queueing limit set in the machine learning decider, a scale up is requested. Conversely, as machine learning jobs run, their memory and CPU usage might decrease or other running jobs might finish or close. In this case, if the duration of decreased resource usage exceeds the set value for `down_scale_delay`, a scale down is requested. Check [Machine learning decider](../deploy-manage/autoscaling/autoscaling-deciders.md) for more detail. To learn more about machine learning jobs in general, check [Create anomaly detection jobs](../explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-create-job)

On a highly available deployment, autoscaling events are always applied to instances in each availability zone simultaneously, to ensure consistency.

## Notifications[ec-autoscaling-notifications]
$$$ece-autoscaling-notifications$$$$$$ech-autoscaling-notifications$$$
In the event that a data tier or machine learning node scales up to its maximum possible size, you’ll receive an email, and a notice also appears on the deployment overview page prompting you to adjust your autoscaling settings to ensure optimal performance.

In {{ece}} deployments, a warning is also issued in the ECE `service-constructor` logs with the field `labels.autoscaling_notification_type` and a value of `data-tier-at-limit` (for a fully scaled data tier) or `ml-tier-at-limit` (for a fully scaled machine learning node). The warning is indexed in the `logging-and-metrics` deployment, so you can use that event to [configure an email notification](../explore-analyze/alerts-cases/watcher.md).

## Restrictions and limitations[ec-autoscaling-restrictions]

$$$ece-autoscaling-restrictions$$$$$$ech-autoscaling-restrictions$$$The following are known limitations and restrictions with autoscaling:

* Autoscaling will not run if the cluster is unhealthy or if the last Elasticsearch plan failed.

In {{ech}} the following additional limitations apply:

* Trial deployments cannot be configured to autoscale beyond the normal Trial deployment size limits. The maximum size per zone is increased automatically from the Trial limit when you convert to a paid subscription.
* ELSER deployments do not scale automatically. For more information, refer to [ELSER](../explore-analyze/machine-learning/nlp/ml-nlp-elser.md) and [Trained model autoscaling](../explore-analyze/machine-learning/nlp/ml-nlp-auto-scale.md).

In {{ece}}, the following additional limitations apply:

* In the event that an override is set for the instance size or disk quota multiplier for an instance by means of the [Instance Overrides API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-all-instances-settings-overrides), autoscaling will be effectively disabled. It’s recommended to avoid adjusting the instance size or disk quota multiplier for an instance that uses autoscaling, since the setting prevents autoscaling.

## Enable or disable autoscaling[ec-autoscaling-enable]

$$$ece-autoscaling-enable$$$$$$ech-autoscaling-enable$$$To enable or disable autoscaling on a deployment:

1. Log in to the ECE [Cloud UI]((/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md) or  [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

2. On the **Deployments** page, select your deployment.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.


3. In your deployment menu, select **Edit**.
4. Select desired autoscaling configuration for this deployment using **Enable Autoscaling for:** dropdown menu.
5. Select **Confirm** to have the autoscaling change and any other settings take effect. All plan changes are shown on the Deployment **Activity** page.

When autoscaling has been enabled, the autoscaled nodes resize according to the [autoscaling settings](../deploy-manage/autoscaling.md#ec-autoscaling-update). Current sizes are shown on the deployment overview page.

When autoscaling has been disabled, you need to adjust the size of data tiers and machine learning nodes manually.

## Update your autoscaling settings[ec-autoscaling-update]

$$$ece-autoscaling-update$$$$$$ech-autoscaling-update$$$Each autoscaling setting is configured with a default value. You can adjust these if necessary, as follows:

1. **Log in** to the console.

::::{tab-set}

:::{tab-item} {{ech}}
[Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body)
:::

:::{tab-item} {{ece}}
[Cloud UI](../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md)
:::

:::{tab-item} {{ecloud}} - Heroku
[Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body)
:::
::::

2. On the **Deployments** page, select your deployment.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. In your deployment menu, select **Edit**.
4. To update a data tier:

    1. Use the dropdown box to set the **Maximum size per zone** to the largest amount of resources that should be allocated to the data tier automatically. The resources will not scale above this value.
    2. You can also update the **Current size per zone**. If you update this setting to match the **Maximum size per zone**, the data tier will remain fixed at that size.
    3. For a hot data tier you can also adjust the **Forecast window**. This is the duration of time, up to the present, for which past storage usage is assessed in order to predict when additional storage is needed.
    4. Select **Save** to apply the changes to your deployment.

5. To update machine learning nodes:

    1. Use the dropdown box to set the **Minimum size per zone** and **Maximum size per zone** to the smallest and largest amount of resources, respectively, that should be allocated to the nodes automatically. The resources allocated to machine learning will not exceed these values. If you set these two settings to the same value, the machine learning node will remain fixed at that size.
    2. Select **Save** to apply the changes to your deployment.

% ECE NOTE
::::{note} - {{ece}}
On Elastic Cloud Enterprise, system-owned deployment templates include the default values for all deployment autoscaling settings.
::::
