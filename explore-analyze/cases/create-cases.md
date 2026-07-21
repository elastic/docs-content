---
navigation_title: Create cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases.html
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Create cases to track incidents, attach alerts and files, assign team members, and push updates to external systems.
---

# Create cases [create-cases]

To create a new case:

1. Find **Cases** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create case**.

   :::{note}
   Cases are [scoped by solution](#cases-limitations). On {{stack}}, search for `Security/Cases` or `Observability/Cases`, or go to **{{stack-manage-app}}** > **Cases**. On {{serverless-short}}, search for `Cases` in {{elastic-sec}} or {{observability}}.
   :::

2. (Optional) Select a template to pre-fill values.
   * {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Create and manage templates on the **Templates** page. Refer to [Case templates](manage-case-templates.md).
   * {applies_to}`stack: ga 9.0-9.4` Create and manage templates in [case settings](configure-case-settings.md#case-templates).

3. Enter a name, severity, and description. Optionally add a category, [assignees](control-case-access.md#give-assignee-access), tags, and additional fields.
   * {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Additional fields come from the [field library](create-case-field-library.md).
   * {applies_to}`stack: ga 9.0-9.4` Additional fields are [custom fields](configure-case-settings.md#case-custom-fields) configured in case settings.

4. (Optional) Adjust sync and extraction options, or leave the defaults:
   * **Sync alert status** syncs alert statuses with the case status (on by default).
   * **Auto-extract observables** extracts observables from attached alerts (on by default). Available in {{sec-serverless}} and {{elastic-sec}} 9.2+ only.

5. (Optional) Select a [connector](configure-case-settings.md#case-connectors) to send the case to an external system. When you create the case, it's pushed to that system automatically.

6. Select **Create case**.

After creating a case, [attach objects](attach-objects-to-cases.md) such as alerts, files, observables, and visualizations. To notify users when they're assigned to a case, [set up email notifications](#add-case-notifications).

## Set up email notifications [add-case-notifications]

Set up email notifications to alert users when they're assigned to a case, so they can respond promptly.

:::::{tab-set}

:::{tab-item} {{ecloud}}

Add the email domains to the [notifications domain allowlist](/explore-analyze/alerting/alerts.md).

You do not need to configure an email connector or update {{kib}} user settings. The preconfigured Elastic-Cloud-SMTP connector is used by default.

:::

:::{tab-item} Self-managed

1. Create a preconfigured email connector.

    ::::{note}
    Email notifications support only [preconfigured email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md), which are defined in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. For examples, refer to [Email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md#preconfigured-email-configuration) and [Configure email accounts for well-known services](kibana://reference/connectors-kibana/email-action-type.md#configuring-email).
    ::::

2. Set the `notifications.connectors.default.email` {{kib}} setting to the name of your email connector.

    ```yaml
    notifications.connectors.default.email: 'mail-dev'

    xpack.actions.preconfigured:
      mail-dev:
        name: preconfigured-email-notification-maildev
        actionTypeId: .email
        config:
          service: other
          from: from address
          host: host name
          port: port number
          secure: true/false
          hasAuth: true/false
    ```

3. If you want the email notifications to contain links back to the case, configure the [server.publicBaseUrl](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.

:::

:::::

## Case visibility across solutions [cases-limitations]

A case created in one solution is only visible within that solution:

* **{{stack-manage-app}}** cases are not visible in {{observability}} or {{elastic-sec}}
* **{{observability}}** cases are not visible in {{stack-manage-app}} or {{elastic-sec}}
* **{{elastic-sec}}** cases are not visible in {{stack-manage-app}} or {{observability}}

Alerts also can't cross solution boundaries. You can only attach alerts from the same solution to cases. For example, you can't attach {{observability}} alerts to an {{elastic-sec}} case.
