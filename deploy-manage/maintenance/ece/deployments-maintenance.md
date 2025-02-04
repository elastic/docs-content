---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode-deployments.html
---

# Deployments maintenance [ece-maintenance-mode-deployments]

In some circumstances, you might need to temporarily restrict access to a node so you can perform corrective actions that might otherwise be difficult to complete. For example, if your cluster is being overwhelmed by requests because it is undersized for its workload, its nodes might not respond to efforts to resize.

These actions act as a maintenance mode for cluster node. Performing these actions can stop the cluster from becoming completely unresponsive so that you can resolve operational issues much more effectively.

* [**Stop routing to the instance**](start-stop-routing-requests.md): Block requests from being routed to the cluster node. This is a less invasive action than pausing the cluster.
* [**Pause an instance**](pause-instance.md): Suspend the node immediately by stopping the container that the node runs on without completing existing requests. This is a more aggressive action to regain control of an unresponsive node.

As an alternative, to quickly add capacity to a deployment if it is unhealthy or at capacity, you can also [override the resource limit for a deployment](../../deploy/cloud-enterprise/resource-overrides.md).



