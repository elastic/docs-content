---
navigation_title: Manage cases
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

# Manage cases [manage-cases]

After creating a case, you can update it with additional information, add supporting materials, and share it with colleagues or external systems.

You can manage cases using the UI or the [cases API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-cases).

## Manage existing cases [manage-case]

You can search existing cases and filter them by attributes such as assignees, categories, severity, status, and tags. You can also select multiple cases and use bulk actions to delete cases or change their attributes.

To view a case, select its name. You can then:

* Add and edit the case's description, comments, assignees, tags, status, severity, and category.

    {applies_to}`stack: ga 9.2+` Copy and paste images into case comments using `Ctrl/Cmd` + `C` and `Ctrl/Cmd` + `V` shortcuts. Pasted images are preformatted in Markdown.

* Add a connector (if you did not select one while creating the case).
* Send updates to external systems (if external connections are configured).
* Refresh the case to retrieve the latest updates.

## Review the case summary [cases-summary]

{applies_to}`serverless:` {applies_to}`stack:`

Select an existing case to access its summary. The case summary, located under the case title, contains metrics that summarize alert information and response times:

* **Total alerts**: Total number of unique alerts attached to the case
* **Associated users**: Total number of unique users that are represented in the attached alerts
* **Associated hosts**: Total number of unique hosts that are represented in the attached alerts
* **Total connectors**: Total number of connectors that have been added to the case
* **Case created**: Date and time that the case was created
* **Open duration**: Time elapsed since the case was created
* **In progress duration**: How long the case has been in the `In progress` state
* **Duration from creation to close**: Time elapsed from when the case was created to when it was closed

## Add visualizations [cases-lens-visualization]

Add a Lens visualization to your case to portray event and alert data through charts and graphs.

To add a visualization to a comment within your case:

1. Select the **Visualization** button. The **Add visualization** dialog appears.
2. Select an existing visualization from your Visualize Library or create a new visualization.

    ::::{important}
    Set an absolute time range for your visualization. This ensures your visualization doesn't change over time after you save it to your case, and provides important context for others viewing the case.
    ::::

3. Save the visualization to your Visualize Library by selecting the **Save to library** button (optional).
4. After you've finished creating your visualization, select **Save and return** to go back to your case.
5. Select **Preview** to show how the visualization will appear in the case comment.
6. Select **Add Comment** to add the visualization to your case.

Alternatively, while viewing a dashboard you can open a panel's menu then select **More actions (…) → Add to existing case** or **More actions (…) → Add to new case**.

After a visualization has been added to a case, you can modify or interact with it by selecting the **Open Visualization** option in the case's comment menu.

## Add context and supporting materials [add-case-context]

Provide additional context and resources by adding the following to the case:

::::{tip}
:applies_to: {stack: ga 9.3}
From the **Attachments** tab, you can search for specific observable values, alert IDs, and file names.
::::

* [Alerts](#add-case-alerts)
* [Files](#add-case-files)
* [Observables](#add-case-observables)


Additional options in {{elastic-sec}}:
* [Events](/solutions/security/investigate/security-cases-features.md#cases-examine-events)
* [Indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case)


### Add alerts [add-case-alerts]

Escalate alerts and track them in a single place by attaching them to cases. To examine the alerts, select the **Alerts** tab in the case. In the table, alerts are organized from oldest to newest. To view alert details, select the **View details** button.

You can find the **Alerts** tab in the following places:

- {applies_to}`serverless:` {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

::::{important}
Each case can have a maximum of 1,000 alerts.
::::

### Add files [add-case-files]

After you create a case, you can upload and manage files on the **Files** tab. To find the tab:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0`: Go to the case's details page.

To download or delete the file or copy the file hash to your clipboard, open the action menu {icon}`boxes_horizontal`. The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, select its name in the activity or file list.

::::{tip}
Uploaded files are also accessible from the **Files** management page, which you can find using the navigation menu or entering `Files` into the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
::::

### Add observables [add-case-observables]

An observable is a piece of information about an investigation, for example, a suspicious URL or a file hash. Use observables to identify correlated events and better understand the severity and scope of a case. 

View and manage observables from the **Observables** tab. You can find the tab in the following places:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0`: Go to the case's details page.  

::::{important}
Each case can have a maximum of 50 observables.
::::

To create an observable:

1. Select **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/explore-analyze/cases/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Select **Add observable**.

After adding an observable to a case, you can remove or edit it by using the **Actions** menu (**…**). 

::::{tip}
Go to the **Similar cases** tab to access other cases with the same observables.
::::

{applies_to}`stack: ga 9.2` {applies_to}`serverless:` With the appropriate subscription or project feature tier, you can use **Auto-extract observables** to instantly extract observables from alerts that you're adding to the case.

## Add Lens visualizations [cases-lens-visualization]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::

Add a Lens visualization to your case to portray event and alert data through charts and graphs.

1. Click the **Visualization** button. The **Add visualization** dialog appears.
2. Select an existing visualization from your Visualize Library or create a new visualization.

    ::::{important}
    Set an absolute time range for your visualization. This ensures your visualization doesn't change over time after you save it to your case, and provides important context for others managing the case.
    ::::

3. Save the visualization to your Visualize Library by clicking the **Save to library** button (optional).

    1. Enter a title and description for the visualization.
    2. Choose if you want to keep the **Update panel on Security** activated. This option is activated by default and automatically adds the visualization to your Visualize Library.

4. After you've finished creating your visualization, click **Save and return** to go back to your case.
5. Click **Preview** to show how the visualization will appear in the case comment.
6. Click **Add Comment** to add the visualization to your case.

Alternatively, while viewing a dashboard you can open a panel's menu then click **More actions (…) → Add to existing case** or **More actions (…) → Add to new case**.

After a visualization has been added to a case, you can modify or interact with it by clicking the **Open Visualization** option in the case's comment menu.

## Export and import cases [cases-export-import]

Cases can be exported and imported as saved objects using the {{kib}} [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md) UI.

::::{note}
Before importing Lens visualizations, Timelines, or alerts into a space, ensure their data is present. Without it, they won't work after being imported.
::::

### Export a case [cases-export]

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for the case by choosing a saved object type or entering the case title in the search bar.
3. Select one or more cases, then click the **Export** button.
4. Click **Export**. The following data will exported to a newline-delimited JSON (`.ndjson`) file:

    * Case details
    * User actions
    * Text string comments
    * Case alerts
    * Lens visualizations (exported as JSON blobs)

    ::::{tip}
    Keep the **Include related objects** option enabled to ensure connectors are exported too.
    ::::

:::{note} 
The following attachments are *not* exported:

* **Case files**: Case files are not exported, but you can access them from the **Files** page (find **Files** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).
* **Alerts**: You must re-add alerts that were attached to the case and ensure the alerts' source documents are present in the environment. Case features that interact with alerts rely on the source documents to properly function.
:::

### Import a case [cases-import]

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Import**.
3. Select the NDJSON file containing the exported case and configure the import options.
4. Click **Import**.
5. Review the import log and click **Done**.

::::{note}
If the imported case had connectors attached to it, you'll be prompted to re-authenticate the connectors. To do so, click **Go to connectors** on the **Import saved objects** flyout and complete the necessary steps. You can also access connectors from the **{{connectors-ui}}** page (find **{{connectors-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).
::::