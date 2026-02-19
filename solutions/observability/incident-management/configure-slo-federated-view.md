---
navigation_title: Configure SLOs for federated views
products:
  - id: observability
  - id: cloud-serverless
applies_to:
  stack: ga 9.4
  serverless: ga
---


# Configure SLOs for federated views [observability-configure-slo-federated-views]

Federated views allow you to view SLOs from remote {{es}} clusters alongside the local SLOs on the SLO listing page of your {{kib}} instance. This enables a centralized overview cluster where you can monitor SLOs across your entire fleet without switching between {{kib}} instances.

The remote SLO is created on a remote cluster and is identified by the presence of a remote field containing `remoteName` (the CCS cluster name) and `kibanaUrl` (the {{kib}} URL of the remote cluster).

From your {{kib}} instance, navigate to the SLOs page and click **Settings** on the menu bar.

On the **SLOs Settings** page, you can configure the following controls:

**Source settings**
:   You can fetch SLOs from every connected remote cluster by enabling the option **Use all remote clusters**.

**Remote clusters**
:   To select specific remote clusters, disable the option **Use all remote clusters**, open the **Select remote clusters** dropdown, and choose the remote clusters from which you want to fetch SLOs.

**Stale SLOs threshold**
:   You can hide SLOs from the overview list if they haven’t been updated within the defined stale threshold.

:::{image} /solutions/images/observability-slo-remote-clusters.png
:alt: Select remote clusters to fetch SLOs
:screenshot:
:::