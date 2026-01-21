---
navigation_title: Install ECE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-installing.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-public.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-your-infra.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-cloud.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-onprem.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Install {{ece}} [ece-installing]

You can deploy {{ece}} (ECE) on public or private clouds, virtual machines, or on-premises.

::::{tip}
If you already have an ECE platform up and running, and you want to add hosts to your installation, refer to [](./install-ece-on-additional-hosts.md).
::::

In ECE, a host refers to any server, VM, or cloud instance where the ECE software is installed. An ECE platform consists of multiple hosts working together to orchestrate {{stack}} applications.

For public cloud deployments, you can choose from the following providers:

* Amazon Web Services (AWS)
* Google Cloud Platform (GCP)
* Microsoft Azure

::::{note}
In these pages we frequently refer to [Docker](https://www.docker.com/), as its currently the most common container engine, but these instructions are generally valid for [Podman](https://podman.io/) as well, with `podman` replacing `docker` in commands as appropriate.
::::

## Prerequisites [ece-install-prerequisites]

Before you start, make sure to [identify your deployment scenario](identify-deployment-scenario.md) and follow all the referenced sections in [](prepare-environment.md). Make sure that your selected infrastructure meets the requirements.

## Configure your ECE hosts [ece-configure-hosts]

After completing the prerequisites, proceed to configure your ECE hosts. This includes installing Docker or Podman, setting up XFS quotas, preparing mount points, and other required configurations.

::::{include} /deploy-manage/deploy/_snippets/ece-supported-combinations.md
::::

ECE supports a [wide range of OS versions](https://www.elastic.co/support/matrix#elastic-cloud-enterprise). Below are some OS-specific instructions for preparing your hosts, though other versions follow a similar process. Choose the appropriate guide for your operating system and follow the instructions:

* [Ubuntu 20.04 LTS (Focal Fossa) and Ubuntu 22.04 LTS (Jammy Jellyfish)](configure-host-ubuntu.md)
* [Red Hat Enterprise Linux (RHEL) 8 and 9](configure-host-rhel.md)
* [Rocky Linux 8 and 9](configure-host-rhel.md)
* [SUSE Linux Enterprise Server (SLES) 12 SP5 and 15](configure-host-suse.md)

::::{important}
Cloud providers default provide automatic operating system patching for their virtual machines. We strongly recommend disabling this feature to avoid potential data loss and installation failure. All patching should be done using the [Perform host maintenance](../../maintenance/ece/perform-ece-hosts-maintenance.md) instructions.
::::

## Install ECE [install-ece]

To install ECE with the official bash script, follow the instructions for the [deployment scenario](./identify-deployment-scenario.md) that best fits your business needs:

   * [Deploy a small installation](deploy-small-installation.md): For development, test, and small-scale use cases.
   * [Deploy a medium installation](deploy-medium-installation.md): For many production setups.
   * [Deploy a large installation](deploy-large-installation.md): For deployments with significant overall search and indexing throughput.
   * [Deploy using Podman](./fresh-installation-of-ece-using-podman-hosts.md): Fresh installation of ECE using Podman hosts.

Alternatively, you can install ECE with the [Ansible](alternative-install-ece-with-ansible.md) playbook. The ECE Ansible playbook is a community project, supported by Elastic, aimed at installing ECE at scale.

To install ECE in an air-gapped environment, refer to [](./air-gapped-install.md).

## Post-installation steps

Once you have installed ECE, check some final [post-installation steps](post-installation-steps.md) to get ready for production.


