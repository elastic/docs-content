---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-os-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-os-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure your operating system [ece-configure-os]

Before installing {{ece}}, you have to prepare your hosts with one of the following Linux distributions:

* [Ubuntu](configure-host-ubuntu.md)
* [Red Hat Enterprise Linux (RHEL) and Rocky Linux](configure-host-rhel.md)
* [SUSE Linux Enterprise Server (SLES)](configure-host-suse.md)

::::{important}
Make sure to use a supported combination of Linux distribution and container engine version, such as `Docker` or `Podman`, as defined in our official [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). Unsupported combinations can lead to various issues in your ECE environment, including failures when creating system deployments, upgrading workload deployments, proxy timeouts, and more.
::::