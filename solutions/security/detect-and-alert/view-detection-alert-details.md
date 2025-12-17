---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/view-alert-details.html
  - https://www.elastic.co/guide/en/serverless/current/security-view-alert-details.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# View detection alert details [security-view-alert-details]

To learn more about an alert, click the **View details** button from the Alerts table. This opens the alert details flyout, which helps you understand and manage the alert.

Use the alert details flyout to begin an investigation, open a case, or plan a response. Click **Take action** at the bottom of the flyout to find more options for interacting with the alert.


## Alert details flyout UI [alert-details-flyout-ui]

The alert details flyout has a right panel, a preview panel, and a left panel. Each panel provides different information about the alert.


### Right panel [right-panel]

The right panel provides an overview. Expand any of the collapsed sections to learn more about the alert. You can also hover over fields on the **Overview** and **Table** tabs to display available [inline actions](/solutions/security/get-started/elastic-security-ui.md#inline-actions).

From the right panel, you can also:

* Click **Expand details** to open the [left panel](/solutions/security/detect-and-alert/view-detection-alert-details.md#left-panel), which shows more information about sections in the right panel.
* Click the history icon (![History icon](/solutions/images/security-history-icon.png "title =15x15")) to display a list of places that you visited from the alert's details flyout, for example, flyouts for other alerts or users. The list can contain up to 10 unique entries. Click any list entry to quickly access the item's details.
* Click the **Chat** icon (![AI assistant chat icon](/solutions/images/security-ai-assistant-chat.png "title =20x20")) to open [AI Assistant](/solutions/security/ai/ai-assistant.md).
* Click the **Share alert** icon (![Share alert icon](/solutions/images/security-share-alert.png "title =20x20")) to get a shareable alert URL. We *do not* recommend copying the URL from your browser’s address bar, which can lead to inconsistent results if you’ve set up filters or relative time ranges for the Alerts page.

    ::::{note}
    For {{stack}} users only:
    If you’ve configured the [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting in the [`kibana.yml`](/deploy-manage/stack-settings.md) file, the shareable URL is also in the `kibana.alert.url` field. You can find the field by searching for `kibana.alert.url` on the **Table** tab.
    ::::


    ::::{important}
    If you’ve enabled grouping on the Alerts page, the alert details flyout won’t open until you expand a collapsed group and select an individual alert.
    ::::

* Click the **Flyout settings** button (![Flyout settings icon](/solutions/images/security-flyout-settings.png "title =20x20")) to configure the flyout's appearance. 
  ![alert flyout settings menu](/solutions/images/security-alerts-flyout-settings-menu.png "")
  The **Overlay** option (which displays the flyout over the Alerts table) is selected by default. The **Push** option displays the flyout next to the table instead. In either display, you can resize the flyout panels to your liking. Clicking **Reset size** reverts the flyout to its default dimensions.
* Find basic details about the alert, such as the:

    * Associated rule
    * Alert status and when the alert was created
    * Alert severity and risk score (these are inherited from rule that generated the alert)
    * Users assigned to the alert (click the **Assign alert** ![Assign alert](/solutions/images/security-assign-alert.png "title =20x20") icon to assign more users)
    * Notes attached to the alert (click the **Add note** ![Add note](/solutions/images/security-add-note-icon.png "title =20x20") icon to create a new note)

* Click the **Table** or **JSON** tabs to display the alert details in table or JSON format. 
  * The **Table** tab shows alert data as field-value pairs. 
  * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1.0` Click the **Pin** button to the left of a field's name to pin the field to the top of the table. Click the **Table settings** button (![Flyout settings icon](/solutions/images/security-flyout-settings.png "title =20x20")) to view additional options:

    * **Show highlighted fields only:** Hide all fields other than highlighted fields. To learn more about highlighted fields, refer to [Investigation](#investigation-section).
    * **Hide empty fields:** Hide all fields that do not have values.
    * **Hide {{kib}} alert fields:** Hides fields that start with `kibana.alert` or `signal`. These fields provide metadata about the alert's lifecycle and operational context. You can hide them to help focus on the fields most relevant to your investigation. 
    ![alert flyout table settings menu](/solutions/images/security-alerts-flyout-table.png "")


  * The **JSON** tab shows alert data in raw JSON format. You can click **Copy to clipboard** to easily export it. 

### Preview panel [preview-panel]

Some areas in the flyout provide previews when you click on them. For example, clicking **Show rule summary** in the rule description displays a preview of the rule’s details. To close the preview, click **Back** or **x**.

### Left panel [left-panel]

The left panel provides an expanded view of what’s shown in the right panel. To open the left panel, do one of the following:

* Click **Expand details** at the top of the right panel.
* Click one of the section titles on the **Overview** tab within the right panel.

## About [about-section]

The About section appears on the **Overview** tab in the right panel. It provides a brief description of the rule that’s related to the alert and an explanation of what generated the alert.

The About section has the following information:

* **Rule description**: Describes the rule’s purpose or detection goals. Click **Show rule summary** to display a preview of the rule’s details. From the preview, click **Show rule details** to view the rule’s details page.
* **Alert reason**: Describes the source event that generated the alert. Event details are displayed in plain text and ordered logically to provide context for the alert. Click **Show full reason** to display the alert reason in the event rendered format within the [preview panel](/solutions/security/detect-and-alert/view-detection-alert-details.md#preview-panel).

    ::::{note}
    The event renderer only displays if an event renderer exists for the alert type. Fields are interactive; hover over them to access the available actions.
    ::::

* **Last alert status change**: Shows the last time the alert’s status was changed, along with the user who changed it.


## Investigation [investigation-section]

The Investigation section is located on the **Overview** tab in the right panel. It offers a couple of ways to begin investigating the alert.

The Investigation section provides the following information:

* **Investigation guide**: The **Show investigation guide** button displays if the rule associated with the alert has an investigation guide. Click the button to open the expanded Investigation view in the left panel.

    ::::{tip}
    Add an [investigation guide](/solutions/security/detect-and-alert/launch-timeline-from-investigation-guides.md#add-ig-actions-rule) to a rule when creating a new custom rule or modifying an existing custom rule’s settings.
    ::::

* **Highlighted fields**: Shows relevant fields for the alert and any [custom highlighted fields](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params) you added to the rule. Custom highlighted fields with values are added to this section. Those without values aren’t added.

    ::::{tip}
    {applies_to}`stack: ga 9.1` You can quickly add and remove custom highlighted fields from the rule by clicking **Add field** in the Highlighted fields table. 
    ::::

## Visualizations [visualizations-section]

The Visualizations section is located on the **Overview** tab in the right panel. It offers a glimpse of the processes that led up to the alert and occurred after it.

Click **Visualizations** to display the following previews:

* **Session view preview**: Shows a preview of [Session View](/solutions/security/investigate/session-view.md) data. Click **Session viewer preview** to open the **Session View** tab in Timeline.
* **Analyzer preview**: Shows a preview of the [visual analyzer graph](/solutions/security/investigate/visual-event-analyzer.md). The preview displays up to three levels of the analyzed event’s ancestors and up to three levels of the event’s descendants and children. The ellipses symbol (**`...`**) indicates the event has more ancestors and descendants to examine. Click **Analyzer preview** to open the **Event Analyzer** tab in Timeline.


### Expanded visualizations view [expanded-visualizations-view]

The **Visualize** tab allows you to maintain the context of the Alerts table, while providing a more detailed view of alerts that you’re investigating in the event analyzer or Session View. To open the tab, click **Session viewer preview** or **Analyzer preview** from the right panel.

As you examine the alert’s related processes, you can also preview the alerts and events which are associated with those processes. Then, if you want to learn more about a particular alert or event, you can click **Show full alert details** to open the full details flyout.

## Insights [insights-section]

The Insights section is located on the **Overview** tab in the right panel. It offers different perspectives from which you can assess the alert. Click **Insights** to display overviews for [related entities](/solutions/security/detect-and-alert/view-detection-alert-details.md#entities-overview), [threat intelligence](/solutions/security/detect-and-alert/view-detection-alert-details.md#threat-intelligence-overview), [correlated data](/solutions/security/detect-and-alert/view-detection-alert-details.md#correlations-overview), and [host and user prevalence](/solutions/security/detect-and-alert/view-detection-alert-details.md#prevalence-overview).


### Entities [entities-overview]

The Entities overview provides high-level details about the user and host that are related to the alert. Host and user risk classifications are also available with a [Platinum subscription](https://www.elastic.co/pricing) or higher in {{stack}} or the Security Analytics Complete [project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.

#### Expanded entities view [expanded-entities-view]

From the right panel, click **Entities** to open a detailed view of the host and user associated with the alert. The expanded view also includes risk scores and classifications and activity on related hosts and users. Access to these features requires a [Platinum subscription](https://www.elastic.co/pricing) or higher in {{stack}} or the Security Analytics Complete [project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}

### Threat intelligence [threat-intelligence-overview]

The Threat intelligence overview shows matched indicators, which provide threat intelligence relevant to the alert.

The Threat intelligence overview provides the following information:

* **Threat match detected**: Only available when examining an alert generated from an [indicator match](/solutions/security/detect-and-alert/create-detection-rule.md#create-indicator-rule) rule. Shows the number of matched indicators that are present in the alert document. Shows zero if there are no matched indicators or you’re examining an alert generated by another type of rule.
* **Fields enriched with threat intelligence**: Shows the number of matched indicators that are present on an alert that *wasn’t* generated from an indicator match rule. If none exist, the total number of matched indicators is zero.


#### Expanded threat intelligence view [expanded-threat-intel-view]

From the right panel, click **Threat intelligence** to open the expanded Threat intelligence view within the left panel.

::::{note}
The expanded threat intelligence view queries indices specified in the `securitySolution:defaultThreatIndex` advanced setting. Refer to [Update default Elastic Security threat intelligence indices](/solutions/security/get-started/configure-advanced-settings.md#update-threat-intel-indices) to learn more about threat intelligence indices.
::::

The expanded Threat intelligence view shows individual indicators within the alert document. You can expand and collapse indicator details by clicking the arrow button at the end of the indicator label. Each indicator is labeled with values from the `matched.field` and `matched.atomic` fields and displays the threat intelligence provider.

Matched threats are organized into two sections, described below. Within each section, matched threats are shown in reverse chronological order, with the most recent at the top. All mapped fields are displayed for each matched threat.

**Threat match detected**

The Threat match detected section is only populated with indicator match details if you’re examining an alert that was generated from an indicator match rule. Indicator matches occur when alert field values match with threat intelligence data you’ve ingested.

**Fields enriched with threat intelligence**

Threat intelligence can also be found on alerts that weren’t generated from indicator match rules. To find this information, {{elastic-sec}} queries alert documents from the past 30 days and searches for fields that contain known threat intelligence. If any are found, they’re logged in this section.

::::{tip}
Use the date time picker to modify the query time frame, which looks at the past 30 days by default. You can also click the **Inspect** button to examine the query that the Fields enriched with threat intelligence section uses.
::::


When searching for threat intelligence, {{elastic-sec}} queries the alert document for the following fields:

* `file.hash.md5`: The MD5 hash
* `file.hash.sha1`: The SHA1 hash
* `file.hash.sha256`: The SHA256 hash
* `file.pe.imphash`: Imports in a PE file
* `file.elf.telfhash`: Imports in an ELF file
* `file.hash.ssdeep`: The SSDEEP hash
* `source.ip`: The IP address of the source (IPv4 or IPv6)
* `destination.ip`: The event’s destination IP address
* `url.full`: The full URL of the event source
* `registry.path`: The full registry path, including the hive, key, and value


### Correlations [correlations-overview]

The Correlations overview shows how an alert is related to other alerts and offers ways to investigate related alerts. Use this information to quickly find patterns between alerts and then take action.

The Correlations overview provides the following information:

* **Suppressed alerts**: Indicates that the alert was created with alert suppression, and shows how many duplicate alerts were suppressed. This information only appears if alert suppression is enabled for the rule.
* **Alerts related by source event**: Shows the number of alerts that were created by the same source event.
* **Cases related to the alert**: Shows the number of cases to which the alert has been added.
* **Alerts related by session ID**: Shows the number of alerts generated by the same session.
* **Alerts related by process ancestry**: Shows the number of alerts that are related by process events on the same linear branch.

    ::::{note}
    To access data about alerts related by process ancestry, you must have a [Platinum or higher subscription](https://www.elastic.co/pricing) in {{stack}} or the appropriate [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
    ::::



#### Expanded correlations view [expanded-correlations-view]

From the right panel, click **Correlations** to open the expanded Correlations view within the left panel.

In the expanded view, corelation data is organized into several tables:

* **Suppressed alerts**: Shows how many duplicate alerts were suppressed. This information only appears if [alert suppression](/solutions/security/detect-and-alert/suppress-detection-alerts.md) is enabled for the rule.
* **Related cases**: Shows cases to which the alert has been added. Click a case’s name to open its details.
* **Alerts related by source event**: Shows alerts created by the same source event. This can help you find alerts with a shared origin and provide more context about the source event. Click the **Investigate in timeline** button to examine related alerts in Timeline.
* **Alerts related by session**: Shows alerts generated during the same [session](/solutions/security/investigate/session-view.md). These alerts share the same session ID, which is a unique ID for tracking a given Linux session. To use this feature, you must enable the **Collect session data** setting in your {{elastic-defend}} integration policy. Refer to [Enable Session View data](/solutions/security/investigate/session-view.md#enable-session-view) for more information.
* **Alerts related by ancestry**: Shows alerts that are related by process events on the same linear branch. Note that alerts generated from processes on child or related branches are not shown. To further examine alerts, click **Investigate in timeline**.


### Prevalence [prevalence-overview]

The Prevalence overview shows whether data from the alert was frequently observed on other host events from the last 30 days. Prevalence calculations use values from the alert’s highlighted fields. Highlighted field values that are observed on less than 10% of hosts in your environment are considered uncommon (not prevalent) and are listed individually in the Prevalence overview. Highlighted field values that are observed on more than 10% of hosts in your environment are considered common (prevalent) and are described as frequently observed in the Prevalence overview.


#### Expanded prevalence view [expanded-prevalence-view]

From the right panel, click **Prevalence** to open the expanded Prevalence view within the left panel. Examine the table to understand the alert’s relationship with other alerts, events, users, and hosts.

::::{tip}
Update the date time picker for the table to show data from a different time range.
::::

The expanded Prevalence view provides the following details:

* **Field**: Shows [highlighted fields](/solutions/security/detect-and-alert/view-detection-alert-details.md#investigation-section) for the alert and any custom highlighted fields that were added to the alert’s rule.
* **Value**: Shows values for highlighted fields and any custom highlighted fields that were added to the alert’s rule.
* **Alert count**: Shows the total number of alert documents that have identical highlighted field values, including the alert you’re currently examining. For example, if the `host.name` field has an alert count of 5, that means there are five total alerts with the same `host.name` value. The Alert count column only retrieves documents that contain the [`event.kind:signal`](ecs://reference/ecs-allowed-values-event-kind.md#ecs-event-kind-signal) field-value pair.
* **Document count**: Shows the total number of event documents that have identical field values. A dash (`——`) displays if there are no event documents that match the field value. The Document count column only retrieves documents that don’t contain the [`event.kind:signal`](ecs://reference/ecs-allowed-values-event-kind.md#ecs-event-kind-signal) field-value pair.

The following features require a [Platinum subscription](https://www.elastic.co/pricing) or higher in {{stack}} or the appropriate [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md)

* **Host prevalence**: Shows the percentage of unique hosts that have identical field values. Host prevalence for highlighted fields is calculated by taking the number of unique hosts with identical highlighted field values and dividing that number by the total number of unique hosts in your environment.
* **User prevalence**: Shows the percentage of unique users that have identical highlighted field values. User prevalence for highlighted fields is calculated by taking the number of unique users with identical field values and dividing that number by the total number of unique users in your environment.


## Response [response-overview]

The **Response** section is located on the **Overview** tab in the right panel. It shows [response actions](/solutions/security/detect-and-alert/create-detection-rule.md) that were added to the rule associated with the alert. Click **Response** to display the response action’s results in the left panel.

## Notes [expanded-notes-view]

The **Notes** tab (located in the left panel) shows all notes attached to the alert, in addition to the user who created them and when they were created. When you add a new note, the alert’s summary also updates and shows how many notes are attached to the alert.

::::{tip}
Go to the **Notes** [page](/solutions/security/investigate/notes.md#manage-notes) to find notes that were added to other alerts.
::::

