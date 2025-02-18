---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/visual-event-analyzer.html
  - https://www.elastic.co/guide/en/serverless/current/security-visual-event-analyzer.html
---

# Visual event analyzer

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/visual-event-analyzer.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-visual-event-analyzer.md

{{elastic-sec}} allows any event detected by {{elastic-endpoint}} to be analyzed using a process-based visual analyzer, which shows a graphical timeline of processes that led up to the alert and the events that occurred immediately after. Examining events in the visual event analyzer is useful to determine the origin of potentially malicious activity and other areas in your environment that may be compromised. It also enables security analysts to drill down into all related hosts, processes, and other events to aid in their investigations.

::::{tip}
If you’re experiencing performance degradation, you can [exclude cold and frozen tier data](/solutions/security/get-started/configure-advanced-settings.md#exclude-cold-frozen-tiers) from analyzer queries.
::::



## Find events to analyze [find-events-analyze]

You can only visualize events triggered by hosts configured with the {{elastic-defend}} integration or any `sysmon` data from `winlogbeat`.

In KQL, this translates to any event with the `agent.type` set to either:

* `endpoint`
* `winlogbeat` with `event.module` set to `sysmon`

To find events that can be visually analyzed:

1. First, display a list of events by doing one of the following:

    * Find **Hosts** in the main menu, or search for `Security/Explore/Hosts` by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Events** tab. A list of all your hosts' events appears at the bottom of the page.
    * Find **Alerts** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then scroll down to the Alerts table.

2. Filter events that can be visually analyzed by entering either of the following queries in the KQL search bar, then selecting **Enter**:

    * `agent.type:"endpoint" and process.entity_id :*`

        Or

    * `agent.type:"winlogbeat" and event.module: "sysmon" and process.entity_id : *`

3. Events that can be visually analyzed are denoted by a cubical **Analyze event** icon. Select this option to open the event in the visual analyzer. The event analyzer is accessible from the **Hosts***, ***Alerts**, and **Timelines** pages, as well as the alert details flyout.

    ::::{tip}
    Turn on the `securitySolution:enableVisualizationsInFlyout` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#visualizations-in-flyout) to access the event analyzer from the **Visualize** tab in the alert or event details flyout.
    ::::


    :::{image} ../../../images/security-analyze-event-button.png
    :alt: analyze event button
    :class: screenshot
    :::

    ::::{note}
    Events that cannot be analyzed will not have the **Analyze event** option available. This might occur if the event has incompatible field mappings.
    ::::


    :::{image} ../../../images/security-analyze-event-timeline.png
    :alt: analyze event timeline
    :class: screenshot
    :::


::::{tip}
You can also analyze events from [Timelines](/solutions/security/investigate/timeline.md).
::::



## Visual event analyzer UI [visual-analyzer-ui]

Within the visual analyzer, each cube represents a process, such as an executable file or network event. Click and drag in the analyzer to explore the hierarchy of all process relationships.

To understand what fields were used to create the process, select the **Process Tree** to show the schema that created the graphical view. The fields included are:

* `SOURCE`: Can be either `endpoint` or `winlogbeat`
* `ID`: Event field that uniquely identifies a node
* `EDGE`: Event field which indicates the relationship between two nodes

:::{image} ../../../images/security-process-schema.png
:alt: process schema
:class: screenshot
:::

Click the **Legend** to show the state of each process node.

:::{image} ../../../images/security-node-legend.png
:alt: node legend
:class: screenshot
:::

Use the date and time filter to analyze the event within a specific time range. By default, the selected time range matches that of the table from which you opened the alert.

:::{image} ../../../images/security-date-range-selection.png
:alt: date range selection
:class: screenshot
:::

Select a different data view to further filter the alert’s related events.

:::{image} ../../../images/security-data-view-selection.png
:alt: data view selection
:class: screenshot
:::

To expand the analyzer to a full screen, select the **Full Screen** icon above the left panel.

:::{image} ../../../images/security-full-screen-analyzer.png
:alt: full screen analyzer
:class: screenshot
:::

The left panel contains a list of all processes related to the event, starting with the event chain’s first process. **Analyzed Events** — the event you selected to analyze from the events list or Timeline — are highlighted with a light blue outline around the cube.

:::{image} ../../../images/security-process-list.png
:alt: process list
:class: screenshot
:::

In the graphical view, you can:

* Zoom in and out of the graphical view using the slider on the far right
* Click and drag around the graphical view to more process relationships
* Observe child process events that spawned from the parent process
* Determine how much time passed between each process
* Identify all events related to each process

:::{image} ../../../images/security-graphical-view.png
:alt: graphical view
:class: screenshot
:::


## Process and event details [process-and-event-details]

To learn more about each related process, select the process in the left panel or the graphical view. The left panel displays process details such as:

* The number of events associated with the process
* The timestamp of when the process was executed
* The file path of the process within the host
* The `process-pid`
* The user name and domain that ran the process
* Any other relevant process information
* Any associated alerts

:::{image} ../../../images/security-process-details.png
:alt: process details
:class: screenshot
:::

When you first select a process, it appears in a loading state. If loading data for a given process fails, click **Reload `{{process-name}}`** beneath the process to reload the data.

Access event details by selecting that event’s URL at the top of the process details view or choosing one of the event pills in the graphical view.

Events are categorized based on the `event.category` value.

:::{image} ../../../images/security-event-type.png
:alt: event type
:class: screenshot
:::

When you select an `event.category` pill, all the events within that category are listed in the left panel. To display more details about a specific event, select it from the list.

:::{image} ../../../images/security-event-details.png
:alt: event details
:class: screenshot
:::

::::{note}
In {{stack}} versions 7.10.0 and newer, there is no limit to the number of events that can be associated with a process. However, in {{stack}} versions 7.9.0 and earlier, each process is limited to only 100 events.
::::


If you have a [Platinum or Enterprise subscription](https://www.elastic.co/pricing), you can also examine alerts associated with events.

To examine alerts associated with the event, select the alert pill (***x* alert**). The left pane lists the total number of associated alerts, and alerts are ordered from oldest to newest. Each alert shows the type of event that produced it (`event.category`), the event timestamp (`@timestamp`), and rule that generated the alert (`kibana.alert.rule.name`). Click on the rule name to open the alert’s details.

In the example screenshot below, five alerts were generated by the analyzed event (`lsass.exe`). The left pane displays the associated alerts and basic information about each one.

:::{image} ../../../images/security-alert-pill.png
:alt: alert pill
:class: screenshot
:::
