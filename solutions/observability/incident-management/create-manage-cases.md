---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
products:
  - id: observability
  - id: cloud-serverless
---

# Create and manage cases [observability-create-a-new-case]

::::{note}

**For Observability serverless projects**, the **Editor** role or higher is required to create and manage cases. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


Open a new case to keep track of issues and share the details with colleagues. To create a case in your Observability project:

1. Find **Cases** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create case**.
3. {applies_to}`stack: preview` {applies_to}`serverless: preview` (Optional) If you defined [templates](/solutions/observability/incident-management/configure-case-settings.md#observability-case-templates), select one to use its default field values.
4. Give the case a name, severity, and description.

    ::::{tip}
    In the `Description` area, you can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax to create formatted text.

    ::::

5. (Optional) Add a category, assignees, and tags.

    **For Observability serverless projects**, you can add users who are assigned the Editor user role (or a more permissive role) for the project.

    **For Elastic Stack**, You can add users only if they meet the necessary [prerequisites](/solutions/observability/incident-management/configure-access-to-cases.md).

6. If you defined [custom fields](/solutions/observability/incident-management/configure-case-settings.md#case-custom-fields), they appear in the **Additional fields** section.
7. (Optional) Under **External Connector Fields**, you can select a connector to send cases to an external system. If you’ve created any connectors previously, they will be listed here. If there are no connectors listed, you can create one. For more information, refer to [External incident management systems](/solutions/observability/incident-management/configure-case-settings.md#cases-external-connectors).

    ::::{note}
    :applies_to:{stack: ga 9.3}
    When specifying **Additional fields** for an {{ibm-r}} connector, fields that are set when an incident is created or changed (for example, an incident is closed) won't display as an option.
    ::::

8. After you’ve completed all of the required fields, click **Create case**.

::::{tip}
You can also create a case from an alert or add an alert to an existing case. From the **Alerts** page, click the **More options** ![More actions](/solutions/images/serverless-boxesHorizontal.svg "") icon and choose either **Add to existing case** or **Create new case**, and select or complete the details as required.

::::



## Add files [observability-create-a-new-case-add-files]

After you create a case, you can upload and manage files on the **Files** tab:

:::{image} /solutions/images/serverless-cases-files-tab.png
:alt: A list of files attached to a case
:screenshot:
:::

To download or delete the file or copy the file hash to your clipboard, open the action menu (…). The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, click its name in the activity or file list.

::::{note}
Uploaded files are also accessible under **Project settings** → **Management** → **Files**. When you export cases as [saved objects](/explore-analyze/find-and-organize/saved-objects.md), the case files are not exported.

::::


You can add images and text, CSV, JSON, PDF, or ZIP files. For the complete list, check [`mime_types.ts`](https://github.com/elastic/kibana/blob/main/x-pack/plugins/cases/common/constants/mime_types.ts).

::::{note}
**File size limits**

There is a 10 MiB size limit for images. For all other MIME types, the limit is 100 MiB.

::::


## Send cases to external incident management systems [observability-create-a-new-case-send-cases-to-external-incident-management-systems]

To send a case to an external system, click the ![push](/solutions/images/serverless-importAction.svg "") button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [](/solutions/observability/incident-management/configure-case-settings.md).


## Manage existing cases [observability-create-a-new-case-manage-existing-cases]

You can search existing cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes.

To view a case, click on its name. You can then:

* Add a new comment.
* Edit existing comments and the description.
* Add or remove assignees.
* Add a connector (if you did not select one while creating the case).
* Send updates to external systems (if external connections are configured).
* Edit the category and tags.
* Change the status.
* Change the severity.
* Remove an alert.
* Refresh the case to retrieve the latest updates.
* Close the case.
* Reopen a closed case.