---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/data-views-in-sec.html
  - https://www.elastic.co/guide/en/serverless/current/security-data-views-in-sec.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# {{data-sources-cap}} and {{elastic-sec}} [security-data-views-in-sec]

{{data-sources-cap}} determine what data displays on {{elastic-sec}} pages with event or alert data. {{data-sources-cap}} are defined by the index patterns they include. Only data from {{es}} [indices](/manage-data/data-store/index-basics.md), [data streams](/manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md) specified in the active {{data-source}} will appear.

::::{important}
Custom indices are not included in the [default {{data-source}}](/solutions/security/get-started/data-views-elastic-security.md#default-data-view-security). Modify it or create a custom {{data-source}} to include custom indices.
::::



## Switch to another {{data-source}} [security-data-views-in-sec-switch-to-another-data-source]

You can tell which {{data-source}} is active by clicking the **{{data-source-cap}}** menu at the upper right of {{elastic-sec}} pages that display event or alert data, such as Overview, Alerts, Timelines, or Hosts. To switch to another {{data-source}}, click **Choose {{data-source}}**, select one of the options, and click **Save**.

:::{image} /solutions/images/security-dataview-button-highlighted.png
:alt: image highlighting how to open the data view selection menu
:::


## Create or modify a {{data-source}} [security-data-views-in-sec-create-or-modify-a-data-source]

To learn how to modify the default **Security Default Data View**, refer to [Update default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices).

To learn how to modify, create, or delete another {{data-source}} refer to [{{kib}} {{data-sources-cap}}](/explore-analyze/find-and-organize/data-views.md).

You can also temporarily modify the active {{data-source}} from the **{{data-source-cap}}** menu by clicking **Advanced options**, then adding or removing index patterns.

:::{image} /solutions/images/security-dataview-filter-example.gif
:alt: video showing how to filter the active data view
:::

This only allows you to add index patterns that match indices that currently contain data (other index patterns are unavailable). Note that any changes made are saved in the current browser window and won’t persist if you open a new tab.

::::{note}
You cannot update the data view for the Alerts page. This includes referencing a cross-cluster search (CCS) data view or any other data view. The Alerts page always shows data from `.alerts-security.alerts-default`.
::::



## The default {{data-source}} [default-data-view-security]

The default {{data-source}} is defined by the `securitySolution:defaultIndex` setting, which you can modify in [advanced settings](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices).

The first time a user visits {{elastic-sec}} within a given {{kib}} [space](/deploy-manage/manage-spaces.md), the default {{data-source}} generates in that space and becomes active.

::::{note}
In {{stack}}, your {{kib}} space must have the **Data View Management** [feature visibility](/deploy-manage/manage-spaces.md) setting enabled for the default {{data-source}} to generate and become active in your space.
::::


If you delete the active {{data-source}} when there are no other defined {{data-sources}}, the default {{data-source}} will regenerate and become active upon refreshing any {{elastic-sec}} page in the space.
