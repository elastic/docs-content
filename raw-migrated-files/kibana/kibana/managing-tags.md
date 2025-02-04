# Tags [managing-tags]

Use tags to categorize your saved objects, then filter for related objects based on shared tags.

To get started, go to the **Tags** management page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).

:::{image} ../../../images/kibana-tag-management-section.png
:alt: Tags management
:class: screenshot
:::


## Required permissions [_required_permissions_10]

To create tags, you must meet the minimum requirements.

* Access to **Tags** requires the `Tag Management` Kibana privilege. To add the privilege, go to the **Roles** page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
* The `read` privilege allows you to assign tags to the saved objects for which you have write permission.
* The `write` privilege enables you to create, edit, and delete tags.

::::{note}
Having the `Tag Management` {{kib}} privilege is not required to view tags assigned on objects you have `read` access to, or to filter objects by tags from the global search.
::::



## Create a tag [settings-create-tag]

Create a tag to assign to your saved objects.

1. Click **Create tag**.
2. Enter a name and select a color for the new tag.

    The name cannot be longer than 50 characters.

3. Click **Create tag**.


## Assign a tag to an object [settings-assign-tag]

To assign and remove tags, you must have `write` permission on the objects to which you assign the tags.

1. Find the tag you want to assign.
2. Click the actions icon ![Actions icon](../../../images/kibana-actions_icon.png ""), and then select **Manage assignments**.
3. Select the objects to which you want to assign or remove tags.

    :::{image} ../../../images/kibana-manage-assignments-flyout.png
    :alt: Assign flyout
    :class: screenshot
    :::

4. Click **Save tag assignments**.


## Delete a tag [settings-delete-tag]

When you delete a tag, you remove it from all saved objects that use it.

1. Click the actions icon ![Actions icon](../../../images/kibana-actions_icon.png ""), and then select **Delete**.
2. Click **Delete tag**.

::::{tip}
To assign, delete, or clear multiple tags, select them in the **Tags** view, and then select the action from the **selected tags** menu.
::::


