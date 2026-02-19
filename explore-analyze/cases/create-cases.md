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
---

# Create cases [create-cases]

1. Go to the **Cases** page:
   * For **{{stack-manage-app}}**: Go to **Management > {{stack-manage-app}} > Cases**, then select **Create case**.
   * For **{{elastic-sec}}**: Find **Cases** in the navigation menu or search for `Security/Cases`, then select **Create case**.
   * For **{{observability}}**: Find **Cases** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create case**.


2. If you defined [templates](configure-case-settings.md#case-templates), you can optionally select one to use its default field values.

3. Give the case a name, severity, and description.

    ::::{tip}
    In the **Description** area, you can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax to create formatted text.
    ::::

    ::::{note}
    If you do not assign your case a severity level, it will be assigned **Low** by default.
    ::::

4. Optionally, add a category, assignees, and tags. You can add users only if they meet the necessary [prerequisites](control-case-access.md).

5. If you defined [custom fields](configure-case-settings.md#case-custom-fields), they appear in the **Additional fields** section.

6. Choose if you want alert statuses to sync with the case's status after they're added to the case. This option is turned on by default.

7. {applies_to}`stack: ga 9.2+` {applies_to}`serverless:` With the appropriate subscription or project feature tier, you can select to automatically extract observables from alerts that you're adding to the case. This option is turned on by default.

8. (Optional) Under **External Connector Fields**, you can select a connector to send cases to an external system. If you've created any connectors previously, they will be listed here. If there are no connectors listed, you can create one. For more information, refer to [External incident management systems](configure-case-settings.md#case-connectors).

9. Select **Create case**.

If you've selected a connector for the case, the case is automatically pushed to the third-party system it's connected to.

{applies_to}`stack: preview` {applies_to}`serverless: preview` Alternatively, you can configure your rules to automatically create cases by using [case actions](kibana://reference/connectors-kibana/cases-action-type.md). By default, the rule adds all of the alerts within a specified time window to a single case.

::::{tip}
You can also create a case from an alert or add an alert to an existing case. From the **Alerts** page, select the **More options** icon and choose either **Add to existing case** or **Create new case**.
::::

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

Alerts also can't be accessed across solutions. You can only attach alerts the same solution to cases. For example, you can't attach {{observability}} alerts to an {{elastic-sec}} case.