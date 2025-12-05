---
navigation_title: Manage case settings
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases-settings.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions for configuring case settings including closure options, custom fields, templates, and connectors.
---

# Manage case settings [manage-cases-settings]

Configure case settings to customize how cases behave, including closure options, custom fields, templates for consistent case creation, and connectors for external incident management systems. Access case settings from **{{stack-manage-app}}** > **Cases** > **Settings**.

To perform these tasks, you must have [full access](setup-cases.md) to the appropriate case and connector features in {{kib}}.

:::{image} /explore-analyze/images/kibana-cases-settings.png
:alt: View case settings
:screenshot:
:::

## Case closures [case-closures]

If you close cases in your external incident management system, they will remain open in **Cases** until you close them manually.

To change whether cases are automatically closed after they are sent to an external system, update the case closure options.

## External incident management systems [case-connectors]

You can add connectors to cases to push information to these external incident management systems:

* {{ibm-r}}
* {{jira}}
* {{sn-itsm}}
* {{sn-sir}}
* {{swimlane}}
* {{hive}}
* {{webhook-cm}}

::::{note}
To create connectors and send cases to external systems, you must have the appropriate {{kib}} feature privileges. Refer to [Configure access to cases](setup-cases.md).
::::

You can create connectors in **{{stack-manage-app}} > {{connectors-ui}}**, as described in [*Connectors*](../../../deploy-manage/manage-connectors.md). Alternatively, you can create them in **{{stack-manage-app}} > Cases > Settings**:

1. From the **Incident management system** list, select **Add new connector**.
2. Select an external incident management system.
3. Enter your required settings. Refer to [{{ibm-r}}](kibana://reference/connectors-kibana/resilient-action-type.md), [Jira](kibana://reference/connectors-kibana/jira-action-type.md), [{{sn-itsm}}](kibana://reference/connectors-kibana/servicenow-action-type.md), [{{sn-sir}}](kibana://reference/connectors-kibana/servicenow-sir-action-type.md), [Swimlane](kibana://reference/connectors-kibana/swimlane-action-type.md), [{{hive}}](kibana://reference/connectors-kibana/thehive-action-type.md), or [{{webhook-cm}}](kibana://reference/connectors-kibana/cases-webhook-action-type.md) for connector configuration details.

You can subsequently choose the connector when you create cases and use it in case templates. To change the default connector for new cases, select the connector from the **Incident management system** list.

To update a connector, click **Update <connector name>** and edit the connector fields as required.

## Custom fields [case-custom-fields]

:::{admonition} Added in 8.15.0
This functionality was added in 8.15.0.
:::

You can add optional and required fields for customized case collaboration.

To create a custom field:

1. In the **Custom fields** section, click **Add field**.
   :::{image} /explore-analyze/images/kibana-cases-custom-fields-add.png
   :alt: Add a custom field in case settings
   :screenshot:
   :::

2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it’s added to all new and existing cases. Existing cases have null values for new text fields until you set them in each case.

You can subsequently remove or edit custom fields on the **Settings** page.

## Templates [case-templates]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any custom fields.

To create a template:

1. In the **Templates** section, click **Add template**.
   :::{image} /explore-analyze/images/kibana-cases-templates-add.png
   :alt: Add a template in case settings
   :screenshot:
   :::

2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.
::::
