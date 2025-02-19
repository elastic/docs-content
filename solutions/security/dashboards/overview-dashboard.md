---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/overview-dashboard.html
  - https://www.elastic.co/guide/en/serverless/current/security-overview-dashboard.html
---

# Overview dashboard

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/overview-dashboard.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-overview-dashboard.md

The Overview dashboard provides a high-level snapshot of alerts and events. It helps you assess overall system health and find anomalies that may require further investigation.

:::{image} ../../../images/security-overview-pg.png
:alt: Overview dashboard
:::


## Live feed [_live_feed]

The live feed on the Overview dashboard helps you quickly access recently created cases, favorited Timelines, and the latest {{elastic-sec}} news.

::::{tip}
The **Security news** section provides the latest {{elastic-sec}} news to help you stay informed of new developments, learn about {{elastic-sec}} features, and more.
::::


:::{image} ../../../images/security-live-feed-ov-page.png
:alt: Overview dashboard with live feed section highlighted
:::


## Histograms [_histograms]

Time-based histograms show the number of detections, alerts, and events that have occurred within the selected time range. To focus on a particular time, click and drag to select a time range, or choose a preset value. The **Stack by** menu lets you select which field is used to organize the data. For example, in the Alert trend histogram, stack by `kibana.alert.rule.name` to display alert counts by rule name within the specified time frame.

Hover over histograms, graphs, and tables to display an **Inspect** button (![Inspect icon](../../../images/security-inspect-icon.png "")) or options menu (![Three-dot menu icon](../../../images/security-three-dot-icon.png "")). Click to inspect the visualization’s {{es}} queries, add it to a new or existing case, or open it in Lens for customization.


## Host and network events [_host_and_network_events]

View event and host counts grouped by data source, such as **Auditbeat** or **{{elastic-defend}}**. Expand a category to view specific counts of host or network events from the selected source.

:::{image} ../../../images/security-events-count.png
:alt: Host and network events on the Overview dashboard
:class: screenshot
:::


## Threat Intelligence [_threat_intelligence]

The Threat Intelligence view on the Overview dashboard provides streamlined threat intelligence data for threat detection and matching.

The view shows the total number of ingested threat indicators, enabled threat intelligence sources, and ingested threat indicators per source. To learn more about the ingested indicator data, click **View indicators**.

::::{note}
For more information about connecting to threat intelligence sources, visit [Enable threat intelligence integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md).
::::


:::{image} ../../../images/security-threat-intelligence-view.png
:alt: threat intelligence view
:class: screenshot
:::

