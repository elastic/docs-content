---
navigation_title: IPv6 support
applies_to:
  deployment:
    ece: ga 4.2
products:
  - id: cloud-enterprise
---

# IPv6 support on ECE [ece-ipv6-support]

{{ece}} (ECE) can be integrated into dual-stack (IPv4 and IPv6) networks. IPv6 clients can reach your deployments and the orchestrator endpoints, and your deployments can establish outbound connections to IPv6 destinations.

Ingress and egress are independent capabilities with different infrastructure requirements. You can enable either one, or both:

* **[IPv6 ingress](#ece-ipv6-ingress)**: IPv4 and IPv6 clients reach your deployments and the Cloud UI. It is handled entirely in front of ECE, so the ECE hosts are not modified. This makes it available to existing IPv4 installations.
* **[IPv6 egress](#ece-ipv6-egress)**: ECE services and deployments open outbound connections to IPv6 destinations. This traffic originates on the ECE hosts, so it requires dual-stack host and container networking.

ECE itself remains an IPv4 platform. IPv6 is supported only for ingress and egress connectivity, and there is no platform-wide IPv6 mode.

:::{note}
For a complete end-to-end tutorial that implements the concepts and requirements described on this page, refer to [Set up IPv6 for ECE on {{aws}}](./ece-ipv6-aws-setup.md). The tutorial covers dual-stack networking, load balancer configuration, Proxy Protocol v2, container networking, and both new and existing ECE installations.
:::

## IPv6 ingress [ece-ipv6-ingress]

ECE endpoints, such as the proxy ports `9200` and `9243` and the coordinator ports `12400` and `12443`, listen on IPv4. IPv6 client access relies on two components:

* A **dual-stack load balancer** in front of ECE, which accepts IPv6 client connections and forwards them to the ECE hosts over IPv4.
* **Proxy Protocol v2** between the load balancer and the ECE proxies, which preserves the original IPv6 client address after the load balancer translates the connection between IPv6 and IPv4.

To enable IPv6 ingress:

* Configure a dual-stack load balancer to forward deployment traffic to the ECE proxies and Cloud UI traffic to the ECE coordinators. Refer to [Load balancers](./ece-load-balancers.md) and [Client IP preservation](./ece-load-balancers.md#ece-client-ip-preservation) for more details.

  * For deployment traffic, use a TCP (L4) listener and configure Proxy Protocol v2 for client IP preservation.
  * For Cloud UI traffic, use an HTTP (L7) listener and configure it to set the `X-Forwarded-For` header for client IP preservation.

* Enable Proxy Protocol v2 on the ECE proxies by using the `--proxy-protocol-version` and `--proxy-protocol-lenient` flags when running the [installation script](./install.md). To enable it on an existing environment, refer to [Add Proxy Protocol v2 support to an existing installation](./ece-ipv6-aws-setup.md#reconfigure-proxies).

* Create `AAAA` DNS records that point to the dual-stack load balancer, including the [wildcard DNS record](./ece-wildcard-dns.md) used for deployment endpoints and the records used for administration traffic. Without them, IPv6 clients cannot resolve the endpoints even if the load balancer is dual-stack.

* When creating firewall rules, allow IPv6 on the load balancer listener ports only. The ECE hosts continue to receive IPv4 traffic only, so no IPv6 inbound rules are required. ECE [port requirements](./ece-networking-prereq.md) are unchanged.

:::{note}
[IP filtering](/deploy-manage/security/ip-filtering-ece.md) rules accept IPv6 addresses and CIDR blocks, so you can filter IPv6 clients the same way as IPv4 clients.
:::

Although ECE endpoints listen on IPv4, IP filtering rules accept IPv6 addresses and CIDR blocks, so you can filter IPv6 clients.

## IPv6 egress [ece-ipv6-egress]

Outbound IPv6 connectivity is needed when ECE services or your deployments must reach destinations available only over IPv6, such as snapshot repositories, authentication providers, webhook targets, or remote clusters.

Unlike IPv6 ingress, egress traffic originates from containers running on the ECE hosts. It therefore relies on dual-stack host and container networking, rather than on a load balancer.

To enable IPv6 egress on ECE hosts that run workloads requiring it:

* Configure dual-stack network interfaces with a working IPv6 route to the destination.
* Enable IPv6 forwarding through the `net.ipv6.conf.all.forwarding` kernel parameter.
* Configure the container runtime for dual-stack networking so containers receive IPv6 addresses and can route IPv6 traffic.
* Configure outbound firewall and routing rules to allow IPv6 traffic to your destinations.

Refer to the host preparation guide for your operating system to configure these requirements before installing ECE:

* [Configure a RHEL host](./configure-host-rhel.md) for Podman-based hosts.
* [Configure an Ubuntu host](./configure-host-ubuntu.md) or [Configure a SUSE host](./configure-host-suse.md) for Docker-based hosts.

::::{important}
Enabling IPv6 egress in an installation that is already running requires host-level networking changes and container recreation. The recommended approach is to replace or reinstall ECE hosts one at a time, following [Perform ECE hosts maintenance](/deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md).
::::

## Limitations [ece-ipv6-limitations]

The following scenarios are not supported:

* **IPv6-only ECE hosts:** Every ECE host requires an IPv4 address and IPv4 connectivity to the other hosts. Hosts can be dual-stack, but not IPv6-only.
* **Internal platform traffic over IPv6:** Communication between ECE hosts and platform containers, such as the ZooKeeper ensemble, runners, allocators, and proxy-to-instance traffic, uses IPv4.
* **Direct IPv6 connections to ECE endpoints:** The ECE proxies and coordinators do not accept IPv6 connections, so IPv6 client access always requires a dual-stack load balancer.
