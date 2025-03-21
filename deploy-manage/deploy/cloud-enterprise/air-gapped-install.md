---
applies_to:
  deployment:
    ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-offline.html
---

# Air-gapped install [ece-install-offline]

Installing ECE on hosts without internet access is commonly referred to as an *offline* or *air-gapped* installation. ECE supports two air-gapped installation methods, depending on whether a private Docker registry is available. In both cases, you must download multiple Docker images and the installation script from Elastic, and load them onto your hosts or private registry.

::::{note}
    The versioning of {{es}} and {{kib}} is synchronized and versions where the major, minor, and patch levels match can be used together. Differences in build versions indicated by a dash do not affect compatibility.
::::

Before you start, you must:

* Follow the same prerequisites described in [](./install.md#ece-install-prerequisites). This includes [](./identify-deployment-scenario.md) and [](./prepare-environment.md) steps.
* [Configure your operating system](./configure-operating-system.md) in all ECE hosts.
* Be part of the `docker` group to run the installation script. You should not install Elastic Cloud Enterprise as the `root` user.
* Set up and run a local copy of the Elastic Package Repository, otherwise your deployments with APM server and Elastic agent won’t work. Refer to the [Running EPR in air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md#air-gapped-diy-epr) documentation.

When you are ready to install ECE, you can proceed:

* [With your private Docker registry](./ece-install-offline-with-registry.md)
* [Without a private Docker registry](./ece-install-offline-no-registry.md)

After installing ECE in your hosts, you can continue with [](./post-installation-steps.md).

::::{note}
Deployment End-of-life (EOL) information relies on the connection to [https://www.elastic.co/support/eol.json](https://www.elastic.co/support/eol.json). If EOL information is updated, Elastic may require you to reconnect to [https://www.elastic.co/support/eol.json](https://www.elastic.co/support/eol.json) over the internet to get this information reflected.
::::
