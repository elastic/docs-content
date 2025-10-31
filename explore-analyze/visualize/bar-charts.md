---
navigation_title: Bar charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building bar charts with Kibana Lens in Elastic.
---

# Bar charts

Bar charts display data using rectangular bars with lengths proportional to the values they represent. They excel at comparing different categories or showing changes over time, helping you quickly spot trends, patterns, and outliers in your data at a glance.

The best way to create bar charts in Kibana is to use **Lens**. You can also use legacy visualization editors, but Lens provides the most current features and best performance.

## When to use bar charts

Bar charts work best for comparing discrete categories or showing data changes over time. Use them when you want to:

- Compare values across different categories (like sales by region or errors by service)
- Show data distribution and identify the highest or lowest performing items
- Track changes over time periods (daily, weekly, monthly trends)
- Display rankings or top/bottom N results
- Visualize survey responses or categorical data analysis

Consider using line charts when you need to show:
- Continuous data trends with many time points
- Multiple intersecting data series where relationships matter more than individual values

Consider using metric charts when you need to show:
- Single key performance indicators without comparison context

## Build bar charts with Kibana

### Requirements

Bar charts work with various data types, including:
- Numeric fields (integers, floats, currency values)
- Date/time fields for time-based grouping
- Categorical fields (strings, keywords) for grouping and breakdowns
- Count of documents as a basic metric
- Calculated values using formulas and aggregations

### Build a bar chart

1. Open **Lens** from the **Visualizations** menu or from a dashboard.
2. Select your data view from the dropdown to specify which data to visualize.
3. From the **Visualization type** dropdown, select **Bar vertical** or **Bar horizontal**.
4. Configure the vertical axis (Y-axis) by dragging a numeric field to the **Vertical axis** area:
   - Lens automatically selects an appropriate aggregation (Count, Sum, Average, and so on)
   - To change the aggregation, select the field and select a different **Quick function**
5. Configure the horizontal axis (X-axis) by dragging a field to the **Horizontal axis** area:
   - Use date fields for time series analysis
   - Use categorical fields to compare different groups
   - Lens automatically creates appropriate buckets and intervals
6. (Optional) Add a **Break down by** field to create multiple data series:
   - Drag a categorical field to split your data into colored segments
   - Configure the series appearance and colors in the field options
7. (Optional) Add multiple layers to compare different data sources or metrics.
8. Customize the appearance using the **Appearance**, **Legend**, and **Axis** options in the toolbar.
9. Save the chart to your dashboard or the Visualize Library.


## Bar chart settings

Customize your visualization so it looks exactly like you want it.

### Vertical axis (Y-axis)

The vertical axis represents the measured values in your bar chart.

**Field selection**
:   Select the numeric field or metric to measure. This determines the height of your bars.

**Aggregation function**
:   Define how to calculate the values. Available options include:
     - **Count** (default): Count of documents
     - **Sum**: Total of all field values
     - **Average**: Mean of all field values
     - **Median**: Middle value when sorted
     - **Min/Max**: Smallest or largest value
     - **Percentiles**: Value at specified percentile (90th, 95th, 99th)
     - **Unique count**: Count of distinct values
     - **Formula**: Custom mathematical expressions using multiple fields

**Name**
:   Customize the display name for your metric. This appears in legends and tooltips.

**Value format**
:   Control how numbers display:
     - **Number**: Standard numeric format (1,234.56)
     - **Percentage**: Show as percentage (12.34%)
     - **Bytes**: Format as data sizes (1.2 GB)
     - **Currency**: Display with currency symbols ($1,234)
     - **Duration**: Show time periods (2h 15m)
     - **Custom**: Define your own format pattern

**Advanced options**
:   Additional settings for complex scenarios:
     - **Filter by**: Apply KQL filters to this specific field
     - **Time shift**: Compare data from different time periods
     - **Reduce by**: Apply mathematical operations across multiple values

### Horizontal axis (X-axis)

The horizontal axis represents the categories or time periods for your data.

