:::{admonition} Additional installation parameters
Before you run an {{ece}} installation command, add the parameters that apply to your environment:

* On each host that uses Podman instead of Docker, add `--podman`.
* On each Podman host where SELinux runs in `enforcing` mode, add `--selinux`.
* {applies_to}`ece: ga 4.2` If you configure Proxy Protocol v2 between the load balancer and the {{ece}} proxies, add `--proxy-protocol-version 2` and `--proxy-protocol-lenient` on every host.

For more information, refer to [](/deploy-manage/deploy/cloud-enterprise/fresh-installation-of-ece-using-podman-hosts.md), [](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md), and [](/deploy-manage/deploy/cloud-enterprise/configure-proxy-protocol.md).
:::
