---
navigation_title: No-data screen in Discover and Dashboards
description: Find out why Discover or Dashboards shows a screen that asks you to add data or create a data view, and how to get to your data.
type: troubleshooting
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Discover or Dashboards asks you to add data or create a data view [discover-dashboards-no-data-screen]

Instead of the app, **Discover** or **Dashboards** shows a screen that asks you to add data or create a data view. This can happen even when {{es}} already holds data. A [data view](/explore-analyze/find-and-organize/data-views.md) tells {{kib}} which {{es}} data to explore, such as indices, data streams, or aliases.

## Symptoms

When you open **Discover** or **Dashboards**, you see one of the following screens instead of the app:

- A **How do you want to explore your data?** screen with a **Create a data view** card and a **Query your data with ES|QL** card.
- A card that asks you to add data. The card is titled **Add integrations**, or **Add data** in some serverless projects. If you can't add integrations, the card is titled **Contact your administrator**.

## Diagnosis

{{kib}} looks for data that you have access to, and for data views in your current [space](/deploy-manage/manage-spaces.md). If you set up [remote clusters](/explore-analyze/cross-cluster-search.md), {{kib}} looks for data in them too.

The screen you see tells you what {{kib}} found:

| Screen | What {{kib}} found |
|---|---|
| **How do you want to explore your data?** | Data in {{es}}, but no data view |
| **Add integrations**, **Add data**, or **Contact your administrator** | No data and no data view |

To decide whether you have data, {{kib}} looks for at least one index or data stream that you can access. An empty index is enough. {{kib}} ignores indices whose names start with a dot.

To decide whether you have a data view, {{kib}} only checks that one exists in the current space. It doesn't check that the data view matches any index, so a data view that matches nothing still opens the app.

### What Discover needs to open

**Discover** opens when either of the following is true:

- A data view exists in the current space.
- {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: unavailable` At least one [{{esql}} data federation](elasticsearch://reference/query-languages/esql/esql-data-federation.md) dataset exists.

If {{es}} has data but none of these conditions is true, **Discover** shows the **How do you want to explore your data?** screen. **Discover** still opens when you use a link or a saved Discover session that contains an {{esql}} query.

### What Dashboards needs to open

**Dashboards** opens when any of the following is true:

- A data view exists in the current space.
- {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: unavailable` At least one [{{esql}} data federation](elasticsearch://reference/query-languages/esql/esql-data-federation.md) dataset exists.
- You have unsaved changes on a new dashboard in your current browser session.
- At least one saved dashboard exists in the current space.

{{kib}} runs this check when you open the **Dashboards** page or create a new dashboard. It doesn't run when you open a saved dashboard directly.

## Resolution

Use the option that matches the screen you see:

- If you see **How do you want to explore your data?**, [create a data view or query without one](#create-data-view-or-query).
- If you see **Add integrations**, **Add data**, or **Contact your administrator**, [add data or find out why you can't see it](#add-data-or-find-missing-data).

### Create a data view or query without one [create-data-view-or-query]

If you see **How do you want to explore your data?**, {{es}} has data that you can explore in either of the following ways:

- To explore the data with a data view, select **Create data view** on the **Create a data view** card and define the data view. When you save it, **Discover** opens on the new data view, and **Dashboards** continues to the dashboard list or the new dashboard. Refer to [Create a data view](/explore-analyze/find-and-organize/data-views/create-data-view.md).
- To query the data without a data view, select **Try ES|QL** on the **Query your data with ES|QL** card. {{kib}} picks an index for the starting query: `logs*` if the name of a local index starts with `logs`, otherwise the first index it finds. In **Discover**, this opens {{esql}} mode with a query on that index. In **Dashboards**, this opens a new dashboard with a chart built from a query on that index. Refer to [](/explore-analyze/discover/try-esql.md).

If **Create data view** is unavailable, your role can't create data views. Ask an administrator to create one or to update your role.

### Add data or find out why you can't see it [add-data-or-find-missing-data]

If you see **Add integrations**, **Add data**, or **Contact your administrator**, {{kib}} found no data that you can access and no data view in the current space.

If you expect data views or dashboards to be there, switch to the {{kib}} space that contains them.

The remaining steps need privileges that not every role has, such as access to integrations, to {{es}} indices, or to data view management. If your role doesn't allow a step, ask an administrator to do it or to update your [role](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

- To add data, select **Browse integrations** on the card (**Add integrations** in earlier versions). The **Contact your administrator** card has no button, because your role can't add integrations. After the data arrives, return to **Discover** or **Dashboards**. If you now see **How do you want to explore your data?**, follow the steps in the previous section. For other ways to ingest data, refer to [](/manage-data/ingest.md).
- If you expect data from an agent, Logstash, or another source, check that {{es}} received it. In **{{index-manage-app}}**, look for the index on the **Indices** tab or the data stream on the **Data Streams** tab. You can also run `GET _cat/indices?v` in the [{{kib}} console](/explore-analyze/query-filter/tools/console.md) to list indices. If it isn't listed, check your ingest pipeline. If it is listed but you still see the screen, check that your role gives you access to the index. Refer to [](/manage-data/data-store/perform-index-operations.md).
- If your data is in an index whose name starts with a dot, create a data view for it on the **Data Views** management page. A data view is enough for **Discover** and **Dashboards** to open. Refer to [Create a data view](/explore-analyze/find-and-organize/data-views/create-data-view.md).

## Resources

- [Data views](/explore-analyze/find-and-organize/data-views.md)
- [{{kib}} spaces](/deploy-manage/manage-spaces.md)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
