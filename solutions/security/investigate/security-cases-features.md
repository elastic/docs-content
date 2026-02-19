---
navigation_title: Security case features
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

# Security case features [security-cases-features]

{{elastic-sec}} includes additional case features beyond the core functionality. For general case management, refer to [Open and manage cases](/explore-analyze/cases/manage-cases.md).

## Timeline integration [cases-timeline]

You can integrate Timeline with your cases to provide additional context and investigation capabilities.

::::{tip}
You can insert a Timeline link in the case description by clicking the Timeline icon (![Timeline icon](/solutions/images/security-add-timeline-button.png "title =20x20")).
::::

For more information about Timeline, refer to [Timeline](/solutions/security/investigate/timeline.md).

## Add events [cases-examine-events]

```{applies_to}
stack: ga 9.2
```

Escalate events and track them in a single place by attaching them to cases. You can add events from an investigation that you've opened in Timeline, or from the **Events** tab on the **Hosts**, **Network**, or **Users** pages.

After adding events to a case, go to the **Events** tab to examine them. Within the tab, events are organized from newest to oldest. Click the **View details** button to find out more about the event.

You can find the **Events** tab in the following places:

- {applies_to}`serverless:` {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga =9.2`: Go to the case's details page.

## Add indicators [cases-indicators]

You can add threat intelligence indicators to cases for enhanced investigation. Refer to [Review indicator details in a case](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case) for more information.

## Add Lens visualizations [cases-lens-visualization]

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
    Set an absolute time range for your visualization. This ensures your visualization doesn't change over time after you save it to your case, and provides important context for others managing the case.
    ::::

3. Save the visualization to your Visualize Library by clicking the **Save to library** button (optional).

    1. Enter a title and description for the visualization.
    2. Choose if you want to keep the **Update panel on Security** activated. This option is activated by default and automatically adds the visualization to your Visualize Library.

4. After you've finished creating your visualization, click **Save and return** to go back to your case.
5. Click **Preview** to show how the visualization will appear in the case comment.
6. Click **Add Comment** to add the visualization to your case.

Alternatively, while viewing a [dashboard](/solutions/security/dashboards.md) you can open a panel's menu then click **More actions (…) → Add to existing case** or **More actions (…) → Add to new case**.

After a visualization has been added to a case, you can modify or interact with it by clicking the **Open Visualization** option in the case's comment menu.

:::{image} /solutions/images/security-cases-open-vis.png
:alt: Shows where the Open Visualization option is
:screenshot:
:::

## Export and import cases [cases-export-import]

Cases can be exported and imported as saved objects using the {{kib}} [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md) UI.

::::{important}
Before importing Lens visualizations, Timelines, or alerts into a space, ensure their data is present. Without it, they won't work after being imported.
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

    * If the imported case had connectors attached to it, you'll be prompted to re-authenticate the connectors. To do so, click **Go to connectors** on the **Import saved objects** flyout and complete the necessary steps. You can also access connectors from the **{{connectors-ui}}** page (find **{{connectors-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).
    * If the imported case had attached alerts, verify that the alerts' source documents exist in the environment. Case features that interact with alerts (such as the Alert details flyout and rule details page) rely on the alerts' source documents to function.
    ::::
