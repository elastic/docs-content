---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/visualize-library.html
description: Store and reuse visualizations in Kibana Visualize Library. Manage shared panels, annotation groups, and visualization assets across multiple dashboards.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# Visualize Library [visualize-library]

The Visualize Library serves as a centralized repository for managing reusable visualization assets in {{product.kibana}}. When you save a panel to the library, you can add it to multiple dashboards, and any updates to the library version automatically propagate to all dashboards using that panel.

The library contains two main sections: **Visualizations** for charts and data panels, and **Annotation groups** for reusable annotations that mark events or milestones across time series visualizations.


## Visualizations [visualize-library-visualizations]

By default the **Visualizations** page opens first. Here you can create new visualizations, or select from a list of previously created visualizations. To learn more, refer to [Save to the Visualize Library](../../explore-analyze/visualize/manage-panels.md).


## Annotation groups [visualize-library-annotation-groups]

**Annotation groups** give you the option to mark points on a visualization panel with events, such as a deployment, to help track performance. These annotations can be reused across multiple visualization panels.
