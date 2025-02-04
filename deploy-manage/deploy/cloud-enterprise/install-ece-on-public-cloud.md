---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-public.html
---

# Install ECE on a Public Cloud [ece-install-public]

You can deploy ECE on any of the following cloud providers:

* Amazon Web Services (AWS)
* Google Cloud Platform (GCP)
* Microsoft Azure

with one of the following operating systems:

* [Ubuntu 20.04 LTS (Focal Fossa) and Ubuntu 22.04 LTS (Jammy Jellyfish)](configure-host-ubuntu-cloud.md)
* [Red Hat Enterprise Linux (RHEL) 8 and 9](configure-host-rhel-cloud.md)
* [Rocky Linux 8 and 9](configure-host-rhel-cloud.md)
* [SUSE Linux Enterprise Server (SLES) 12 SP5 and 15](configure-host-suse-cloud.md)

::::{important} 
Cloud providers default provide automatic operating system patching for their virtual machines. We strongly recommend disabling this feature to avoid potential data loss and installation failure. All patching should be done via [Perform host maintenance](../../maintenance/ece/perform-ece-hosts-maintenance.md).
::::




