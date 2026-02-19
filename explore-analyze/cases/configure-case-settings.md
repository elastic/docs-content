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

# Configure case settings [configure-case-settings]

Configure case closure options, custom fields, templates, and connectors for external incident management systems.

To access case settings:
* For **{{stack-manage-app}}**: Go to **{{stack-manage-app}} > Cases** and click **Settings**.
* For **{{elastic-sec}}**: Find **Cases** in the navigation menu or search for `Security/Cases`, then click **Settings**.
* For **{{observability}}**: Go to **Cases** → **Settings**.


::::{note}
To perform these tasks, you must have [full access](control-case-access.md) to the appropriate case and connector features.

{applies_to}`serverless:` For {{observability}} serverless projects, the **Editor** role or higher is required to create and edit connectors. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
::::


## Close cases automatically [case-closures]

If you close cases in your external incident management system, the cases will remain open in {{kib}} until you close them manually.

To close cases when they are sent to an external system, select the option to automatically close cases when pushing a new incident to an external system.

## Configure external connectors [case-connectors]

Connectors let you send cases to external incident management systems. To create and manage connectors, you need the appropriate {{kib}} feature privileges and subscription or project feature tier. Refer to [Control access to cases](control-case-access.md).

### Create a connector [create-connector]

You can create connectors in **{{stack-manage-app}} > {{connectors-ui}}** (see [Connectors](/deploy-manage/manage-connectors.md)) or from the case **Settings** page:

1. From the **Incident management system** list, select **Add new connector**.
2. Select the system to send cases to:

    * [{{ibm-r}} connector](kibana://reference/connectors-kibana/resilient-action-type.md)
    * [{{jira}} connector](kibana://reference/connectors-kibana/jira-action-type.md)
    * [{{sn-itsm}} connector](kibana://reference/connectors-kibana/servicenow-action-type.md)
    * [{{sn-sir}} connector](kibana://reference/connectors-kibana/servicenow-sir-action-type.md)
    * [{{swimlane}} connector](kibana://reference/connectors-kibana/swimlane-action-type.md)
    * [{{hive}} connector](kibana://reference/connectors-kibana/thehive-action-type.md)
    * [{{webhook-cm}} connector](kibana://reference/connectors-kibana/cases-webhook-action-type.md)

3. Enter your required settings, then click **Save**.

### Edit a connector [edit-connector]

1. Select the required connector from the incident management system list.
2. Click **Update <connector name>**.
3. Modify the connector fields as needed, then click **Save & close**.

### Set the default connector [default-connector]

Select a connector from the **Incident management system** list to set it as the default for new cases. You can also choose a connector when creating individual cases or in case templates.

### About field mappings [mapped-case-fields]

When you push a case to an external system, case fields are automatically mapped to corresponding fields in that system. For example, the case title maps to the short description in {{sn}} and the summary in {{jira}}. Case tags map to labels in {{jira}}, and comments map to work notes in {{sn}}.

With a {{webhook-cm}} connector, you can map case fields to custom or existing fields.

When you push updates, mapped fields are either overwritten or appended, depending on the field and connector. Retrieving data from external systems is not supported.

## Add custom fields [case-custom-fields]

You can add optional and required fields for customized case collaboration.

To create a custom field:

1. In the **Custom fields** section, click **Add field**.
2. You must provide a field label and type (text or toggle). You can optionally designate it as a required field and provide a default value.

When you create a custom field, it's added to all new and existing cases. In existing cases, new custom text fields initially have null values.

You can subsequently remove or edit custom fields on the **Settings** page.

## Create templates [case-templates]

Templates let you pre-fill case fields like severity, tags, title, description, and custom fields—speeding up case creation and ensuring consistency across your team. When creating a case, you can select a template and use its values or override them. Updating or deleting templates does not affect existing cases.

To create a template:

1. In the **Templates** section, click **Add template**.
2. Provide a template name and case severity. 
3. (Optional) Add template tags and a description, values for each case field, and a case connector.

## Add observable types [cases-observable-types]

::::{admonition} Requirements
Ensure you have the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

In addition to the preset observable types (such as IP addresses and file hashes), you can create up to 10 custom types to match your investigation needs. Custom observable types appear as options when you [add observables to cases](manage-cases.md#add-case-observables).

1. In the **Observable types** section, click **Add observable type**.
2. Enter a descriptive label for the observable type, then click **Save**.

You can edit or remove custom observable types from the **Settings** page. Be aware that deleting a custom observable type also deletes all instances of it from your cases.