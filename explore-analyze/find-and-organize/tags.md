---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/tags.html
  - https://www.elastic.co/guide/en/kibana/current/managing-tags.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: kibana
---

# Tags [managing-tags]


Use tags to categorize your saved objects, then filter for related objects based on shared tags.

To get started, go to the **Tags** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/kibana-tag-management-section.png
:alt: Tags management
:screenshot:
:::


## Permissions [_required_permissions_10]

To create tags, you must meet the minimum requirements.

* Access to **Tags** requires a role with the the `Tag Management` Kibana privilege.
* The `read` privilege allows to assign tags to the saved objects for which you have write permission.
* The `write` privilege allows to create, edit, and delete tags.

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
2. Click the actions icon ![Actions icon](/explore-analyze/images/kibana-actions_icon.png ""), and then select **Manage assignments**.
3. Select the objects to which you want to assign or remove tags.

   :::{image} /explore-analyze/images/kibana-manage-assignments-flyout.png
   :alt: Assign flyout
   :screenshot:
   :width: 50%
   :::

4. Click **Save tag assignments**.


## Delete a tag [settings-delete-tag]

When you delete a tag, you remove it from all saved objects that use it.

1. Click the actions icon ![Actions icon](/explore-analyze/images/kibana-actions_icon.png ""), and then select **Delete**.
2. Click **Delete tag**.

::::{tip}
To assign, delete, or clear multiple tags, select them in the **Tags** view, and then select the action from the **selected tags** menu.
::::


## Manage tags programmatically [tags-api]
```{applies_to}
stack: experimental 9.5
serverless: experimental
```

You can create, read, update, and delete tags outside the {{kib}} UI using the Tags API. Use it to manage tags as code, automate tag creation in CI/CD pipelines, or integrate tag management into your own tooling.

The Tags API replaces the tag CRUD endpoints under `/api/saved_objects_tagging`, which are deprecated. If you have automation that calls those endpoints, migrate it to the Tags API.

For the available operations and the full request and response schema, refer to the [Tags API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-tags) ([serverless version](https://www.elastic.co/docs/api/doc/serverless/group/endpoint-tags)).


