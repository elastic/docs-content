---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: For self-managed clusters
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps for self-managed clusters

For ECE ({{ece}}), ECK ({{eck}}), and self-managed clusters, AutoOps can be set up in all supported [regions](ec-autoops-regions.md#autoops-for-self-managed-clusters-regions) through [Cloud Connect](/deploy-manage/cloud-connect.md). More regions are coming soon.

Cloud Connect enables users of ECE, ECK, and self-managed clusters to use {{ecloud}} services. This means you can take advantage of the simplified cluster monitoring, real-time issue detection, and performance recommendations of AutoOps without having to run and manage the underlying infrastructure.

## How it works

To connect your ECE, ECK, or self-managed cluster to AutoOps, you have to use your {{ecloud}} account to install {{agent}}. 

The agent first connects to your ECE, ECK, or self-managed {{es}} cluster. Then, it registers your cluster with {{ecloud}} using the Cloud Connect API and begins to send data from your cluster to AutoOps in your selected CSP region. Refer to [](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md) for instructions on how to get started.

:::{image} /deploy-manage/images/self-managed-autoops-diagram.png
:alt: Diagram depicting how AutoOps for self-managed clusters works
:::

After this setup is complete, you can start using AutoOps to monitor your cluster. Learn more about what you can do with AutoOps in [events](/deploy-manage/monitor/autoops/ec-autoops-events.md) and [views](/deploy-manage/monitor/autoops/views.md).  


## Section overview

In this section, you'll find the following information:

* How to [connect your self-managed cluster to AutoOps](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md)
* How to [connect your local development cluster to AutoOps](/deploy-manage/monitor/autoops/cc-connect-local-dev-to-autoops.md)
* How to [manage users of your connected clusters](/deploy-manage/monitor/autoops/cc-manage-users.md)
* A [troubleshooting guide](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-troubleshooting.md) to help you with any issues you may encounter

:::{tip}
Refer to our [FAQ](/deploy-manage/monitor/autoops/ec-autoops-faq.md#questions-about-autoops-for-self-managed-clusters) for answers to commonly asked questions about AutoOps for self-managed clusters.
:::