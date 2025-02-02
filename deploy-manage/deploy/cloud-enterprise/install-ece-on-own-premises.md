---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-your-infra.html
---

# Install ECE on your own premises [ece-install-your-infra]

Before you start, make sure that your existing infrastructure meets the [requirements](prepare-environment.md).

ECE supports a [wide range of OS versions](https://www.elastic.co/support/matrix). Here are some OS-specific instructions for preparing your hosts; other versions will be similar:

* [Ubuntu 20.04 LTS (Focal Fossa) and 22.04 LTS (Jammy Jellyfish)](configure-host-ubuntu-onprem.md)
* [Red Hat Enterprise Linux (RHEL) 8 and 9, and Rocky Linux 8 and 9](configure-host-rhel-onprem.md)
* [SUSE Linux Enterprise Server (SLES) 12 SP5 and 15](configure-host-suse-onprem.md)

After your hosts are prepared, choose your preferred installation type:

* [Install ECE online](install-ece-onprem.md)
* [Install ECE offline](air-gapped-install.md)

::::{note} 
In these pages we frequently refer to [Docker](https://www.docker.com/), as its currently the most common container engine, but these instructions are generally valid for [Podman](https://podman.io/) as well, with `podman` replacing `docker` in commands as appropriate.
::::





