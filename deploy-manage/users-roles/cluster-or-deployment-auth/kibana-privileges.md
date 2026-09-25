---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-privileges.html
applies_to:
  stack: all
products:
  - id: kibana
---

# {{kib}} privileges [kibana-privileges]

{{kib}} privileges grant users access to features within {{kib}}. Roles have privileges to determine whether users have write or read access.

To learn how to assign privileges to a role, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

## Base privileges [_base_privileges]

Assigning a base privilege applies the same access level across all feature groups instead of setting a level for each feature.

:::{note}
Some features and sub-feature privileges are excluded from base privileges and must be granted individually.
:::

$$$kibana-privileges-all$$$

* **All**: Grants full read-write access.
* **Read**: Grants read-only access.
* **Customize**: Allows you to set the access level for each feature separately.



### Assigning base privileges [_assigning_base_privileges]

From the role management screen:

:::{image} /deploy-manage/images/kibana-assign-base-privilege.png
:alt: Assign base privilege
:screenshot:
:::

Using the [role APIs]({{kib-apis}}group/endpoint-roles):

```js
PUT /api/security/role/my_kibana_role
{
  "elasticsearch": {
    "cluster" : [ ],
    "indices" : [ ]
  },
  "kibana": [
    {
      "base": ["all"],
      "feature": {},
      "spaces": ["marketing"]
    }
  ]
}
```



## Feature privileges [kibana-feature-privileges]

Assigning a feature privilege grants access to a specific feature. For each feature, select the type of access you want to allow:

% TODO: Replace this list with the shared snippet once https://github.com/elastic/docs-content/pull/8281 merges:
% :::{include} /deploy-manage/_snippets/feature-privilege-access-levels.md
% :::

* **All**: Users have full access to the feature, which includes performing all available actions and managing configuration.
* **Read**: Users can view the feature, but can't perform any actions or manage configuration.
* **None**: Users can't access or view the feature.

:::{note}
Some features don't have a **Read** privilege.
:::

In role management, features are organized into the following groups.

% TODO: Three rows in the following table should link out to their catalogs once those are published.
% TODO: Elasticsearch row: link to the Elasticsearch catalog (issue 1704).
% TODO: Observability row: link to the Observability catalog (issue 1703).
% TODO: Security row: link to /solutions/security/get-started/security-kibana-privileges.md once https://github.com/elastic/docs-content/pull/8281 merges.

:::{table}
:widths: description

