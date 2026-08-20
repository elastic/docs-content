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

**Source settings** {applies_to}`serverless: unavailable`
:   You can fetch SLOs from every connected remote cluster by enabling the option **Use all remote clusters**.

**Remote clusters** {applies_to}`serverless: unavailable`
:   To select the remote clusters from which you want to fetch SLOs, disable the option **Use all remote clusters** and open the **Select remote clusters** dropdown.

**Stale SLOs threshold**
:   You can hide SLOs from the overview list if they haven’t been updated within the defined stale threshold.

**Stale instances cleanup**
:   Automatically cleanup stale SLO instances that have not been updated within the stale threshold.

:::{image} /solutions/images/observability-slo-remote-clusters.png
:alt: Select remote clusters to fetch SLOs
:screenshot:
:::

:::{note}
* The **SLOs Settings** page is specific to your {{kib}} [space](/deploy-manage/manage-spaces.md). 
* {applies_to}`serverless: preview` **Source settings**, **Remote clusters**, and federated views are not available on {{serverless-full}}. To monitor SLO breaches across {{es}} projects, create SLOs in this project and [scope them](/solutions/observability/incident-management/create-an-slo.md#slo-cps-scope) to linked projects.
:::

## Configure SLOs for federated views [observability-configure-slo-settings-federated-view]
```{applies_to}
serverless: unavailable
```

Federated views allow you to view SLOs from remote {{es}} clusters alongside the local SLOs on the SLO listing page of your {{kib}} instance. This enables a centralized overview cluster where you can monitor SLOs across your entire fleet within the same {{kib}} space.

:::{important}
Before configuring SLOs, ensure that:
- {{es}} Cross-Cluster Search (CCS) is properly set up between the overview cluster and the remote clusters.
- The remote clusters are running {{kib}} with the SLO feature enabled and have SLOs created.
:::

Remote SLOs appear on the [SLO overview](/solutions/observability/incident-management/service-level-objectives-slos.md#slo-in-elastic). Open the three dots menu on a remote SLO:

**Details**
:   Opens a new panel that displays details of the remote instance.

**Edit**
:   Opens the SLO in edit mode on the remote cluster. You are redirected to the remote {{kib}} instance to modify the SLO definition.

**Clone**
:   Opens the clone SLO flow on the remote cluster. You are redirected to the remote {{kib}} instance to create a copy of the SLO.

**Delete**
:   Opens the delete confirmation on the remote cluster. You are redirected to the remote {{kib}} instance to remove the SLO.

**Manage burn rate rules**
:   Opens burn rate rules management for this SLO on the remote cluster. You are redirected to the remote {{kib}} instance to view, create, or edit burn rate alert rules.

**Reset**
:   Resets the SLO's error budget or rolling window on the remote cluster. You are redirected to the remote {{kib}} instance to complete this action.

**Add to dashboard**
:   Adds the remote SLO as a panel to a dashboard in your local {{kib}} instance. The SLO continues to display data from the remote cluster.

**Create new alert rule**
:   Disabled for remote SLOs. To create burn rate or other alert rules for a remote SLO, use **Manage burn rate rules** to open the remote {{kib}} instance and create the rule there.

