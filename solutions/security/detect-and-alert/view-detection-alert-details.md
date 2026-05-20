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
description: Use the alert details flyout to investigate, manage, and respond to detection alerts in Elastic Security.
---

# View detection alert details [security-view-alert-details]

To learn more about an alert, click the **View details** icon ({icon}`expand`) from the Alerts table. This opens the alert details flyout, which helps you understand and manage the alert.

Use the alert details flyout to begin an investigation, open a case, or plan a response. Click **Take action** at the bottom of the flyout to find more options for interacting with the alert.


## Alert details flyout UI [alert-details-flyout-ui]

The alert details flyout has a right panel, a preview panel, and a left panel. Each panel provides different information about the alert.


### Right panel [right-panel]

The right panel provides an overview of the alert. Expand collapsed sections to see more details, or hover over fields on the **Overview** and **Table** tabs to access [inline actions](/solutions/security/get-started/elastic-security-ui.md#inline-actions).

::::{important}
If you've enabled grouping on the Alerts page, expand a group and select an individual alert to open the flyout.
::::

#### Toolbar actions

| Icon | Name | Action |
|------|------|--------|
| {icon}`arrow_down` | Expand details | Open the [left panel](#left-panel) for deeper investigation of each section. |
| {icon}`clockCounter` | History | View up to 10 recently visited flyouts (alerts, users, etc.) and click to navigate back. |
| {icon}`new_chat` | Chat | Open [AI Assistant](/solutions/security/ai/ai-assistant.md). |
| {icon}`share` | Share alert | Get a shareable URL. Don't copy from the browser address bar. It might include filters or relative time ranges that produce inconsistent results. |
| {icon}`gear` | Flyout settings | Choose **Overlay** (flyout over table) or **Push** (flyout beside table). You can resize panels and click **Reset size** to restore defaults. |

::::{note}
:applies_to:{stack: ga}
If you've configured [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) in `kibana.yml`, the shareable URL also appears in the `kibana.alert.url` field on the **Table** tab.
::::

#### Alert details

The header displays key alert information:

* **Rule**: The rule that generated the alert
* **Status**: Current alert status and creation time
* **Severity and risk score**: Inherited from the rule
* **Assignees**: Users assigned to the alert (click the **Add** icon {icon}`plus_in_circle` to add more)
* **Notes**: Attached notes (click the **Add** icon {icon}`plus_in_circle` to add a note)

#### View formats

Switch between tabs to view alert data in different formats:

**Table tab**

Shows alert fields as name-value pairs. 

{applies_to}`stack: ga 9.1.0` Click {icon}`pin` next to a field to pin it to the top.

Click {icon}`gear` **Table settings** for additional options:

| Setting | Description |
|---------|-------------|
| Show highlighted fields only | Display only [highlighted fields](#investigation-section). |
| Hide empty fields | Hide fields without values. |
| Hide {{kib}} alert fields | Hide `kibana.alert` and `signal` fields to focus on investigation-relevant data. |

![alert flyout table settings menu](/solutions/images/security-alerts-flyout-table.png "")

**JSON tab**

Shows raw JSON. Click **Copy to clipboard** to export.

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

The Investigation section (on the **Overview** tab) provides starting points for investigating the alert.

| Section | What it provides | How to use it |
|-----------|------------------|---------------|
| Investigation guide | Step-by-step instructions written for this rule type. Only appears if the rule has an [investigation guide](/solutions/security/detect-and-alert/write-investigation-guides.md). | Click **Show investigation guide** to open the guide in the left panel. Follow the steps to investigate systematically. |
| Highlighted fields | Key fields relevant to the alert, plus any [custom highlighted fields](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) defined in the rule. | Review these fields first to quickly understand what triggered the alert. Fields without values are hidden. |

::::{tip}
{applies_to}`stack: ga 9.1` Click **Add field** in the Highlighted fields table to add or remove custom highlighted fields directly from the alert flyout.
::::

## Visualizations [visualizations-section]

The Visualizations section (on the **Overview** tab) shows processes that led to the alert and what happened after. Use these previews to understand the attack chain without leaving the alert flyout.

| Section | What it shows | How to use it |
|---------|---------------|---------------|
| Session view preview| Process activity during the Linux session | See commands executed before and after the alert. Click to open Session View in Timeline for the full session history. |
| Analyzer preview | Process tree (up to 3 ancestor and 3 descendant levels) | Trace how the process was spawned and what it launched. The {icon}`boxes_horizontal` icon indicates more levels exist. Click to open Event Analyzer in Timeline. |


### Expanded visualizations view [expanded-visualizations-view]

Click either preview to open the **Visualize** tab, which provides a detailed view while keeping the Alerts table visible. From here you can:

* Examine related processes and their associated alerts or events
* Click **Show full alert details** on any related item to investigate it further


## Insights [insights-section]

The Insights section is located on the **Overview** tab in the right panel. It offers different perspectives from which you can assess the alert. Click **Insights** to display overviews for related entities, threat intelligence, correlated data, and host and user prevalence.


### Entities [entities-overview]

The Entities overview provides high-level details about the user and host that are related to the alert. Host and user risk classifications are also available with a [Platinum subscription](https://www.elastic.co/pricing) or higher in {{stack}} or the Security Analytics Complete [project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.

#### Expanded entities view [expanded-entities-view]

From the right panel, click **Entities** to open a detailed view of the host and user associated with the alert. The expanded view also includes risk scores and classifications and activity on related hosts and users. Access to these features requires a [Platinum subscription](https://www.elastic.co/pricing) or higher in {{stack}} or the Security Analytics Complete [project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}

### Threat intelligence [threat-intelligence-overview]

The Threat intelligence overview shows matched indicators, which provide threat intelligence relevant to the alert. It provides the following information:

* **Threat match detected**: Only available when examining an alert generated from an [indicator match](/solutions/security/detect-and-alert/indicator-match.md) rule. Shows the number of matched indicators that are present in the alert document. Shows zero if there are no matched indicators or you’re examining an alert generated by another type of rule.
* **Fields enriched with threat intelligence**: Shows the number of matched indicators that are present on an alert that *wasn’t* generated from an indicator match rule. If none exist, the total number of matched indicators is zero.


#### Expanded threat intelligence view [expanded-threat-intel-view]

Click **Threat intelligence** in the right panel to open the expanded view, which shows details for each matched indicator. Indicators are listed with the most recent first, and you can expand any indicator to see all its mapped fields.

The view organizes matches into two sections:

| Section | What it shows | How to use it |
|---------|---------------|---------------|
| Threat match detected | Indicators that triggered an [indicator match rule](/solutions/security/detect-and-alert/indicator-match.md). Only appears for alerts from indicator match rules. | Review which specific indicators matched to confirm the threat and assess severity. |
| Fields enriched with threat intelligence | Indicators found by scanning alert fields against your threat intelligence indices. Applies to any rule type. | Check if known malicious IPs, hashes, or URLs appear in the alert. Use the date picker to adjust the search time frame, or click **Inspect** to view the query. |

::::{note}
This view queries the threat intelligence indices defined in [`securitySolution:defaultThreatIndex`](/solutions/security/get-started/configure-advanced-settings.md#update-threat-intel-indices).
::::

{{elastic-sec}} checks the following alert fields for matches against your threat intelligence data:

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

The Correlations section reveals connections between alerts, helping you identify attack patterns and scope the impact of a threat. Use correlations to answer questions like: Is this alert part of a larger attack? What other suspicious activity occurred during the same session? Has this alert already been investigated?

The overview displays counts for each correlation type. Click **Correlations** to open the expanded view with full details.

| Correlation type | What it tells you | How to use it |
|------------------|-------------------|---------------|
| Suppressed alerts | The rule uses [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md), and this alert represents multiple duplicate detections. | Check the suppression count to understand the true volume of matching events. A high count may indicate an ongoing attack or a noisy rule that needs tuning. |
| Alerts related by source event | Multiple rules triggered on the same underlying event. | Review related alerts to see if different rules detected complementary aspects of the same threat. This helps you understand the full context of a single suspicious event. |
| Cases related to the alert | This alert has been added to one or more cases. | Click a case name to see prior investigation work. Avoid duplicating effort if the alert is already being tracked. |
| Alerts related by session ID | Other alerts occurred during the same Linux session. | Examine the session timeline to trace an attacker's actions from initial access through their objectives. Requires [Session View data](/solutions/security/investigate/session-view.md#enable-session-view) to be enabled. |
| Alerts related by process ancestry | Alerts share a parent-child process relationship. | Trace execution chains to understand how a threat propagated. Click **Investigate in timeline** to visualize the process tree. |

::::{note}
**Alerts related by process ancestry** requires a [Platinum or higher subscription](https://www.elastic.co/pricing) in {{stack}} or the appropriate [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
::::


### Prevalence [prevalence-overview]

The Prevalence overview shows whether data from the alert was frequently observed on other host events from the last 30 days. Prevalence calculations use values from the alert’s highlighted fields. Highlighted field values that are observed on less than 10% of hosts in your environment are considered uncommon (not prevalent) and are listed individually in the Prevalence overview. Highlighted field values that are observed on more than 10% of hosts in your environment are considered common (prevalent) and are described as frequently observed in the Prevalence overview.


#### Expanded prevalence view [expanded-prevalence-view]

From the right panel, click **Prevalence** to open the expanded Prevalence view within the left panel. Examine the table to understand the alert’s relationship with other alerts, events, users, and hosts.

::::{tip}
Update the date time picker for the table to show data from a different time range.
::::

The expanded Prevalence view displays a table with the following columns:

| Column | What it shows | How to use it |
|--------|---------------|---------------|
| Field | [Highlighted fields](#investigation-section) and custom highlighted fields from the rule. | Identify which fields are being evaluated for prevalence. |
| Value | The actual values for each highlighted field. | See the specific data being compared across your environment. |
| Alert count | Number of alerts with identical field values (including this alert). | High counts suggest a widespread issue or a noisy detection. Low counts may indicate targeted activity. |
| Document count | Number of non-alert events with identical field values. A dash (`——`) means no matches. | Compare alert volume against normal event volume to assess signal-to-noise ratio. |
| Host prevalence | Percentage of hosts with identical field values. Requires [Platinum subscription](https://www.elastic.co/pricing) or higher. | Low percentages (uncommon values) may indicate suspicious activity. |
| User prevalence | Percentage of users with identical field values. Requires [Platinum subscription](https://www.elastic.co/pricing) or higher. | Uncommon user activity patterns can reveal compromised accounts. |


## Response [response-overview]

The **Response** section is located on the **Overview** tab in the right panel. It shows [response actions](/solutions/security/detect-and-alert/using-the-rule-ui.md) that were added to the rule associated with the alert. Click **Response** to display the response action’s results in the left panel.

## Notes [expanded-notes-view]

The **Notes** tab (located in the left panel) shows all notes attached to the alert, in addition to the user who created them and when they were created. When you add a new note, the alert’s summary also updates and shows how many notes are attached to the alert.

::::{tip}
Go to the **Notes** [page](/solutions/security/investigate/notes.md#manage-notes) to find notes that were added to other alerts.
::::

