---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
products:
  - id: observability
  - id: cloud-serverless
applies_to:
  stack: all
  serverless:
    observability: all
---

# Create and manage cases [observability-create-a-new-case]

Open a new {{observability}} case to keep track of issues and share the details with colleagues. You can create and manage cases using the cases UI.

::::{applies-switch}

:::{applies-item} stack:
**Requirements**

To access and send cases to external systems, you need the appropriate [subscription](https://www.elastic.co/pricing), and your role must have the required {{kib}} feature privileges. Refer to [](../incident-management/configure-access-to-cases.md) for more information.
:::

:::{applies-item} serverless:
**Requirements**

For {{observability}} projects, you need the appropriate [feature tier](https://www.elastic.co/pricing), and your role must have the **Editor** role or higher to create and manage cases. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
:::

::::

## Create a case [create-observability-case]

To create a case:

1. Find **Cases** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create case**.
3. {applies_to}`stack: preview` {applies_to}`serverless: preview` (Optional) If you defined [templates](/solutions/observability/incident-management/configure-case-settings.md#observability-case-templates), select one to use its default field values.
4. Give the case a name, severity, and description.

    ::::{tip}
    In the **Description**, you can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax to format text.

    ::::

5. (Optional) Add a category, assignees, and tags.

    ::::{applies-switch}

    :::{applies-item} stack:
    You can add users only if they meet the necessary [prerequisites](/solutions/observability/incident-management/configure-access-to-cases.md).
    :::

    :::{applies-item} serverless:
    You can add users who are assigned the **Editor** user role (or a more permissive role) for the project.
    :::

    ::::

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

:::{include} /solutions/_snippets/add-case-files.md
:::

## Send cases to external incident management systems [observability-create-a-new-case-send-cases-to-external-incident-management-systems]

To send a case to an external system, click the ![push](/solutions/images/serverless-importAction.svg "") button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [](/solutions/observability/incident-management/configure-case-settings.md).


## Manage existing cases [observability-create-a-new-case-manage-existing-cases]

You can search existing cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes.

{applies_to}`stack: ga 9.3` To find cases that were created during a specific time range, use the date time picker above the Cases table. The default time selection is the last 30 days. Clicking **Show all cases** displays every {{observability}} case in your space. The action also adjusts the starting time range to the date of when the first case was created.

To view a case, click on its name. You can then:

* Add and edit the case's description, comments, assignees, tags, status, severity, and category.
* Add a connector (if you did not select one while creating the case).
* Send updates to external systems (if external connections are configured).
* Refresh the case to retrieve the latest updates.
* Add and manage the following items:
   * Alerts
   * Files