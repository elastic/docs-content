---
navigation_title: Open and manage cases
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Open and manage cases in Elastic Security [security-cases-open-manage]

You can create and manage cases using the UI or the [cases API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-cases).


## Open a new case [cases-ui-open]

Open a new case to keep track of security issues and share their details with colleagues.

1. Find **Cases** in the navigation menu or search for `Security/Cases` by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create case**. If no cases exist, the Cases table will be empty and you’ll be prompted to create one by clicking the **Create case** button inside the table.
2. {applies_to}`stack: preview` {applies_to}`serverless: preview` If you defined [templates](/solutions/security/investigate/configure-case-settings.md#cases-templates), you can optionally select one to use its default field values.
3. Give the case a name, assign a severity level, and provide a description. You can use [Markdown](https://www.markdownguide.org/cheat-sheet) syntax in the case description.

    ::::{note}
    If you do not assign your case a severity level, it will be assigned **Low** by default.
    ::::


    ::::{tip}
    You can insert a Timeline link in the case description by clicking the Timeline icon (![Timeline icon](/solutions/images/security-add-timeline-button.png "title =20x20")).
    ::::

4. Optionally, add a category, assignees and relevant tags. You can add users only if they meet the necessary [prerequisites](/solutions/security/investigate/cases-requirements.md).
5. {applies_to}`stack: preview` {applies_to}`serverless: preview` If you defined [custom fields](/solutions/security/investigate/configure-case-settings.md#cases-ui-custom-fields), they appear in the **Additional fields** section.
6. Choose if you want alert statuses to sync with the case’s status after they are added to the case. This option is turned on by default, but you can turn it off after creating the case.
7. {applies_to}`stack: ga 9.2` With the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md), you can choose to automatically extract observables from alerts that you're adding to the case. This option is turned on by default. You can turn it off after creating the case by toggling **Auto-extract observables** on the case's **Observables** tab.
8. (Optional) Under **External Connector Fields**, you can select a connector to send cases to an external system. If you’ve created any connectors previously, they will be listed here. If there are no connectors listed, you can create one. For more information, refer to [External incident management systems](/solutions/security/investigate/configure-case-settings.md#cases-ui-integrations)

    ::::{note}
    :applies_to:{stack: ga 9.3}
    When specifying **Additional fields** for an {{ibm-r}} connector, fields that are set when an incident is created or changed (for example, an incident is closed) won't display as an option.
    ::::

9. Click **Create case**.

    ::::{note}
    If you’ve selected a connector for the case, the case is automatically pushed to the third-party system it’s connected to.
    ::::

% Check with Lisa if email notifications is an ESS-only feature. Not in Serverless docs: https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html

## Add email notifications [cases-ui-notifications]

You can configure email notifications that occur when users are assigned to cases.

For {{kib}} on {{ecloud}}:

1. Add the email domains to the [notifications domain allowlist](/explore-analyze/alerts-cases/alerts.md).

    You do not need to take any more steps to configure an email connector or update {{kib}} user settings, since the preconfigured Elastic-Cloud-SMTP connector is used by default.


For self-managed {{kib}}:

1. Create a preconfigured email connector.

    ::::{note}
    At this time, email notifications support only [preconfigured email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md), which are defined in the [`kibana.yml`](/deploy-manage/stack-settings.md) file.
    ::::

2. Set the `notifications.connectors.default.email` {{kib}} setting to the name of your email connector.
3. If you want the email notifications to contain links back to the case, you must configure the [server.publicBaseUrl](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.

When you subsequently add assignees to cases, they receive an email.


## Manage existing cases [cases-ui-manage]

From the Cases page, you can search existing cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes. General case metrics, including how long it takes to close cases, are provided above the table.

{applies_to}`stack: ga 9.3.0` To find cases that were created during a specific time range, use the date time picker above the Cases table. The default time selection is the last 30 days. Clicking **Show all cases** displays every {{elastic-sec}} case in your space. The action also adjusts the starting time range to the date of when the first case was created.

To explore a case, click on its name. You can then:

* [Review the case summary](/solutions/security/investigate/open-manage-cases.md#cases-summary)
* [Add and manage comments](/solutions/security/investigate/open-manage-cases.md#cases-manage-comments)

    ::::{tip}
    Comments can contain Markdown. For syntax help, click the Markdown icon (![Click markdown icon](/solutions/images/security-markdown-icon.png "title =20x20")) in the bottom right of the comment.
    ::::

* Examine [alerts](/solutions/security/investigate/open-manage-cases.md#cases-examine-alerts), [indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case), and {applies_to}`stack: ga 9.2.0` [events](/solutions/security/investigate/open-manage-cases.md#cases-examine-events) attached to the case
* [Add files](/solutions/security/investigate/open-manage-cases.md#cases-add-files)
* [Add a Lens visualization](/solutions/security/investigate/open-manage-cases.md#cases-lens-visualization)
* Modify the case’s description, assignees, category, severity, status, and tags.
* [Manage connectors](/solutions/security/investigate/configure-case-settings.md#cases-ui-integrations) and send updates to external systems (if you’ve added a connector to the case)
* [Add observables](/solutions/security/investigate/open-manage-cases.md#cases-add-observables)
* [Copy the case UUID](/solutions/security/investigate/open-manage-cases.md#cases-copy-case-uuid)
* Refresh the case to retrieve the latest updates


### Review the case summary [cases-summary]

Click on an existing case to access its summary. The case summary, located under the case title, contains metrics that summarize alert information and response times. These metrics update when you attach additional unique alerts to the case, add connectors, or modify the case’s status:

* **Total alerts**: Total number of unique alerts attached to the case
* **Associated users**: Total number of unique users that are represented in the attached alerts
* **Associated hosts**: Total number of unique hosts that are represented in the attached alerts
* **Total connectors**: Total number of connectors that have been added to the case
* **Case created**: Date and time that the case was created
* **Open duration**: Time elapsed since the case was created
* **In progress duration**: How long the case has been in the `In progress` state
* **Duration from creation to close**: Time elapsed from when the case was created to when it was closed

### Manage case comments [cases-manage-comments]

To edit, delete, or quote a comment, select the appropriate option from the **More actions** menu (**…**).

:::{image} /solutions/images/security-cases-manage-comments.png
:alt: Shows you a summary of the case
:screenshot:
:::


### Examine alerts attached to a case [cases-examine-alerts]

To explore the alerts attached to a case, click the **Alerts** tab. In the table, alerts are organized from oldest to newest. To [view alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md), click the **View details** button.

:::{image} /solutions/images/security-cases-alert-tab.png
:alt: Shows you the Alerts tab
:screenshot:
:::

::::{note}
Each case can have a maximum of 1,000 alerts.
::::

### Examine events attached to a case [cases-examine-events]
```{applies_to}
stack: ga 9.2
```

After adding events to cases from the Events table (which you can access from the **Events** tab on the **Hosts**, **Network**, or **Users** pages) or from Timeline, you can examine them in the case's **Events** tab. Within the tab, events are organized from newest to oldest. Click the **View details** button to find out more about the event.

### Add files [cases-add-files]

To upload files to a case, select the **Files** tab, then click **Add files**. You can set file types and sizes by configuring your [{{kib}} case settings](kibana://reference/configuration-reference/cases-settings.md).

% Check with Lisa whether following note is only applicable to Serverless or if it's for ESS too.

::::{note}
There is a 10 MiB size limit for images. For all other MIME types, the limit is 100 MiB.

::::

To download or delete the file, or copy the file hash to your clipboard, open the **Actions** menu (**…**). The available hash functions are MD5, SHA-1, and SHA-256.

When you add a file, a comment is added to the case activity log. To view an image, click its name in the activity or file list.


### Add a Lens visualization [cases-lens-visualization]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


Add a Lens visualization to your case to portray event and alert data through charts and graphs.

:::{image} /solutions/images/security-add-vis-to-case.gif
:alt: Shows how to add a visualization to a case
:screenshot:
:::

To add a Lens visualization to a comment within your case:

1. Click the **Visualization** button. The **Add visualization** dialog appears.
2. Select an existing visualization from your Visualize Library or create a new visualization.

    ::::{important}
    Set an absolute time range for your visualization. This ensures your visualization doesn’t change over time after you save it to your case, and provides important context for others managing the case.
    ::::

3. Save the visualization to your Visualize Library by clicking the **Save to library** button (optional).

    1. Enter a title and description for the visualization.
    2. Choose if you want to keep the **Update panel on Security** activated. This option is activated by default and automatically adds the visualization to your Visualize Library.

4. After you’ve finished creating your visualization, click **Save and return** to go back to your case.
5. Click **Preview** to show how the visualization will appear in the case comment.
6. Click **Add Comment** to add the visualization to your case.

Alternatively, while viewing a [dashboard](/solutions/security/dashboards.md) you can open a panel’s menu then click **More actions (…) → Add to existing case** or **More actions (…) → Add to new case**.

After a visualization has been added to a case, you can modify or interact with it by clicking the **Open Visualization** option in the case’s comment menu.

:::{image} /solutions/images/security-cases-open-vis.png
:alt: Shows where the Open Visualization option is
:screenshot:
:::


### Add observables [cases-add-observables]

::::{admonition} Requirements
Ensure you have the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

::::


An observable is a piece of information about an investigation, for example, a suspicious URL or a file hash. Use observables to identify correlated events and better understand the severity and scope of a case.

To create an observable:

1. Click the **Observables** tab, then click **Add observable**.

    ::::{note}
    Each case can have a maximum of 50 observables.
    ::::

2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/solutions/security/investigate/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Click **Add observable**.

After adding an observable to a case, you can remove or edit it by using the **Actions** menu (**…**).

::::{tip}
Go to the **Similar cases** tab to access other cases with the same observables.
::::

### Copy the case UUID [cases-copy-case-uuid]

Each case has a universally unique identifier (UUID) that you can copy and share. To copy a case’s UUID to a clipboard, go to the Cases page and select **Actions** → **Copy Case ID** for the case you want to share. Alternatively, go to a case’s details page, then from the **More actions** menu (…), select **Copy Case ID**.

:::{image} /solutions/images/security-cases-copy-case-id.png
:alt: Copy Case ID option in More actions menu
:width: 250px
:screenshot:
:::


## Export and import cases [cases-export-import]

Cases can be [exported](/solutions/security/investigate/open-manage-cases.md#cases-export) and [imported](/solutions/security/investigate/open-manage-cases.md#cases-import) as saved objects using the {{kib}} [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md) UI.

::::{important}
Before importing Lens visualizations, Timelines, or alerts into a space, ensure their data is present. Without it, they won’t work after being imported.
::::



### Export a case [cases-export]

Use the **Export** option to move cases between different {{elastic-sec}} instances. When you export a case, the following data is exported to a newline-delimited JSON (`.ndjson`) file:

* Case details
* User actions
* Text string comments
* Case alerts
* Lens visualizations (exported as JSON blobs).

::::{note}
The following attachments are *not* exported:

* **Case files**: Case files are not exported. However, they are accessible from **Files** (find **Files** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)) to download and re-add.
* **Alerts**: Alerts attached to cases are not exported. You must re-add them after importing cases.

::::


To export a case:

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for the case by choosing a saved object type or entering the case title in the search bar.
3. Select one or more cases, then click the **Export** button.
4. Click **Export**. A confirmation message that your file is downloading displays.

    ::::{tip}
    Keep the **Include related objects** option enabled to ensure connectors are exported too.
    ::::


:::{image} /solutions/images/security-cases-export-button.png
:alt: Shows the export saved objects workflow
:screenshot:
:::


### Import a case [cases-import]

To import a case:

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Import**.
3. Select the NDJSON file containing the exported case and configure the import options.
4. Click **Import**.
5. Review the import log and click **Done**.

    ::::{important}
    Be mindful of the following:

    * If the imported case had connectors attached to it, you’ll be prompted to re-authenticate the connectors. To do so, click **Go to connectors** on the **Import saved objects** flyout and complete the necessary steps. You can also access connectors from the **{{connectors-ui}}** page (find **{{connectors-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).
    * If the imported case had attached alerts, verify that the alerts' source documents exist in the environment. Case features that interact with alerts (such as the Alert details flyout and rule details page) rely on the alerts' source documents to function.

    ::::

## Search cases [search-security-cases]
