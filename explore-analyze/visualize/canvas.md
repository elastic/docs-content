---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/canvas.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Canvas [canvas]

:::{note}
Canvas is only available for upgraded installations with existing workpads.
:::

**Canvas** is a data visualization and presentation tool that allows you to pull live data from {{es}}, then combine the data with colors, images, text, and your imagination to create dynamic, multi-page, pixel-perfect displays. If you are a little bit creative, a little bit technical, and a whole lot curious, then **Canvas** is for you.

With **Canvas**, you can:

* Create and personalize your work space with backgrounds, borders, colors, fonts, and more.
* Customize your workpad with your own visualizations, such as images and text.
* Pull your data directly from {{es}}, then show it off with charts, graphs, progress monitors, and more.
* Focus the data you want to display with filters.

:::{image} /explore-analyze/images/kibana-canvas_logWebTrafficWorkpadTemplate_7.17.0.png
:alt: Logs Web Traffic workpad template
:::


## Create workpads [create-workpads]

A *workpad* provides you with a space where you can build presentations of your live data. You can create a workpad from scratch, start with a preconfigured workpad, import an existing workpad, or use a sample data workpad.


### Minimum requirements [canvas-minimum-requirements]

To create workpads, you must meet the minimum requirements.

* If you need to set up {{kib}}, use [our free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs).
* Make sure you have [data indexed into {{es}}](/manage-data/ingest.md) and a [data view](../find-and-organize/data-views.md).
* Have an understanding of [{{es}} documents and indices](../../manage-data/data-store/index-basics.md).
* Make sure you have sufficient privileges to create and save workpads. When the read-only indicator appears, you have insufficient privileges, and the options to create and save workpads are unavailable. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).

You can open **Canvas** using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).


### Start with a blank workpad [start-with-a-blank-workpad]

To use the background colors, images, and data of your choice, start with a blank workpad.

1. On the **Canvas** page, click **Create workpad**.
2. Specify the **Workpad settings**.

    1. Add a **Name** to your workpad.
    2. In the **Width** and **Height** fields, specify the size, or select one of default layouts.
    3. Click the **Background** color picker, then select the color for your workpad.



### Create workpads from templates [create-workpads-from-templates]

If you’re unsure about where to start, you can use one of the preconfigured templates that come with **Canvas**.

1. On the **Canvas** page, select **Templates**.
2. Click the preconfigured template that you want to use.
3. Add your own **Name** to the workpad.


### Import existing workpads [import-existing-workpads]

When you want to use a workpad that someone else has already started, import the JSON file.

On the **Canvas** page, drag the file to the **Import workpad JSON file** field.


### Use sample data workpads [use-sample-data-workpads]

Each of the {{kib}} sample data sets comes with a workpad that you can use for your own workpad inspiration.

1. Add a [sample data set](../index.md#gs-get-data-into-kibana).
2. On a sample data card, click **View data**, then select **Canvas**.


## Add elements [add-canvas-elements]

Create a story about your data by adding elements to your workpad that include images, text, charts, and more.


### Create elements [create-elements]

Choose the type of element you want to use, then use the preconfigured demo data to familiarize yourself with the element. When you’re ready, connect the element to your own data. By default, most of the elements you create use the demo data until you change the data source. The demo data includes a small data set that you can use to experiment with your element.

1. Click **Add element**, then select the element you want to use.
2. To connect the element to your data, select **Data > Demo data**, then select one of the following data sources:

    * **{{es}} SQL** — Access your data in {{es}} using [SQL syntax](elasticsearch://reference/query-languages/sql/sql-spec.md).
    * **{{es}} documents** — Access your data in {{es}} without using aggregations. To use, select a {{data-source}} and fields. Use **{{es}} documents** when you have low-volume datasets, and you want to view raw documents or to plot exact, non-aggregated values on a chart.
    * **Timelion** — Access your time series data using [**Timelion**](legacy-editors/timelion.md) queries. To use **Timelion** queries, you can enter a query using the [Lucene Query Syntax](../query-filter/languages/lucene-query-syntax.md).

        Each element can display a different {{data-source}}, and pages and workpads often contain multiple {{data-sources}}.

3. To save, use the following options:

    * To save a single element, select the element, then click **Edit > Save as new element**.
    * To save a group of elements, press and hold Shift, select the elements you want to save, then click **Edit > Save as new element**.


To access your saved elements, click **Add element > My elements**.


### Add panels from the Visualize Library [add-kibana-visualizations]

Add a panel that you saved in **Visualize Library** to your workpad.

1. Click **Add from library**, then select the panel you want to add.
2. To use the customization options, open the panel menu, then select one of the following options:

    * **Edit map** — Opens [Maps](maps.md) so that you can edit the panel.
    * **Edit Visualization** — Opens the visualization editor so that you can edit the panel.
    * **Panel settings** — Allows you to change the title, description, and time range for the panel.
    * **Inspect** — Allows you to drill down into the panel data.



### Add your own images [add-your-own-images]

To personalize your workpad, add your own logos and graphics.

1. Click **Add element > Manage assets**.
2. On the **Manage workpad assets** window, drag and drop your images.
3. To add the image to the workpad, click **Create image element**.


## Add pages [add-more-pages]

Organize and separate your ideas by adding more pages.

1. Click **Page 1**, then click **+**.
2. On the **Page** editor panel, select the page transition from the **Transition** dropdown.


## Share your workpad [workpad-share-options]

To share workpads with a larger audience, click {icon}`share` **Share** in the toolbar. For detailed information about the sharing options, refer to [Reporting](../report-and-share.md).


## Export workpads [export-single-workpad]

Want to export multiple workpads? Go to the **Canvas** page, select the workpads you want to export, then click **Export**.

