# Configure case settings [observability-case-settings]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to create and edit connectors. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


To access case settings in an {{obs-serverless}} project, go to **Cases** → **Settings**.

:::{image} ../../../images/serverless-observability-cases-settings.png
:alt: View case settings
:class: screenshot
:::


## Case closures [observability-case-settings-case-closures]

If you close cases in your external incident management system, the cases will remain open in {{obs-serverless}} until you close them manually (the information is only sent in one direction).

To close cases when they are sent to an external system, select **Automatically close cases when pushing new incident to external system**.


## External incident management systems [observability-case-settings-external-incident-management-systems]

If you are using an external incident management system, you can integrate {{obs-serverless}} cases with this system using connectors. These third-party systems are supported:

* {ibm-r}
* {{jira}} (including {{jira}} Service Desk)
* {sn-itsm}
* {sn-sir}
* {swimlane}
* TheHive
* {webhook-cm}

You need to create a connector to send cases, which stores the information required to interact with an external system. For each case, you can send the title, description, and comment when you choose to push the case — for the **Webhook - Case Management** connector, you can also send the status and severity fields.

::::{important}
To add, modify, or delete a connector, you must have the Admin user role for the project (or a more permissive role).

::::


After creating a connector, you can set your cases to automatically close when they are sent to an external system.


### Create a connector [observability-case-settings-create-a-connector]

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to: **{{sn}}**, **{{jira}}***, ***{{ibm-r}}***, ***{{swimlane}}***, ***TheHive**, or **{{webhook-cm}}**.

    :::{image} ../../../images/serverless-observability-cases-add-connector.png
    :alt: Add a connector to send cases to an external source
    :class: screenshot
    :::

3. Enter your required settings. For connector configuration details, refer to:

    * [{{ibm-r}} connector](https://www.elastic.co/guide/en/kibana/current/resilient-action-type.html)
    * [{{jira}} connector](https://www.elastic.co/guide/en/kibana/current/jira-action-type.html)
    * [{{sn-itsm}} connector](https://www.elastic.co/guide/en/kibana/current/servicenow-action-type.html)
    * [{{sn-sir}} connector](https://www.elastic.co/guide/en/kibana/current/servicenow-sir-action-type.html)
    * [{{swimlane}} connector](https://www.elastic.co/guide/en/kibana/current/swimlane-action-type.html)
    * [TheHive connector](https://www.elastic.co/guide/en/kibana/current/thehive-action-type.html)
    * [{{webhook-cm}} connector](https://www.elastic.co/guide/en/kibana/current/cases-webhook-action-type.html)

4. Click **Save**.


### Edit a connector [observability-case-settings-edit-a-connector]

You can create additional connectors, update existing connectors, and change the connector used to send cases to external systems.

::::{tip}
You can also configure which connector is used for each case individually. Refer to [Create and manage cases](../../../solutions/observability/incident-management/create-manage-cases.md).

::::


To change the default connector used to send cases to external systems:

1. Select the required connector from the **Incident management system** list.

To update an existing connector:

1. Click **Update <connector name>**.
2. Update the connector fields as required.


## Custom fields [observability-case-settings-custom-fields]

You can add optional and required fields for customized case collaboration.

To create a custom field:

1. In the **Custom fields** section, click **Add field**.

    :::{image} ../../../images/serverless-observability-cases-custom-fields.png
    :alt: Add a custom field
    :class: screenshot
    :::

2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it’s added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.


## Templates [observability-case-settings-templates]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any custom fields.

To create a template:

1. In the **Templates** section, click **Add template**.

    :::{image} ../../../images/serverless-observability-cases-templates.png
    :alt: Add a case template
    :class: screenshot
    :::

2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its field values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.

::::
