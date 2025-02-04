---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-overview-view.html
---

# Overview [ec-autoops-overview-view]

The **Overview** page displays the current status of customer deployments in Elastic Cloud Hosted that are linked to the same Elastic organization.

:::{image} ../../../images/cloud-autoops-overview-page.png
:alt: The Overview page
:::

::::{note}
The **Overview** page displays a complete list of deployments only if AutoOps is available in the specific Cloud Service Provider (CSP) region.
::::


High-level metrics are available, including the most important and currently open events in a single pane. You can view the cluster status, the number of open events in each {{es}} deployments over different periods of time, and navigate to a specific deployment for more details.


## Deployments table [ec-autoops-deployment-table]

The deployment view table lists all active deployments with {{es}} clusters and also deployments for which AutoOps collected the information but are no longer active. AutoOps provides real-time indications on {{es}} status, number of open critical events, number of {{es}} nodes and total number of shards. Select one of the deployments to get a more detailed view of all open and closed events.


## {{es}} Info [ec-autoops-es-info]

This section shows the number of active deployments, the number of nodes, and a summary of used resources, such as total disk size used and total memory connected for all clusters connected.


## Top events [ec-autoops-top-events]

This section provides a quick overview of the top open events in the selected period. You can filter by deployment, severity, name, and search for a specific event across all of the connected deployments.

The default view lists the top 10 important events across all deployments, sorted by severity.

The event card indicates when the last event occurred, the number of occurrences across all deployments, the deployments impacted by the event, and it includes a direct link to the event to get additional details.


## Events in time period [ec-autoops-events-time-period]

This time series chart displays all events identified across the connected deployments during the selected period. This allows you to detect which deployment is generating the most events, investigate, and take appropriate actions to resolve any issues.

