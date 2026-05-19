---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/visualize-library.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
---

# Visualize Library [visualize-library]

The **Visualize Library** is a space where you can save visualization panels that you may want to use across multiple dashboards. The **Visualize Library** consists of two pages:

* **Visualizations**
* **Annotation groups**


## Access the Visualize Library [visualize-library-access]

Find **Visualize** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` When using the Security and Observability solution views or project types, the **Dashboards** page includes **Visualizations** and **Annotation groups** tabs for direct access to the Visualize Library. With the **Classic** solution view or in previous versions, the Visualize Library is available from the **Visualize** page in the navigation menu.


## Visualizations [visualize-library-visualizations]

By default the **Visualizations** page opens first. Here you can create new visualizations, or select from a list of previously created visualizations. To learn more, refer to [Save to the Visualize Library](../../explore-analyze/visualize/manage-panels.md).


## Panel types compatible with the Visualize Library [visualize-library-compatibility]

Not all panel types support saving to the Visualize Library. Only panels that can be saved as standalone saved objects appear in the Visualize Library and can be linked across multiple dashboards.

**Compatible with the Visualize Library:**

- **Lens** visualizations
- **ES|QL** visualizations
- **Maps**
- **Custom visualizations** (Vega)
- **Discover sessions**: saved as shared Discover session objects
- **Aggregation-based** (legacy)
- **TSVB** (legacy)

**Dashboard-only (not saved to the Visualize Library):**

The following panel types are always dashboard-only. They cannot be saved to the Visualize Library and are permanently removed from the dashboard when you delete them:

- **Alerts** panels
- **Collapsible sections**, **Markdown text**, **Image**, and **Links** panels: layout and content elements
- **Anomaly swim lane**, **Anomaly chart**, and **Single Metric Viewer**: machine learning panels
- **Change point detection**: AIOps panel
- **SLO Overview**, **SLO Alerts**, and **SLO Error Budget**: observability panels


## Annotation groups [visualize-library-annotation-groups]

**Annotation groups** give you the option to mark points on a visualization panel with events, such as a deployment, to help track performance. These annotations can be reused across multiple visualization panels.
