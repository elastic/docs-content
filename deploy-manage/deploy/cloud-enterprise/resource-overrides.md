---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-resource-overrides.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Resource overrides [ece-resource-overrides]

{{ecloud}} allocators assign resources to {{es}} instances based on RAM, where RAM is proportional to CPU and disk resources. As needed, you can temporarily override the allocated resources to stabilize the deployment. To do this, use the contextual menu available on each instance in the deployment UI.

Overrides are intended to be temporary and may be lost after making configuration changes to the deployment. You should reset overrides as soon as possible, or make them permanent by [changing your configuration](./configure-deployment.md).

The RAM to CPU proportions can’t be overridden per instance.

## Override disk quota

You can override the RAM to disk storage capacity for an instance under **Override disk quota** from the instance’s drop-down menu. This can be helpful when troubleshooting [watermark errors](../../../troubleshoot/elasticsearch/fix-watermark-errors.md) that result in a red [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) status, which blocks configuration changes. A **Reset system default** message appears while disk quota overrides are set.

::::{note}
Overriding the disk storage capacity does not restart the {{es}} node.
::::

## Override RAM, CPU and disk

Alternatively, you can override all resource allocations by selecting **Override instance size** from the instance’s drop-down menu. This overrides the alloted RAM, maintaining a proportional CPU and disk size. This can be helpful if the {{es}} cluster is overwhelmed by requests. You should [resize the deployment](resize-deployment.md) when the volume of requests stabilizes.

::::{note}
Overriding the instance size restarts the {{es}} node.
::::

When an instance within a deployment has resource overrides, it displays a warning banner reading **Elastic added temporary capacity to stabilize the deployment**. [Configuration changes](working-with-deployments.md) can still be safely submitted.

## Disabling CPU quotas at deployment level [cpu-hard-limit]

In addition to overriding resources for individual instances, you can also completely disable CPU limits for your deployment from the **Operations** page of each deployment.

::::{note}
When running ECE on Podman, CPU quotas for existing instances cannot be removed or updated. As a result, disabling the CPU hard limit has no effect on Podman-based allocators.
::::

::::{important}
Disabling the CPU hard limit for an entire deployment is an advanced action and should be approached with caution. This setting removes CPU quotas from the containers, which means some instances could consume excessive CPU resources and degrade the performance of other instances running on the same allocators.

We strongly recommend making this change only under the guidance of Elastic Support, and only as a temporary measure or for troubleshooting purposes.
::::

To disable CPU limits of your deployment instances, choose one of the following methods:

* Open the **Operations** page of the deployment UI, and select **Turn off** in the **CPU hard limit** section.

* Use the [advanced editor](./advanced-cluster-configuration.md), and in the **{{es}} cluster data** section, look for the following setting:

  ```yaml
        "resources": {
          "cpu": {
            "hard_limit": false
          }
        }
  ```

  Set `hard_limit` to `false` to disable CPU limits, or to `true` to enforce strict CPU limits (default behavior).

This change doesn’t require a restart of the deployment.