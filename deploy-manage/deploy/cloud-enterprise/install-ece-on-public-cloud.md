---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-public.html
---

# Install ECE on a Public Cloud [ece-install-public]

You can deploy {{ece}} (ECE) on any of the following cloud providers:

* Amazon Web Services (AWS)
* Google Cloud Platform (GCP)
* Microsoft Azure

To install ECE on a public cloud, follow these steps:

1. Configure your hosts by following the appropriate guide for your operating system:

   * [Ubuntu 20.04 LTS (Focal Fossa) and Ubuntu 22.04 LTS (Jammy Jellyfish)](configure-host-ubuntu-cloud.md)
   * [Red Hat Enterprise Linux (RHEL) 8 and 9](configure-host-rhel-cloud.md)
   * [Rocky Linux 8 and 9](configure-host-rhel-cloud.md)
   * [SUSE Linux Enterprise Server (SLES) 12 SP5 and 15](configure-host-suse-cloud.md)

   ::::{important} 
   Cloud providers default provide automatic operating system patching for their virtual machines. We strongly recommend disabling this feature to avoid potential data loss and installation failure. All patching should be done through [Perform host maintenance](../../maintenance/ece/perform-ece-hosts-maintenance.md) instructions.
   ::::

2. Follow the instructions for the the ECE deployment scenario that best fits your business needs:

   * [Deploy a small installation](deploy-small-installation-cloud.md): For development, test, and small-scale use cases.
   * [Deploy a medium installation](deploy-medium-installation-cloud.md): For many production setups.
   * [Deploy a large installation](deploy-large-installation-cloud.md): For deployments with significant overall search and indexing throughput.
   * [Deploy using Podman](fresh-installation-of-ece-using-podman-hosts-cloud.md): Fresh installation of ECE using Podman hosts.

::::{note}
For installations using Podman instead of Docker, refer to [Podman considerations](./fresh-installation-of-ece-using-podman-hosts-cloud.md)
::::

