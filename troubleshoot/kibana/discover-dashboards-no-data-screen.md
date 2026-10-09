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

Instead of the app, **Discover** or **Dashboards** shows a screen that asks you to add data or create a data view. This can happen even when {{es}} already holds data.

## Symptoms

When you open **Discover** or **Dashboards**, you see one of the following screens instead of the app:

- A **How do you want to explore your data?** screen with a **Create a data view** card and a **Query your data with ES|QL** card.
- A card that asks you to add data. The card is titled **Add integrations**, or **Add data** in some serverless projects. If you can't add integrations, the card is titled **Contact your administrator**.

## Diagnosis

{{kib}} runs its checks with your own permissions, in your current [space](/deploy-manage/manage-spaces.md). Data you can't access, and data views in another space, count as missing.

The screen you see tells you what {{kib}} found:

| Screen | What {{kib}} found |
|---|---|
| **How do you want to explore your data?** | Data in {{es}}, but no data view |
| **Add integrations**, **Add data**, or **Contact your administrator** | No data and no data view |

{{kib}} counts data when it finds at least one index or data stream that you can access, on the local cluster or on a remote cluster. An index with no documents counts. An index whose name starts with a dot doesn't count.

{{kib}} counts a data view when one exists in the current space. It doesn't check whether the data view matches any index.

### What Discover needs to open

**Discover** opens when either of the following is true:

- A data view exists in the current space.
- {applies_to}`stack: experimental 9.6+` At least one [{{esql}} data federation](elasticsearch://reference/query-languages/esql/esql-data-federation.md) dataset exists.

If {{es}} has data but none of these conditions is true, **Discover** shows the **How do you want to explore your data?** screen. **Discover** still opens when you use a link or a saved Discover session that contains an {{esql}} query.

### What Dashboards needs to open

**Dashboards** opens when any of the following is true:

- A data view exists in the current space.
- {applies_to}`stack: experimental 9.6+` At least one [{{esql}} data federation](elasticsearch://reference/query-languages/esql/esql-data-federation.md) dataset exists.
- You have unsaved changes on a new dashboard in your current browser session.
- At least one saved dashboard exists in the current space.

{{kib}} runs this check when you open the **Dashboards** page or create a new dashboard. It doesn't run when you open a saved dashboard directly.

## Resolution

Use the option that matches the screen you see.

### Create a data view or query without one

If you see **How do you want to explore your data?**, {{es}} has data that you can explore in either of the following ways:

- To explore the data with a data view, select **Create data view** on the **Create a data view** card and define the data view. When you save it, the screen closes and the app opens, in **Discover** or in **Dashboards**. Refer to [Create a data view](/explore-analyze/find-and-organize/data-views/create-data-view.md).
- To query the data without a data view, select **Try ES|QL** on the **Query your data with ES|QL** card. In **Discover**, this opens {{esql}} mode. In **Dashboards**, this opens a new dashboard with a chart built from an {{esql}} query on your data. Refer to [](/explore-analyze/discover/try-esql.md).

If **Create data view** is unavailable, your role can't create data views. Ask an administrator for the required permissions.

### Add data or find out why you can't see it

If you see **Add integrations**, **Add data**, or **Contact your administrator**, {{kib}} found no data and no data view. The **Contact your administrator** card has no button, because your role can't add integrations.

- To add data, select **Browse integrations** on the card. After the data arrives, return to **Discover** or **Dashboards**. If you now see **How do you want to explore your data?**, follow the steps in the previous section. For other ways to ingest data, refer to [](/manage-data/ingest.md).
- If you expect data to be there, make sure you're in the {{kib}} space that contains your data views and dashboards.
- If the data is in {{es}} but you still see the screen, ask an administrator to confirm that your [role](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) gives you access to the indices.
- If your data is in an index whose name starts with a dot, create a data view for it on the **Data Views** management page. A data view is enough for **Discover** and **Dashboards** to open. Refer to [Create a data view](/explore-analyze/find-and-organize/data-views/create-data-view.md).

## Resources

- [Data views](/explore-analyze/find-and-organize/data-views.md)
- [{{kib}} spaces](/deploy-manage/manage-spaces.md)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
