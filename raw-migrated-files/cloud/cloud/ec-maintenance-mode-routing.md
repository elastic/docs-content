# Request routing [ec-maintenance-mode-routing]

The {{ecloud}} proxy service routes traffic from external sources to the deployment, between deployments, and between products within a deployment. For example, it routes API requests from your local machine to your deployment, CCR and CCS requests between your deployments, and communications between {{kib}} and {{es}}. It does not direct the TCP traffic between {{es}} nodes, nor does it manage requests starting within {{es}} outwards to external sources such as to snapshot repositories.

The {{ecloud}} proxy routes HTTP requests to its deployment’s individual product instances through the product’s endpoint. By default, instances are enabled to route HTTP traffic and will report no special messaging.

It might be helpful to temporarily block upstream requests in order to protect some or all instances or products within your deployment. For example, you might stop request routing in the following cases:

* If another team within your company starts streaming new data into your production {{integrations-server}} without previous load testing, both it and {{es}} might experience performance issues. You might consider stopping routing requests on all {{integrations-server}} instances in order to protect your downstream {{es}} instance.
* If {{es}} is being overwhelmed by upstream requests, it might experience increased response times or even become unresponsive. This might impact your ability to resize components in your deployment and increase the duration of pending plans or increase the chance of plan changes failing. Because every {{es}} node is an [implicit coordinating node](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md), you should stop routing requests across all {{es}} nodes to completely block upstream traffic.


## Considerations [ec_considerations]

* {{ecloud}} will automatically set and remove routing blocks during  plan changes. Elastic recommends avoiding manually overriding these settings for a deployment while its plans are pending.
* The [{{es}} API console](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-console.md) bypasses {{ecloud}} proxy routing blocks against {{es}} to enable administrative tasks while plan changes are pending. You should generally default traffic to the {{es}} endpoint. However, if you enable **Stop routing requests** across all {{es}} nodes, you need to use this UI to administer your cluster.
* While {{es}} has **Stop routing requests** set across all nodes, other products with the deployment may become unhealthy. This is because {{es}} is a prerequisite for those other products, such as {{kib}}. In {{kib}}, this results in a [**Kibana server is not ready yet**](/troubleshoot/kibana/error-server-not-ready.md) message.
* Enabling **Stop routing requests** does not affect your [billing](../../../deploy-manage/cloud-organization/billing.md). If needed, you can stop charges for a deployment by [deleting the deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md).


## Stop routing requests [ec_stop_routing_requests]

To block HTTP requests for an instance, select **Stop routing requests** under from instance’s menu.

The instance will then report **Not routing requests**. It will complete existing requested traffic, but not be sent new requests.


## Restart routing requests [ec_restart_routing_requests]

To unblock HTTP requests for an instance, select **Start routing requests** under from instance’s menu.
