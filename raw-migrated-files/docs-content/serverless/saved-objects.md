# Saved objects [saved-objects]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

To get started, go to **{{project-settings}} → {{manage-app}} → {{saved-objects-app}}**:

:::{image} ../../../images/serverless-saved-object-management.png
:alt: {saved-objects-app}
:class: screenshot
:::


## View and delete [saved-objects-view-and-delete]

* To view and edit a saved object in its associated application, click the object title.
* To show objects that use this object, so you know the impact of deleting it, click the actions icon ![More actions](../../../images/serverless-boxesHorizontal.svg "") and then select **Relationships**.
* To delete one or more objects, select their checkboxes, and then click **Delete**.


## Import and export [saved-objects-import-and-export]

Use import and export to move objects between different {{kib}} instances. These actions are useful when you have multiple environments for development and production. Import and export also work well when you have a large number of objects to update and want to batch the process.


### Import [saved-objects-import]

Import multiple objects in a single operation.

1. In the toolbar, click **Import**.
2. Select the NDJSON file that includes the objects you want to import.
3. Select the import options. By default, saved objects already in {{kib}} are overwritten.
4. Click **Import**.


### Export [saved-objects-export]

Export objects by selection or type.

* To export specific objects, select them in the table, and then click **Export**.
* To export objects by type, click **Export objects** in the toolbar.

{{kib}} creates an NDJSON with all your saved objects. By default, the NDJSON includes child objects related to the saved objects. Exported dashboards include their associated {{data-sources}}.


## Copy to other spaces [saved-objects-copy-to-other-spaces]

Copy saved objects and their related objects between spaces.

1. Click the actions icon ![Actions](../../../images/serverless-boxesHorizontal.svg "").
2. Click **Copy to spaces**.
3. Specify whether to automatically overwrite any objects that already exist in the target spaces, or resolve them on a per-object basis.
4. Select the spaces in which to copy the object.

The copy operation automatically includes child objects that are related to the saved object.
