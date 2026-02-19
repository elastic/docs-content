---
navigation_title: Configure settings
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases-settings.html
  - https://www.elastic.co/guide/en/security/current/cases-manage-settings.html
  - https://www.elastic.co/guide/en/observability/current/manage-cases-settings.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-settings.html
  - https://www.elastic.co/guide/en/serverless/current/observability-case-settings.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
---

# Configure case settings [manage-cases-settings]

Configure case closure options, custom fields, templates, and connectors for external incident management systems.

To access case settings:
* For **{{stack-manage-app}}**: Go to **{{stack-manage-app}} > Cases** and click **Settings**.
* For **{{elastic-sec}}**: Find **Cases** in the navigation menu or search for `Security/Cases`, then click **Settings**.
* For **{{observability}}**: Go to **Cases** → **Settings**.


::::{note}
To perform these tasks, you must have [full access](configure-case-access.md) to the appropriate case and connector features.

{applies_to}`serverless:` For {{observability}} serverless projects, the **Editor** role or higher is required to create and edit connectors. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
::::


## Case closures [case-closures]

If you close cases in your external incident management system, the cases will remain open in {{kib}} until you close them manually.

To close cases when they are sent to an external system, select the option to automatically close cases when pushing new incident to external system.

## External incident management systems [case-connectors]

You can push cases to these externxal incident management systems:

* {{ibm-r}}
* {{jira}} (including Jira Service Desk)
* {{sn-itsm}}
* {{sn-sir}}
* {{swimlane}}
* {{hive}}
* {{webhook-cm}}

To create connectors and send cases to external systems, you must have the appropriate {{kib}} feature privileges and subscription or project feature tier. Refer to [Configure access to cases](configure-case-access.md).

You can create connectors in **{{stack-manage-app}} > {{connectors-ui}}**, as described in [Connectors](/deploy-manage/manage-connectors.md). Alternatively, you can create them from case settings.

To create a new connector:

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to: **{{sn}}**, **{{jira}}**, **{{ibm-r}}**, **{{swimlane}}**, **{{hive}}**, or **{{webhook-cm}}**.
3. Enter your required settings. For connector configuration details, refer to:

    * [{{ibm-r}} connector](kibana://reference/connectors-kibana/resilient-action-type.md)
    * [{{jira}} connector](kibana://reference/connectors-kibana/jira-action-type.md)
    * [{{sn-itsm}} connector](kibana://reference/connectors-kibana/servicenow-action-type.md)
    * [{{sn-sir}} connector](kibana://reference/connectors-kibana/servicenow-sir-action-type.md)
    * [{{swimlane}} connector](kibana://reference/connectors-kibana/swimlane-action-type.md)
    * [{{hive}} connector](kibana://reference/connectors-kibana/thehive-action-type.md)
    * [{{webhook-cm}} connector](kibana://reference/connectors-kibana/cases-webhook-action-type.md)

4. Click **Save**.

To change the settings of an existing connector:

1. Select the required connector from the incident management system list.
2. Click **Update <connector name>**.
3. In the **Edit connector** flyout, modify the connector fields as required, then click **Save & close** to save your changes.

To change the default connector used to send cases to external systems, select the required connector from the incident management system list.


You can subsequently choose the connector when you create cases and use it in case templates. To change the default connector for new cases, select the connector from the **Incident management system** list.

### Mapped case fields [mapped-case-fields]

{applies_to}`serverless:` {applies_to}`stack:`

When you export a case to an external system, case fields are mapped to existing fields in the external system. For example, the case title is mapped to the short description in {{sn}} and the summary in {{jira}} incidents. Case tags are mapped to labels in {{jira}}. Case comments are mapped to work notes in {{sn}}.

When you use a {{webhook-cm}} connector, case fields can be mapped to custom or existing fields.

When you push updates to external systems, mapped fields are either overwritten or appended, depending on the field and the connector.

Retrieving data from external systems is not supported.

## Custom fields [case-custom-fields]

You can add optional and required fields for customized case collaboration.

To create a custom field:

1. In the **Custom fields** section, click **Add field**.
2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it's added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.

## Templates [case-templates]

You can make the case creation process faster and more consistent by adding templates. A template defines values for one or all of the case fields (such as severity, tags, description, and title) as well as any custom fields.

To create a template:

1. In the **Templates** section, click **Add template**.
2. You must provide a template name and case severity. You can optionally add template tags and a description, values for each case field, and a case connector.

When users create cases, they can optionally select a template and use its field values or override them.

::::{note}
If you update or delete templates, existing cases are unaffected.
::::


## Observable types [cases-observable-types]

{applies_to}`serverless:` {applies_to}`stack:`

::::{admonition} Requirements
Ensure you have the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
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