**Field selection**
:   Select the field to group your data by:
     - **Date fields**: Automatically create time-based intervals
     - **Categorical fields**: Group by unique values (up to configurable limits)
     - **Numeric fields**: Create ranges or intervals

**Interval settings** (for date/numeric fields)
:   Control how data gets grouped:
     - **Auto**: Lens selects optimal intervals based on data range
     - **Custom**: Set specific intervals (hourly, daily, weekly, and so on)
     - **Calendar intervals**: Use calendar-aligned periods (months, quarters)

**Top values settings** (for categorical fields)
:   Configure category display:
     - **Number of values**: Limit how many categories to show (default: 5)
     - **Group remaining as "Other"**: Combine less frequent values
     - **Order by**: Sort by document count, alphabetical, or metric value

**Missing values**
:   Select how to handle documents without the field:
     - **Skip**: Don't show documents without the field
     - **Show**: Include as a separate category

## Break down by

Split your data into multiple series using a categorical field.

**Field selection**
:   Select a categorical field to split each bar into segments:
     - Status fields (success, error, warning)
     - Geographic regions or locations
     - Product categories or service types
     - User roles or customer segments

**Series configuration**
:   Control how multiple series display:
     - **Number of series**: Limit how many break down values to show
     - **Group remaining as "Other"**: Combine less frequent break down values
     - **Order by**: Sort series by document count or metric value

**Color mapping**
:   Assign specific colors to series values:
     - **Use legacy palettes**: Standard color schemes
     - **Assign colors to terms**: Map specific colors to specific values
     - **Color mode**: Categorical (distinct colors) or gradient (color variations)

### Appearance options

Customize the visual presentation of your bar chart.

**Bar orientation**
:   Select the chart orientation:
     - **Vertical**: Bars extend upward (good for comparing categories)
     - **Horizontal**: Bars extend to the right (better for long category names)

**Bar styling**
:   Control bar appearance:
     - **Bar width**: Adjust spacing between bars
     - **Border width**: Add borders around bars
     - **Border color**: Set border color

**Missing values** (for time series data)
:   Handle gaps in your data:
     - **Hide**: Don't show gaps in data
     - **Zero**: Show gaps as zero values
     - **Linear**: Connect gaps with straight lines

**Grid and reference lines**
:   Add visual guides to your chart:
     - **Grid lines**: Show horizontal and vertical grid lines
     - **Reference lines**: Add static or calculated reference lines
     - **Annotations**: Mark specific events or periods

### Legend settings

Control how the legend appears and what information it shows.

**Visibility and position**
:   Configure legend display:
     - **Show legend**: Turn the legend on or off
     - **Position**: Place legend inside, outside, top, bottom, start, or end
     - **Width**: Control legend width when positioned on sides

**Legend content**
:   Select what information to display:
     - **Values**: Show current values for each series
     - **Percentages**: Display each series as percentage of total
     - **Statistics**: Add statistical information (max, min, average)

**Label formatting**
:   Customize legend text:
     - **Truncate labels**: Shorten long category names
     - **Legend values**: Show additional statistics in the legend

### Axis customization

Fine-tune how your axes appear and behave.

#### Vertical axis (Y-axis) options

**Scale settings**
:   Control value range and scaling:
     - **Bounds**: Set minimum and maximum values manually
     - **Scale type**: Linear or logarithmic scaling
     - **Zero baseline**: Force axis to start at zero

**Axis labels**
:   Customize axis text and formatting:
     - **Title**: Add descriptive axis title
     - **Label rotation**: Rotate labels to prevent overlap
     - **Label format**: Apply number formatting to axis labels

**Grid lines**
:   Configure visual grid:
     - **Show grid lines**: Display horizontal reference lines
     - **Grid line style**: Solid, dashed, or dotted lines

### Bottom axis (X-axis) options

**Label management**
:   Handle category labels:
     - **Show labels**: Turn category labels on or off
     - **Label rotation**: Rotate text to fit more labels
     - **Label truncation**: Shorten long category names

