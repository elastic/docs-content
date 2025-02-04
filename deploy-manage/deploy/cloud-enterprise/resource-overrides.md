---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-resource-overrides.html
---

# Resource overrides [ece-resource-overrides]

{{ecloud}} allocators allot {{es}} instance sizes based on RAM, where RAM is proportional to CPU and disk resources. As needed, you can temporarily override the allocated resources to stabilize the deployment. You should reset overrides as soon as possible, or make your the override permanent by [changing your configuration](working-with-deployments.md).

The RAM to CPU proportions can’t be overridden per instance.

You can override the RAM to disk storage capacity for an instance under **Override disk quota** from the instance’s drop-down menu. This can be helpful when troubleshooting [watermark errors](../../../troubleshoot/elasticsearch/fix-watermark-errors.md) that result in a red [cluster health](https://www.elastic.co/guide/en/elasticsearch/reference/current/_cluster_health.html) status, which blocks configuration changes. A **Reset system default** message appears while disk quota overrides are set. Overriding the disk storage capacity does not restart the {{es}} node.

Alternatively, you can override all resource allocations by selecting **Override instance size** from the instance’s drop-down menu. This overrides the alloted RAM, maintaining a proportional CPU and disk size. This can be helpful if the {{es}} cluster is overwhelmed by requests. You should [resize the deployment](resize-deployment.md) when the volume of requests stabilizes. Overriding the instance size restarts the {{es}} node.

When an instance within a deployment has resource overrides, it displays a warning banner reading **Elastic added temporary capacity to stabilize the deployment**. [Configuration changes](working-with-deployments.md) can still be safely submitted.
