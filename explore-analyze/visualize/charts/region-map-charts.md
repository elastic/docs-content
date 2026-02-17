---
navigation_title: Region map charts
applies_to:
  stack: ga
  serverless: ga
description: Instructions and best practices for building region map charts with Kibana Lens in Elastic.
---

# Build region map charts with {{kib}}

Region map charts display data on a geographic map, using colors to represent values for different regions such as countries, states, or provinces. They are ideal for showing geographic distributions, comparing metrics across locations, and identifying regional patterns in your data.

You can create region map charts in {{kib}} using [**Lens**](../lens.md).

![Example Lens region map chart](/explore-analyze/images/region-map-chart-example.png)

## Build a region map chart

:::{include} ../../_snippets/lens-prerequisites.md
:::

To build a region map chart:

::::::{stepper}

:::::{step} Access Lens
**Lens** is {{kib}}'s main visualization editor. You can access it:
- From a dashboard: On the **Dashboards** page, open or create the dashboard where you want to add a region map chart, then add a new visualization.
- From the **Visualize library** page by creating a new visualization.
:::::

:::::{step} Set the visualization to Region map
New visualizations often start as **Bar** charts.

Using the **Visualization type** dropdown, select **Region map**.
:::::

:::::{step} Define the data to show
1. Select the {{data-source}} that contains your data.
2. Configure the [**Region key**](#region-key-settings) dimension to define which geographic field to use. This field should contain region codes (ISO country codes, state abbreviations, and more) that can be matched to map boundaries.
3. Configure the [**Metric**](#metric-settings) dimension to define the value displayed for each region. This determines the color intensity.

The chart preview updates to show a map with regions colored by metric value. If regions appear gray, verify that your field values match the expected geographic codes (such as ISO country codes). Also check that the correct EMS boundaries and join field are selected in the Region key dimension settings.
:::::

:::::{step} Customize the chart to follow best practices
Tweak the appearance of the chart to your needs. Consider the following best practices:

**Use appropriate region granularity**
:   Match the EMS boundaries to your data. For example, use the World Countries boundaries for global data, or a country-specific boundary set for more granular regional analysis.

**Select the correct join field**
:   Ensure your data values match the selected [join field](#region-key-settings). For example, if your data contains two-letter country codes, select the `iso2` join field.

**Handle missing regions**
:   Regions with no matching data appear gray. If too many regions are gray, verify that your field values match the selected join field format.

**Consider choropleth best practices**
:   Region maps are choropleth maps, where color represents data values. Be aware that larger regions can visually dominate, even if their values are smaller.

Refer to [Region map chart settings](#region-map-chart-settings) to find all configuration options for your region map chart.
:::::

:::::{step} Save the chart
- If you accessed Lens from a dashboard, select **Save and return** to save the visualization and add it to that dashboard, or select **Save to library** to add the visualization to the Visualize library and reuse it later.
- If you accessed Lens from the Visualize library, select **Save**. A menu opens and lets you add the visualization to a dashboard and to the Visualize library.
:::::

::::::

## Region map chart settings [region-map-chart-settings]

Customize your region map chart to display exactly the information you need, formatted the way you want.

### Region key settings [region-key-settings]

The **Region key** dimension defines which geographic areas to display on the map.

**Data**
:   The **Region key** dimension supports the following functions:

    - **Top values**: Display the regions with the highest metric values.
      - **Field**: Select the field containing geographic identifiers to group by.
      - **Number of values**: How many regions to display.
      :::{include} ../../_snippets/lens-rank-by-options.md
      :::
      :::{include} ../../_snippets/lens-breakdown-advanced-settings.md
      :::
    - **Filters**: Define custom KQL filters to create specific regions.

**EMS boundaries**
:   Select the geographic boundary shapes to use for the map. The Elastic Maps Service (EMS) provides boundary data that defines region outlines. For example, **World Countries** provides country polygons, while **US States** provides state polygons. Other boundary sets may be available based on your EMS configuration.

**Join field**
:   Select which property of the boundary shapes to use for matching your data. Each boundary set exposes one or more properties that can be used to link your region key values to the correct shape on the map. For example, the World Countries boundaries can be matched by two-letter ISO country code (`iso2`), three-letter code (`iso3`), or country name. Select the property that matches the format of your data.

    For instance, if your data contains values like `US`, `GB`, `DE`, select the `iso2` join field. If it contains values like `United States`, `United Kingdom`, select the country name join field instead.

**Appearance**
:   - **Name**: Customize the region label displayed in tooltips.

### Metric settings [metric-settings]

The **Metric** dimension defines the value that determines each region's color.

**Data**
:   The value that determines region color intensity. When you drag a field onto the chart, {{kib}} suggests a function based on the field type. You can use aggregation functions like `Sum`, `Average`, `Count`, `Median`, and more, or create custom calculations with [formulas](/explore-analyze/visualize/lens.md#lens-formulas).

    :::{include} ../../_snippets/lens-value-advanced-settings.md
    :::

**Appearance**
:   - **Name**: Customize the metric label displayed in tooltips.
    - **Value format**: Control how numeric values are displayed (number, percent, bytes, and more).

## Region map chart examples

The following examples show various configuration options for building impactful region map charts.

**Website traffic by destination country**
:   Visualize which countries receive the most web traffic:

    * Example based on: {{kib}} Sample Data Logs
    * **Region key**: `geo.dest` (Top values)
    * **EMS boundaries**: World Countries
    * **Metric**: Count

![Region map showing website traffic by destination country](/explore-analyze/images/region-map-example-traffic.png "=70%")

**Customer distribution by country**
:   Show where your customers are located around the world:

    * Example based on: {{kib}} Sample Data eCommerce
    * **Region key**: `geoip.country_iso_code` (Top 50 values)
    * **EMS boundaries**: World Countries
    * **Metric**: Unique count of `customer_id`

![Region map showing customer distribution by country](/explore-analyze/images/region-map-example-customers.png "=70%")

**Average ticket price by destination country**
:   Compare average flight ticket prices across destination countries:

    * Example based on: {{kib}} Sample Data Flights
    * **Region key**: `DestCountry` (Top 50 values)
    * **EMS boundaries**: World Countries
    * **Metric**: Average of `AvgTicketPrice`

![Region map showing average ticket price by destination country](/explore-analyze/images/region-map-example-ticket-price.png "=70%")
