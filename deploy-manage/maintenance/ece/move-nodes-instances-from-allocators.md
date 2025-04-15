---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-move-nodes.html
applies_to:
  deployment:
     ece:
---

# Move nodes or instances from allocators [ece-move-nodes]

You might need to move {{es}} nodes, {{kib}} instances, and other components of the {{stack}} between allocators from time to time for a number of reasons:

* To prepare for removing the allocator role from the first host on which you installed {{ece}}.
* To avoid downtime during maintenance: You can create a new allocator, move all deployments from an existing allocator to the new one, and then deal with the allocator that needs maintenance.
* To make room on an allocator: You can move some smaller deployments to another allocator if you need additional room for a larger one on an allocator.
* To move deployments after a failure: When host failures happen, you can move all deployments from the affected allocator to a healthy allocator quickly before spending any time on fixing the failure.

::::{tip}
When you move all nodes from an existing allocator to the new one, ECE migrates the data to new nodes. The migration can take some time, especially when deployments contain large amounts of data and have a heavy workload. Is your deployment under a heavy workload? You might need to [stop routing requests](deployments-maintenance.md) first.
::::

## Before you begin [ece_before_you_begin_9]

Before you move the nodes and instances that are part of a deployment, you need to make sure that you have sufficient capacity on another allocator. For example: If you have a deployment with a single 32 GB {{es}} node and a 4 GB {{kib}} instance, the allocator that you are moving the deployment to needs to have at least 36 GB of capacity. Note that moving nodes does not actually move the same node onto a different allocator. Under the covers, {{ece}} creates a new node and then migrates the data for you.

{{ece}} will adhere to the high availability configuration when moving nodes, so make sure you have the additional capacity available in the relevant availability zone.  For example: If you selected to deploy your cluster accross 3 availability zones, nodes can only move to an allocator in the same availability zone as the failed allocator. This is meant to ensure that the cluster can tolerate the failure of 2 availability zones.

If you followed our recommendation and [tagged your allocators](../../deploy/cloud-enterprise/ece-configuring-ece-tag-allocators.md) to indicate what allocators you want components of the {{stack}} to run on, the spare capacity you plan to use must be available on an allocator with the same tags. If you did not tag your allocators and edit the default instance configurations, ECE will move nodes and instances to wherever there is space.

When you move all nodes from an existing allocator to the new one, ECE migrates the data to new nodes. The migration can take some time, especially when clusters contain large amounts of data and have a heavy workload. Is your cluster under a heavy workload? You might need to [stop routing requests](deployments-maintenance.md) first.

## Moving nodes from allocators [move-nodes-from-allocators]

To move nodes from one allocator to another one:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Allocators**.
3. Review the list of all allocators that are part of this installation and look for allocators that are unhealthy or find the allocator that you want to free up.
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

4. Recommended: [Put the allocator into maintenance mode](enable-maintenance-mode.md) before continuing.
5. Select the name of an unhealthy allocator and then choose **Move Nodes** from the menu.
6. Select the nodes you want, then choose **Move Nodes**.
7. To customize how you would like to move the nodes, select **Customize settings**, choose your options, then select **Move nodes**.
   ::::{important}
   Review **Customize Settings** before proceeding to move nodes.
   ::::

   Gracefully move data
   :   (Default) Gracefully move the data from the instances we’re about to remove from the cluster before stopping them. Never disable this setting at the same time as enabling `override_failsafe` on a non-Highly Available cluster since it can result in data loss.

   Skip snapshot
   :   If an allocator has failed or is otherwise unhealthy, select this option to move the nodes but disable the snapshot attempt. As this can perform potentially destructive actions on the deployment, do not use this option on a healthy allocator unless you are an advanced user.

   Restore snapshot to latest success
   :   Restore the cluster to the last successful snapshot. Recommended for single-node clusters hosted on unhealthy allocators. Any data indexed after the last snapshot was taken is lost.

   Extended maintenance
   :   Keep new instances in maintenance mode until a snapshot has been restored. If not enabled, new instances remain in maintenance mode only until they can join a cluster.

   Set target allocators
   :   Request that instances be moved to the specified allocators. If no allocators are specified, or those specified are unsuitable for the instances being moved, then any suitable healthy allocator can be used.

   Reallocate
   :   Create new containers for all nodes in the cluster.

   Set Timeout
   :   On by default.
   ::::{tip}
   If you did not enable maintenance mode, set a target allocator under the advanced options when moving nodes to make sure the nodes do not end up on the same allocator again. By default, moving a node moves it to any allocator that has enough capacity.
   ::::

8. Repeat **step 6** for each of the node types until no nodes remain on the allocator.
9. Optionally, once the nodes have been moved, **Delete Allocator**.
