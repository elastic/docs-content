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

::::{important}
Make sure to use a combination of Linux distribution and Container Engine version that is supported, following our official [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). Using unsupported combinations can cause multiple issues with you ECE environment, such as failures to create system deployments, to upgrade workload deployments, proxy timeouts, and more.
::::


Before installing {{ece}}, you have to prepare your hosts with one of the following Linux distributions:

* [Ubuntu](configure-host-ubuntu.md)
* [Red Hat Enterprise Linux (RHEL) and Rocky Linux](configure-host-rhel.md)
* [SUSE Linux Enterprise Server (SLES)](configure-host-suse.md)
