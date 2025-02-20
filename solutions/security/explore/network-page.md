---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/network-page-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-network-page-overview.html
---

# Network page

The Network page provides key network activity metrics in an interactive map, and network event tables that enable interaction with Timeline. You can drag and drop items of interest from the Network view to Timeline for further investigation.

:::{image} ../../../images/security-network-ui.png
:alt: network ui
:class: screenshot
:::


## Map [map-ui]

The map provides an interactive visual overview of your network traffic. Hover over source and destination points to show more information, such as host names and IP addresses.

::::{note}
To access the interactive map in {{stack}}, you need either `Read` or `All` privileges for `Maps` (**Kibana Privileges** → **Analytics** → **Maps**). In serverless, you must have the appropriate user role. To learn more about map setup, refer to [Configure network map data](/solutions/security/explore/configure-network-map-data.md).
::::


There are several ways to drill down:

* Click a point, hover over the host name or destination IP, then  use the filter icon to add a field to the filter bar.
* Drag a field from the map to Timeline.
* Click a host name to go to the Hosts page.
* Click an IP address to open its details page.

You can start an investigation using the map, and the map refreshes to show related data when you run a query or update the time range.

::::{tip}
To add and remove layers, click on the **Options** menu (**…​**) in the top right corner of the map.
::::



## Widgets and data tables [map-widgets-tables]

Interactive widgets let you drill down for deeper insights:

* Network events
* DNS queries
* Unique flow IDs
* TLS handshakes
* Unique private IPs

There are also tabs for viewing and investigating specific types of data:

* **Events**: All network events. To display alerts received from external monitoring tools, scroll down to the events table and select **Show only external alerts** on the right.
* **Flows**: Source and destination IP addresses and countries.
* **DNS**: DNS network queries.
* **HTTP**: Received HTTP requests (HTTP requests for applications using [Elastic APM](/solutions/observability/apps/application-performance-monitoring-apm.md) are monitored by default).
* **TLS**: Handshake details.
* **Anomalies**: Anomalies discovered by [machine learning jobs](/solutions/security/advanced-entity-analytics/anomaly-detection.md).

The Events table includes inline actions and several customization options. To learn more about what you can do with the data in these tables, refer to [*Manage detection alerts*](/solutions/security/detect-and-alert/manage-detection-alerts.md).


## IP details page [ip-details-page]

An IP’s details page shows related network information for the selected IP address.

To view an IP’s details page, click its IP address link from the Source IPs or Destination IPs table.

The IP’s details page includes the following sections:

* **Summary**: General details such as the location, when the IP address was first and last seen, the associated host ID and host name, and links to external sites for verifying the IP address’s reputation.

    ::::{note}
    By default, the external sites are [Talos](https://talosintelligence.com/) and [VirusTotal](https://www.virustotal.com/). Refer to [Display reputation links on IP detail pages](/solutions/security/get-started/configure-advanced-settings.md#ip-reputation-links) to learn how to configure IP reputation links.
    ::::

* **Alert metrics**: The total number of alerts by severity, rule, and status (`Open`, `Acknowledged`, or `Closed`).
* **Data tables**: The same data tables as on the main Network page, except with values for the selected IP address instead of all IP addresses.

:::{image} ../../../images/security-IP-detail-pg.png
:alt: IP details page
:class: screenshot
:::


