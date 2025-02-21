# Configure case settings [security-cases-settings]

To access case settings in an {{elastic-sec}} project, go to **Cases** → **Settings**.

:::{image} ../../../images/serverless-security-cases-settings.png
:alt: Shows the case settings page
:class: screenshot
:::


## Case closures [security-cases-settings-case-closures]

If you close cases in your external incident management system, the cases will remain open in {{elastic-sec}} until you close them manually.

To close cases when they are sent to an external system, select **Automatically close Security cases when pushing new incident to external system**.


## External incident management systems [security-cases-settings-external-incident-management-systems]

You can push {{elastic-sec}} cases to these third-party systems:

* {sn-itsm}
* {sn-sir}
* {{jira}} (including Jira Service Desk)
* {ibm-r}
* {swimlane}
* {hive}
* {webhook-cm}

To push cases, you need to create a connector, which stores the information required to interact with an external system. After you have created a connector, you can set {{elastic-sec}} cases to automatically close when they are sent to external systems.

::::{admonition} Requirements
:class: note

To create connectors and send cases to external systems, you need the Security Analytics Complete [project feature](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) and the appropriate user role. For more information, refer to [Cases prerequisites](../../../solutions/security/investigate/cases-requirements.md).

::::


To create a new connector

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to: **{{sn}}**, **{{jira}}***, ***{{ibm-r}}***, ***{{swimlane}}***, ***{{hive}}**, or **{{webhook-cm}}**.
3. Enter your required settings. For connector configuration details, refer to:

    * [{{sn-itsm}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-action-type.md)
    * [{{sn-sir}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-sir-action-type.md)
    * [{{jira}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/jira-action-type.md)
    * [{{ibm-r}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/resilient-action-type.md)
    * [{{swimlane}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/swimlane-action-type.md)
    * [{{hive}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/thehive-action-type.md)
    * [{{webhook-cm}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/cases-webhook-action-type.md)


To change the settings of an existing connector:

1. Select the required connector from the incident management system list.
2. Click **Update <connector name>**.
3. In the **Edit connector** flyout, modify the connector fields as required, then click **Save & close** to save your changes.

To change the default connector used to send cases to external systems, select the required connector from the incident management system list.


### Mapped case fields [security-cases-settings-mapped-case-fields]

When you export an {{elastic-sec}} case to an external system, case fields are mapped to existing fields in the external system. For example, the case title is mapped to the short description in {{sn}} and the summary in {{jira}} incidents. Case tags are mapped to labels in {{jira}}. Case comments are mapped to work notes in {{sn}}.

When you use a {{webhook-cm}} connector, case fields can be mapped to custom or existing fields.

When you push updates to external systems, mapped fields are either overwritten or appended, depending on the field and the connector.

Retrieving data from external systems is not supported.


## Custom fields [security-cases-settings-custom-fields]

You can add optional and required fields for customized case collaboration.

1. In the **Custom fields** section, click **Add field**.

    :::{image} ../../../images/serverless-security-cases-custom-fields.png
    :alt: Add a custom field
    :class: screenshot
    :::

2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it’s added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.


## Templates [security-cases-settings-templates]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any custom fields.

To create a template:

1. In the **Templates** section, click **Add template**.

    :::{image} ../../../images/serverless-security-cases-templates.png
    :alt: Add a case template
    :class: screenshot
    :::

2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its field values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.

::::



## Observable types [security-cases-observable-types]

::::{admonition} Requirements
To use observables, you must have the Security Analytics Essentials [project feature](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

::::


Create custom observable types for enhanced case collaboration.

1. In the **Observable types** section, click **Add observable type**.
2. Enter a descriptive label for the observable type, then click **Save**.

After creating a new observable type, you can remove or edit it from the **Settings** page.

::::{note}
You can create up to 10 custom observable types.
::::


::::{important}
Deleting a custom observable type deletes all instances of it.
::::


:::{image} ../../../images/serverless-security-cases-observable-types.png
:alt: Add an observable type in case settings
:class: screenshot
:::