| Group | What it contains |
| --- | --- |
| **Analytics** | Privileges for the features you use to explore and visualize data. Refer to [Privileges in the Analytics group](#kibana-privileges-analytics). |
| **Alerting V2** {applies_to}`stack: ga 9.5+` | Privileges for the {{alerting-v2-system}}. Refer to [Configure access to the {{alerting-v2-system}}](/explore-analyze/alerting/experimental-alerting-system/get-started/configure-access.md). <br> {applies_to}`stack: ga =9.5` Before 9.5.4, this group is called **Alerting**. |
| **Elasticsearch** | Privileges for {{es}} features. |
| **Observability** | Privileges for {{observability}} features. |
| **Security** | Privileges for {{elastic-sec}} features. |
| **Management** | Privileges for the features you use to administer {{kib}} and your data. Refer to [Privileges in the Management group](#kibana-privileges-management). |
:::

### Sub-feature privileges [_sub_feature_privileges]

Some features allow for finer access control than the **All** and **Read** privileges. This additional level of control is a [subscription feature](https://www.elastic.co/subscriptions).


### Assigning feature privileges [_assigning_feature_privileges]

From the role management screen:

:::{image} /deploy-manage/images/kibana-assign-subfeature-privilege.png
:alt: Assign feature privilege
:screenshot:
:::

Using the [role APIs]({{kib-apis}}group/endpoint-roles):

```js
PUT /api/security/role/my_kibana_role
{
  "elasticsearch": {
    "cluster" : [ ],
    "indices" : [ ]
  },
  "kibana": [
    {
      "base": [],
      "feature": {
        "visualize_v2": ["all"],
        "dashboard_v2": ["read", "url_create"]
      },
      "spaces": ["marketing"]
    }
  ]
}
```

## Privileges in the Analytics group [kibana-privileges-analytics]

Each of the following privileges controls access to a different feature.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Discover** | Access [Discover](/explore-analyze/discover.md), and save and manage Discover sessions. Turn on **Customize sub-feature privileges** to grant individual Discover privileges. For the full list, refer to [Discover sub-feature privileges](#kibana-privileges-discover-subfeatures). |
| **Dashboard** | Access [dashboards](/explore-analyze/dashboards.md), and create and edit them. Turn on **Customize sub-feature privileges** to grant individual dashboard privileges. For the full list, refer to [Dashboard sub-feature privileges](#kibana-privileges-dashboard-subfeatures). |
| **Canvas** | Access [Canvas](/explore-analyze/visualize/canvas.md), and create and edit workpads. Turn on **Customize sub-feature privileges** to grant the reporting privilege. For details, refer to [Canvas sub-feature privileges](#kibana-privileges-canvas-subfeatures). |
| **Maps** | Access [Maps](/explore-analyze/visualize/maps.md), and create and edit maps. |
| **Machine Learning** | Access [{{ml}}](/explore-analyze/machine-learning.md), and create and manage jobs and trained models. This privilege grants the same access level to {{data-sources}}, dashboards, Discover sessions, and visualizations. |
| **Graph** | Access [Graph](/explore-analyze/visualize/graph.md), and create and edit graphs. |
| **Visualize library** | Access the [Visualize library](/explore-analyze/visualize.md), and create and edit visualizations. Turn on **Customize sub-feature privileges** to grant individual Visualize library privileges. For the full list, refer to [Visualize library sub-feature privileges](#kibana-privileges-visualize-subfeatures). |
| **Agent Builder** {applies_to}`stack: ga 9.2+` | Access [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md), including agents, tools, and conversations.<br> {applies_to}`stack: ga 9.4+` Turn on **Customize sub-feature privileges** to grant individual {{agent-builder}} privileges. For the full list, refer to [{{agent-builder}} permissions](/explore-analyze/ai-features/agent-builder/permissions.md). |
| **Agent Builder - Semantic Metadata Layer (SML)** {applies_to}`stack: ga 9.5+` | Access the semantic metadata that {{agent-builder}} uses to interpret your data.<br> {applies_to}`stack: ga =9.5` This privilege is called **Agent Context Layer**. |
| **Workflows** {applies_to}`stack: ga 9.3+` | Access [Workflows](/explore-analyze/workflows.md), and create, edit, and run workflows. Turn on **Customize sub-feature privileges** to grant individual workflow privileges. For the full list, refer to [Workflows sub-feature privileges](#kibana-privileges-workflows-subfeatures). |
:::

### Discover sub-feature privileges [kibana-privileges-discover-subfeatures]

These privileges control specific actions in Discover. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Create Short URLs** | Create short URLs for Discover sessions, so that they can be shared. |
| **Store Background search** | Save the results of a long-running search, so that they can be viewed again without rerunning the search.<br> {applies_to}`stack: ga 9.0-9.1` This privilege is called **Store Search Sessions**. |
| **Generate CSV reports** | Export the results of a Discover session as a CSV file. |
:::

### Dashboard sub-feature privileges [kibana-privileges-dashboard-subfeatures]

These privileges control specific actions on dashboards. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Create Short URLs** | Create short URLs for dashboards, so that they can be shared. |
| **Store Background search** | Save the results of a long-running search, so that they can be viewed again without rerunning the search.<br> {applies_to}`stack: ga 9.0-9.1` This privilege is called **Store Search Sessions**. |
| **Generate PDF or PNG reports** | Export a dashboard as a PDF or PNG file. |
| **Generate CSV reports from Discover session panels** | Export the data behind a Discover session panel as a CSV file. |
:::

### Canvas sub-feature privileges [kibana-privileges-canvas-subfeatures]

This privilege controls a specific action in Canvas. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Generate PDF reports** | Export a workpad as a PDF file. |
:::

### Visualize library sub-feature privileges [kibana-privileges-visualize-subfeatures]

These privileges control specific actions in the Visualize library. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Create Short URLs** | Create short URLs for visualizations, so that they can be shared. |
| **Generate PDF or PNG reports** | Export a visualization as a PDF or PNG file. |
:::

### Workflows sub-feature privileges [kibana-privileges-workflows-subfeatures]

```yaml {applies_to}
stack: ga 9.3+
```

These privileges control specific actions on workflows. Selecting **All** includes every privilege in the following table except **Update managed workflows**, which you grant separately.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Create** | Create workflows. |
| **Update** | Edit existing workflows. |
| **Delete** | Delete workflows. |
| **Execute** | Run workflows. |
| **Read** | View workflows. |
| **Read Workflow Execution** | View the results of a workflow run, including its logs. |
| **Cancel Workflow Execution** | Stop a workflow that's currently running. |
| **Read managed workflows** {applies_to}`stack: ga 9.5+` | View the workflows that Elastic provides. |
| **Read managed workflow execution** {applies_to}`stack: ga 9.5+` | View the results of a managed workflow run. |
| **Update managed workflows** {applies_to}`stack: ga 9.5+` | Edit the workflows that Elastic provides. |
:::

## Privileges in the Management group [kibana-privileges-management]

Each of the following privileges controls access to a different feature.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Streams** {applies_to}`stack: ga 9.1+` | Access [Streams](/solutions/observability/streams/streams.md), and change stream processing, retention, and routing.<br> {applies_to}`stack: ga =9.1` This privilege is in the **Observability** group. |
| **AI Anonymization** {applies_to}`stack: ga 9.4+` | Change the anonymization rules that control which field values are masked before they're sent to a large language model. |
| **Dev Tools** | Access [Console](/explore-analyze/query-filter/tools/console.md), {{searchprofiler}}, and Grok Debugger. Users also need the matching {{es}} cluster and index privileges for the requests they run. |
| **Advanced Settings** | Change the settings that control how {{kib}} behaves in a space, such as the default index pattern and date format. |
| **Data View Management** | Create and edit [{{data-sources}}](/explore-analyze/find-and-organize/data-views.md). |
| **Files Management** | Manage the files that other features store in {{kib}}. |
| **Shared images** | Upload and manage the images that other features reuse, such as dashboard panel images. |
| **Saved Objects Management** | Manage [saved objects](/explore-analyze/find-and-organize/saved-objects.md), including importing, exporting, and copying them between spaces. |
| **Saved Query Management** | Save and manage [queries](/explore-analyze/query-filter/tools/saved-queries.md) across all features that use them. |
| **Tag Management** | Create and edit [tags](/explore-analyze/find-and-organize/tags.md), and apply them to saved objects. |
| **Stack Rules** | Create and manage [{{stack}} rules](/explore-analyze/alerting.md), such as index threshold and {{es}} query rules. |
| **Stack Alerts** {applies_to}`stack: ga 9.5+` | View and manage the alerts that {{stack}} rules generate, without granting access to the rules themselves. |
| **Osquery** | Access [Osquery](/solutions/security/investigate/osquery.md), and run and save queries. Turn on **Customize sub-feature privileges** to grant individual Osquery privileges. For the full list, refer to [Osquery sub-feature privileges](#kibana-privileges-osquery-subfeatures). |
| **Actions and Connectors** | Create and manage [connectors](/deploy-manage/manage-connectors.md), and run the actions that rules and cases trigger. Turn on **Customize sub-feature privileges** to grant the endpoint security privilege. For details, refer to [Actions and Connectors sub-feature privileges](#kibana-privileges-actions-subfeatures). |
| **Cases** | Access [cases](/explore-analyze/cases.md), and create and edit them. Turn on **Customize sub-feature privileges** to grant individual case privileges. For the full list, refer to [Customize sub-feature privileges for cases](/explore-analyze/cases/control-case-access.md#cases-sub-feature-privileges). |
| **Inference Endpoints** | Create and manage [{{infer}} endpoints](/explore-analyze/elastic-inference/inference-api.md).<br> {applies_to}`stack: ga 9.0-9.3` This privilege is in the **Elasticsearch** group. |
| **Cloud Connect** {applies_to}`stack: ga 9.3+` | Connect a cluster to {{ecloud}} services. This privilege appears on {{ece}} and self-managed clusters, but not on {{ech}}. |
| **Automatic Import** {applies_to}`stack: ga 9.4+` | Access [Automatic Import](/solutions/security/get-started/automatic-import.md), and create custom integrations from sample data. |
| **Data Set Quality** | Access the [Data Set Quality](/solutions/observability/data-set-quality-monitoring.md) page. Turn on **Customize sub-feature privileges** to grant individual data set quality privileges. For the full list, refer to [Data Set Quality sub-feature privileges](#kibana-privileges-data-set-quality-subfeatures). |
| **Fleet** | Access [{{fleet}}](/reference/fleet/index.md), and manage agents and agent policies. Turn on **Customize sub-feature privileges** to grant individual {{fleet}} privileges. For the full list, refer to [{{fleet}} privileges and available actions](/reference/fleet/fleet-roles-privileges.md#fleet-roles-and-privileges-sub-features-table). |
| **Integrations** | Browse and install [integrations](/reference/fleet/index.md). |
| **Maintenance Windows** | Create and manage [maintenance windows](/explore-analyze/alerting/alerts/maintenance-windows.md), which suppress rule notifications for a scheduled period. |
| **Manage Scheduled Reports** {applies_to}`stack: ga 9.1+` | View and manage the [scheduled reports](/explore-analyze/report-and-share/automating-report-generation.md) of every user in the space. |
| **Query activity** {applies_to}`stack: ga 9.4+` | Access [Query activity](/deploy-manage/monitor/query-activity.md), and cancel long-running queries. |
| **Rules Settings** | Change the settings that apply to all rules in a space. Turn on **Customize sub-feature privileges** to grant individual rule settings privileges. For the full list, refer to [Rules Settings sub-feature privileges](#kibana-privileges-rules-settings-subfeatures). |
| **Stack Monitoring** | Access [{{stack}} monitoring](/deploy-manage/monitor/stack-monitoring.md). This privilege has no access levels to select: to grant access, assign the `monitoring_user` role. |
| **AI Assistant** {applies_to}`stack: removed 9.3+` | Change which AI Assistants are available, from the AI Assistant settings in {{stack}} Management.<br> {applies_to}`stack: ga =9.2` This privilege is called **AI Assistant Settings**. |
| **Setup guides** {applies_to}`stack: removed 9.2+` | Access the getting-started page that helps you ingest data and start using Search, {{observability}}, or Security. |
| **Entity Manager** {applies_to}`stack: removed 9.1+` | Access the Elastic Entity Model of hosts, containers, and services in {{observability}}. |
:::

### Osquery sub-feature privileges [kibana-privileges-osquery-subfeatures]

These privileges control specific parts of Osquery. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Live queries** | Run live queries against hosts, and view the results. **Read** allows viewing the results of queries that other users ran. Select **Run Saved queries** within this privilege to also allow running saved queries without being able to change them. |
| **Saved queries** | Create, edit, and delete saved queries. |
| **Packs** | Create, edit, and delete query packs, and schedule them to run against agent policies. |
:::

### Actions and Connectors sub-feature privileges [kibana-privileges-actions-subfeatures]

This privilege controls a specific action on connectors. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Execute** | Run the endpoint security connectors, which include SentinelOne, CrowdStrike, and Microsoft Defender for Endpoint. |
:::

### Data Set Quality sub-feature privileges [kibana-privileges-data-set-quality-subfeatures]

```yaml {applies_to}
stack: ga 9.1+
```

These privileges control specific actions on the **Data Set Quality** page. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Manage rules** | Create and edit the rules that alert on degraded documents. |
| **Manage alerts** | View and manage the alerts that those rules generate. |
:::

### Rules Settings sub-feature privileges [kibana-privileges-rules-settings-subfeatures]

These privileges control the settings that apply to all rules in a space. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Flapping detection** | Change the settings that control when an alert is treated as flapping between states. |
| **Alert deletion** {applies_to}`stack: ga 9.1+` | Change how long alerts are kept before they're deleted, and delete them on demand. |
:::




