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

**Discover** provides a Security-specific experience for exploring alert and event data. When the Security experience is active, Discover adds color-coded row indicators, security-focused default columns, and a contextual overview tab in the document flyout that surfaces key alert and event context.

For general **Discover** concepts and features, refer to [](/explore-analyze/discover.md).


:::{image} /solutions/images/security-discover-profile.png
:screenshot:
:alt: Discover with the Security solution defult data view selected.
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

### Alert and Event Overview tab

When you expand a document in **Discover**, the document flyout includes an **Alert Overview** or **Event Overview** tab depending on the document type. This tab surfaces key information to help you quickly understand the document and decide on next steps.

The overview tab includes the following sections:

**About**
:   An ECS-based description of the event category, helping you understand the type of activity the document represents.

**Description**
:   The detection rule description. Appears for alert documents.

**Reason**
:   The reason the alert was generated. Appears for alert documents.

**Explore in Alerts** or **Explore in Timeline**
:   For alerts, links directly to the alert in the {{security-app}} [Alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md) page. For events, opens the event in [Timeline](/solutions/security/investigate/timeline.md) for further investigation.
