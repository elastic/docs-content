---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode-routing.html
  - https://www.elastic.co/guide/en/cloud/current/ec-maintenance-mode-routing.html
applies_to:
  deployment:
     ece:
     ess:
---

# Start and stop routing requests [maintenance-mode-routing]

The cloud proxy service routes traffic from external sources to the deployment, between deployments, and between products within a deployment. For example, it routes API requests from your local machine to your deployment, CCR and CCS requests between your deployments, and communications between {{kib}} and {{es}}. It does not direct the TCP traffic between {{es}} nodes, nor does it manage requests starting within {{es}} outwards to external sources such as to snapshot repositories.

The cloud proxy routes HTTP requests to its deployment’s individual product instances through the product’s endpoint. By default, instances are enabled to route HTTP traffic and will report no special messaging.

It might be helpful to temporarily block upstream requests in order to protect some or all instances or products within your deployment. For example, you might stop request routing in the following cases:

* If another team within your company starts streaming new data into your production {{integrations-server}} without previous load testing, both it and {{es}} might experience performance issues. You might consider stopping routing requests on all {{integrations-server}} instances in order to protect your downstream {{es}} instance.
* If {{es}} is being overwhelmed by upstream requests, it might experience increased response times or even become unresponsive. This might impact your ability to resize components in your deployment and increase the duration of pending plans or increase the chance of plan changes failing. Because every {{es}} node is an [implicit coordinating node](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#node-roles-list), you should stop routing requests across all {{es}} nodes to completely block upstream traffic.

## Considerations [request-routing-considerations]

* ECE and ECH will automatically set and remove routing blocks during plan changes. Elastic recommends avoiding manually overriding these settings for a deployment while its plans are pending.
* The [{{es}} API console](/explore-analyze/query-filter/tools/console.md) bypasses cloud proxy routing blocks against {{es}} to enable administrative tasks while plan changes are pending. You should generally default traffic to the {{es}} endpoint. However, if you enable **Stop routing requests** across all {{es}} nodes, you need to use this UI to administer your cluster.
* While {{es}} has **Stop routing requests** set across all nodes, other products with the deployment may become unhealthy. This is because {{es}} is a prerequisite for those other products, such as {{kib}}. In {{kib}}, this results in a [**Kibana server is not ready yet**](/troubleshoot/kibana/error-server-not-ready.md) message.
* In {{ech}}, enabling **Stop routing requests** does not affect your [billing](/deploy-manage/cloud-organization/billing.md). If needed, you can stop charges for a deployment by [deleting the deployment](/deploy-manage/uninstall/delete-a-cloud-deployment.md).

## Stop routing requests [stop-routing-requests]

To block HTTP requests for an instance, select **Stop routing requests** under from instance’s menu.

The instance will then report **Not routing requests**. It will complete existing requested traffic, but not be sent new requests.

## Restart routing requests [restart-routing-requests]

To unblock HTTP requests for an instance, select **Start routing requests** under from instance’s menu.

## Toggle routing to all instances on an allocator
```{applies_to}
deployment:
  ece:
```
In {{ece}}, in addition to stopping routing requests for particular instances, you can also massively disable routing to all instances on a specified allocator with the [allocator-toggle-routing-requests.sh](https://download.elastic.co/cloud/allocator-toggle-routing-requests.sh) script. The script runs with the following parameters in the form environment variables:

* `API_URL` Url of the administration API.
* `AUTH_HEADER` Curl format string representing the authentication header.
* `ALLOCATOR_ID` Action target allocator id.
* `ENABLE_TRAFFIC` Wether traffic to the selected allocator instances should be enabled (`true`) or disabled (`false`).

This is an example of script execution to disable routing on all instances running on a given allocator:

```bash
AUTH_HEADER="Authorization: ApiKey $(cat ~/api.key)" API_URL="https://adminconsole:12443" ALLOCATOR_ID="192.168.44.10" ENABLE_TRAFFIC=false ./allocator-toggle-routing-requests.sh
```

The same script can be used to enable traffic again:

```bash
AUTH_HEADER="Authorization: ApiKey $(cat ~/api.key)" API_URL="https://adminconsole:12443" ALLOCATOR_ID="192.168.44.10" ENABLE_TRAFFIC=true ./allocator-toggle-routing-requests.sh
```
