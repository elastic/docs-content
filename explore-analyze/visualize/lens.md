---
navigation_title: Visualizations
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/lens.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Lens visualizations [lens]

**Lens** is {{kib}}'s visualization editor for building charts, tables, maps, and metrics. It supports two modes for creating visualizations:

- **Point-and-click**: Configure your visualization interactively by selecting fields from a [data view](/explore-analyze/find-and-organize/data-views.md), choosing aggregations, and setting dimensions and display options. No query writing required. Data views are created automatically when you [upload a file](/manage-data/ingest/upload-data-files.md) or [add sample data](/manage-data/ingest/sample-data.md); otherwise, you need to create one manually.
- **Query**: Write an [{{esql}}](elasticsearch://reference/query-languages/esql.md) or [PromQL](elasticsearch://reference/query-languages/esql/commands/promql.md) query to retrieve and transform your data, then configure the visualization on top of the result. Best suited for cross-index queries, complex filtering, and custom calculations. Refer to [ES|QL visualizations](esorql.md) for details.

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-dashboards
:::

With Lens, you can create the following visualization types:

| **Chart type** | **Use when you want to...** |
| --- | --- |
| **XY charts** | **Plot data on axes to reveal trends, comparisons, and distributions.** |
| [Bar](/explore-analyze/visualize/charts/bar-charts.md) | Compare values across discrete categories or show distributions with histogram buckets. |
| [Line](/explore-analyze/visualize/charts/line-charts.md) | Show how a metric changes over time or another continuous dimension. |
| [Area](/explore-analyze/visualize/charts/area-charts.md) | Show change over time while emphasizing volume or stacked proportions. |
| **Partition charts** | **Divide a total into segments to show how parts relate to the whole.** |
| [Pie](/explore-analyze/visualize/charts/pie-charts.md) | Show how parts make up a whole with a small number of slices. |
| [Treemap](/explore-analyze/visualize/charts/treemap-charts.md) | Show hierarchical proportions across nested categories. |
| [Waffle](/explore-analyze/visualize/charts/waffle-charts.md) | Show part-to-whole as a grid of equal cells where filled cells represent proportion. |
| [Mosaic](/explore-analyze/visualize/charts/mosaic-charts.md) | Compare part-to-whole across two categorical dimensions in a tiled layout. |
| **Single value charts** | **Highlight a key number, KPI, or progress toward a goal.** |
| [Metric](/explore-analyze/visualize/charts/metric-charts.md) | Highlight a single KPI or a small set of critical numbers. |
| [Gauge](/explore-analyze/visualize/charts/gauge-charts.md) | Show progress toward a target or status against thresholds for a single metric. |
| **More charts** | **Additional visualizations for tabular data, spatial patterns, and text analysis.** |
| [Table](/explore-analyze/visualize/charts/tables.md) | Present precise values, rankings, or multi-metric details in a compact layout. |
| [Heat map](/explore-analyze/visualize/charts/heat-map-charts.md) | Reveal density or patterns across two dimensions using color intensity. |
| [Tag cloud](/explore-analyze/visualize/charts/tag-cloud-charts.md) | Highlight the most frequent or important terms in a dataset. |
| [Region map](/explore-analyze/visualize/charts/region-map-charts.md) | Show how values vary across geographic regions (choropleth). |

## Create visualizations with the API [lens-api]

```{applies_to}
stack: preview 9.4
serverless: preview
```

You can create and manage Lens visualizations programmatically using the Visualizations API ([stateful](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-visualizations), [serverless](https://www.elastic.co/docs/api/doc/serverless/group/endpoint-visualizations)). This is useful for managing visualizations as code, automating their lifecycle, or building tooling around Lens charts.

Visualizations created through this API can be added to dashboards using the Kibana UI or the Dashboards API.

:::{note}
The Visualizations API is in technical preview and may change in future releases.
:::

## Create visualizations [create-the-visualization-panel]

If you’re unsure about the visualization type you want to use, or how you want to display the data, drag the fields you want to visualize onto the workspace, then let **Lens** choose for you.

If you already know the visualization type you want to use, and how you want to display the data, use the following process.

:::::{stepper}

::::{step} Choose the visualization type

New visualizations generally default to **Bar** or **Line** charts. You can change that manually to the visualization type that you want.

As you drag fields into the workspace or to the layer pane, Lens automatically generates alternative visualizations. To view them, click **Suggestions** at the bottom of the workspace. If a suggested visualization meets your needs, click **Save and return** to add it to the dashboard.

::::

::::{step} Choose the data you want to visualize

As you drag fields to the layer pane, Lens automatically selects an aggregation function, for example **Date histogram**, **Intervals**, or **Top values**. Click a field to learn more about its data or to edit its appearance.

::::

::::{step}  Customize the appearance of your visualization

$$$configure-the-visualization-components$$$
$$$customize-visualization-appearance$$$
$$$customize-visualization-legend$$$

In the Lens editor, use the {icon}`brush` **Style** and ![Legend icon](/explore-analyze/images/kibana-legend-icon.svg "") **Legend** controls in the layer pane to customize your visualization. The available controls vary by chart type. For all settings, open the dedicated page for your chart from the [visualization type table](#lens).

::::

::::{step} (Optional) Add layers

You can add multiple layers to a visualization, such as **Visualization**, [**Annotations**](#add-annotations), or [**Reference lines**](#add-reference-lines). Click the **Add layer** icon {icon}`plus_square` , then choose the layer type and select the {{data-source}}. 
To duplicate or delete a layer, click ![Actions menu to duplicate Lens visualization layers](/explore-analyze/images/kibana-vertical-actions-menu.png "") on the layer tab.

::::

::::{step} Save and add the panel
$$$save-the-lens-panel$$$
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.

::::


:::::

Once you have created your visualization, you can edit it directly on the dashboard. Click the **Edit visualization configuration** icon ![Edit visualization icon](/explore-analyze/images/kibana-edit-visualization-icon.png "") on the panel.


### Change the fields list [change-the-fields]

When you can create a visualization, you can change the fields list to display a different {{data-source}}, a different time range, or add your own fields. To do that, open the {{data-source}} dropdown and select **Add a field to this {{data-source}}**.

![Dropdown menu located next to {{data-source}} field with items for adding and managing fields](/explore-analyze/images/kibana-lens_dataViewDropDown_8.4.0.png "")


If the fields list is empty, change the [time filter](../query-filter/filtering.md).

For more information about adding fields to {{data-sources}} and examples, refer to [Explore your data with runtime fields](../find-and-organize/data-views.md#runtime-fields).

### Assign colors to terms [assign-colors-to-terms]
```{applies_to}
stack: preview =9.0, ga 9.1+
serverless: ga
```

You can assign specific colors to terms in your visualizations. This color mapping can be useful in several situations:

* **Visual recognition and recall**: Keep colors consistent for each term regardless of filters or sorting.
* **Semantic meaning**: Use colors to convey meaning or categorization.
* **Consistency**: Align with brand colors and improve overall aesthetic consistency.

![A bar chart with terms mapped to specific colors](../images/color_mapping.png)

#### Supported visualization types

Color mapping is available for the following **Lens** visualization types:

* **Data tables**: Assign colors to terms in **Rows** or **Metrics** fields. You can apply colors to cell backgrounds or text.
* **XY charts (Area, Bar, Line)**: Assign colors to breakdown dimensions that split your data into multiple series.
* **Partition charts (Donut, Pie, Treemap, Waffle)**: Assign colors to the main slice or group-by dimension that defines the chart segments.
* **Tag clouds**: Assign colors to the tags dimension that determines the terms displayed in the cloud.

#### Configure color mapping in a chart

To assign colors to terms in your visualization:

1. Create a visualization using one of the supported types.
2. Add a categorical field that contains the terms you want to color.
3. In the field configuration, look for the **Color by value** option:
   * For data tables: Select **Cell** or **Text**
   * For other chart types: This option appears when you have a categorical breakdown
4. Click the **Edit colors** icon. In the menu that opens, keep **Use legacy palettes** turned off to be able to assign colors to specific terms
5. Select a color palette from the available options:
   * **Elastic**: The default and most recent palette. It is intentionally built from a color spectrum designed for flexibility and consistency, while being suited for future accessibility improvements.
   * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` **Elastic (line optimized)**: A variant of the Elastic palette that reorders colors for better contrast between adjacent series in line charts. Lens automatically applies this palette when you create or switch to a line chart. Switching to a different chart type reverts to the standard palette. You can override this by manually selecting a different palette.
   * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` **Severity**: A theme-aware categorical palette designed for severity-based data, with colors that adapt to both light and dark themes.
   * **{{kib}} 7.0**: A palette that matches the {{kib}} 7.0 color theme for visualizations
   * **{{kib}} 4.0**: A palette that matches the {{kib}} 4.0 color theme for visualizations
   * **Elastic classic**: A palette made of classic Elastic brand colors
6. Select the color mode you'd like to use with this palette:
   * **Categorical**: Assign a distinct color to each term
   * **Gradient**: Assign gradients of the same color to each term
7. Choose which terms to color. You can assign colors manually or select **Add all unassigned terms** for automatic assignment.
   :::{tip}
   You can assign several terms to the same color.
   :::
8. Choose how to handle unassigned terms: Use the selected color palette or assign a single color.


#### Color options and accessibility

**Discrete colors and gradients**

Choose from discrete color sets or generate sequential or divergent gradients. Gradients work well for Likert scales and other term scales.

**Theme-aware neutral colors**

Use neutral gray colors that adjust automatically between light and dark themes. These help de-emphasize less important data.

**Accessibility warnings**

The system warns you when colors don't have enough contrast for accessibility.

#### Best practices

**Maintain consistency**

Use color mapping to create consistent color schemes when the same categorical data appears across multiple visualizations in your dashboards.

**Use semantic colors**

Leverage color associations that users already understand (such as red for errors, green for success) to make your visualizations more intuitive.

**Consider performance**

Color mapping works best with fields that have a reasonable number of distinct values. Fields with hundreds or thousands of unique terms may impact visualization performance.

**Plan for themes**

When choosing colors, consider how they appear in both light and dark themes. Use theme-aware neutral colors when you want to de-emphasize data.


### Create visualizations with keyboard navigation [drag-and-drop-keyboard-navigation]

To use a keyboard instead of a mouse, use the **Lens** fully accessible and continuously improved drag system.

1. Select the field in the fields list or layer pane. Most fields have an inner and outer select state. The inner state opens a panel with detailed information or options. The outer state allows you to drag the field. Tab through the fields until you get the outer state on the field.

   :::{image} /explore-analyze/images/kibana-lens_drag_drop_2.png
   :alt: Lens drag and drop focus state
   :screenshot:
   :::

2. Complete the following actions:

    * To select a field, press Space bar.
    * To select where you want to drop the field, use the Left and Right arrows.
    * To reorder the fields on the layer pane, use the Up and Down arrows.
    * To duplicate an action, use the Left and Right arrows, then select the **Drop a field or click to add** field you want to use.

      :::{image} /explore-analyze/images/kibana-lens_drag_drop_3.gif
      :alt: Using drag and drop to reorder
      :screenshot:
      :::

3. To confirm the action, press Space bar. To cancel, press Esc.


### Use formulas to perform math [lens-formulas]

Lens formulas let you do math using a combination of {{es}} aggregations and math functions. For example, you can use formulas to divide two values and produce a percent value.

When you add a categorical field to your visualization, select the field to open its appearance settings, choose **Formula**, and set **Appearance** > **Value format** to **Percent** for a more accurate display.

For more details on how it works, click the **Formula reference** icon ![Formula reference icon](/explore-analyze/images/kibana-formula_reference.png "") on the Formula panel.

These are examples of common formulas:

**Filter ratio**
:   To filter a document set, use `kql=''`, then compare to other documents within the same grouping:

    ```
    count(kql='response.status_code > 400') / count()
     ```

**Week over week**
:   To get the value for each grouping from the previous week, use `shift='1w'`.

    ```
    percentile(system.network.in.bytes, percentile=99) /
    percentile(system.network.in.bytes, percentile=99, shift='1w')
    ```
    You are unable to combine different time shifts, such as `count(shift="1w") - count()` and `count(shift="1w") - count(shift="1m")`, with the **Top values** function.

**Percent of total**
:   To convert each grouping into a percent of the total, formulas calculate `overall_sum` for all groupings:

    ```
    sum(products.base_price) / overall_sum(sum(products.base_price))
    ```

### Compare differences over time [compare-data-with-time-offsets]

Compare your real-time data to the results that are offset by a time increment. For example, you can compare the real-time percentage of a user CPU time spent to the results offset by one hour.

1. In the layer pane, click the field you want to offset.
2. Click **Advanced**.
3. In the **Time shift** field, enter the time offset increment.

For a time shift example, refer to [Compare time ranges](../dashboards/create-dashboard-of-panels-with-ecommerce-data.md#compare-time-ranges).

### Create partition charts with multiple metrics [create-partition-charts-with-multiple-metrics]

To create partition charts, such as pie charts, configure one or more **Slice by** dimensions to define the partitions, and a **Metric** dimension to define the size. To create partition charts with multiple metrics, use the layer settings. Multiple metrics are unsupported for mosaic visualizations.

For detailed instructions on creating pie charts, including best practices and configuration options, refer to [Build pie charts with {{kib}}](/explore-analyze/visualize/charts/pie-charts.md).

1. In the layer pane, click ![Actions menu for the partition visualization layer](/explore-analyze/images/kibana-lens_layerActions_8.5.0.png ""), then select **Settings**/**Layer settings**.
2. Select **Multiple metrics**.
3. Click **X**.


### Improve visualization loading time [improve-visualization-loading-time]
```{applies_to}
stack: preview
```

Data sampling allows you to improve the visualization loading time. When you create your visualization, click the **Settings**/**Layer settings** icon {icon}`gear` and use the slider to adjust the **Sampling** percentage. For example, on large datasets, you can decrease loading time by using a lower sampling percentage. This increases performance but reduces accuracy.


### Add annotations [add-annotations]
```{applies_to}
stack: preview
```

Annotations allow you to call out specific points in your visualizations that are important, such as significant changes in the data. You can add annotations for any {{data-source}}, add text and icons, specify the line format and color, and more.
Click the **Add layer** icon {icon}`plus_square` , select **Annotations** and select the annotation method you want to use:

:::{dropdown} New annotation
1. Select the {{data-source}} for the annotation.
2. From the fields list, drag a field to the **Horizontal axis** field.

To use global filters in the annotation, click the **Settings**/**Layer settings** icon {icon}`gear` on the annotations layer, and select **Use global filters**.

From the annotation panel, you can choose the type of placement and adjust the its appearance.

**Placement**
:   
    - **Static date** — Displays annotations for specific times or time ranges. To create static annotations:
      1. Select **Static date**.
      2. In the **Annotation date** field, click ![Annodation date icon in Lens](/explore-analyze/images/kibana-lens_annotationDateIcon_8.6.0.png ""), then select the date.
      3. To display the annotation as a time range, select **Apply as range**, then specify the **From** and **To** dates.

    - **Custom query** — Displays annotations based on custom {{es}} queries. For information about queries, check [Semi-structured search](/explore-analyze/query-filter/languages/kql.md#semi-structured-search). To create custom query annotations:
      1. Select **Custom query**.
      2. Enter the **Annotation query** for the data you want to display. For detailed information about queries and examples, check [Semi-structured search](/explore-analyze/query-filter/languages/kql.md#semi-structured-search).
      3. Select the **Target date field**.

**Appearance**
:   Configure the annotation settings, including:
   - **Name**: Enter the name of the annotation.
   - **Icon decoration**: Choose from various icon styles to represent your annotations on the visualization. Options include markers like circles, triangles, squares, and other symbols.
   - **Text decoration**: Set the style for the text labels of your annotations.
   - **Line**: Control the width/thickness of annotation lines.
   - **Color**: Set a custom color for your annotation markers.
   - **Hide annotation**: Temporarily hide annotations from your visualization without deleting them.

**Tooltip**
:  Add a field to the annotation tooltip
   1. If you created a custom query annotation, click **Add field** to add a field to the annotation tooltip.

Once you are done, you can add your new annotation layer to the **Visualize Library** so that it can be reused in other visualizations. Note that any changes made to the annotation group is reflected in all visualizations to which it is added.
:::

:::{dropdown} Load from library
Add a library annotation group to a visualization.
:::


:::{image} /explore-analyze/images/kibana-lens_annotations_8.2.0.png
:alt: Lens annotations
:screenshot:
:::


### Add reference lines [add-reference-lines]

With reference lines, you can identify specific values in your visualizations with icons, colors, and other display options. You can add reference lines to any visualization type that displays axes.

For example, to track the number of bytes in the 75th percentile, add a shaded **Percentile** reference line to your time series visualization.

:::{image} /explore-analyze/images/kibana-lens_referenceLine_7.16.png
:alt: Lens drag and drop focus state
:screenshot:
:::

From your visualization, click **Add layer > Reference lines**. Click the vertical axis value, and specify the reference line you want to use by choosing one fhe following placement methods:

**Static**
:   To add a static reference line.

**Quick functions**
:   To add a dynamic reference line.

**Formula**
:   To calculate the reference line value with math.

You can also customize the display by adjusting the **Appearance** settings.


### Apply filters [filter-the-data]

You can use the query bar to create queries that filter all the data in a visualization, or use the layer pane and legend filters to apply filters based on field values.


#### Apply multiple KQL filters [filter-with-the-function]

With the **Filters** function, you can apply more than one KQL filter, and apply a KQL filter to a single layer so you can visualize filtered and unfiltered data at the same time.

1. In the layer pane, click a field.
2. Click the **Filters** function.
3. Click **Add a filter**, then enter the KQL filter you want to apply.

    To try the **Filters** function on your own, refer to [Compare a subset of documents to all documents](../dashboards/create-dashboard-of-panels-with-web-server-data.md#custom-ranges).



#### Apply a single KQL filter [filter-with-the-advanced-option]

With the **Filter by** advanced option, you can assign a color to each filter group in **Bar** and **Line and area** visualizations, and build complex tables. For example, to display failure rate and the overall data.

1. In the layer pane, click a field.
2. Click **Add advanced options**, then select **Filter by**.
3. Enter the KQL filter you want to apply.


#### Apply legend filters [filter-with-legend-filters]

Apply filters to visualizations directly from the values in the legend. **Bar**, **Line and area**, and **Proportion** visualizations support legend filters.

In the legend, click the field, then choose one of the following options:

* **Filter for value** — Applies a filter that displays only the field data in the visualization.
* **Filter out value** — Applies a filter that removes the field data from the visualization.

#### Filter pill actions

:::{include} ../_snippets/global-filters.md
:::


## Explore the data in Discover [explore-lens-data-in-discover]

When your visualization includes one data view, you can open and explore the visualization data in **Discover**.

To get started, click **Explore data in Discover** in the toolbar.

For more information about exploring your data with **Discover**, check out [Discover](../discover.md).


## View the visualization data and requests [view-data-and-requests]

To view the data included in the visualization and the requests that collected the data, use the **Inspector**.

1. In the toolbar, click **Inspect**.
2. Open the **View** dropdown, then click **Data**.

    1. From the dropdown, select the table that contains the data you want to view.
    2. To download the data, click **Download CSV**, then select the format type.

3. Open the **View** dropdown, then click **Requests**.

    1. From the dropdown, select the requests you want to view.
    2. To view the requests in **Console**, click **Request**, then click **Open in Console**.


## Frequently asked questions [lens-faq]

For answers to common **Lens** questions, review the following.

::::{dropdown} When should I normalize the data by unit or use a custom interval?
:name: when-should-i-normalize-the-data-by-unit-or-use-a-custom-interval

* **Normalize by unit** — Calculates the average for the interval. When you normalize the data by unit, the data appears less granular, but **Lens** is able to calculate the data faster.
* **Customize time interval** — Creates a bucket for each interval. When you customize the time interval, you can use a large time range, but **Lens** calculates the data slower.

To normalize the interval:

1. In the layer pane, click a field.
2. Click **Add advanced options > Normalize by unit**.
3. From the **Normalize by unit** dropdown, select an option, then click **Close**.

To create a custom interval:

1. In the layer pane, click a field.
2. Select **Customize time interval**.
3. Change the **Minimum interval**, then click **Close**.

::::


::::{dropdown} What data is categorized as Other?
:name: what-is-the-other-category

The **Other** category contains all of the documents that do not match the specified criteria or filters. Use **Other** when you want to compare a value, or multiple values, to a whole.

By default, **Group other values as "Other"** is enabled when you use the **Top values** function.

To disable **Group other values as "Other"**, click a field in the layer pane, click **Advanced**, then deselect **Group other values as "Other"**.

::::


::::{dropdown} How do I add documents without a field?
:name: how-can-i-include-documents-without-the-field-in-the-operation

By default, **Lens** retrieves only the documents from the fields. For bucket aggregations, such as **Top values**, you can add documents that do not contain the fields, which is helpful when you want to make a comparison to the whole documentation set.

1. In the layer pane, click a field.
2. Click **Advanced**, then select **Include documents without this field**.

::::


::::{dropdown} When do I use runtime fields vs. formula?
:name: when-do-i-use-runtime-fields-vs-formula

Use runtime fields to format, concatenate, and extract document-level fields. Runtime fields work across all of {{kib}} and are best used for smaller computations without compromising performance.

Use formulas to compare multiple {{es}} aggregations that can be filtered or shifted in time. Formulas apply only to **Lens** panels and are computationally intensive.

::::


::::{dropdown} Can I add more than one y-axis scale?
:name: is-it-possible-to-have-more-than-one-Y-axis-scale

For each y-axis, you can select **Left** and **Right**, and configure a different scale.

::::


::::{dropdown} Why is my value the incorrect color when I use value-based coloring?
:name: why-is-my-value-with-the-right-color-using-value-based-coloring

Here’s a short list of few different aspects to check:

* Make sure the value falls within the desired color stop value defined in the panel. Color stop values are "inclusive".
* Make sure you have the correct value precision setup. Value formatters could round the numeric values up or down.
* Make sure the correct color continuity option is selected. If the number is below the first color stop value, a continuity of type `Below` or `Above and below range` is required.
* The default values set by the Value type are based on the current data range displayed in the data table.

    * If a custom `Number` configuration is used, check that the color stop values are covering the current data range.
    * If a `Percent` configuration is used, and the data range changes, the colors displayed are affected.


::::


::::{dropdown} How do I sort by multiple columns?
:name: can-i-sort-by-multiple-columns

Multiple column sorting is unsupported, but is supported in **Discover**. For information on how to sort multiple columns in **Discover**, refer to [Explore the fields in your data](../discover/discover-get-started.md#explore-fields-in-your-data).

::::


::::{dropdown} Why is my field missing from the fields list?
:name: why-my-field-is-missing-from-the-fields-list

The following field types do not appear in the **Available fields** list:

* Full-text
* geo_point
* flattened
* object

Verify if the field appears in the **Empty fields** list. **Lens** uses heuristics to determine if the fields contain values. For sparse data sets, the heuristics are less precise.

::::


::::{dropdown} What do I do with gaps in time series visualizations?
:name: how-to-handle-gaps-in-time-series-visualizations

When you create **Area** and **Line** charts with sparse time series data, open **Visual options** in the editor toolbar, then select a **Missing values** option.

::::


::::{dropdown} Can I statically define the y-axis scale?
:name: is-it-possible-to-change-the-scale-of-Y-axis

You can set the scale, or *bounds*, for area, bar, and line charts. You can configure the bounds for all functions, except **Percentile**. Logarithmic scales are unsupported.

To configure the bounds, use the menus in the editor toolbar. Bar and area charts required 0 in the scale between **Lower bound** and **Upper bound**.

::::


::::{dropdown} Is it possible to display icons in data tables?
:name: is-it-possible-to-show-icons-in-datatable

You can display icons with [field formatters](../find-and-organize/data-views.md) in data tables.

::::


::::{dropdown} How do I inspect {{es}} queries in visualizations?
:name: is-it-possible-to-inspect-the-elasticsearch-queries-in-Lens

You can inspect the requests sent by the visualization to {{es}} using the Inspector. It can be accessed within the editor or in the dashboard.

::::


::::{dropdown} How do I isolate a single series in a chart?
:name: how-to-isolate-a-single-series-in-a-chart

For area, line, and bar charts, press Shift, then click the series in the legend. All other series are automatically deselected.

::::


::::{dropdown} How do I visualize saved Discover sessions?
:name: is-it-possible-to-use-saved-serches-in-lens

Visualizing saved Discover sessions is unsupported.

::::


::::{dropdown} How do I change the number of suggestions?
:name: is-it-possible-to-decrease-or-increase-the-number-of-suggestions

Configuring the **Suggestions** is unsupported.

::::


::::{dropdown} Is it possible to have pagination in a data table?
:name: is-it-possible-to-have-pagination-for-datatable

Pagination in a data table is unsupported. To use pagination in data tables, create an [aggregation-based data table](legacy-editors/aggregation-based.md#types-of-visualizations).

::::


::::{dropdown} How do I change the color for a single data point?
:name: is-it-possible-to-select-color-for-specific-bar-or-point

Specifying the color for a single data point, such as a single bar or line, is unsupported.

::::


::::{dropdown} How does dynamic coloring work for the metric visualization?
:name: dynamic-metric-coloring

In the color palette editor, if you select **Value type: Number** the colors are applied based on the **Primary metric** value.

The **Primary metric** refers to the large number displayed in each tile.

![Illustration of where to find the primary metric in a metric visualization.](/explore-analyze/images/kibana-lens_primaryMetric.png "")

If you select **Value type: Percent**, the primary metric values are mapped to a range between 0 and 100 percent. The bounds of the range depend on your configuration.

The logic is as follows. If there is a Breakdown dimension for multiple visualization tiles:

* When there is a **Maximum dimension**, the range is from zero to the value of your **Maximum dimension**.
* When there is no **Maximum dimension**, the range is from the smallest primary metric values to the greatest primary metric values.

If there is no Breakdown dimension for a single visualization tile:

* When there is a **Maximum dimension**, the range is from zero to the value of your **Maximum dimension**.
* When there is no **Maximum dimension**, **Value type: Percent** cannot be selected because there’s no way to determine a range.

::::
