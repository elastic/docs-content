---
navigation_title: Proxy Protocol
applies_to:
  deployment:
    ece: ga 4.2
products:
  - id: cloud-enterprise
---

# Configure Proxy Protocol v2 in the ECE proxies [ece-configure-proxy-protocol]

ECE needs the real client address to enforce [IP filtering](/deploy-manage/security/ip-filtering-ece.md) rules and to report client addresses in the [proxy request logs](/deploy-manage/monitor/orchestrators/ece-proxy-log-fields.md). When a load balancer forwards deployment traffic, the ECE proxies receive the load balancer address as the source of every connection unless one of the mechanisms described in [Client IP preservation](./ece-load-balancers.md#ece-client-ip-preservation) is in place.

The two most common combinations are:

* **HTTP (L7) mode**: the load balancer sets the `X-Forwarded-For` header with the client source IP.
* **TCP (L4) mode**: the load balancer sends [Proxy Protocol v2](https://www.haproxy.org/download/2.8/doc/proxy-protocol.txt) metadata, and the ECE proxies must be configured to parse it. This is also the only mechanism that can preserve an [IPv6 client address](./ece-ipv6-support.md).

This page covers the TCP (L4) path: how to enable Proxy Protocol v2 parsing in the ECE proxies for {{es}} HTTP traffic, on ports `9200` and `9243`. This is the only Proxy Protocol configuration that ECE exposes. For the other ports, the client IP mechanism is fixed and only configured on the load balancer side, as described in [Port and mode configuration](./ece-load-balancers.md#ece-load-balancer-ports).

:::{note}
In ECE versions earlier than 4.2, Proxy Protocol v2 parsing on the {{es}} HTTP ports is disabled and the installation flags described on this page are not available. If you need the real client address on an earlier version, consider the following options:

* Use [direct source IP preservation](./ece-load-balancers.md#ece-client-ip-preservation) instead, if your load balancer can forward connections without replacing the client source address.
* [Upgrade to ECE 4.2 or later](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md), which is the recommended way to use Proxy Protocol v2.
* Enable Proxy Protocol v2 on your current version by patching the proxy container set directly. Follow [our KB article](https://ela.st/ece-configure-ppv2-via-containersets-api) and contact [Elastic Support](/troubleshoot/index.md#contact-us) for assistance with the procedure.
:::

## Enable Proxy Protocol v2 [ece-proxy-protocol-enable]

Proxy Protocol v2 for deployment HTTP traffic is configured through the ECE installation script, using the following flags on every host that holds the [proxy role](./ece-roles.md):

| Flag | Description |
| --- | --- |
| `--proxy-protocol-version 2` | Configures the ECE proxy to parse Proxy Protocol v2 headers on the {{es}} HTTP ports. |
| `--proxy-protocol-lenient` | Accepts connections with and without Proxy Protocol headers. Required because load balancer health checks typically do not send them. |

::::{important}
Proxy Protocol v2 must be enabled on both the load balancer and the ECE proxies. A load balancer that prepends Proxy Protocol metadata to a proxy that is not configured to parse it breaks client connections.

The flags are applied per host when you run the installation script, so only the hosts you install with them are configured. If you intend to use Proxy Protocol v2 across the installation, it is safe to pass the flags on every host, including hosts that do not currently hold the proxy role.
::::

**New installations**

Add the flags to the [installation](./install.md) command on each host:

```bash
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install \
  --proxy-protocol-version 2 \
  --proxy-protocol-lenient
```

**Existing installations**

To enable Proxy Protocol v2 in an existing installation, reinstall the proxies one at a time with the flags, following [Perform ECE hosts maintenance](/deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md#ece-perform-host-maintenance-delete-runner). Working through the hosts one by one keeps the remaining proxies serving traffic while each one is replaced.

Because `--proxy-protocol-lenient` accepts connections with and without Proxy Protocol headers, reconfigure the proxies first and enable Proxy Protocol v2 on the load balancer only after every proxy has been reinstalled. Enabling it on the load balancer first breaks traffic to the proxies that are not reconfigured yet.

## Verify the configuration [ece-proxy-protocol-verify]

On each host with the proxy role, confirm that the proxy container has the Proxy Protocol environment variables for HTTP traffic:

```bash
sudo podman exec $(sudo podman ps --format '{{.Names}}' | grep frc-proxies-proxyv2) env | grep CLOUD_HTTP_PROXY_PROTO
```

On Docker-based hosts, replace `podman` with `docker`. The output should include both variables:

```text
CLOUD_HTTP_PROXY_PROTO_VERSION=2
CLOUD_HTTP_PROXY_PROTO_LENIENT=true
```

After you enable Proxy Protocol v2 on both the load balancer and the proxies, send a test request through the load balancer and confirm that the `client_ip` field in the proxy request logs shows the real client address instead of the load balancer address.

## Related [ece-proxy-protocol-related]

* [Load balancers](./ece-load-balancers.md) and [Client IP preservation](./ece-load-balancers.md#ece-client-ip-preservation)
* [IPv6 support on ECE](./ece-ipv6-support.md)
* [Manage IP filters in ECE](/deploy-manage/security/ip-filtering-ece.md)
