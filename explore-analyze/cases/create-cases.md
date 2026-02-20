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

1. Go to the **Cases** page, then select **Create case**.

   ::::{applies-switch}

   :::{applies-item} stack: ga
   To access the **Cases** page:
   * **{{stack-manage-app}}**: Go to **{{stack-manage-app}}** > **Cases**.
   * **{{elastic-sec}}**: Find **Cases** in the navigation menu or search for `Security/Cases` using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
   * **{{observability}}**: Find **Cases** in the navigation menu or search for `Observability/Cases` using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
   :::

   :::{applies-item} serverless: ga
   To access the **Cases** page:
   * **{{elastic-sec}}**: Find **Cases** in the navigation menu or search for `Cases` using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
   * **{{observability}}**: Find **Cases** in the navigation menu or search for `Cases` using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

   :::

   ::::

2. (Optional) Select a [template](configure-case-settings.md#case-templates) to pre-fill field values.

3. Enter a name, severity, and description. If you do not assign your case a severity level, it will be assigned **Low** by default. The description supports [Markdown](https://www.markdownguide.org/cheat-sheet).

4. (Optional) Add a category, [assignees](control-case-access.md), and tags.

5. (Optional) Fill in any [custom fields](configure-case-settings.md#case-custom-fields) in the **Additional fields** section.

6. Configure sync and extraction options:
   * **Sync alert status** syncs alert statuses with the case status (on by default).
   * {applies_to}`security: ga 9.2+` **Auto-extract observables** extracts observables from attached alerts (on by default, requires appropriate subscription).

      :::{note}
      Observables are not available in {{observability}} for {{stack}} or {{serverless-short}}.
      :::

7. (Optional) Select a [connector](configure-case-settings.md#case-connectors) to send the case to an external system.

8. Select **Create case**. If you've selected a connector for the case, the case is automatically pushed to the third-party system it's connected to.

## Set up email notifications [add-case-notifications]

Set up email notifications to alert users when they're assigned to a case, so they can respond promptly.

:::::{tab-set}

:::{tab-item} {{ecloud}}

Add the email domains to the [notifications domain allowlist](/explore-analyze/alerting/alerts.md).

You do not need to configure an email connector or update {{kib}} user settings—the preconfigured Elastic-Cloud-SMTP connector is used by default.

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

Alerts also can't cross solution boundaries—you can only attach alerts from the same solution to cases. For example, you can't attach {{observability}} alerts to an {{elastic-sec}} case.