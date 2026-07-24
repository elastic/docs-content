---
navigation_title: Attach objects
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases.html
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Attach alerts, files, observables, dashboards, maps, Discover sessions, and Lens visualizations to cases to provide context and supporting materials.
---

# Attach objects to cases [attach-objects-to-cases]

After [creating a case](create-cases.md), you can attach supporting materials to build a complete picture of an incident.  You can attach [alerts](#add-case-alerts) to escalate and track detections, [files](#add-case-files) like screenshots or logs as evidence, [observables](#add-case-observables) such as IP addresses or file hashes to identify patterns, and more.  

In {{elastic-sec}}, you can also attach [events](/solutions/security/investigate/security-cases.md#cases-add-events), [threat intelligence indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case), [Timelines](/solutions/security/investigate/security-cases.md#cases-timeline), and [entities](/solutions/security/investigate/security-cases.md#cases-add-entities) to connect cases to known threats.

## Supported object types [supported-object-types]

| Object | Description | Stack | Serverless |
| --- | --- | --- | --- |
| [Alerts](#add-case-alerts) | Attach alerts to escalate and track detections. | Security, Observability | Security, Observability |
| [Files](#add-case-files) | Upload screenshots, logs, or other supporting files. | Security, Observability, Stack Management | Security, Observability |
| [Observables](#add-case-observables) | Add IP addresses, file hashes, domains, or URLs to identify patterns. | Security, Stack Management | Security |
| [Lens visualizations](#cases-lens-visualization) | Embed charts and graphs to illustrate event and alert data. | Security, Observability, Stack Management | Security, Observability |
| [Dashboards](#cases-saved-objects) | Attach a dashboard to preserve a multi-panel view of related data. | Security, Observability, Stack Management | Security, Observability |
| [Maps](#cases-saved-objects) | Attach a map to show geographic context for an investigation. | Security, Observability, Stack Management | Security, Observability |
| [Discover sessions](#cases-saved-objects) | Attach a saved Discover session to preserve search context. | Security, Observability, Stack Management | Security, Observability |
| [Events](/solutions/security/investigate/security-cases.md#cases-add-events) | Attach host, network, or user events from Timeline. | Security | Security |
| [Indicators](/solutions/security/investigate/indicators-of-compromise.md#attach-indicator-to-case) | Link threat intelligence indicators to document evidence of compromise. | Security | Security |
| [Timelines](/solutions/security/investigate/security-cases.md#cases-timeline) | Attach a Timeline to preserve investigation context and share it with your team, as a link or a structured, filterable table {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` | Security | Security |
| [Entities](/solutions/security/investigate/security-cases.md#cases-add-entities) {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` | Attach a host, user, or service entity to connect a case to what's under investigation. | Security | Security |

## Add alerts [add-case-alerts]

Escalate alerts and track them in a single place by attaching them to cases. 

To add alerts, select **More actions (…)** on a single alert or use the **Bulk actions** menu for multiple alerts, then choose **Add to a new case** or **Add to existing case**. You can add up to 1,000 alerts to a case.

After adding alerts, you can review them under **Alerts** on the case's **Attachments** tab. Alerts are organized from oldest to newest, and you can select **View details** to inspect individual alerts.

## Add files [add-case-files]

After you create a case, you can upload and manage files under the **Files** tab. Each file can be up to 100 MiB (10 MiB for images), and a case can have up to 100 files attached.

{applies_to}`stack: ga 9.5` You can also upload a file from the **Activity** tab. Select **Attach**, then **Upload file**.

When you upload a file, a comment is added to the case activity log, and the file becomes accessible from the **Files** management page. To view an image, select its name in the activity or file list. To download or delete a file, or copy its hash (MD5, SHA-1, or SHA-256) to your clipboard, open the action menu {icon}`boxes_horizontal`.

### Supported file types [cases-file-types]

Cases accepts the following categories of files:

| Category | Examples |
| --- | --- |
| Images | PNG, JPEG, GIF, WebP, SVG, TIFF, BMP, and specialized formats such as HEIC, HEIF, DICOM, Adobe Photoshop (PSD), and AutoCAD (DWG, DXF) |
| Documents | PDF, plain text, CSV, JSON |
| Archives | ZIP, GZIP, BZIP, BZIP2, 7-Zip, TAR |

If your file isn't one of these types (for example, a Microsoft Office format like `.xlsx` or `.docx`) compress it into a ZIP archive and attach the archive instead.

## Add observables [add-case-observables]

Observables are discrete pieces of data relevant to an investigation, such as IP addresses, file hashes, domain names, or URLs. By attaching observables to cases, you can spot patterns across incidents or events. For example, if the same malicious IP appears in multiple cases, you may be dealing with a coordinated attack or shared threat infrastructure. This correlation helps you assess the true scope of an incident and prioritize your response.

You can view and manage case observables under **Observables** on the case's **Attachments** tab. Each case supports up to 50 observables.

### Manually add an observable [cases-manual-add-observable]

1. Select **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/explore-analyze/cases/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Select **Add observable**.

After adding an observable to a case, you can remove or edit it using the action menu {icon}`boxes_horizontal`. To find related investigations, check the **Similar cases** tab for other cases that share the same observables.

### Auto-extract observables [cases-auto-extract-observables]

```{applies_to}
stack: ga 9.2
serverless:
  security: ga
```

With the appropriate subscription, you can auto-extract observables from alerts instead of adding them manually. Note that auto-extracting observables is unavailable for {{observability}} cases.

{applies_to}`stack: ga 9.5` Auto-extraction also runs for cases created with the Cases API or a [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md) action, as long as **Auto-extract observables** is turned on in the global case configuration or case template.

## Add Lens visualizations [cases-lens-visualization]

```{applies_to}
stack: beta
```

Add Lens visualizations to case descriptions or comments to portray event and alert data through charts and graphs. You can add them from dashboard panels or create visualizations directly in a case. To add a visualization from a dashboard, open a panel's menu, select the action menu {icon}`boxes_horizontal`, then **Add to existing case** or **Add to new case**.

To create a visualization in a case:

1. Click **Visualization** to open the dialog, then select an existing visualization from your Visualize Library or create a new one. Use an absolute time range so it remains consistent over time.
2. (Optional) Click **Save to library**, enter a title and description, and save to reuse the visualization elsewhere.
3. Click **Save and return** to go back to your case.
4. Click **Preview** to see how the visualization will appear, then click **Add Comment** to attach it.

To modify a visualization after adding it, click **Open Visualization** in the case comment menu.

### Attach a visualization by reference [cases-lens-by-reference]

```{applies_to}
stack: preview 9.5
serverless: preview
```

You can also attach an existing Lens visualization by reference, which keeps a live link to the source so the case reflects the latest version whenever it's edited. Select **Attach**, then **Saved object** from the case's **Activity** tab, search for the visualization, and select it to open it in Lens, where you can adjust it before returning to the case.

## Add dashboards, maps, and Discover sessions [cases-saved-objects]

```{applies_to}
stack: ga 9.5
```

Attach an existing dashboard, map, or Discover session to a case to give teammates a direct path back to the full, interactive view.

To attach these objects:

1. Go to the case's details page, then select the **Activity** tab.
2. Select **Attach**, then **Saved object**.
3. In the **Attach saved object** dialog, search for the dashboard, map, or Discover session by title. Optionally, filter by type, then select **Attach** next to the item you want.

The attached object appears in the case activity log and in its own section on the **Attachments** tab, labeled with the object's title. Dashboards and maps also show an inline snapshot when one is available. Select the title to open the full dashboard, map, or Discover session.