**Time axis settings** (for time-based data)
:   Configure time display:
     - **Time zone**: Select time zone for date labels
     - **Date format**: Control how dates appear on axis
     - **Interval bounds**: Align intervals to calendar periods

## Advanced features

### Layers and multiple data sources

Add multiple data layers to compare different metrics or data sources.

**Adding layers**
:   Create complex visualizations:
     - **Add layer**: Combine multiple data views in one chart
     - **Layer types**: Mix bar charts with line charts or areas
     - **Layer order**: Control which data appears on top

**Multi-axis charts**
:   Use multiple Y-axes for different value ranges:
     - **Right axis**: Add metrics with different scales
     - **Dual axis**: Compare related but differently scaled metrics

### Filtering and queries

Apply filters to focus on specific data subsets.

**Global filters**
:   Apply dashboard-wide filtering:
     - **Time filter**: Select date ranges using the time picker
     - **Query bar**: Enter KQL (Kibana Query Language) queries
     - **Filter pills**: Add specific field value filters

**Chart-specific filters**
:   Filter individual chart elements:
     - **Legend filters**: Select specific series to show/hide
     - **Brush selection**: Select time ranges directly on the chart
     - **Drill-down filters**: Filter to specific categories by selecting bars

### Formulas and calculations

Create advanced metrics using mathematical expressions.

**Formula syntax**
:   Build complex calculations:
     - **Basic math**: Add, subtract, multiply, divide aggregations
     - **Functions**: Use count(), sum(), average(), percentile(), and more
     - **Filters**: Apply KQL filters within formulas: `count(kql='status:error')`
     - **Time shifts**: Compare periods: `sum(sales) / sum(sales, shift='1w')`

**Common formula patterns**
:   Useful calculation examples:
     - **Conversion rate**: `count(kql='action:purchase') / count() * 100`
     - **Error rate**: `count(kql='level:ERROR') / count() * 100`
     - **Growth rate**: `(sum(revenue) - sum(revenue, shift='1M')) / sum(revenue, shift='1M') * 100`

<!-- VISUAL 3: A dashboard showing multiple bar chart variations: a simple vertical bar chart comparing categories, a horizontal bar chart with multiple series (break down by), and a time-series bar chart showing trends over time. Each should demonstrate different styling options like colors, legends, and axis configurations. Include callouts showing the different use cases and configuration highlights. -->

## Examples of bar charts

### Sales by region comparison
Compare performance across different geographic areas:
- **Vertical axis**: Sum of `sales_amount` field
- **Horizontal axis**: `region` field (top 10 values)
- **Break down by**: `product_category` field
- **Format**: Currency ($)
- **Time range**: Last quarter

### Website traffic trends
Monitor daily website visits over time:
- **Vertical axis**: Count of documents
- **Horizontal axis**: `@timestamp` field with daily intervals
- **Break down by**: `traffic_source` field
- **Missing values**: Show as zero
- **Time range**: Last 30 days

### Error rate monitoring
Track application error rates by service:
- **Vertical axis**: Formula `count(kql='log.level:ERROR') / count() * 100`
- **Horizontal axis**: `service.name` field
- **Format**: Percentage (%)
- **Reference line**: Static line at 5% error threshold
- **Color**: Red bars above threshold, green below

### Performance comparison with targets
Show actual versus target performance metrics:
- **Vertical axis**: Average of `response_time_ms`
- **Horizontal axis**: `service_name` field
- **Layers**: Add reference line layer showing target response time
- **Format**: Duration (milliseconds)
- **Colors**: Value-based coloring (green < 100ms, yellow < 500ms, red >= 500ms)

### Hourly order distribution
Analyze business patterns throughout the day:
- **Vertical axis**: Count of `order_id` field
- **Horizontal axis**: `order_time` field with hourly intervals
- **Break down by**: `order_type` field (online, in-store, mobile)
- **Time range**: Last 7 days
- **Bar orientation**: Vertical with stacked series