---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/es-ui-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-ui.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Elastic Security UI


The {{security-app}} is a highly interactive workspace designed for security analysts that provides a clear overview of events and alerts from your environment. You can use the interactive UI to drill down into areas of interest.


## Search [search-overview]

Filter for alerts, events, processes, and other important security data by entering [{{kib}} Query Language (KQL)](/explore-analyze/query-filter/languages/kql.md) queries in the search bar, which appears at the top of each page throughout the app. A date/time filter set to `Today` is enabled by default, but can be changed to any time range.

:::{image} /solutions/images/security-search-bar.png
:alt: search bar
:screenshot:
:::

* To refine your search results, select **Add Filter** (![Add filter icon](/solutions/images/security-add-filter-icon.png "title =20x20")), then enter the field, operator (such as `is not` or `is between`), and value for your filter.
* To save the current KQL query and any applied filters, select **Saved query menu** (![Saved query menu icon](/solutions/images/security-saved-query-menu-icon.png "title =20x20")), enter a name for the saved query, and select **Save saved query**.


## Visualization actions [visualization-actions]

Many {{elastic-sec}} histograms, graphs, and tables display an **Inspect** button (![Inspect icon](/solutions/images/security-inspect-icon.png "title =20x20")) when you hover over them. Click to examine the {{es}} queries used to retrieve data throughout the app.

:::{image} /solutions/images/security-inspect-icon-context.png
:alt: Inspect icon
:width: 400px
:screenshot:
:::

Other visualizations display an options menu (![Three-dot menu icon](/solutions/images/security-three-dot-icon.png "title =20x20")), which allows you to inspect the visualization’s queries, add it to a new or existing case, or open it in Lens for customization.

:::{image} /solutions/images/security-viz-options-menu-open.png
:alt: Options menu opened
:width: 500px
:screenshot:
:::


## Inline actions for fields and values [inline-actions]

Throughout the {{security-app}}, you can hover over many data fields and values to display inline actions, which allow you to customize your view or investigate further based on that field or value.

:::{image} /solutions/images/security-inline-actions-menu.png
:alt: Inline additional actions menu
:width: 500px
:screenshot:
:::

In some visualizations, these actions are available in the legend by clicking a value’s options icon (![Vertical three-dot icon](/solutions/images/security-three-dot-icon-vertical.png "title =20x20")).

:::{image} /solutions/images/security-inline-actions-legend.png
:alt: Actions in a visualization legend
:width: 650px
:screenshot:
:::

Inline actions include the following (some actions are unavailable in some contexts):

* **Filter In**: Add a filter that includes the selected value.
* **Filter Out**: Add a filter that excludes the selected value.
* **Add to timeline**: Add a filter to Timeline for the selected value.
* **Toggle column in table**: Add or remove the selected field as a column in the alerts or events table. (This action is only available on an alert’s or event’s details flyout.)
* **Show top _x_**: Display a pop-up window that shows the selected field’s top events or detection alerts.
* **Copy to Clipboard**: Copy the selected field-value pair to paste elsewhere.


## {{security-app}} pages [_security_app_pages]

The {{security-app}} contains the following pages that enable analysts to view, analyze, and manage security data.

### Discover [security-ui-discover]

Use the [Discover](/explore-analyze/discover.md) UI to filter your data or learn about its structure.


### Dashboards [_dashboards]

Expand this section to access the following dashboards, which provide interactive visualizations that summarize your data:

- Overview
- Detection & Response
- {applies_to}`stack: beta 9.3+` {applies_to}`serverless: beta` Kubernetes
- Cloud Security Posture
- Cloud Native Vulnerability Management
- Entity Analytics
- Data Quality.

You can also create and view custom dashboards. Refer to [](/solutions/security/dashboards.md) for more information.


### Rules [_rules]

Expand this section to access the following pages:

* [Rules](/solutions/security/detect-and-alert/manage-detection-rules.md): Create and manage rules to monitor suspicious events.

* [Benchmarks](/solutions/security/cloud/benchmarks.md): View, set up, or configure cloud security benchmarks.

