# Open and manage new cases [manage-cases]

To perform these tasks, you must have [full access](../../../solutions/observability/incident-management/configure-access-to-cases.md) to the {{observability}} case feature in {{kib}}.


## Open a new case [new-case-observability]

Open a new case to keep track of issues and share the details with colleagues.

1. Find **Cases** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Click **Create case**.
3. If you defined [templates](../../../solutions/observability/incident-management/configure-case-settings.md#observability-case-templates), optionally select one to use its default field values. [preview]
4. Give the case a name, severity, and description.

    ::::{tip}
    In the `Description` area, you can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax to create formatted text.
    ::::

5. Optionally, add a category, assignees, and tags. You can add users only if they meet the necessary [prerequisites](../../../solutions/observability/incident-management/configure-access-to-cases.md).
6. If you defined [custom fields](../../../solutions/observability/incident-management/configure-case-settings.md#case-custom-fields), they appear in the **Additional fields** section. [8.15.0]
7. Under External incident management system, select a [connector](../../../solutions/observability/incident-management/configure-case-settings.md#cases-external-connectors). If you’ve previously added one, that connector displays as the default selection. Otherwise, the default setting is `No connector selected`.
8. After you’ve completed all of the required fields, click **Create case**.


## Add email notifications [add-case-notifications]

You can configure email notifications that occur when users are assigned to cases.

For hosted {{kib}} on {{ess}}:

1. Add the email domains to the [notifications domain allowlist](../../../explore-analyze/alerts/kibana.md).

    You do not need to take any more steps to configure an email connector or update {{kib}} user settings, since the preconfigured Elastic-Cloud-SMTP connector is used by default.


For self-managed {{kib}}:

1. Create a preconfigured email connector.

    ::::{note}
    At this time, email notifications support only [preconfigured email connectors](https://www.elastic.co/guide/en/kibana/current/pre-configured-connectors.html), which are defined in the `kibana.yml` file.
    ::::

2. Set the `notifications.connectors.default.email` {{kib}} setting to the name of your email connector.
3. If you want the email notifications to contain links back to the case, you must configure the [server.publicBaseUrl](../../../deploy-manage/deploy/self-managed/configure.md#server-publicBaseUrl) setting.

When you subsequently add assignees to cases, they receive an email.


## Add files [add-observability-case-files]

After you create a case, you can upload and manage files on the **Files** tab:

:::{image} ../../../images/observability-case-files.png
:alt: A list of files attached to a case
:class: screenshot
:::

The acceptable file types and sizes are affected by your [{{kib}} case settings](https://www.elastic.co/guide/en/kibana/current/cases-settings.html).

To download or delete the file or copy the file hash to your clipboard, open the action menu (…). The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, click its name in the activity or file list.

::::{note}
Uploaded files are also accessible on the **Files** page. To open **Files**, find **Stack Management** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search). When you export cases as [saved objects](../../../explore-analyze/find-and-organize/saved-objects.md), the case files are not exported.

::::



## Send cases to external incident management systems [push-observability-case]

To send a case to an external system, click the button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [Configure case settings](../../../solutions/observability/incident-management/configure-case-settings.md).


## Manage existing cases [manage-case-observability]

You can search existing cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes.

To view a case, click on its name. You can then:

* Add a new comment.
* Edit existing comments and the description.
* Add or remove assignees.
* Add a [connector](../../../solutions/observability/incident-management/configure-case-settings.md#cases-external-connectors) (if you did not select one while creating the case).
* Send updates to external systems (if external connections are configured).
* Edit the category and tags.
* Change the status.
* Change the severity.
* Remove an alert.
* Refresh the case to retrieve the latest updates.
* Close the case.
* Reopen a closed case.
