---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-installing.html
---

# Install [ece-installing]

Before you start, make sure you [identify your deployment scenario](identify-deployment-scenario.md) and [prepare your hosts](prepare-environment.md).

You can get ECE up and running using the official bash script on a [public cloud](install-ece-on-public-cloud.md) or on [your own premises](install-ece-on-own-premises.md). Alternatively, you can install ECE with the [Ansible](alternative-install-ece-with-ansible.md) playbook. The ECE Ansible playbook is a community project, supported by Elastic, aimed at installing ECE at scale.

Once you have installed ECE, check some final [post-installation steps](post-installation-steps.md) to get ready for production.

::::{tip} 
This outline pertains to troubleshooting on the container engine level. The following outline is structured according to [Docker](https://www.docker.com/) as the most common engine but is also valid for [Podman](https://podman.io/), replacing out commands as needed.
::::


::::{note} 
In these pages we frequently refer to [Docker](https://www.docker.com/), as its currently the most common container engine, but these instructions are generally valid for [Podman](https://podman.io/) as well, with `podman` replacing `docker` in commands as appropriate.
::::


