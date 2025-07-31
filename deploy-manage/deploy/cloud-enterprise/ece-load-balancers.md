---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-load-balancers.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Load balancers [ece-load-balancers]

[{{ece}} architecture](./ece-architecture.md) is designed to be used in conjunction with at least one load balancer. A load balancer is not included with {{ece}}, so you need to provide one yourself and place it in front of the {{ece}} proxies.

Use the following recommendations when configuring your load balancer:

* **High availability**: The exact number of load balancers depends on the utilization rate for your clusters. In a highly available installation, use at least two load balancers for each availability zone in your installation.
* **Inbound ports**: Load balancers require that inbound traffic is open on the ports used by {{es}}, {{kib}}, and the transport client.
* **X-found-cluster**: ECE proxy uses the header `X-found-cluster` to know which cluster’s UUID (Universally Unique Identifier) the traffic needs to be routed to. If the load balancer rewrites a URL, make sure the HTTP header `X-Found-Cluster` gets added. For example: `X-found-cluster: d59109b8d542c5c4845679e597810796`.
* **X-Forwarded-For**: Configure load balancers to strip inbound `X-Forwarded-For` headers and to replace them with the client source IP as seen by the load balancer. This is required to prevent clients from spoofing their IP addresses. {{ece}} uses `X-Forwarded-For` for logging client IP addresses and, if you have implemented IP filtering, for traffic management.
* **HTTP**: Use *HTTP mode* for ports 9200/9243 (HTTP traffic to clusters) and also for ports 12400/12443 (adminconsole traffic).
* **TCP**: Use *TCP mode* for ports 9300/9343 (transport client traffic to clusters) and the load balancer should enable the proxy protocol support.
* **TCP**: Use *TCP mode* for port 9400 for TLS authenticated passthrough between clusters for cross-cluster search (CCS) and replication (CCR), if used. The load balancer should **not** enable the proxy protocol support.
* **TCP**: Use *HTTP mode* for port 9443 for API key authenticated traffic between clusters for cross-cluster search (CCS) and replication (CCR), if used. Make sure that all load balancers or proxies sending this traffic to deployments hosted on {{ece}} are sending HTTP/1.1 traffic.
* **Deployment traffic and Admin traffic**: Create separate load balancers for Deployment traffic ({{es}} and {{kib}} traffic) and Admin traffic (Cloud UI Console and Admin API). This separation allows you to migrate to a large installation topology without reconfiguring or creating an additional load balancer.
* **Traffic across proxies**: Balance traffic evenly across all proxies. Proxies are constantly updated with the internal routing information on how to direct requests to clusters on allocators that are hosting their nodes across zones. Proxies prefer cluster nodes in their local zone and route requests primarily to nodes in their own zone.
* **Network**: Use network that is fast enough from a latency and throughput perspective to be considered local for the {{es}} clustering requirement. There shouldn’t be a major advantage in "preferring local" from a load balancer perspective (rather than a proxy perspective), it might even lead to potential hot spotting on specific proxies, so it should be avoided.
* **TCP Timeout**: Use the default (or required) TCP timeout value from the cloud provider and do not to set a timeout for the load balancer.


## Proxy health check for ECE 2.0 and earlier [ece_proxy_health_check_for_ece_2_0_and_earlier]

You can use `/__elb_health__` on your proxy hosts and check for a 200 response that indicates healthy.

```
http://<proxy-address>:9200>/__elb_health__
```

or

```
https://<proxy-address>:9243>/__elb_health__
```

This returns a healthy response as:

```
{"ok":true,"status":200}
```


## Proxy health check for ECE 2.1 and later [ece_proxy_health_check_for_ece_2_1_and_later]

For {{ece}} 2.1 and later, the health check endpoint has changed. You can use `/_health` on proxy hosts with a result of either a 200 OK to indicate healthy or a 502 Bad Gateway response for unhealthy. A healthy response also means that internal routing tables in the proxy are valid and initialized, but not necessarily up-to-date.

```
http://<PROXY_ADDRESS>:9200/_health
```

or

```
https://<PROXY_ADDRESS>:9243/_health
```

This returns a healthy response as:

```
{"ok":true,"status":200}
```
