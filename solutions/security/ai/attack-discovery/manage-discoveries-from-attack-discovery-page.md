---
navigation_title: Manage from Attack Discovery page
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage discoveries from the Attack Discovery page [manage-discoveries]

Use this page when you are a SOC analyst managing saved discoveries from the dedicated **Attack Discovery** page. Change status, share, bulk-act on, and search discoveries there. For guidance on which page to use for your version, refer to [Manage saved discoveries](/solutions/security/ai/attack-discovery/manage-saved-discoveries.md).

:::{note}
:applies_to: {"stack": "preview =9.4, ga 9.5+", "serverless": "ga"}
To triage discoveries next to their related alerts, and to assign or tag them, use the [Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) at **Detections > Views > Attacks** instead.
:::

## Change a discovery's status [discovery-status]

You can set a discovery's status to indicate that it's under active investigation or that it's been resolved:

| Status | Meaning |
|--------|---------|
| Open | Needs investigation (default) |
| Acknowledged | Under active investigation |
| Closed | Resolved |

Attacks on the [Attacks page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md) use this same status lifecycle.

To change a discovery's status, click **Take action**, then select **Mark as acknowledged** or **Mark as closed**. You can choose to change the status of only the discovery, or of both the discovery and the alerts associated with it.

## Share discoveries [share-attack-discoveries]

By default, scheduled discoveries are shared with all users in a {{kib}} space.

Manually generated discoveries are private by default. To share them, change **Not shared** to **Shared** next to the discovery's name.

:::{note}
Once a discovery is shared, its visibility cannot be changed.
:::

## Take bulk actions [take-bulk-actions]

You can take bulk actions on multiple discoveries, such as bulk-changing their status or adding them to a case. To do this, select the checkboxes next to each discovery, then click **Selected *x* Attack discoveries** and choose the action you want to take.

## Search and filter saved discoveries [search-filter-discoveries]

You can search and filter saved discoveries to help locate relevant findings.

* Use the search box to perform full-text searches across your generated discoveries.

* **Visibility**: Use this filter to, for example, show only [shared](#share-attack-discoveries) discoveries.

* **Status**: Filter discoveries by their [current status](#discovery-status).

* **Connector**: Filter discoveries by connector name. Connectors that are deleted after discoveries have been generated are shown with a **Deleted** tag.

* Time filter: Adjust the time filter to view discoveries generated within a specific timeframe.

## Incorporate discoveries with other workflows [attack-discovery-workflows]

There are several ways you can incorporate discoveries into your {{elastic-sec}} workflows:

* Click an entity’s name to open the entity details flyout and view more details that may be relevant to your investigation.
* Hover over an entity’s name to either add the entity to Timeline (![Add to timeline icon](/solutions/images/security-icon-add-to-timeline.png "title =20x20")) or copy its field name and value to the clipboard (![Copy to clipboard icon](/solutions/images/security-icon-copy.png "title =20x20")).
* Click **Take action**, then select **Add to new case** or **Add to existing case** to add a discovery to a [case](/solutions/security/investigate/security-cases.md). This makes it easy to share the information with your team and other stakeholders.
* Click **Investigate in timeline** to explore the discovery in [Timeline](/solutions/security/investigate/timeline.md).
* Click **View in AI Assistant** or **Add to chat** to attach the discovery to a conversation. You can then ask follow-up questions about the discovery or associated alerts.
* **Automate the triage end-to-end** with [Elastic Workflows](/explore-analyze/workflows.md). The [AI-driven alert triage workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md) shows how to invoke an Agent Builder agent on each discovery, open a case populated with the analysis, isolate the affected host, and notify the SOC.

:::{image} /solutions/images/security-add-discovery-to-assistant.gif
:alt: Attack Discovery view in AI Assistant
:width: 60%
:::
