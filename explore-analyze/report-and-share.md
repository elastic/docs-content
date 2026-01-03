---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-getting-started.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Reporting and sharing [reporting-getting-started]

$$$install-reporting-packages$$$

$$$set-reporting-server-host$$$

$$$csv-limitations$$$

$$$embed-code$$$

$$$grant-user-access-basic$$$

$$$grant-user-access-external-provider$$$

$$$grant-user-access$$$

$$$reporting-elasticsearch-configuration$$$

$$$reporting-roles-user-api$$$

$$$securing-reporting$$$


{{kib}} provides you with several options to share **Discover** sessions, dashboards, **Visualize Library** visualizations, and **Canvas** workpads. These sharing options are available from the {icon}`share` **Share** and {icon}`download` **Export** menus in the toolbar.

## Permissions

To be able to share objects or generate reports, you must have a role that allows these actions on the specific {{es}} indices and {{kib}} applications containing the data that you want to share. Check [Configuring reporting](/deploy-manage/kibana-reporting-configuration.md) for more information.

## Share with a direct link [share-a-direct-link]

You can share direct links to saved Discover sessions, dashboards, and visualizations. To do that, look for the {icon}`share` **Share** icon.

{applies_to}`stack: ga 9.1` When applicable, you can choose to share the object using a relative or an absolute time range:
* **Relative time range**: The link shows current data. For example, if you share a "Last 7 days" view, users will see the most recent 7 days when they open the link.
* **Absolute time range** (default): The link shows a fixed time period. For example, if you share a "Last 7 days" view on January 7, 2025, the link will always show that exact week of January 1-7, 2025, regardless of when users open the link.

::::{tip}
When sharing an object with unsaved changes, you get a temporary link that might break in the future, for example in case of upgrade. Save the object to get a permanent link instead.
::::


To access the object shared with the link, users need to authenticate.

