# Spaces [spaces]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

Spaces enable you to organize your dashboards and other saved objects into meaningful categories. Once inside a space, you see only the dashboards and saved objects that belong to that space.

When you create and enter a new project, you’re using the default space of that project.

You can identify the space you’re in or switch to a different space from the header.

:::{image} ../../../images/serverless-space-breadcrumb.png
:alt: Space breadcrumb
:screenshot:
:::

You can view and manage the spaces of a project from the **Spaces** page in **Management**.


## Required permissions [spaces-required-permissions]

You must have an admin role on the project to manage its **Spaces**.


## Create or edit a space [spaces-create-or-edit-a-space]

You can have up to 100 spaces in a project.

1. Click **Create space** or select the space you want to edit.
2. Provide:

    * A meaningful name and description for the space.
    * A URL identifier. The URL identifier is a short text string that becomes part of the {{kib}} URL. {{kib}} suggests a URL identifier based on the name of your space, but you can customize the identifier to your liking. You cannot change the space identifier later.

3. Customize the avatar of the space to your liking.
4. Save the space.

{{kib}} also has an [API](https://www.elastic.co/docs/api/doc/serverless/group/endpoint-spaces) if you prefer to create spaces programmatically.


## Customize access to space [spaces-customize-access-to-space]

Customizing access to a space is available for the following project types only: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

As an administrator, you can define custom roles with specific access to certain spaces and features in a project. Refer to [Custom roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md).


## Delete a space [spaces-delete-a-space]

Deleting a space permanently removes the space and all of its contents. Find the space on the *Spaces* page and click the trash icon in the Actions column.

You can’t delete the default space, but you can customize it to your liking.


## Move saved objects between spaces [spaces-move-saved-objects-between-spaces]

To move saved objects between spaces, you can [copy objects](../../../explore-analyze/find-and-organize.md#saved-objects-copy-to-other-spaces) or [export and import objects](../../../explore-analyze/find-and-organize.md#saved-objects-import-and-export).
