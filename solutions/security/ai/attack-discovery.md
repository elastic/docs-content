---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/attack-discovery.html
  - https://www.elastic.co/guide/en/serverless/current/attack-discovery.html
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Attack Discovery

Attack Discovery leverages large language models (LLMs) to analyze alerts in your environment and identify threats. Each "discovery" represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible. This can help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond.

For a demo, refer to the following video (click to view).

[![Attack Discovery video](https://play.vidyard.com/eT92arEbpRddmSM4JeyzdX.jpg)](https://videos.elastic.co/watch/eT92arEbpRddmSM4JeyzdX?)


## Role-based access control (RBAC) for Attack Discovery [attack-discovery-rbac]

To use Attack Discovery, your role needs specific privileges.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.3+", "serverless": "ga" }

Ensure your role has:

* `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack Discover** {{kib}} feature and at least `Read` privileges for the **Security > Rules** {{kib}} feature.

    ![attack-discovery-rules-rbac](/solutions/images/attack-discovery-rules-rbac.png "elasticsearch =60%x60%")

* The appropriate [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges), based on what you want to do with Attack Discovery alerts:

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br> - `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts. This includes:<br>- Generating discovery alerts manually<br>- Generating discovery alerts using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status |- `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read`, `view_index_metadata`, `write`, and `maintenance`|

:::

:::{applies-item} stack: ga 9.1-9.2

Ensure your role has:

* `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack Discover** {{kib}} feature.

    ![attack-discovery-rbac](/solutions/images/security-attck-disc-rbac.png)

* The appropriate [index privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges), based on what you want to do with Attack Discovery alerts:

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br> - `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts. This includes:<br>- Generating discovery alerts manually<br>- Generating discovery alerts using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status |- `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read`, `view_index_metadata`, `write`, and `maintenance`|

:::

:::{applies-item} stack: ga =9.0

Ensure your role has `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack Discover** {{kib}} feature.

![attack-discovery-rbac](/solutions/images/security-attck-disc-rbac.png)

:::

::::


## Set up Attack Discovery

By default, Attack Discovery analyzes up to 100 alerts from the last 24 hours, but you can customize how many and which alerts it analyzes using the settings menu. To open it, click the settings icon next to the **Run** button.

:::{note}
In {{stack}} 9.0.0 and earlier, the **Run** button is called **Generate**.
:::

::::{image} /solutions/images/security-attack-discovery-settings.png
:alt: Attack Discovery's settings menu
:width: 500px
::::

You can select which alerts Attack Discovery will process by filtering based on a KQL query, the time and date selector, and the **Number of alerts** slider. Note that sending more alerts than your chosen LLM can handle may result in an error. Under **Alert summary** you can view a summary of the selected alerts grouped by various fields, and under **Alerts preview** you can see more details about the selected alerts.

:::{admonition} How to add non-ECS fields to Attack Discovery
Attack Discovery is designed for use with alerts based on data that complies with ECS, and by default only analyses ECS-compliant fields. However, you can enable Attack Discovery to review additional fields by following these steps:

1.  Select an alert with some of the non-ECS fields you want to analyze, and go to its details flyout. From here, use the **Ask AI Assistant** button to open AI Assistant.
2.  At the bottom of the chat window, the alert's information appears. Click **Edit** to open the anonymization window to this alert's fields.
3.  Search for and select the non-ECS fields you want Attack Discovery to analyze. Set them to **Allowed**.
4.  Check the `Update presets` box to add the allowed fields to the space's default anonymization settings.

The next time you run Attack Discovery it will be able to analyze the selected fields.
:::

## Generate discoveries manually[attack-discovery-generate-discoveries]

You’ll need to select an LLM connector before you can analyze alerts. To get started:

1. Click the **Attack Discovery** page from {{elastic-sec}}'s navigation menu.
2. Do one of the following:
   - {applies_to}`stack: ga 9.1` Click the settings icon next to the **Run** button, then in the settings menu, select an existing connector from the dropdown menu, or add a new one.
   - {applies_to}`stack: ga 9.0` Select an existing connector from the dropdown menu, or add a new one.

   :::{admonition} Recommended models
   While Attack Discovery is compatible with many different models, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) to see which models perform best.

   :::


    :::{image} /solutions/images/security-attck-disc-select-model-empty.png
    :alt: attck disc select model empty
    :::

3. Once you’ve selected a connector, do one of the following to start the analysis:
   - {applies_to}`stack: ga 9.1` Click **Save and run**.
   - {applies_to}`stack: ga 9.0` Click **Generate**.
   
It may take from a few seconds up to several minutes to generate discoveries, depending on the number of alerts and the model you selected. Once the analysis is complete, any threats it identifies will appear as discoveries. Click each one’s title to expand or collapse it. Click **Run** at any time to start the Attack Discovery process again with the selected alerts.

::::{important}
Attack Discovery uses the same data anonymization settings as [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md). To configure which alert fields are sent to the LLM and which of those fields are obfuscated, use the Elastic AI Assistant settings. Consider the privacy policies of third-party LLMs before sending them sensitive data.
::::


## What information does each discovery include? [attack-discovery-what-info]

Each discovery includes the following information describing the potential threat, generated by the connected LLM:

1. A descriptive title and a summary of the potential threat.
2. The number of associated alerts and which parts of the [MITRE ATT&CK matrix](https://attack.mitre.org/) they correspond to.
3. The implicated entities (users and hosts), and what suspicious activity was observed for each.

:::{image} /solutions/images/security-attck-disc-example-disc.png
:alt: Attack Discovery detail view
:::


## Incorporate discoveries with other workflows [attack-discovery-workflows]

There are several ways you can incorporate discoveries into your {{elastic-sec}} workflows:

* Click an entity’s name to open the entity details flyout and view more details that may be relevant to your investigation.
* Hover over an entity’s name to either add the entity to Timeline (![Add to timeline icon](/solutions/images/security-icon-add-to-timeline.png "title =20x20")) or copy its field name and value to the clipboard (![Copy to clipboard icon](/solutions/images/security-icon-copy.png "title =20x20")).
* Click **Take action**, then select **Add to new case** or **Add to existing case** to add a discovery to a [case](/solutions/security/investigate/cases.md). This makes it easy to share the information with your team and other stakeholders.
* Click **Investigate in timeline** to explore the discovery in [Timeline](/solutions/security/investigate/timeline.md).
* Click **View in AI Assistant** to attach the discovery to a conversation with AI Assistant. You can then ask follow-up questions about the discovery or associated alerts.

:::{image} /solutions/images/security-add-discovery-to-assistant.gif
:alt: Attack Discovery view in AI Assistant
:::

## Schedule discoveries

```yaml {applies_to}
stack: ga 9.1
```

You can define recurring schedules (for example, daily or weekly) to automatically generate attack discoveries without needing manual runs. For example, you can generate discoveries every 24 hours and send a Slack notification to your SecOps channel if discoveries are found. Notifications are sent using configured [connectors](/deploy-manage/manage-connectors.md), such as Slack or email, and you can customize the notification content to tailor alert context to your needs.

:::{note}
You can still generate discoveries manually at any time, regardless of an active schedule.
:::

To create a new schedule:

1. In the top-right corner, select **Schedule**.
2. In the **Attack discovery schedule** flyout, select **Create new schedule**.
3. Enter a name for the new schedule.
4. Select the LLM connector to use for generating discoveries, or add a new one.
5. Use the KQL query bar, time filter, and alerts slider to customize the set of alerts that will be analyzed.
6. Define the schedule's frequency (for example, every 24 hours).
7. Optionally, select the [connectors](/deploy-manage/manage-connectors.md) to use for receiving notifications, and define their actions.
8. Click **Create & enable schedule**.

After creating new schedules, you can view their status, modify them or delete them from the **Attack discovery schedule** flyout.

:::{tip}
Scheduled discoveries are shown with a **Scheduled Attack discovery** icon ({icon}`calendar`). Click the icon to view the schedule that created it.
:::

## View saved discoveries

```yaml {applies_to}
stack: ga 9.1
```

Attack discoveries are automatically saved on the **Attack Discovery** page each time you generate them. Once saved, discoveries remain available for later review, reporting, and tracking over time. This allows you to revisit discoveries to monitor trends, maintain audit trails, and support investigations as your environment evolves.

### Change a discovery's status

You can set a discovery's status to indicate that it's under active investigation or that it's been resolved. To do this, click **Take action**, then select **Mark as acknowledged** or **Mark as closed**.

You can choose to change the status of only the discovery, or of both the discovery and the alerts associated with it.

### Share attack discoveries

By default, scheduled discoveries are shared with all users in a {{kib}} space.

Manually generated discoveries are private by default. To share them, change **Not shared** to **Shared** next to the discovery's name.

:::{note}
Once a discovery is shared, its visibility cannot be changed.
:::

### Take bulk actions

You can take bulk actions on multiple discoveries, such as bulk-changing their status or adding them to a case. To do this, select the checkboxes next to each discovery, then click **Selected *x* Attack discoveries** and choose the action you want to take.

### Search and filter saved discoveries

You can search and filter saved discoveries to help locate relevant findings.

* Use the search box to perform full-text searches across your generated discoveries.

* **Visibility**: Use this filter to, for example, show only shared discoveries.

* **Status**: Filter discoveries by their current status.

* **Connector**: Filter discoveries by connector name. Connectors that are deleted after discoveries have been generated are shown with a **Deleted** tag.

* Time filter: Adjust the time filter to view discoveries generated within a specific timeframe.

