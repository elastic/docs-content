---
applies_to:
  stack: ga 9.1+
  serverless:
    security: ga
description: Explore security alerts and events using the Security-specific Discover experience in Kibana.
products:
  - id: security
  - id: cloud-serverless
---

# Explore Security data in Discover

**Discover** provides a Security-specific experience for exploring alert and event data. When the Security experience is active, Discover adds color-coded row indicators, security-focused default columns, and contextual alert and event details when you expand a document.

For general **Discover** concepts and features, refer to [](/explore-analyze/discover.md).


:::{image} /solutions/images/security-discover-profile.png
:screenshot:
:alt: Discover with the Security solution default data view selected.
:::

## Access the Security Discover experience

How the Security experience activates depends on your deployment type:

- {applies_to}`security: ga` The Security experience activates automatically when you open **Discover** from your {{sec-serverless}} project.
- {applies_to}`stack: ga` The Security experience activates when you open **Discover** from the {{elastic-sec}} [solution view](/deploy-manage/manage-spaces.md).

## Security-specific Discover features

With the Security experience active, **Discover** adds the following features to help you triage and investigate alerts and events.

### Row indicators

Color-coded indicators appear on the left side of each row in the data table, helping you distinguish between alerts and events at a glance:

- **Alerts**: Yellow indicator
- **Events**: Gray indicator

### Default columns for alert data

When you use a {{data-source}} that includes security alerts data, such as the default {{elastic-sec}} {{data-source}}, **Discover** displays pre-configured columns optimized for alert triage.

### Alert and event details flyout

When you expand an alert or event row in **Discover**, a details flyout opens. The flyout experience varies by version.

::::{applies-switch}
:::{applies-item} { "stack": "ga 9.4", "serverless": "ga" }

The document flyout includes an overview tab, plus **Table** and **JSON** tabs. The **Take action** button at the bottom lets you interact with the document.

For alerts, the header also displays the status, risk score, assignees, and attached notes. Click **Add note** to open the [Notes](/solutions/security/detect-and-alert/view-detection-alert-details.md#expanded-notes-view) flyout, where you can view and add notes using a markdown editor.

The overview tab includes the following sections:

**About**
:   A description of the document. For alerts, shows the rule description and the reason the alert was generated. For events, shows the ECS event category description.

**Investigation**
:   Highlighted fields relevant to the document. For alerts, also includes a link to the [investigation guide](/solutions/security/detect-and-alert/view-detection-alert-details.md#investigation-section) if one is defined for the rule.

**Visualizations**
:   Previews showing process activity. Click either preview to open a dedicated flyout with a full view:

    - [Session View](/solutions/security/investigate/session-view.md): Shows process activity during the Linux session, including commands executed before and after the alert.
    - [Analyzer](/solutions/security/investigate/visual-event-analyzer.md): Shows a process tree of the events that led to the alert, including parent and child processes.

**Insights**
:   Overviews of threat intelligence matches, correlated alerts, and prevalence data. Click any subsection to open a dedicated flyout.

    - **Threat intelligence**: Matched indicators from indicator match rules, and fields enriched with threat intelligence. Appears for alerts only. For details on what this view shows, refer to [Threat intelligence](/solutions/security/detect-and-alert/view-detection-alert-details.md#threat-intelligence-overview).
    - **Correlations**: Related cases and correlated alerts, grouped by source event, session, and process ancestry. For details on what this view shows, refer to [Correlations](/solutions/security/detect-and-alert/view-detection-alert-details.md#correlations-overview).
    - **Prevalence**: How common alert field values are across your environment, with alert counts, document counts, and host and user prevalence percentages. For details on what this view shows, refer to [Prevalence](/solutions/security/detect-and-alert/view-detection-alert-details.md#prevalence-overview).

:::

:::{applies-item} stack: ga 9.1-9.3

The document flyout includes an overview tab, plus **Table** and **JSON** tabs. The overview tab surfaces key information to help you quickly understand the document and decide on next steps.

The overview tab includes the following sections:

**About**
:   An ECS-based description of the event category, helping you understand the type of activity the document represents.

**Description**
:   The detection rule description. Appears for alert documents.

**Reason**
:   The reason the alert was generated. Appears for alert documents.

**Explore in Alerts** or **Explore in Timeline**
:   For alerts, links directly to the alert in the {{security-app}} [Alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md) page. For events, opens the event in [Timeline](/solutions/security/investigate/timeline.md) for further investigation.

:::
::::
