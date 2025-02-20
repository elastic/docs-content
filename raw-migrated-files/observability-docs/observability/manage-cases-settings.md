# Configure case settings [manage-cases-settings]

To change case closure options and add custom fields, templates, and connectors for external incident management systems, go to **Cases** → **Settings**.

:::{image} ../../../images/observability-cases-settings.png
:alt: View case settings
:class: screenshot
:::


## Case closures [close-connector-observability]

If you close cases in your external incident management system, the cases will remain open in Elastic Observability until you close them manually.

To close cases when they are sent to an external system, select **Automatically close cases when pushing new incident to external system**.


## External incident management systems [cases-external-connectors]

If you are using an external incident management system, you can integrate Elastic Observability cases with that system using *connectors*. These third-party systems are supported:

* {{sn-itsm}}
* {{sn-sir}}
* {{jira}} (including {{jira}} Service Desk)
* {{ibm-r}}
* {{swimlane}}
* TheHive
* {{webhook-cm}}

::::{important}
To send cases to external systems, you need the appropriate license, and your role must have the **Cases** {{kib}} privilege as a user. For more details, refer to [Configure access to cases](../../../solutions/observability/incident-management/configure-access-to-cases.md).
::::


You need to create a connector to send cases, which stores the information required to interact with an external system.

After creating a connector, you can set your cases to [automatically close](../../../solutions/observability/incident-management/configure-case-settings.md#close-connector-observability) when they are sent to an external system.


### Create a connector [new-connector-observability]

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to: **{{sn}}**, **{{jira}}**, **{{ibm-r}}**, **{{swimlane}}**, **TheHive**, or **{{webhook-cm}}**.
3. Enter your required settings. For connector configuration details, refer to [{{ibm-r}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/resilient-action-type.md), [{{jira}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/jira-action-type.md), [{{sn-itsm}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-action-type.md), [{{sn-sir}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/servicenow-sir-action-type.md), [{{swimlane}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/swimlane-action-type.md), [TheHive connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/thehive-action-type.md), or [{{webhook-cm}} connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/cases-webhook-action-type.md).
4. Click **Save**.


### Edit a connector [Edit-connector-observability]

You can create additional connectors, update existing connectors, and change the connector used to send cases to external systems.

::::{tip}
You can also configure which connector is used for each case individually. See [Open a new case](../../../solutions/observability/incident-management/create-manage-cases.md#new-case-observability).
::::


To change the default connector used to send cases to external systems:

1. Select the required connector from the **Incident management system** list.

To update an existing connector:

1. Click **Update <connector name>**.
2. Update the connector fields as required.


## Custom fields [case-custom-fields]

You can add optional and required fields for customized case collaboration. [8.15.0]

1. In the **Custom fields** section, click **Add field**.

    :::{image} ../../../images/observability-cases-add-custom-field.png
    :alt: Add a custom field in case settings
    :class: screenshot
    :::

2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it’s added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.


## Templates [observability-case-templates]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any [custom fields](../../../solutions/observability/incident-management/configure-case-settings.md#case-custom-fields).

To create a template:

1. In the **Templates** section, click **Add template**.
2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its field values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.
::::


