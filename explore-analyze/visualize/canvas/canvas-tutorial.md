---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/canvas-tutorial.html
description: Step-by-step tutorial for creating Canvas workpads with ecommerce data. Learn to build sales monitoring dashboards with custom elements and data visualizations.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Tutorial: Create a workpad for monitoring sales [canvas-tutorial]

In this tutorial, you'll learn the fundamentals of building Canvas workpads by creating a sales monitoring dashboard. You'll explore how to add images, create metric displays, build data tables, and apply time range controls. By the end, you'll understand the core workflows for creating custom presentations with live data.

The tutorial uses eCommerce sample data to demonstrate these techniques, but you can apply the same approaches to any data set.

**Prerequisites:**

- Access to {{kib}} (version 8.0 or later)
- eCommerce sample data installed (instructions below)


## Open and set up Canvas [_open_and_set_up_canvas]

To create a workpad of the eCommerce store data, add the data set, then create the workpad.

1. [Install the eCommerce sample data](../../index.md#gs-get-data-into-kibana).
2. Go to **Canvas** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Select **Create workpad**.


## Customize your workpad with images [_customize_your_workpad_with_images]

To customize your workpad to look the way you want, add your own images.

1. Click **Add element > Image > Image**.

    The default Elastic logo image appears on the page.

2. Add your own image.

    1. Click the Elastic logo.
    2. Drag the image file to the **Select or drag and drop an image** field.

       :::{image} /explore-analyze/images/kibana-canvas_tutorialCustomImage_7.17.0.png
       :alt: The Analytics logo added to the workpad
       :screenshot:
       :::



## Customize your data with metrics [_customize_your_data_with_metrics]

Customize your data by connecting it to the Sample eCommerce orders data.

1. Click **Add element > Chart > Metric**.

    By default, the element is connected to the demo data, which enables you to experiment with the element before you connect it to your own.

2. To connect the element to your own data, make sure the element is selected, then click **Data > Demo data > Elasticsearch SQL**.

    1. To select the total price field and set it to the sum_total_price field, enter the following in the **Query** field:

        ```text
        SELECT sum(taxless_total_price) AS sum_total_price FROM "kibana_sample_data_ecommerce"
        ```

    2. Click **Save**.

        All fields are pulled from the sample eCommerce orders {{data-source}}.

3. At this point, the element appears as an error, so you need to change the element display options.

    1. Click **Display**
    2. From the **Value** dropdowns, make sure **Unique** and **sum_total_price** are selected.
    3. Change the **Label** to `Total sales`.

4. The error is gone, but the element could use some formatting. To format the number, use the **Canvas** expression language.

    1. Click **Expression editor**.

        You’re now looking at the raw data syntax that Canvas uses to display the element.

    2. Change `metricFormat="0,0.[000]"` to `metricFormat="$0a"`.
    3. Click **Run**.


:::{image} /explore-analyze/images/kibana-canvas_tutorialCustomMetric_7.17.0.png
:alt: The total sales metric added to the workpad using Elasticsearch SQL
:screenshot:
:::


## Show off your data with charts [_show_off_your_data_with_charts]

To show what your data can do, add charts, graphs, progress monitors, and more to your workpad.

1. Click **Add element > Chart > Area**.
2. Make sure that the element is selected, then click **Data > Demo data > Elasticsearch SQL**.

    1. To obtain the taxless total price by date, enter the following in the **Query** field:

        ```text
        SELECT order_date, taxless_total_price FROM "kibana_sample_data_ecommerce" ORDER BY order_date
        ```

    2. Click **Save**.

3. Change the display options.

    1. Click **Display**
    2. From the **X-axis** dropdown, make sure **Value** and **order_date** are selected.
    3. From the **Y-axis** dropdown, select **Value**, then select **taxless_total_price**.


:::{image} /explore-analyze/images/kibana-canvas_tutorialCustomChart_7.17.0.png
:alt: Custom line chart added to the workpad using Elasticsearch SQL
:screenshot:
:::


## Show how your data changes over time [_show_how_your_data_changes_over_time]

To focus your data on a specific time range, add the time filter.

1. Click **Add element > Filter > Time filter**.
2. Click **Display**
3. To use the date time field from the sample data, enter `order_date` in the **Column** field, then click **Set**.

% image doesn't exist (also broken in asciidoc /explore-analyze/visualize/canvas/canvas-tutorial.md#_show_how_your_data_changes_over_time)

% :::{image} /explore-analyze/images/kibana-canvas_tutorialCustomTimeFilter_7.17.0.png
% :alt: Custom time filter added to the workpad
% :screenshot:
% :::

To see how the data changes, set the time filter to **Last 7 days**. As you change the time filter options, the elements automatically update.

Your workpad is complete!


## What’s next? [_whats_next_5]

Now that you know the basics, you’re ready to explore on your own.

Here are some things to try:

* Play with the [sample Canvas workpads](/explore-analyze/index.md).
* Build presentations of your own data with [workpads](../canvas.md#create-workpads).
* Deep dive into the [expression language and functions](canvas-function-reference.md) that drive **Canvas**.
