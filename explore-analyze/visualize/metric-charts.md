---
navigation_title: Metric charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building metric charts with Kibana Lens in Elastic.
---

# Build metric charts with {{kib}}

Metric charts display key performance indicators (KPIs) as large, prominent numbers that are easy to read at a glance. They excel at highlighting the most important values on your dashboards—whether that's total sales, active users, system uptime, or error rates. Use metric charts when you need to communicate status quickly, show progress toward goals, or compare current performance against historical trends.

% <!-- IMAGE: Screenshot showing a dashboard with multiple metric charts displaying different KPIs like total sales ($1.2M with a +15% trend), active users (45,234 with a down arrow), and system uptime (99.8% with a green up arrow). The metrics should show different formatting options and trend indicators to demonstrate the variety of styles available. -->

The best way to create metric charts in {{kib}} is to use **Lens**.

## Requirements

Metric charts work with any data that can be aggregated into numeric values. You can use:

* Numeric fields (integers, floats, longs, doubles)
* Count aggregations on any document set
* Percentiles and other statistical aggregations
* Calculated values using formulas
* Time-shifted values for trend comparisons

If you want to show trends, you also need a date field so you can compare values across different time periods.

## Build a metric chart

Create a basic metric chart in a few steps.

1. Open **Lens** from the navigation menu or from a dashboard.
2. Select the {{data-source}} that contains your data.
3. From the **Visualization type** dropdown, select **Metric**.
4. Drag a numeric field from the fields list to the **Metric** dimension in the layer pane.

    {{kib}} automatically selects an appropriate aggregation function like Sum, Average, or Count based on your field type.

5. Configure the metric display options using the appearance settings in the editor toolbar.
6. Save your visualization by selecting **Save and return** to add it to a dashboard, or **Save to library** to reuse it across multiple dashboards.

For a more advanced metric chart, you can add secondary metrics for comparisons, break down metrics by categories, or configure trend indicators to show whether your metrics are improving or declining.

## Metric chart settings

Customize your metric chart to display exactly the information you need, formatted the way you want.

### Data configuration

Define what data to display in your metric visualization.

**Primary metric**
:   The main numeric value that appears prominently in your chart. This is required. You can use aggregation functions like Sum, Average, Count, Median, or create custom calculations with formulas. Select the metric dimension in the layer pane to configure the aggregation function, add filters, or adjust the display name.

