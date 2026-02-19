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
* **X-found-cluster**: The ECE proxy uses the header `X-found-cluster` to route traffic to the correct cluster via the cluster UUID (Universally Unique Identifier). If the load balancer rewrites a URL, make sure the HTTP header `X-Found-Cluster` gets added. For example: `X-found-cluster: d59109b8d542c5c4845679e597810796`.
* **Deployment traffic and Admin traffic**: Create separate load balancers for deployment traffic ({{es}} and {{kib}} traffic) and admin traffic (Cloud UI Console and Admin API). This separation allows you to migrate to a large installation topology without reconfiguring or creating an additional load balancer.
* **Traffic across proxies**: Balance traffic evenly across all proxies. Proxies are constantly updated with internal routing information on how to direct requests to clusters on allocators hosting their nodes across zones. Proxies prefer cluster nodes in their local zone and route requests primarily to nodes in their own zone.
* **Network**: Use a network that is fast enough from a latency and throughput perspective to be considered local for the {{es}} clustering requirement. There shouldn't be a major advantage in "preferring local" from a load balancer perspective (rather than a proxy perspective), and it might lead to potential hot spotting on specific proxies, so it should be avoided.
* **TCP timeout**: Use the default (or required) TCP timeout value from the cloud provider. Do not set a custom timeout on the load balancer.

## Port and mode configuration [ece-load-balancer-ports]

The following table describes the supported load balancer modes for each port range. TLS termination occurs at the ECE proxy for all ports.

| Ports | Traffic type | Supported modes | Client IP mechanism | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 9200/9243 | {{es}} HTTP | HTTP (L7) or TCP (L4) | `X-Forwarded-For` (L7) or Proxy Protocol v2 (L4) | |
| 9300/9343 | Transport client | TCP (L4) | Proxy Protocol v2 | Enable proxy protocol on the LB |
| 9400 | CCS/CCR (TLS auth) | TCP (L4) | — | Do **not** enable proxy protocol |
| 9443 | CCS/CCR (API key auth) | HTTP (L7) | `X-Forwarded-For` | Must send HTTP/1.1 traffic |
| 12400/12443 | Admin console | HTTP (L7) | `X-Forwarded-For` | |

## Client IP preservation [ece-client-ip-preservation]

The ECE proxy must be able to determine the real client IP address for [IP filtering](/deploy-manage/security/ip-filtering-ece.md) and [request logging](/deploy-manage/monitor/orchestrators/ece-proxy-log-fields.md). The mechanism depends on the load balancer mode:

* **`X-Forwarded-For` header** (HTTP/L7 mode): Configure the load balancer to strip inbound `X-Forwarded-For` headers and replace them with the client source IP. This prevents clients from spoofing their IP addresses.
* **Proxy Protocol v2** (TCP/L4 mode): The load balancer prepends client connection metadata that the ECE proxy reads directly. Enable Proxy Protocol v2 on both the load balancer and the ECE proxy configuration.
* **Direct source IP preservation**: If the load balancer forwards connections transparently without modifying the source IP, no additional configuration is needed.

If you use TCP mode for ports 9200/9243, make sure one of these mechanisms is in place. Without real client IP information, [IP filtering](/deploy-manage/security/ip-filtering-ece.md) cannot function correctly and [proxy logs](/deploy-manage/monitor/orchestrators/ece-proxy-log-fields.md) will only show the load balancer's IP address.

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
