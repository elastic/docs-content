---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/visual-event-analyzer.html
  - https://www.elastic.co/guide/en/serverless/current/security-visual-event-analyzer.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Visual event analyzer [security-visual-event-analyzer]

{{elastic-sec}} allows any event detected by {{elastic-endpoint}} or supported third-party integrations to be analyzed using a process-based visual analyzer, which shows a graphical timeline of processes that led up to the alert and the events that occurred immediately after. Examining events in the visual event analyzer is useful to determine the origin of potentially malicious activity and other areas in your environment that may be compromised. It also enables security analysts to drill down into all related hosts, processes, and other events to aid in their investigations.

::::{tip}
If you’re experiencing performance degradation, you can [exclude cold and frozen tier data](/solutions/security/get-started/configure-advanced-settings.md#exclude-cold-frozen-tiers) from analyzer queries. This setting is only available for the {{stack}}.
::::



## Find events to analyze [find-events-analyze]

You can visualize events from the following sources:

* {{elastic-defend}} integration
* Sysmon data collected through {{winlogbeat}}
* Third-party integrations:
  * [CrowdStrike](integration-docs://reference/crowdstrike.md) (Falcon logs collected through Event Stream or FDR)
  * [SentinelOne Cloud Funnel](integration-docs://reference/sentinel_one_cloud_funnel.md)
  * {applies_to}`stack: ga 9.2` [Microsoft Defender for Endpoint](integration-docs://reference/microsoft_defender_endpoint.md)

In KQL, this translates to any event with the `agent.type` set to:

* `endpoint`
* `winlogbeat` with `event.module` set to `sysmon`
* `filebeat` with `event.module` set to `crowdstrike`
* `filebeat` with `event.module` set to `sentinel_one_cloud_funnel`
* {applies_to}`stack: ga 9.2` `filebeat` with `event.module` set to `microsoft_defender_endpoint`

{applies_to}`stack: ga 9.2` The visual analyzer also supports analyzing `event.kind: "alert"` events from third-party integrations. To view these events, your role must have `read` privileges for the `alerts-security.alerts-*` indices.

To find events that can be visually analyzed:

1. First, display a list of events by doing one of the following:

    * Find **Hosts** in the main menu, or search for `Security/Explore/Hosts` by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Events** tab. A list of all your hosts' events appears at the bottom of the page.
    * Find **Alerts** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then scroll down to the Alerts table.

2. Filter events that can be visually analyzed by entering one of the following queries in the KQL search bar, then selecting **Enter**:

    * `agent.type:"endpoint" and process.entity_id :*`
    * `agent.type:"winlogbeat" and event.module: "sysmon" and process.entity_id : *`
    * `agent.type:"filebeat" and event.module: "crowdstrike" and process.entity_id : *`
    * `agent.type:"filebeat" and event.module: "sentinel_one_cloud_funnel" and process.entity_id : *`
    * {applies_to}`stack: ga 9.2` `agent.type:"filebeat" and event.module: "microsoft_defender_endpoint" and process.entity_id : *` 

    ::::{note}
    {applies_to}`stack: ga 9.2` To specifically filter for alert-kind events from third-party integrations, add `event.kind:"alert"`. For example:
    `agent.type:"filebeat" and event.module:"microsoft_defender_endpoint" and event.kind:"alert" and process.entity_id:*`
    ::::

3. Events that can be visually analyzed are denoted by a cubical **Analyze event** icon. Select this option to open the event in the visual analyzer. The event analyzer is accessible from the **Hosts**, **Alerts**, and **Timelines** pages, as well as the alert details flyout.

    ::::{note}
    Events that cannot be analyzed will not have the **Analyze event** option available. This might occur if the event has incompatible field mappings.
    ::::

    :::{image} /solutions/images/security-analyze-event-button.png
    :alt: analyze event button
    :screenshot:
    :::

    ::::{tip}
    You can also analyze events from [Timelines](/solutions/security/investigate/timeline.md).
    ::::

## Visual event analyzer UI [visual-analyzer-ui]

Within the visual analyzer, each cube represents a process, such as an executable file or network event. In the analyzer, you can:

* Zoom in and out of the Analyzer Graph view using the slider
* Click and drag around the Analyzer Graph view to explore the hierarchy of all process relationships
* Observe child process events that spawned from the parent process
* Determine how much time passed between each process
* Identify all events related to each process

Use the following icons to perform more actions:

* To understand what fields were used to create the process, select the **Process Tree** icon ({icon}`info`) to show the schema that created the Analyzer Graph view. The fields included are:

   * `SOURCE`: Indicates the data source—for example, `endpoint` or `winlogbeat`
   * `ID`: Event field that uniquely identifies a node
   * `EDGE`: Event field that indicates the relationship between two nodes

* Click the **Legend** icon ({icon}`node`) to show the state of each process node.

* Select a different data view ({icon}`index_settings`) to further filter the alert’s related events.

* Use the time filter ({icon}`calendar`) to analyze the event within a specific time range. By default, the selected time range matches that of the table from which you opened the alert.


* Click the list icon ({icon}`editor_unordered_list`) to open the preview analyzer panel. This displays a list of all processes related to the event, starting with the event chain’s first process. The **Analyzed Event**—the event you selected to analyze from the events list or Timeline—is highlighted with a light blue outline around the cube.

:::{image} /solutions/images/security-visual-event-analyzer.png
:alt: visual event analyzer
:screenshot:
:::


## Process and event details [process-and-event-details]

To learn more about each related process, select the process in the preview analyzer panel or the Analyzer Graph view. The preview analyzer panel then displays process details such as:

* The number of events associated with the process
* The timestamp of when the process was executed
* The file path of the process within the host
* The `process-pid`
* The user name and domain that ran the process
* Any other relevant process information
* Any associated alerts

:::{image} /solutions/images/security-process-details.png
:alt: process details
:screenshot:
:::

When you first select a process, it appears in a loading state. If loading data for a given process fails, click **Reload `{{process-name}}`** beneath the process to reload the data.

Access event details by selecting that event’s URL at the top of the process details view or choosing one of the event pills in the Analyzer Graph view. Events are categorized based on the `event.category` value.

When you select an `event.category` pill (for example, **_x_ file** or **_x_ registry**), all the events within that category are listed in the preview analyzer panel. To display more details about a specific event, select it from the list.

::::{note}
- You must have the appropriate [{{stack}}](https://www.elastic.co/pricing) subscription or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) to examine alerts associated with events.
- There is no limit to the number of events that can be associated with a process.
::::

To examine alerts associated with the event, select the alert pill (**_x_ alert**). The preview analyzer panel lists the total number of associated alerts, ordered from oldest to newest. Each alert shows the type of event that produced it (`event.category`), the event timestamp (`@timestamp`), and rule that generated the alert (`kibana.alert.rule.name`). Click on the rule name to open the alert’s details.

In the example screenshot, the analyzed event (`sdclt.exe`) generated three alerts. The preview analyzer panel displays basic information about each one.

:::{image} /solutions/images/security-alert-pill.png
:alt: alert pill
:screenshot:
:::