**Secondary metric**
:   An optional additional value that provides context or enables comparisons. Common uses include:
    * Time-shifted values to show trends (for example, last week's sales compared to this week)
    * Different aggregations on the same data (for example, showing both average and median response times)
    * Related metrics for context (for example, showing total count alongside an average)
    
    When you add a secondary metric, you can configure it to display as a [trend indicator](#trend-indicators) with colors and directional arrows.

**Maximum**
:   An optional reference value that defines the upper bound for your metric. When you specify a maximum, you can use percent-based color coding to show how close your metric is to this target. This is useful for showing progress toward goals or capacity limits.

**Break down by**
:   Split your metric into multiple tiles based on a categorical field. Each unique value creates its own tile, making it easy to compare metrics across regions, products, time periods, or any other dimension. You can assign [consistent colors](lens.md#assign-colors-to-terms) to each breakdown value for better recognition across your dashboards.

### Trend indicators
```{applies_to}
stack: ga 9.1
serverless: ga
```

When you have both primary and secondary metrics, you can add trend indicators that compare them visually. This feature helps you spot improvements or declines at a glance.

% <!-- IMAGE: Side-by-side comparison showing the same metric chart. Left side shows a basic metric with just numbers. Right side shows the same metric with trend indicators enabled—displaying a green up arrow with +12% in a colored badge next to the secondary metric. The comparison should clearly show how trend indicators enhance the visualization. -->

To configure trend indicators:

1. Add a secondary metric to your chart.
2. Select the secondary metric dimension in the layer pane.
3. Look for the **Color by value** option and configure the following settings:

**Color by value**
:   Controls whether and how your secondary metric displays trend indicators:
    * **None**: No special formatting (default)
    * **Static**: Displays the secondary metric in a colored badge with a single color you choose
    * **Dynamic**: Enables trend indicators with colors and directional icons that change based on the comparison

**Color palette** (when Dynamic is selected)
:   Choose a palette that matches how you interpret changes:
    * Green-to-red palettes work well when increases are positive
    * Red-to-green palettes work well when decreases are positive
    * Consider your users' expectations—green typically signals improvement while red signals issues

**Display** (when Dynamic is selected)
:   Choose what to show in the trend indicator:
    * **Icon**: Shows only directional arrows: ↑ for increases, ↓ for decreases, = for no change
    * **Value**: Shows only the numeric value of the secondary metric
    * **Both**: Shows both the icon and value (default and most informative)

**Compare to** (when Dynamic is selected)
:   Define the baseline for your comparison:
    * **Static value**: Compare against a fixed number you specify. Use this when you have a specific target or threshold.
    * **Primary metric**: Compare the secondary metric directly against the primary metric. When you select this option, {{kib}} automatically updates the secondary metric to show the difference, and changes its label to "Difference." You can customize this label using the **Prefix** field in the metric configuration.

::::{tip}
Use the `shift` parameter in formulas to create time-based comparisons. For example, if your primary metric uses `count()` to show this week's orders, use `count(shift='1w')` as your secondary metric to compare against last week.
::::

### Appearance options
```{applies_to}
stack: ga 9.2
```

Control how your metric chart looks by selecting the {icon}`brush` **Appearance** button in the editor toolbar.

**Primary metric**
:   Customize how the main number appears:
    * **Position**: Where to place the metric within its tile
    * **Alignment**: Left, center, or right alignment
    * **Font size**: Make the number larger for emphasis or smaller to fit more content

**Title and subtitle**
:   Add descriptive text above your metrics:
    * Enter a title and optional subtitle
    * Choose the **Alignment** (left, center, or right)
    * Adjust the **Font weight** to make titles more or less prominent

**Secondary metric**
:   Control how the secondary value displays:
    * **Alignment**: Position relative to the primary metric

**Icon position**
:   When using trend indicators with icons, choose where the icon appears relative to the metric values.

### Value formatting

Format your metric values so they're easy to understand at a glance. Select a metric dimension in the layer pane to access these options:

**Value format**
:   Choose how numbers display:
    * **Number**: Standard numeric formatting with customizable decimal places
    * **Percent**: Display as a percentage (multiply by 100 and add %)
    * **Bytes**: Format as file sizes (B, KB, MB, GB, TB)
    * **Currency**: Display with currency symbols
    * **Duration**: Show as time periods (seconds, minutes, hours)
    * **Custom**: Define your own number format pattern

**Decimals**
:   Specify how many decimal places to show. Use 0 for whole numbers, or increase for more precision.

**Compact values**
:   Turn this on to abbreviate large numbers. For example, 1,500,000 becomes 1.5M.

**Prefix and Suffix**
:   Add text before or after the metric value for additional context. For example, add "$" as a prefix for currency, or "ms" as a suffix for milliseconds.

### Color customization

Control the colors of your metrics to create visually meaningful dashboards.

**Color by value** (for primary metric)
:   Apply colors based on the metric's value using thresholds:
    * Set threshold values that trigger color changes
    * Choose colors for each threshold range
    * Use this to highlight when metrics enter warning or critical ranges

**Color mapping** (for breakdown metrics)
:   When you break down metrics by a categorical field, you can assign specific colors to each category. This maintains color consistency when the same categories appear across multiple visualizations. For detailed information, refer to [Assign colors to terms](lens.md#assign-colors-to-terms).

## Best practices

Follow these guidelines to create effective metric charts:

**Keep it focused**
:   Show only the most important numbers. If a value doesn't drive decisions, leave it off the dashboard.

**Choose the right aggregation**
:   Think about what the number represents. Use Sum for totals, Average for typical values, Median when outliers skew averages, and Percentiles for understanding distribution.

**Make trends meaningful**
:   When showing trends, compare similar time periods. Compare week-over-week, month-over-month, or year-over-year. Avoid comparing a Monday to a Saturday if they have different patterns.

**Use color wisely**
:   Assign colors that match your users' expectations. Red typically means problems, yellow means caution, and green means good. But consider your specific context—for costs, lower might be better (green), while for revenue, higher is better (green).

**Format for readability**
:   Round to appropriate precision. Showing 1.2M is clearer than 1,234,567.89 for high-level metrics. But show more precision when small changes matter.

**Provide context**
:   Use titles and subtitles to explain what the metric means. "45,234" is a number, but "Active Users" gives it meaning, and adding "Last 24 Hours" as a subtitle makes it actionable.

**Limit breakdowns**
:   When breaking down metrics, show 5-10 categories at most. More than that becomes hard to scan. Consider filtering to top values or creating a different visualization type.

## Examples

Here are common patterns you can adapt for your own data.

### Executive dashboard KPI

Display total revenue as a prominent number on an executive dashboard:

* **Primary metric**: `sum(sales.revenue)`
* **Value format**: Currency with 1 decimal place
* **Title**: "Total Revenue"
* **Subtitle**: "Current Quarter"
* **Color by value**: Green when above target, red when below

### Website traffic with trend

Monitor current traffic and show whether it's increasing or decreasing compared to the previous period:

* **Primary metric**: `count()` (current week's page views)
* **Secondary metric**: `count(shift='1w')` (previous week's page views)
* **Trend indicator**: Dynamic coloring enabled
* **Compare to**: Primary metric
* **Display**: Both icon and value
* **Color palette**: Green for increases (more traffic is positive)
* **Title**: "Weekly Page Views"

### System performance by service

Compare response times across multiple services using breakdown:

* **Primary metric**: `average(response_time_ms)`
* **Break down by**: `service.name`
* **Value format**: Number with suffix "ms"
* **Title**: "Average Response Time"
* **Color mapping**: Assign consistent colors to each service name
* **Color by value**: Red above 500ms, yellow between 200-500ms, green below 200ms

### Error rate with formula

Calculate and display error percentage using a formula:

* **Primary metric formula**: `count(kql='status_code >= 400') / count() * 100`
* **Value format**: Percent with 2 decimals
* **Title**: "Error Rate"
* **Color by value**: Green below 1%, yellow between 1-5%, red above 5%

### Capacity utilization

Show current usage against maximum capacity:

* **Primary metric**: `average(system.memory.used.bytes)`
* **Maximum**: `average(system.memory.total.bytes)`
* **Value format**: Bytes
* **Title**: "Memory Usage"
* **Color by value** (Percent mode): Green 0-70%, yellow 70-90%, red above 90%

### Multi-service comparison

Create a comprehensive view with multiple services side-by-side:

* **Primary metric**: `count()`
* **Break down by**: `service.name`
* **Value format**: Number, compact values enabled
* **Title**: "Request Volume by Service"
* **Subtitle**: "Last Hour"
* **Color mapping**: Assign brand colors to each service for consistency

% <!-- IMAGE: A complete dashboard showing 3-4 of the examples above in action. Should include: a revenue metric with currency formatting, a traffic metric with a trend indicator showing an up arrow, and a breakdown showing multiple services with different colors. This demonstrates how different metric chart patterns work together on a real dashboard. -->

