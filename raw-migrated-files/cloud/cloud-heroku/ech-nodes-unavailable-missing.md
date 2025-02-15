# Some nodes are unavailable and are displayed as missing [ech-nodes-unavailable-missing]

**Health check**

* Use the [Metrics inventory](https://www.elastic.co/guide/en/observability/current/monitor-infrastructure-and-hosts.html) to identify unavailable or unhealthy nodes. If the number of minimum master nodes is down, {{es}} is not available.

**Possible causes**

* Hardware issue.
* Routing has stopped because of a previous ES configuration failure.
* Disk/memory/CPU are saturated.
* The network is saturated or disconnected.
* Nodes are unable to join.

**Resolutions**

* Hardware issue: Any unhealthy hardware detected by the platform is automatically vacated within the hour. If this doesn’t happen, contact support.
* Routing stopped: A failed {{es}} configuration might stop the nodes routing. Restart the routing manually to bring the node back to health.
* Disk/memory/CPU saturated:

    * [Delete unused data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
    * Increase disk size.
    * [Enable autoscaling](../../../deploy-manage/autoscaling.md).
    * Configuration of ILM policies.
    * [Manage data tiers](../../../manage-data/lifecycle/data-tiers.md).

* Network saturated or disconnected: Contact support.
* Nodes unable to join: Fix the {{es}} configuration.
* Nodes unable to join: Contact support.