Anonymous users can also access the link if you have configured [Anonymous authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#anonymous-authentication) and your anonymous service account has privileges to access what you want to share.

![getting a shareable link for a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltc45bb05c1fab3e60/68826ffb4f04ad6e224c2248/share-dashboard.gif)


## Export as a file [manually-generate-reports]

:::{note}
For more information on how to configure reporting in {{kib}}, refer to [Configure reporting in {{kib}}](/deploy-manage/kibana-reporting-configuration.md).
:::

Create and download PDF, PNG, or CSV reports of saved Discover sessions, dashboards, visualizations, and workpads.

* **PDF** {applies_to}`serverless: unavailable` — Generate and download PDF files of dashboards, visualizations, and **Canvas** workpads. PDF reports are a [subscription feature](https://www.elastic.co/subscriptions).
* **PNG** {applies_to}`serverless: unavailable` — Generate and download PNG files of dashboards and visualizations. PNG reports are a [subscription feature](https://www.elastic.co/subscriptions).
* **CSV Reports** — Generate CSV reports of saved Discover sessions. [Certain limitations apply](/explore-analyze/report-and-share.md#csv-limitations).
* **CSV Download** — Generate and download CSV files of **Lens** visualizations.
* **Download as JSON** — Generate and download JSON files of **Canvas** workpads.

$$$reporting-layout-sizing$$$
The layout and size of the report depends on what you are sharing. For saved Discover sessions, dashboards, and visualizations, the layout depends on the size of the panels. For workpads, the layout depends on the size of the worksheet dimensions.

To change the output size, change the size of the browser, which resizes the shareable container before the report generates. It might take some trial and error before you’re satisfied.

In the following dashboard, the shareable container is highlighted:

:::{image} /explore-analyze/images/kibana-shareable-container.png
:alt: Shareable Container
:screenshot:
:::

1. Open the saved Discover session, dashboard, visualization, or **Canvas** workpad you want to share.
2. Choose a file type for the report.

    * {applies_to}`stack: ga 9.1+` From the toolbar, click the {icon}`download` **Export** icon, then choose a file type. 
    * {applies_to}`stack: ga =9.0` From the toolbar, click **Share** > **Export** tab, then choose a file type. Note that when you create a dashboard report that includes a data table or Discover session, the PDF includes only the visible data.

    ::::{note}
    When you create a dashboard report that includes a data table or Discover session, the PDF includes only the visible data.
    ::::

    ::::{tip}

    Tips for generating PDF reports:

    * If you are creating dashboard PDFs, select **For printing** to create printer-friendly PDFs with multiple A4 portrait pages and two visualizations per page.
    * {applies_to}`stack: ga 9.0+` If you are creating workpad PDFs, select **Full page layout** to create PDFs without margins that surround the workpad.
    
    ::::

3. Click the button that generates or exports the report. A message appears, indicating that the report is in the export queue.

    ::::{note}
    To generate the report from outside of {{kib}} or from {{watcher}}, use the POST URL, then submit an HTTP `POST` request using a script or {{watcher}}.

    {applies_to}`stack: ga 9.1+` You can schedule a recurring task in {{kib}} that generates reports on a repeating basis. Refer to [Automatically generate reports](report-and-share/automating-report-generation.md) to learn more. 
    ::::

Go to the **Reporting** page to access all of your reports. To find the page, navigate to **Stack Management > Alerts and Insights > Reporting** in the main menu, or use the [global search field](find-and-organize/find-apps-and-objects.md).

::::{note}
In self-managed installations and {{ech}} deployments, reports are stored in {{es}} and managed by the `kibana-reporting` {{ilm}} ({{ilm-init}}) policy. By default, the policy stores reports forever. To learn more about {{ilm-init}} policies, refer to the {{es}} [{{ilm-init}} documentation](/manage-data/lifecycle/index-lifecycle-management.md).
::::

### CSV report limitations [csv-limitations]

We recommend using CSV reports to export moderate amounts of data only. The feature enables analysis of data in external tools, but it is not intended for bulk export or to backup Elasticsearch data. Report timeout and incomplete data issues are likely if you are exporting data where:

* More than 250 MB of data is being exported
* Data is stored on slow storage tiers
* Any shard needed for the search is unavailable
* Network latency between nodes is high
* Cross-cluster search is used
* ES|QL is used and result row count exceeds the limits of ES|QL queries

To work around the limitations, use filters to create multiple smaller reports, or extract the data you need directly with the Elasticsearch APIs.

For more information on using Elasticsearch APIs directly, see [Scroll API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-scroll), [Point in time API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time), [ES|QL](elasticsearch://reference/query-languages/esql/esql-rest.md) or [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv) with CSV response data format. We recommend that you use an official Elastic language client: details for each programming language library that Elastic provides are in the [{{es}} Client documentation](/reference/elasticsearch-clients/index.md).

[Reporting parameters](kibana://reference/configuration-reference/reporting-settings.md) can be adjusted to overcome some of these limiting scenarios. Results are dependent on data size, availability, and latency factors and are not guaranteed.


### PNG/PDF report limitations [pdf-limitations]
```{applies_to}
serverless: unavailable
```

We recommend using PNG/PDF reports to export moderate amounts of data only. The feature enables a high-level export capability, but it’s not intended for bulk export. If you need to export several pages of image data, consider using multiple report jobs to export a small number of pages at a time. If the screenshot of exported dashboard contains a large number of pixels, consider splitting the large dashboard into smaller artifacts to use less memory and CPU resources.

For the most reliable configuration of PDF/PNG {{report-features}}, consider installing {{kib}} using [Docker](/deploy-manage/deploy/self-managed/install-kibana-with-docker.md) or using [Elastic Cloud](https://cloud.elastic.co).


## Create JSON files [download-as-json]

Create and share JSON files for workpads.

1. Go to **Canvas**.
2. Open the workpad you want to share.
3. From the toolbar, click {icon}`download` **Export**, then select **JSON**.


## Embed outside of {{kib}} [_embed_outside_of_kib]

* {applies_to}`stack: beta` {applies_to}`serverless: beta` **Share on a website** — Download and securely share **Canvas** workpads on any website.
* **Embed code** — Embed fully interactive dashboards as an iframe on web pages.

::::{note}
:name: reporting-on-cloud-resource-requirements

For {{ech}} deployments, {{kib}} instances require a minimum of 2GB RAM to generate PDF or PNG reports. To change {{kib}} sizing, [edit the deployment](https://cloud.elastic.co?page=docs&placement=docs-body).
::::



## Share workpads on a website [add-workpad-website]
```{applies_to}
stack: beta
serverless: beta
```

Create and securely share static **Canvas** workpads on a website. To customize the behavior of the workpad on your website, you can choose to autoplay the pages or hide the workpad toolbar.

1. Go to **Canvas**.
2. Open the workpad you want to share.
3. Click **Share > Share on a website**.
4. To customize the workpad behavior to autoplay the pages or hide the toolbar, use the inline parameters.

   To make sure that your data remains secure, the data in the JSON file is not connected to {{kib}}. **Canvas** does not display elements that manipulate the data on the workpad.

   ::::{note}
   Shareable workpads encode the current state of the workpad in a JSON file. When you make changes to the workpad, the changes do not appear in the shareable workpad on your website.
   ::::

5. To change the settings, click the settings icon, then choose the settings you want to use.


## Embed code [embed-code]

Display your dashboards on an internal company website or personal web page with an iframe. To embed other {{kib}} objects, manually create the HTML code.

For information about granting access to embedded dashboards, refer to [Authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).

1. Open the dashboard you want to share.
2. Click **Share > Embed code**.
3. Specify which parts of the dashboard you want to include: Top menu, query, time filter, and filter bar.
4. Click **Copy embed code**.