* [Shared Exception Lists](/solutions/security/detect-and-alert/rule-exceptions.md#shared-exception-list-intro): View and manage rule exceptions and shared exception lists.

* [MITRE ATT&CK® coverage](/solutions/security/detect-and-alert/mitre-attandckr-coverage.md): Review your coverage of MITRE ATT&CK® tactics and techniques, based on installed rules.


### Alerts [_alerts]

View and manage alerts to monitor activity within your network. Refer to [Detections and alerts](/solutions/security/detect-and-alert.md) for more information.


### Attack discovery

Use large language models (LLMs) to analyze alerts in your environment and identify threats. Refer to [](/solutions/security/ai/attack-discovery.md) for more information.


### Assets [security-ui-assets]

The Assets section allows you to manage the following features:

* [{{fleet}}](/reference/fleet/manage-elastic-agents-in-fleet.md)
* [Endpoint protection](/solutions/security/manage-elastic-defend.md)

    * [Endpoints](/solutions/security/manage-elastic-defend/endpoints.md): View and manage hosts running {{elastic-defend}}.
    * [Policies](/solutions/security/manage-elastic-defend/policies.md): View and manage {{elastic-defend}} integration policies.
    * [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md): View and manage trusted Windows, macOS, and Linux applications.
    * [Event filters](/solutions/security/manage-elastic-defend/event-filters.md): View and manage event filters, which allow you to filter endpoint events you don’t need to want stored in {{es}}.
    * [Host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md): View and manage host isolation exceptions, which specify IP addresses that can communicate with your hosts even when those hosts are blocked from your network.
    * [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md): View and manage the blocklist, which allows you to prevent specified applications from running on hosts, extending the list of processes that {{elastic-defend}} considers malicious.
    * [Response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md): Find the history of response actions performed on hosts.

* [Cloud security](/solutions/security/cloud.md)


### Cases [_cases]

Open and track security issues. Refer to [Cases](/solutions/security/investigate/cases.md) to learn more.


### Entity analytics
```yaml {applies_to}
stack: ga 9.1
serverless: ga
```

:::{admonition} Requirements
:applies_to: {stack: removed 9.3, serverless: removed}
To access this section, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#access-privileged-user-monitoring).
:::

Expand this section to access the following pages:

- [Entity analytics](/solutions/security/advanced-entity-analytics/overview.md): Access a comprehensive overview of entity risk scores and anomalies identified by prebuilt {{anomaly-jobs}}.
- [Privileged user monitoring](/solutions/security/advanced-entity-analytics/monitor-privileged-user-activitites.md): Set up your privileged users and monitor their activities to identify suspicious behavior. 


### Explore [_explore]

Expand this section to access the following pages:

* [Hosts](/solutions/security/explore/hosts-page.md): Examine key metrics for host-related security events using graphs, charts, and interactive data tables.

* [Network](/solutions/security/explore/network-page.md): Explore the interactive map to discover key network activity metrics and investigate network events further in Timeline.

* [Users](/solutions/security/explore/users-page.md): Access a comprehensive overview of user data to help you understand authentication and user behavior within your environment.


### Investigations [security-ui-investigations]

Expand this section to access the following pages:

* [Timelines](../investigate/timeline.md): Investigate alerts and complex threats — such as lateral movement — in your network. Timelines are interactive and allow you to share your findings with other team members.

    ::::{tip}
    Click the **Timeline** button at the bottom of the {{security-app}} to start an investigation.

    ::::

* [Notes](/solutions/security/investigate/notes.md): View and interact with all existing notes.

* [Osquery](../investigate/osquery.md): Deploy Osquery with {{agent}}, then run and schedule queries.


### Findings [_findings]

Identify misconfigurations and vulnerabilities in your cloud infrastructure. For setup instructions, refer to [Cloud Security Posture Management](/solutions/security/cloud/cloud-security-posture-management.md), [Kubernetes Security Posture Management](/solutions/security/cloud/kubernetes-security-posture-management.md), or [Cloud Native Vulnerability Management](/solutions/security/cloud/cloud-native-vulnerability-management.md).


### Intelligence [_intelligence]

The Intelligence section contains the Indicators page, which collects data from enabled threat intelligence feeds and provides a centralized view of indicators of compromise (IoCs). Refer to [Indicators of compromise](/troubleshoot/security/indicators-of-compromise.md) to learn more.


### {{ml-cap}} [security-ui-ml-cap]

Manage {{ml}} jobs and settings. Refer to [{{ml-cap}} docs](/explore-analyze/machine-learning/anomaly-detection.md) for more information.

### Get started [_get_started]

Quickly add security integrations that can ingest data and monitor your hosts.

### Developer tools [security-ui-dev-tools]

Use additional API and analysis tools to interact with your data.

### Management [_manage]

Use the management or project settings pages to access and manage:

- Additional security features
- {applies_to}`stack: ga` [Stack monitoring](/deploy-manage/monitor/stack-monitoring.md)
- [{{integrations}}](/reference/fleet/manage-integrations.md)
- Indices, data streams, and rollups
- {applies_to}`serverless: ga` [Billing](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md) and [subscription](/deploy-manage/cloud-organization/billing/manage-subscription.md) options for your {{serverless-short}} project


## Accessibility features [timeline-accessibility-features]

Accessibility features, such as keyboard focus and screen reader support, are built into the Elastic Security UI. These features offer additional ways to navigate the UI and interact with the application.


### Interact with draggable elements [draggable-timeline-elements]

Use your keyboard to interact with draggable elements in the Elastic Security UI:

* Press the `Tab` key to apply keyboard focus to an element within a table. Or, use your mouse to click on an element and apply keyboard focus to it.

  :::{image} /solutions/images/security-timeline-accessiblity-keyboard-focus.gif
  :alt: timeline accessiblity keyboard focus
  :width: 650px
  :screenshot:
  :::

* Press `Enter` on an element with keyboard focus to display its menu and press `Tab` to apply focus sequentially to menu options. The `f`, `o`, `a`, `t`, `c` hotkeys are automatically enabled during this process and offer an alternative way to interact with menu options.

  :::{image} /solutions/images/security-timeline-accessiblity-keyboard-focus-hotkeys.gif
  :alt: timeline accessiblity keyboard focus hotkeys
  :width: 500px
  :screenshot:
  :::

* Press the spacebar once to begin dragging an element to a different location and press it a second time to drop it. Use the directional arrows to move the element around the UI.

  :::{image} /solutions/images/security-timeline-ui-accessiblity-drag-n-drop.gif
  :alt: timeline ui accessiblity drag n drop
  :screenshot:
  :::

* If an event has an event renderer, press the `Shift` key and the down directional arrow to apply keyboard focus to the event renderer and `Tab` or `Shift` + `Tab` to navigate between fields. To return to the cells in the current row, press the up directional arrow. To move to the next row, press the down directional arrow.

  :::{image} /solutions/images/security-timeline-accessiblity-event-renderers.gif
  :alt: timeline accessiblity event renderers
  :screenshot:
  :::


### Navigate the Elastic Security UI [timeline-tab]

Use your keyboard to navigate through rows, columns, and menu options in the Elastic Security UI:

* Use the directional arrows to move keyboard focus right, left, up, and down in a table.

  :::{image} /solutions/images/security-timeline-accessiblity-directional-arrows.gif
  :alt: timeline accessiblity directional arrows
  :width: 500px
  :screenshot:
  :::

* Press the `Tab` key to navigate through a table cell with multiple elements, such as buttons, field names, and menus. Pressing the `Tab` key will sequentially apply keyboard focus to each element in the table cell.

  :::{image} /solutions/images/security-timeline-accessiblity-tab-keys.gif
  :alt: timeline accessiblity tab keys
  :width: 400px
  :screenshot:
  :::

* Use `CTRL + Home` to shift keyboard focus to the first cell in a row. Likewise, use `CTRL + End` to move keyboard focus to the last cell in the row.

  :::{image} /solutions/images/security-timeline-accessiblity-shifting-keyboard-focus.gif
  :alt: timeline accessiblity shifting keyboard focus
  :screenshot:
  :::

* Use the `Page Up` and `Page Down` keys to scroll through the page.

  :::{image} /solutions/images/security-timeline-accessiblity-page-up-n-down.gif
  :alt: timeline accessiblity page up n down
  :screenshot:
  :::
