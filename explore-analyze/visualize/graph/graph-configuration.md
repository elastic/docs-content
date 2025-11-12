---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/graph-configuration.html
description: Configure Graph workspace settings for data views, fields, colors, icons, and data storage. Control how graph visualizations are saved and displayed.
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: kibana
---

# Configure Graph [graph-configuration]

When a user saves a graph workspace in Kibana, it is stored in the `.kibana` index along with other saved objects like visualizations and dashboards. By default, both the configuration and data are saved for the workspace:

**configuration**
:   The selected data view, fields, colors, icons, and settings.

**data**
:   The visualized content (the vertices and connections displayed in the workspace).

The data in a saved workspace is like a report—it is a saved snapshot that potentially summarizes millions of raw documents. Once saved, these summaries are no longer controlled by security policies. Because the original documents might be deleted after a workspace is saved, there’s no practical basis for checking permissions for the data in a saved workspace.

For this reason, you can configure the save policy for graph workspaces to ensure appropriate handling of your data. You can allow all users to save only the configuration information for a graph, require all users to explicitly include the workspace data, or completely disable the ability to save a workspace.

For example, to disable the save option entirely, set `xpack.graph.savePolicy` to `none` in [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.graph.savePolicy: none
```

The supported save policies are:

`none`
:   Neither the configuration or data can be saved.

`config`
:   Only the configuration is saved.

`configAndData`
:   Both configuration and data are saved. This is the default policy.

`configAndDataWithConsent`
:   Only the configuration is saved unless the user explicitly selects the include data option.


## Use Security to grant access [_use_security_to_grant_access]

You can also use security to grant read only or all access to different roles. When security is used to grant read only access, the following  indicator in Kibana is displayed. For more information on granting access to Kibana, see [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).

:::{image} /explore-analyze/images/kibana-graph-read-only-badge.png
:alt: Example of Graph's read only access indicator in Kibana's header
:screenshot:
:width: 50%
:::


## Disable drilldown configuration [disable-drill-down]

By default, users can configure *drilldown* URLs to display additional information about a selected vertex in a new browser window. For example, you could configure a drilldown URL to perform a web search for the selected vertex term.

To prevent users from adding drilldown URLs,  set `xpack.graph.canEditDrillDownUrls` to `false` in [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.graph.canEditDrillDownUrls: false
```

