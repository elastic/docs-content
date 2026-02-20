---
navigation_title: Configure SLOs settings
products:
  - id: observability
  - id: cloud-serverless
applies_to:
  stack: ga 9.4
  serverless: ga
---

# Configure SLOs settings[observability-configure-slo-settings]

From your {{kib}} instance, navigate to the SLOs page and click **Settings** on the menu bar.

On the **SLOs Settings** page, you can configure the following controls:

**Source settings**
:   You can fetch SLOs from every connected remote cluster by enabling the option **Use all remote clusters**.

**Remote clusters**
:   To select the remote clusters from which you want to fetch SLOs, disable the option **Use all remote clusters** and open the **Select remote clusters** dropdown.

**Stale SLOs threshold**
:   You can hide SLOs from the overview list if they haven’t been updated within the defined stale threshold.

**Stale instances cleanup**
:   Automatically cleanup stale SLO instances that have not been updated within the stale threshold.

:::{image} /solutions/images/observability-slo-remote-clusters.png
:alt: Select remote clusters to fetch SLOs
:screenshot:
:::

## Configure SLOs for federated views[observability-configure-slo-settings-federated-view] 

Federated views allow you to view SLOs from remote {{es}} clusters alongside the local SLOs on the SLO listing page of your {{kib}} instance. This enables a centralized overview cluster where you can monitor SLOs across your entire fleet within the same {{kib}} space.

### Prerequisites[observability-federated-view-prerequisites]

- {{es}} Cross-Cluster Search (CCS) must be configured between the overview cluster and remote clusters.
- Remote clusters must be running {{kib}} with the SLO feature and have SLOs created.
- The remote cluster's `kibanaUrl` should be set in the SLO summary documents for full functionality (edit/clone/delete links).

Use the three dots menu on the remote SLO to perform the following operations:

**Details**
:   Opens a new panel that displays details of the remote SLO instance.

**Edit**, **Clone**, **Delete**
:   TBD 

**Manage burn rate rules**
:   TBD

**Reset**
:   TBD

**Add to dashboard**
:   TBD

**Create new alert rule**
:   TBD

