---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-manage-settings.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-settings.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
navigation_title: Configure case settings
---

# Configure case settings for {{elastic-sec}} [security-cases-settings]

This page explains how to change case closure options, add custom fields, templates, and connectors for external incident management systems, and create custom observable types.
First, find **Cases** in the navigation menu or search for `Security/Cases` by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Settings**. In {{serverless-short}}, you can access case settings in an {{elastic-sec}} project, go to **Cases** → **Settings**.

:::{image} /solutions/images/security-cases-settings.png
:alt: Shows the case settings page
:screenshot:
:::

::::{note}
On {{stack}}, view and change case settings, you must have the appropriate {{kib}} feature privileges. Refer to [Cases requirements](/solutions/security/investigate/cases-requirements.md).
::::



## Case closures [close-sent-cases]

If you close cases in your external incident management system, the cases will remain open in {{elastic-sec}} until you close them manually.

To close cases when they are sent to an external system, select the option to automatically close cases when pushing new incident to external system.


## External incident management systems [cases-ui-integrations]

You can push {{elastic-sec}} cases to these third-party systems:

* {{sn-itsm}}
* {{sn-sir}}
* {{jira}} (including Jira Service Desk)
* {{ibm-r}}
* {{swimlane}}
* {{hive}}
* {{webhook-cm}}

To push cases, you need to create a connector, which stores the information required to interact with an external system. After you have created a connector, you can set {{elastic-sec}} cases to automatically close when they are sent to external systems.

::::{important}
To create connectors and send cases to external systems, ensure you have the appropriate role privileges and [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md). For more information, refer to [Cases requirements](/solutions/security/investigate/cases-requirements.md).
::::


To create a new connector:

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to: **{{sn}}**, **{{jira}}**, **{{ibm-r}}**, **{{swimlane}}**, **{{hive}}**, or **{{webhook-cm}}**.
3. Enter your required settings. For connector configuration details, refer to:

    * [{{sn-itsm}} connector](kibana://reference/connectors-kibana/servicenow-action-type.md)
    * [{{sn-sir}} connector](kibana://reference/connectors-kibana/servicenow-sir-action-type.md)
    * [{{jira}} connector](kibana://reference/connectors-kibana/jira-action-type.md)
    * [{{ibm-r}} connector](kibana://reference/connectors-kibana/resilient-action-type.md)
    * [{{swimlane}} connector](kibana://reference/connectors-kibana/swimlane-action-type.md)
    * [{{hive}} connector](kibana://reference/connectors-kibana/thehive-action-type.md)
    * [{{webhook-cm}} connector](kibana://reference/connectors-kibana/cases-webhook-action-type.md)


To change the settings of an existing connector:

1. Select the required connector from the incident management system list.
2. Click **Update <connector name>**.
3. In the **Edit connector** flyout, modify the connector fields as required, then click **Save & close** to save your changes.

To change the default connector used to send cases to external systems, select the required connector from the incident management system list.


### Mapped case fields [mapped-case-fields]

When you export an {{elastic-sec}} case to an external system, case fields are mapped to existing fields in the external system. For example, the case title is mapped to the short description in {{sn}} and the summary in {{jira}} incidents. Case tags are mapped to labels in {{jira}}. Case comments are mapped to work notes in {{sn}}.

When you use a {{webhook-cm}} connector, case fields can be mapped to custom or existing fields.

When you push updates to external systems, mapped fields are either overwritten or appended, depending on the field and the connector.

Retrieving data from external systems is not supported.


## Custom fields [cases-ui-custom-fields]

You can add optional and required fields for customized case collaboration.

1. In the **Custom fields** section, click **Add field**.

    :::{image} /solutions/images/security-cases-add-custom-field.png
    :alt: Add a custom field in case settings
    :screenshot:
    :::

2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it’s added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.


## Templates [cases-templates]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any custom fields.

To create a template:

1. In the **Templates** section, click **Add template**.

    :::{image} /solutions/images/security-cases-add-template.png
    :alt: Add a template in case settings
    :screenshot:
    :::

2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.
::::



## Observable types [cases-observable-types]

::::{admonition} Requirements
Ensure you have the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

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


:::{image} /solutions/images/security-cases-observable-types.png
:alt: Add an observable type in case settings
:screenshot:
:::
