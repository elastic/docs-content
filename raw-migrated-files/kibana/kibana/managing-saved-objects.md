# Manage saved objects [managing-saved-objects]

Edit, import, export, and copy your saved objects. These objects include dashboards, visualizations, maps, {{data-sources}}, **Canvas** workpads, and other saved objects.

You can find the **Saved Objects** page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).

:::{image} ../../../images/kibana-management-saved-objects.png
:alt: Saved Objects
:class: screenshot
:::


## Required permissions [_required_permissions_5]

To access **Saved Objects**, you must have the required `Saved Objects Management` {{kib}} privilege.

To add the privilege, go to the **Roles** management page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).

::::{note}
Granting access to `Saved Objects Management` authorizes users to manage all saved objects in {{kib}}, including objects that are managed by applications they may not otherwise be authorized to access.
::::



## View and delete [managing-saved-objects-view]

* To view and edit a saved object in its associated application, click the object title.
* To show objects that use this object, so you know the impact of deleting it, click the actions icon ![Actions icon](../../../images/kibana-actions_icon.png "") and then select **Relationships**.
* To delete one or more objects, select their checkboxes, and then click **Delete**.


## Import and export [managing-saved-objects-export-objects]

Use import and export to move objects between different {{kib}} instances. These actions are useful when you have multiple environments for development and production. Import and export also work well when you have a large number of objects to update and want to batch the process.

{{kib}} also provides import and export [saved objects APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) to automate this process.


### Import [_import]

Import multiple objects in a single operation.

1. In the toolbar, click **Import**.
2. Select the NDJSON file that includes the objects you want to import.
3. Select the import options. By default, saved objects already in {{kib}} are overwritten.
4. Click **Import**.

::::{note}
The [`savedObjects.maxImportExportSize`](../../../deploy-manage/deploy/self-managed/configure.md#savedObjects-maxImportExportSize) configuration setting limits the number of saved objects to include in the file. The [`savedObjects.maxImportPayloadBytes`](../../../deploy-manage/deploy/self-managed/configure.md#savedObjects-maxImportPayloadBytes) setting limits the overall size of the file that you can import.
::::



### Export [_export]

Export objects by selection or type.

* To export specific objects, select them in the table, and then click **Export**.
* To export objects by type, click **Export objects** in the toolbar.

{{kib}} creates an NDJSON with all your saved objects. By default, the NDJSON includes child objects related to the saved objects. Exported dashboards include their associated {{data-sources}}.

::::{note}
The [`savedObjects.maxImportExportSize`](../../../deploy-manage/deploy/self-managed/configure.md#savedObjects-maxImportExportSize) configuration setting limits the number of saved objects that you can export.
::::



### Compatibility across versions [_compatibility_across_versions]

With each release, {{kib}} introduces changes to the way saved objects are stored. When importing a saved object, {{kib}} runs the necessary migrations to ensure that the imported saved objects are compatible with the current version.

However, saved objects can only be imported into the same version, a newer minor on the same major, or the next major. Exported saved objects are not backward compatible and cannot be imported into an older version of {{kib}}. For example:

|     |     |     |
| --- | --- | --- |
| Exporting version | Importing version | Compatible? |
| 6.7.0 | 6.8.1 | Yes |
| 6.8.1 | 7.3.0 | Yes |
| 7.3.0 | 7.11.1 | Yes |
| 7.11.1 | 7.6.0 | No |
| 6.8.1 | 8.0.0 | No |


## Copy to other {{kib}} spaces [managing-saved-objects-copy-to-space]

Copy saved objects and their related objects between spaces.

1. Click the actions icon ![Actions icon](../../../images/kibana-actions_icon.png "").
2. Click **Copy to spaces**.
3. Select the spaces in which to copy the object.
4. Specify whether to automatically overwrite any objects that already exist in the target spaces, or resolve them on a per-object basis.

    The copy operation automatically includes child objects that are related to the saved object. If you don’t want this behavior, use the [copy saved objects to space API](https://www.elastic.co/guide/en/kibana/current/spaces-api-copy-saved-objects.html) instead.



## Share to other {{kib}} spaces [managing-saved-objects-share-to-space]

Make a single saved object available in multiple spaces.

1. Click the actions icon ![Actions icon](../../../images/kibana-actions_icon.png "").
2. Select **Share to spaces**.
3. Select the spaces in which to share the object. Or, indicate that you want the object to be shared to *all spaces*, which includes those that exist now and any created in the future.

    Not all saved object types are shareable. If an object is shareable, the **Spaces** column shows where the object exists. You can click those space icons to open the Share UI.

    The share operation automatically includes child objects that are related to the saved objects.


$$$spaces-api-update-objects-spaces-example-1$$$
To share a saved object to a space programmatically with the [spaces APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-spaces), follow these steps:

1. Collect reference graph and spaces context for each saved object that you want to share using get shareable references API:

    ```sh
    $ curl -X POST /api/spaces/_get_shareable_references
    {
      "objects": [
        {
          "type": "index-pattern",
          "id": "90943e30-9a47-11e8-b64d-95841ca0b247"
        }
      ]
    }
    ```

    The API returns the following:

    ```json
    {
      "objects": [
        {
          "type": "index-pattern",
          "id": "90943e30-9a47-11e8-b64d-95841ca0b247",
          "spaces": ["default"],
          "inboundReferences": [],
          "spacesWithMatchingOrigins": ["default"]
        }
      ]
    }
    ```

2. Check each saved object for `spacesWithMatchingOrigins` conflicts.

    Objects should not be shared to spaces with matching origins or you will create URL conflicts (causing the same URL to point to different saved objects).

3. Check each saved object for `spacesWithMatchingAliases` conflicts.

    If these match the spaces that these saved objects will be shared to you should disable legacy URL aliases for them using the disable legacy URL aliases API.

    When sharing to all spaces (`*`) all entries in `spacesWithMatchingAliases` should be checked.

4. Update spaces of each saved object and all its references:

    ```sh
    $ curl -X POST /api/spaces/_update_objects_spaces
    {
      "objects": [
        {
          "type": "index-pattern",
          "id": "90943e30-9a47-11e8-b64d-95841ca0b247"
        }
      ],
      "spacesToAdd": ["test"],
      "spacesToRemove": []
    }
    ```

    The API returns the following:

    ```json
    {
      "objects": [
        {
          "type": "index-pattern",
          "id": "90943e30-9a47-11e8-b64d-95841ca0b247",
          "spaces": ["default", "test"]
        }
      ]
    }
    ```



