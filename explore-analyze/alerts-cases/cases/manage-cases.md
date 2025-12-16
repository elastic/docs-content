---
navigation_title: Open and manage cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Open and manage cases in {{kib}} [manage-cases]

Open a new case to keep track of issues and share their details with colleagues. You can create and manage cases using the cases UI.

:::{note} 
**Requirements**

To access and send cases to external systems, you need the appropriate [subscription or feature tier](https://www.elastic.co/pricing), and your role must have the required {{kib}} feature privileges. Refer to [](../../../explore-analyze/alerts-cases/cases/setup-cases.md) for more information.
:::

## Open a new case [open-case]

To open a case:

1. Go to **Management > {{stack-manage-app}} > Cases**, then click **Create case**.
   :::{image} /explore-analyze/images/kibana-cases-create.png
   :alt: Create a case in {{stack-manage-app}}
   :screenshot:
   :::

2. If you defined [templates](manage-cases-settings.md#case-templates), you can optionally select one to use its default field values.
3. Give the case a name, severity, and description.
   ::::{tip}
   In the `Description` area, you can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax to create formatted text.
   ::::

4. Optionally, add a category, assignees, and tags. You can add users only if they meet the necessary [prerequisites](setup-cases.md).
5. If you defined any [custom fields](manage-cases-settings.md#case-custom-fields), they appear in the **Additional fields** section.
6. (Optional) Under **External Connector Fields**, you can select a connector to send cases to an external system. If you’ve created any connectors previously, they will be listed here. If there are no connectors listed, you can create one. For more information, refer to [External incident management systems](manage-cases-settings.md#case-connectors).

    ::::{note}
    :applies_to:{stack: ga 9.3}
    When specifying **Additional fields** for an {{ibm-r}} connector, fields that are set when an incident is created or changed (for example, an incident is closed) won't display as an option.
    ::::


7. After you’ve completed all of the required fields, click **Create case**.

{applies_to}`stack: preview` {applies_to}`serverless: preview` Alternatively, you can configure your rules to automatically create cases by using [case actions](kibana://reference/connectors-kibana/cases-action-type.md). By default, the rule adds all of the alerts within a specified time window to a single case. You can optionally choose a field to group the alerts and create separate cases for each group. You can also choose whether you want the rule to reopen cases or open new ones when the time window elapses.

## Add email notifications [add-case-notifications]

You can configure email notifications that occur when users are assigned to cases.

For {{kib}} on {{ecloud}}:

1. Add the email domains to the [notifications domain allowlist](../alerts.md).

    You do not need to take any more steps to configure an email connector or update {{kib}} user settings, since the preconfigured Elastic-Cloud-SMTP connector is used by default.

For self-managed {{kib}}:

1. Create a preconfigured email connector.
   ::::{note}
   At this time, email notifications support only preconfigured connectors, which are defined in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. For examples, refer to [Email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md#preconfigured-email-configuration) and [Configure email accounts for well-known services](kibana://reference/connectors-kibana/email-action-type.md#configuring-email).
   ::::

2. Set the `notifications.connectors.default.email` {{kib}} setting in kibana.yml to the name of your email connector.

   ```js
   notifications.connectors.default.email: ‘mail-dev’

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

3. If you want the email notifications to contain links back to the case, you must configure the [server.publicBaseUrl](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.

When you subsequently add assignees to cases, they receive an email.

## Add files [add-case-files]

After you create a case, you can upload and manage files on the **Files** tab. To find the tab:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0`: Go to the case's details page.  

To download or delete the file or copy the file hash to your clipboard, open the action menu (**...**). The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, click its name in the activity or file list.

::::{note}
Uploaded files are also accessible from the **Files** management page, which you can find using the navigation menu or entering `Files` into the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
::::

::::{important}
When you export cases as [saved objects](/explore-analyze/find-and-organize/saved-objects.md), the attached case files are not exported.
::::

## Add visualizations [add-case-visualization]

You can also optionally add visualizations. For example, you can portray event and alert data through charts and graphs.

:::{image} /explore-analyze/images/kibana-cases-visualization.png
:alt: Adding a visualization as a comment within a case
:screenshot:
:::

To add a visualization to a comment within your case:

1. Click the **Visualization** button. The **Add visualization** dialog appears.
2. Select an existing visualization from your Visualize Library or create a new visualization.
   ::::{important}
   Set an absolute time range for your visualization. This ensures your visualization doesn’t change over time after you save it to your case and provides important context for viewers.
   ::::

3. After you’ve finished creating your visualization, click **Save and return** to go back to your case.
4. Click **Preview** to see how the visualization will appear in the case comment.
5. Click **Add Comment** to add the visualization to your case.

Alternatively, while viewing a [dashboard](../../dashboards.md) you can open a panel’s menu then click **More > Add to existing case** or **More > Add to new case**.

After a visualization has been added to a case, you can modify or interact with it by clicking the **Open Visualization** option in the case’s comment menu.

## Manage cases [manage-case]

In **Management > {{stack-manage-app}} > Cases**, you can search cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes. 

{applies_to}`stack: ga 9.3.0` To find cases that were created during a specific time range, use the date time picker above the Cases table. The default time selection is the last 30 days. Clicking **Show all cases** displays every {{stack-manage-app}} case in your space. The action also adjusts the starting time range to the date of when the first case was created. 

To view a case, click on its name. You can then:

* Add and edit the case's description, comments, assignees, tags, status, severity, and category.
* Add a connector (if you did not select one while creating the case).
* Send updates to external systems (if external connections are configured).
* Refresh the case to retrieve the latest updates.
* Add and manage the following items:
   * Alerts
   * Files
   * Observables