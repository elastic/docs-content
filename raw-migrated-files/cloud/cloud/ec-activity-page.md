# Keep track of deployment activity [ec-activity-page]

The deployment **Activity** page gives you a convenient way to follow all configuration changes that have been applied to your deployment, including which resources were affected, when the changes were applied, who initiated the changes, and whether or not the changes were successful. You can also select **Details** for an expanded, step-by-step view of each change applied to each deployment resource.

To view the activity for a deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. In your deployment menu, select **Activity**.
4. You can:

    1. View the activity for all deployment resources (the default).
    2. Use one of the available filters to view configuration changes by status or type. You can use the query field to create a custom search. Select the filter buttons to get examples of the query format.
    3. Select one of the resource filters to view activity for only that resource type.


:::{image} ../../../images/cloud-ec-ce-activity-page.png
:alt: The Activity page
:::

In the table columns you find the following information:

Change
:   Which deployment resource the configuration change was applied to.

Summary
:   A summary of what change was applied, when the change was performed, and how long it took.

Applied by
:   The user who submitted the configuration change. `System` indicates configuration changes initiated automatically by the {{ecloud}} platform.

Actions
:   Select **Details** for an expanded view of each step in the configuration change, including the start time, end time, and duration. You can select **Reapply** to re-run the configuration change.

