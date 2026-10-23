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
* [Red Hat Enterprise Linux (RHEL) 8, 9, and 10](configure-host-rhel.md)
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

## Require an install password to add hosts [ece-install-password]

```{applies_to}
deployment:
  ece: ga 4.3
```

When you install {{ece}} on an additional host, the host reads a set of bootstrap secrets from the installation to join it. By default, any host that can reach the installation over the network can read these secrets. To protect them, you can set an install password. While a password is set, a host can only join when it is installed with the same password. For the security background, refer to [](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation.md#ece-securing-install-password).

To start a new installation with an install password, add `--install-password PASSWORD` to the installation command on the first host, or set the password in the `INSTALL_PASSWORD` environment variable before you run the script. The environment variable keeps the password out of your shell history and of the process list.

```sh
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --install-password PASSWORD
```

To set, change, or remove the install password of an existing installation, run the `set-install-password` command on the first host or on any host that holds the director role:

```sh
bash elastic-cloud-enterprise.sh set-install-password --pwd PASSWORD
```

Use `--generate` instead of `--pwd` to let the script generate a password and print it, or `--unset` to remove the password. {{ece}} stores only a digest of the password, so you don't need the current password to change or remove it.

After you set a password, install every additional host with `--install-password PASSWORD`, as described in [](./install-ece-on-additional-hosts.md). Hosts that are already part of the installation don't need the password.

::::{important}
If you upgrade an existing installation, set the install password only after every host runs {{ece}} 4.3 or later. On a host that still runs an earlier version, the services forwarder loses access to the bootstrap secrets when it restarts. If that happens, remove the password with `--unset`.
::::

For all options, refer to [elastic-cloud-enterprise.sh set-install-password](cloud://reference/cloud-enterprise/ece-installation-script-set-install-password.md).

## Post-installation steps

Once you have installed ECE, check some final [post-installation steps](post-installation-steps.md) to get ready for production.


