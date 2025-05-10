---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-jvm.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# JVM heap size [ece-jvm]

::::{important} 
ECE uses default JVM heap sizes for services that work for testing. Make sure to configure the JVM heap size that fits your use case. Not following the recommended settings may cause issues later on as volume of data and usage increases.
::::

When you install ECE specify the recommended JVM heap sizes with `--memory-settings JVM_SETTINGS` parameter, based on the use cases as described below:

* [Deploy a small installation](deploy-small-installation.md): For development, test, and small-scale use cases.
* [Deploy a medium installation](deploy-medium-installation.md): For many production setups.
* [Deploy a large installation](deploy-large-installation.md): For deployments with significant overall search and indexing throughput.

Other JVM heap sizes can be left at their defaults.

::::{note} 
In the current release, there is no direct way to change the Java heap size in the UI. In case you need to configure the settings after ECE installation, refer to [Cloud UI login failures](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-issues-login-failure) for further guidance.
::::


