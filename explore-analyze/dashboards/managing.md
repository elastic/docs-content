---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_manage_dashboards.html
---

# Managing dashboards [_manage_dashboards]


## Browse dashboards [find-dashboards]

When looking for specific dashboards to open or share, several actions are available to you to help you find them quicker.

**Search by name, description, or tag**

On your list of **Dashboards**, use the search field to look for specific terms. These terms will be highlighted in real time in your dashboard list to help you locate what’s relevant to you.

**Filter by tag**

When creating or editing dashboards, you can assign them tags that allow you to retrieve them faster in the future.

On your dashboard list, you have an option that lets you filter dashboards in or out based on their tags.

**Filter by creator**

The user who created or imported a dashboard is identified as the dashboard’s **creator**. This information is visible right from the dashboard list, and you can filter that list by creator.

Similarly, managed dashboards created by integrations are identified as created by Elastic.

::::{note}
The creator information is only available for dashboards created on or after version 8.14. For dashboards from previous versions, the creator is empty.
::::


:::{image} ../../images/kibana-dashboard-filter-by-creator.png
:alt: Option to filter the list of dashboards by creator
:::

**Sort by name or last update date**

By default, your most recently viewed dashboards are displayed first. You can instead sort the dashboard list based on their name or their last update date.


## Keep track of your favorite dashboards [_keep_track_of_your_favorite_dashboards]

You can mark any dashboards as favorite, using the ✩ **star icon**.

All dashboards marked as favorite are gathered in the **Starred** tab so you can find them quickly.

The list of starred dashboards is personal. Dashboards marked as favorite by other users only appear for those users.

![List of starred dashboards](../../images/kibana-dashboard-starred-list.png "")


## View dashboard usage [_view_dashboard_usage]

You can check how much a dashboard is being used by clicking its **View details** icon in your list of dashboards.

![View details icon in the list of dashboards](../../images/kibana-view-details-dashboards-8.16.0.png "")

These details include a graph showing the total number of views during the last 90 days.

![Graph showing the number of views during the last 90 days](../../images/kibana-dashboard-usage-count.png "")
