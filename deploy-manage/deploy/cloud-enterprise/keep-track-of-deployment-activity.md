---
navigation_title: Keep track of deployment activity
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-activity-page.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Keep track of deployment activity on {{ece}} [ece-activity-page]

The deployment **Activity** page gives you a convenient way to follow all configuration changes that have been applied to your deployment, including which resources were affected, when the changes were applied, who initiated the changes, and whether or not the changes were successful. You can also select **Details** for an expanded, step-by-step view of each change applied to each deployment resource.

To view the activity for a deployment:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In your deployment menu, select **Activity**.
4. You can:

    1. View the activity for all deployment resources (the default).
    2. Use one of the available filters to view configuration changes by status or type. You can use the query field to create a custom search. Select the filter buttons to get examples of the query format.
    3. Select one of the resource filters to view activity for only that resource type.


:::{image} /deploy-manage/images/cloud-enterprise-ec-ce-activity-page.png
:alt: The Activity page
:::

In the table columns you find the following information:

Change
:   Which deployment resource the configuration change was applied to.

Summary
:   A summary of what change was applied, when the change was performed, and how long it took.

Applied by
:   The user who submitted the configuration change. `System` indicates configuration changes initiated automatically by the {{ece}} platform.

Actions
:   Select **Details** for an expanded view of each step in the configuration change, including the start time, end time, and duration. You can select **Reapply** to re-run the configuration change.

