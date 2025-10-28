---
navigation_title: In ECE and ECH
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-autoscaling.html
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling-example.html
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling-example.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-autoscaling-example.html
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling-api-example.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling-api-example.html
applies_to:
  deployment:
    ece: ga
    ess: ga
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Autoscaling in {{ece}} and {{ech}}

## Overview [ec-autoscaling-intro]
When you first create a deployment it can be challenging to determine the amount of storage your data nodes will require. The same is relevant for the amount of memory and CPU that you want to allocate to your machine learning nodes. It can become even more challenging to predict these requirements for weeks or months into the future. In an ideal scenario, these resources should be sized to both ensure efficient performance and resiliency, and to avoid excess costs. Autoscaling can help with this balance by adjusting the resources available to a deployment automatically as loads change over time, reducing the need for monitoring and manual intervention.

To learn more about configuring and managing autoscaling, check the following sections:

* [Overview](#ec-autoscaling-intro)
* [When does autoscaling occur?](#ec-autoscaling-factors)
* [Notifications](#ec-autoscaling-notifications)
* [Restrictions and limitations](#ec-autoscaling-restrictions)
* [Enable or disable autoscaling](#ec-autoscaling-enable)
* [Update your autoscaling settings](#ec-autoscaling-update)

You can also have a look at our [autoscaling example](#ec-autoscaling-example), as well as a sample request to [create an autoscaled deployment through the API](#ec-autoscaling-api-example).

::::{note}
Autoscaling is enabled for the Machine Learning tier by default for new deployments.
::::

Currently, autoscaling behavior is as follows:

* **Data tiers**

    * Each {{es}} [data tier](../../manage-data/lifecycle/data-tiers.md) scales upward based on the amount of available storage. When we detect more storage is needed, autoscaling will scale up each data tier independently to ensure you can continue and ingest more data to your hot and content tier, or move data to the warm, cold, or frozen data tiers.
    * In addition to scaling up existing data tiers, a new data tier will be automatically added when necessary, based on your [index lifecycle management policies](/manage-data/lifecycle/index-lifecycle-management.md).
    * To control the maximum size of each data tier and ensure it will not scale above a certain size, you can use the maximum size per zone field.
    * Autoscaling based on memory or CPU, as well as autoscaling downward, is not currently supported. In case you want to adjust the size of your data tier to add more memory or CPU, or in case you deleted data and want to scale it down, you can set the current size per zone of each data tier manually.

* **Machine learning nodes**

    * Machine learning nodes can scale upward and downward based on the configured machine learning jobs.
    * When a machine learning job is opened, or a machine learning trained model is deployed, if there are no machine learning nodes in your deployment, the autoscaling mechanism will automatically add machine learning nodes. Similarly, after a period of no active machine learning jobs, any enabled machine learning nodes are disabled automatically.
    * To control the maximum size of your machine learning nodes and ensure they will not scale above a certain size, you can use the maximum size per zone field.
    * To control the minimum size of your machine learning nodes and ensure the autoscaling mechanism will not scale machine learning below a certain size, you can use the minimum size per zone field.
    * The determination of when to scale is based on the expected memory and CPU requirements for the currently configured machine learning jobs and trained models.

::::{note}
For any {{es}} component the number of availability zones is not affected by autoscaling. You can always set the number of availability zones manually and the autoscaling mechanism will add or remove capacity per availability zone.
::::

## When does autoscaling occur?[ec-autoscaling-factors]

Several factors determine when data tiers or machine learning nodes are scaled.

For a data tier, an autoscaling event can be triggered in the following cases:

* Based on an assessment of how shards are currently allocated, and the amount of storage and buffer space currently available.

* When past behavior on a hot tier indicates that the influx of data can increase significantly in the near future. Refer to [Reactive storage decider](autoscaling-deciders.md) and [Proactive storage decider](autoscaling-deciders.md) for more detail.

* Through ILM  policies. For example, if a deployment has only hot nodes and autoscaling is enabled, it automatically creates warm or cold nodes, if an ILM policy is trying to move data from hot to warm or cold nodes.

On machine learning nodes, scaling is determined by an estimate of the memory and CPU requirements for the currently configured jobs and trained models. When a new machine learning job tries to start, it looks for a node with adequate native memory and CPU capacity. If one cannot be found, it stays in an `opening` state. If this waiting job exceeds the queueing limit set in the machine learning decider, a scale up is requested. Conversely, as machine learning jobs run, their memory and CPU usage might decrease or other running jobs might finish or close. In this case, if the duration of decreased resource usage exceeds the set value for `down_scale_delay`, a scale down is requested. Check [Machine learning decider](autoscaling-deciders.md) for more detail. To learn more about machine learning jobs in general, check [Create anomaly detection jobs](../../explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-create-job).

On a highly available deployment, autoscaling events are always applied to instances in each availability zone simultaneously, to ensure consistency.

## Notifications[ec-autoscaling-notifications]
In the event that a data tier or machine learning node scales up to its maximum possible size, you’ll receive an email, and a notice also appears on the deployment overview page prompting you to adjust your autoscaling settings to ensure optimal performance.

In {{ece}} deployments, a warning is also issued in the ECE `service-constructor` logs with the field `labels.autoscaling_notification_type` and a value of `data-tier-at-limit` (for a fully scaled data tier) or `ml-tier-at-limit` (for a fully scaled machine learning node). The warning is indexed in the `logging-and-metrics` deployment, so you can use that event to [configure an email notification](../../explore-analyze/alerts-cases/watcher.md).

## Restrictions and limitations[ec-autoscaling-restrictions]

### Generic limitations

The following are known limitations and restrictions with autoscaling:

* Autoscaling will not run if the cluster is unhealthy or if the last {{es}} plan failed.

### {{ech}} specific limitations

In {{ech}} the following additional limitations apply:

* Trial deployments cannot be configured to autoscale beyond the normal Trial deployment size limits. The maximum size per zone is increased automatically from the Trial limit when you convert to a paid subscription.
* ELSER deployments do not scale automatically. For more information, refer to [ELSER](../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md) and [Trained model autoscaling](../autoscaling/trained-model-autoscaling.md).
* The maximum configurable node count is 32, which means `Maximum size per zone` in autoscaling is limited to multiplying the maximum RAM size of the instance configuration in use by 32. For example, for the instance configuration [`aws.es.datahot.c6gd`](cloud://reference/cloud-hosted/aws-default.md), the maximum RAM size is 60GB. Therefore, the `Maximum size per zone` in autoscaling is limited to `60GB x 32 = 1.875TB` (displayed as `1.88TB` in the {{ecloud}} console UI). Review [Restrictions and known problems > Node Count and Size](../deploy/elastic-cloud/restrictions-known-problems.md#ec-node-count-size) for more guidance. 


### {{ece}} specific limitations

In {{ece}}, the following additional limitations apply:

* In the event that an override is set for the instance size or disk quota multiplier for an instance by means of the [Instance Overrides API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-all-instances-settings-overrides), autoscaling will be effectively disabled. It’s recommended to avoid adjusting the instance size or disk quota multiplier for an instance that uses autoscaling, since the setting prevents autoscaling.

## Enable or disable autoscaling[ec-autoscaling-enable]

To enable or disable autoscaling on a deployment:

:::{include} ../_snippets/find-manage-deployment-ech-and-ece.md
:::

4. Under the deployment's name in the navigation menu, select **Edit**.
5. Select desired autoscaling configuration for this deployment using **Enable Autoscaling for:** dropdown menu.
6. Select **Confirm** to have the autoscaling change and any other settings take effect. All plan changes are shown on the Deployment **Activity** page.

When autoscaling has been enabled, the autoscaled nodes resize according to the [autoscaling settings](#ec-autoscaling-update). Current sizes are shown on the deployment overview page.

When autoscaling has been disabled, you need to adjust the size of data tiers and machine learning nodes manually.

## Update your autoscaling settings[ec-autoscaling-update]

Each autoscaling setting is configured with a default value. You can adjust these if necessary, as follows:

:::{include} ../_snippets/find-manage-deployment-ech-and-ece.md
:::

3. Under the deployment's name in the navigation menu, select **Edit**.
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
On {{ece}}, system-owned deployment templates include the default values for all deployment autoscaling settings.
::::

## Autoscaling example [ec-autoscaling-example]

To help you better understand the available autoscaling settings, this example describes a typical autoscaling workflow on sample {{ece}} or {{ech}} deployment.

1. Enable autoscaling:

    * On an **existing deployment**, open the deployment **Edit** page to find the option to turn on autoscaling.
    * When you create a new deployment, you can find the autoscaling option under **Advanced settings**.

        Once you confirm your changes or create a new deployment, autoscaling is activated with system default settings that you can adjust as needed (though for most use cases the default settings will likely suffice).

2. View and adjust autoscaling settings on data tiers:

    1. Open the **Edit** page for your deployment to get the current and maximum size per zone of each {{es}} data tier. In this example, the hot data and content tier has the following settings:

        | Current size per zone | Maximum size per zone |
        | --- | --- |
        | 45GB storage | 1.41TB storage |
        | 1GB RAM | 32GB RAM |
        | Up to 2.5 vCPU | 5 vCPU |

        The fault tolerance for the data tier is set to 2 availability zones.

        :::{image} /deploy-manage/images/cloud-enterprise-ec-ce-autoscaling-data-summary2.png
        :alt: A screenshot showing sizing information for the autoscaled data tier
        :::

    2. Use the dropdown boxes to adjust the current and/or the maximum size of the data tier. Capacity will be added to the hot content and data tier when required, based on its past and present storage usage, until it reaches the maximum size per zone. Any scaling events are applied simultaneously across availability zones. In this example, the tier has plenty of room to scale relative to its current size, and it will not scale above the maximum size setting. There is no minimum size setting since downward scaling is currently not supported on data tiers.

3. View and adjust autoscaling settings on a machine learning instance:

    1. From the deployment **Edit** page you can check the minimum and maximum size of your deployment’s machine learning instances. In this example, the machine learning instance has the following settings:

        | Minimum size per zone | Maximum size per zone |
        | --- | --- |
        | 1GB RAM | 64GB RAM |
        | 0.5 vCPU up to 8 vCPU | 32 vCPU |

        The fault tolerance for the machine learning instance is set to 1 availability zone.

        :::{image} /deploy-manage/images/cloud-enterprise-ec-ce-autoscaling-ml-summary2.png
        :alt: A screenshot showing sizing information for the autoscaled machine learning node
        :::

    2. Use the dropdown boxes to adjust the minimum and/or the maximum size of the data tier. Capacity will be added to or removed from the machine learning instances as needed. The need for a scaling event is determined by the expected memory and vCPU requirements for the currently configured machine learning job. Any scaling events are applied simultaneously across availability zones. Note that unlike data tiers, machine learning nodes do not have a **Current size per zone** setting. That setting is not needed since machine learning nodes support both upward and downward scaling.

4. Over time, the volume of data and the size of any machine learning jobs in your deployment are likely to grow. Let’s assume that to meet storage requirements your hot data tier has scaled up to its maximum allowed size of 64GB RAM and 32 vCPU. At this point, a notification appears on the deployment overview page indicating that the tier has scaled to capacity.
5. If you expect a continued increase in either storage, memory, or vCPU requirements, you can use the **Maximum size per zone** dropdown box to adjust the maximum capacity settings for your data tiers and machine learning instances, as appropriate. And, you can always re-adjust these levels downward if the requirements change.

As you can see, autoscaling greatly reduces the manual work involved to manage a deployment. The deployment capacity adjusts automatically as demands change, within the boundaries that you define. Check our main [Deployment autoscaling](../autoscaling.md) page for more information.

## Autoscaling through the API [ec-autoscaling-api-example]

This example demonstrates how to use the {{ecloud}} RESTful API to create a deployment with autoscaling enabled.

The example deployment has a hot data and content tier, warm data tier, cold data tier, and a machine learning node, all of which will scale within the defined parameters. To learn about the autoscaling settings, check [Deployment autoscaling](../autoscaling.md) and [Autoscaling example](#ec-autoscaling-example).

To learn more about the {{ece}} API, see the [RESTful API](cloud://reference/cloud-enterprise/restful-api.md) documentation. For details on the {{ech}} API, check [RESTful API](cloud://reference/cloud-hosted/ec-api-restful.md).

### Requirements [ec_requirements]

Note the following requirements when you run this API request:

* All {{es}} components must be included in the request, even if they are not enabled (that is, if they have a zero size). All components are included in this example.
* The request requires a format that supports data tiers. Specifically, all {{es}} components must contain the following properties:

    * `id`
    * `node_attributes`
    * `node_roles`

* The `size`, `autoscaling_min`, and `autoscaling_max` properties must be specified according to the following rules. This is because:

    * On data tiers only upward scaling is currently supported.
    * On machine learning nodes both upward and downward scaling is supported.
    * On all other components autoscaling is not currently supported.
* On {{ece}}, autoscaling is supported for custom deployment templates on version 2.12 and above. To learn more, refer to [Updating custom templates to support `node_roles` and autoscaling](../deploy/cloud-enterprise/ce-add-support-for-node-roles-autoscaling.md).

$$$ece-autoscaling-api-example-requirements-table$$$

|  | `size` | `autoscaling_min` | `autoscaling_max` |
| --- | --- | --- | --- |
| data tier | ✓ | ✕ | ✓ |
| machine learning node | ✕ | ✓ | ✓ |
| coordinating and master nodes | ✓ | ✕ | ✕ |
| {{kib}} | ✓ | ✕ | ✕ |
| APM | ✓ | ✕ | ✕ |

* ✓ = Include the property.
* ✕ = Do not include the property.

* These rules match the behavior of the {{ech}} and {{ece}} user console.

* The `elasticsearch` object must contain the property `"autoscaling_enabled": true`.

### API request example [ec_api_request_example]

::::{note}
Although autoscaling can scale some tiers by CPU, the primary measurement of tier size is memory. Limits on tier size are in terms of memory.
::::

Run this example API request to create a deployment with autoscaling:

::::{tab-set}

:::{tab-item} {{ece}}

```sh
curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments -H 'content-type: application/json' -d '
{
 "name": "my-first-autoscaling-deployment",
 "resources": {
   "elasticsearch": [
     {
       "ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "autoscaling_enabled": true,
         "cluster_topology": [
           {
             "id": "hot_content",
             "node_roles": [
               "master",
               "ingest",
               "remote_cluster_client",
               "data_hot",
               "transform",
               "data_content"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "hot"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.default",
             "size": {
               "value": 4096,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "warm",
             "node_roles": [
               "data_warm",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "warm"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.highstorage",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "cold",
             "node_roles": [
               "data_cold",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "cold"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.highstorage",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "coordinating",
             "node_roles": [
               "ingest",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "instance_configuration_id": "coordinating",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "master",
             "node_roles": [
               "master"
             ],
             "zone_count": 1,
             "instance_configuration_id": "master",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "ml",
             "node_roles": [
               "ml",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "instance_configuration_id": "ml",
             "autoscaling_min": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           }
         ],
         "elasticsearch": {
           "version": "8.13.1"
         },
         "deployment_template": {
           "id": "default"
         }
       },
       "settings": {
         "dedicated_masters_threshold": 6
       }
     }
   ],
   "kibana": [
     {
       "ref_id": "main-kibana",
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "zone_count": 1,
         "cluster_topology": [
           {
             "instance_configuration_id": "kibana",
             "size": {
               "value": 1024,
               "resource": "memory"
             },
             "zone_count": 1
           }
         ],
         "kibana": {
           "version": "8.13.1"
         }
       }
     }
   ],
   "apm": [
     {
       "ref_id": "main-apm",
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "apm",
             "size": {
               "value": 512,
               "resource": "memory"
             },
             "zone_count": 1
           }
         ],
         "apm": {
           "version": "8.13.1"
         }
       }
     }
   ],
   "enterprise_search": []
 }
}
'
```

:::

:::{tab-item} {{ech}}

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments" \
-d '
{
 "name": "my-first-autoscaling-deployment",
 "resources": {
   "elasticsearch": [
     {
       "ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "autoscaling_enabled": true,
         "cluster_topology": [
           {
             "id": "hot_content",
             "node_roles": [
               "remote_cluster_client",
               "data_hot",
               "transform",
               "data_content",
               "master",
               "ingest"
             ],
             "zone_count": 2,
             "elasticsearch": {
               "node_attributes": {
                 "data": "hot"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "aws.data.highio.i3",
             "size": {
               "resource": "memory",
               "value": 8192
             },
             "autoscaling_max": {
               "value": 118784,
               "resource": "memory"
             }
           },
           {
             "id": "warm",
             "node_roles": [
               "data_warm",
               "remote_cluster_client"
             ],
             "zone_count": 2,
             "elasticsearch": {
               "node_attributes": {
                 "data": "warm"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "aws.data.highstorage.d3",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 118784,
               "resource": "memory"
             }
           },
           {
             "id": "cold",
             "node_roles": [
               "data_cold",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "cold"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "aws.data.highstorage.d3",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 59392,
               "resource": "memory"
             }
           },
           {
             "id": "coordinating",
             "zone_count": 2,
             "node_roles": [
               "ingest",
               "remote_cluster_client"
             ],
             "instance_configuration_id": "aws.coordinating.m5d",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "master",
             "node_roles": [
               "master"
             ],
             "zone_count": 3,
             "instance_configuration_id": "aws.master.r5d",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "ml",
             "node_roles": [
               "ml",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "instance_configuration_id": "aws.ml.m5d",
             "autoscaling_min": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 61440,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           }
         ],
         "elasticsearch": {
           "version": "7.11.0"
         },
         "deployment_template": {
           "id": "aws-io-optimized-v2"
         }
       },
       "settings": {
         "dedicated_masters_threshold": 6
       }
     }
   ],
   "kibana": [
     {
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "aws.kibana.r5d",
             "zone_count": 1,
             "size": {
               "resource": "memory",
               "value": 1024
             }
           }
         ],
         "kibana": {
           "version": "7.11.0"
         }
       },
       "ref_id": "main-kibana"
     }
   ],
   "apm": [
     {
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "aws.apm.r5d",
             "zone_count": 1,
             "size": {
               "resource": "memory",
               "value": 512
             }
           }
         ],
         "apm": {
           "version": "7.11.0"
         }
       },
       "ref_id": "main-apm"
     }
   ],
   "enterprise_search": []
 }
}
'
```

:::

::::
