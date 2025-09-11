---
navigation_title: Analyze monitor data
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-analyze.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-analyze.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Analyze data from synthetic monitors

The Synthetics UI gives you a high-level overview of your service’s availability and allows you to dig into details to diagnose what caused downtime.

## Overview [synthetics-analyze-overview]

The Synthetics **Overview** tab provides you with a high-level view of all the services you are monitoring to help you quickly diagnose outages and other connectivity issues within your network.

To access this page, find `Synthetics` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and make sure you’re on the **Overview** tab.

This overview includes a snapshot of the current status of all monitors, the number of errors that occurred over the last 6 hours, and the number of alerts over the last 12 hours. All monitors created using projects or using the UI will be listed below with information about the location, current status, and duration average.

::::{note}
When you use a single monitor configuration to create monitors in multiple locations, each location is listed as a separate monitor as they run as individual monitors and the status and duration average can vary by location.

::::

:::{image} /solutions/images/observability-synthetics-monitor-page.png
:alt: Synthetics UI
:screenshot:
:::

To get started with your analysis in the Overview tab, you can search for monitors or use the filter options including current status (up, down, or disabled), monitor type (for example, journey or HTTP), location, and more.

Then click an individual monitor to see some details in a flyout. From there, you can click **Go to monitor** to go to an individual monitor’s page to see more details (as described below).

## All monitor types [synthetics-analyze-individual-monitors]

When you go to an individual monitor’s page, you’ll see much more detail about the monitor’s performance over time. The details vary by monitor type, but for every monitor at the top of the page you’ll see:

* The monitor’s **name** with a down arrow icon that you can use to quickly move between monitors.
* The **location** of the monitor. If the same monitor configuration was used to create monitors in multiple locations, you’ll also see a down arrow icon that you can use to quickly move between locations that use the same configuration.
* The latest **status** and when the monitor was **last run**.
* The **![Beaker icon](/solutions/images/observability-beaker.svg "") Run test manually** button that allows you to run the test on demand before the next scheduled run.

    ::::{note}
    This is only available for monitors running on Elastic’s global managed testing infrastructure. It is not available for monitors running on {{private-location}}s.

    ::::

* The **![Pencil icon](/solutions/images/observability-pencil.svg "") Edit monitor** button that allows you to edit the monitor’s configuration.

:::{image} /solutions/images/observability-synthetics-analyze-individual-monitor-header.png
:alt: Header at the top of the individual monitor page for all monitor types in the {{synthetics-app}}
:screenshot:
:::

Each individual monitor’s page has three tabs: Overview, History, and Errors.

### Overview [synthetics-analyze-individual-monitors-overview]

The **Overview** tab has information about the monitor availability, duration, and any errors that have occurred since the monitor was created. The *Duration trends* chart displays the timing for each check that was performed in the last 30 days. This visualization helps you to gain insights into how quickly requests resolve by the targeted endpoint and gives you a sense of how frequently a host or endpoint was down.

:::{image} /solutions/images/observability-synthetics-analyze-individual-monitor-details.png
:alt: Details in the Overview tab on the individual monitor page for all monitor types in the {{synthetics-app}}
:screenshot:
:::

### History [synthetics-analyze-individual-monitors-history]

The **History** tab has information on every time the monitor has run. It includes some high-level stats and a complete list of all test runs. Use the calendar icon (![Calendar icon](/solutions/images/observability-calendar.svg "")) and search bar to filter for runs that occurred in a specific time period.

For browser monitors, you can click on any run in the **Test runs** list to see the details for that run. Read more about what information is included the in [Details for one run](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-run) section below.

:::{image} /solutions/images/observability-synthetics-analyze-individual-monitor-history.png
:alt: The History tab on the individual monitor page for all monitor types in the {{synthetics-app}}
:screenshot:
:::

If the monitor is configured to [retest on failure](/solutions/observability/synthetics/configure-projects.md#synthetics-configuration-monitor), you’ll see retests listed in the **Test runs** table. Runs that are retests include a rerun icon (![Refresh icon](/solutions/images/observability-refresh.svg "")) next to the result badge.

:::{image} /solutions/images/observability-synthetics-retest.png
:alt: A failed run and a retest in the table of test runs in the {{synthetics-app}}
:screenshot:
:::

### Errors [synthetics-analyze-individual-monitors-errors]

The **Errors** tab has information on failed runs. If the monitor is configured to [retest on failure](/solutions/observability/synthetics/configure-projects.md#synthetics-configuration-monitor), failed runs will only result in an error if both the initial run and the rerun fail. This can reduce noise related to transient problems.

The Errors tab includes a high-level overview of all alerts and a complete list of all failures. Use the calendar icon (![Calendar icon](/solutions/images/observability-calendar.svg "")) and search bar to filter for runs that occurred in a specific time period.

For browser monitors, you can click on any run in the **Error** list to open an **Error details** page that includes most of the same information that is included the in [Details for one run](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-run) section below.

:::{image} /solutions/images/observability-synthetics-analyze-individual-monitor-errors.png
:alt: The Errors tab on the individual monitor page for all monitor types in the {{synthetics-app}}
:screenshot:
:::

## Browser monitors [synthetics-analyze-journeys]

For browser monitors, you can look at results at various levels of granularity:

* See an overview of journey runs over time.
* Drill down into the details of a single run.
* Drill down further into the details of a single *step* within a journey.

### Journey runs over time [journey_runs_over_time]

The journey page on the Overview tab includes:

* An overview of the **last test run** including high-level information for each step.
* **Alerts** to date including both active and recovered alerts.
* **Duration by step** over the last 24 hours.
* A list of the **last 10 test runs** that link to the [details for each run](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-run).

:::{image} /solutions/images/observability-synthetics-analyze-journeys-over-time.png
:alt: Individual journey page for browser monitors in the {{synthetics-app}}
:screenshot:
:::

From here, you can either drill down into:

* The latest run of the full journey by clicking **![Inspect icon](/solutions/images/observability-inspect.svg "") View test run** or a past run in the list of **Last 10 test runs**. This will take you to the view described below in [Details for one run](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-run).
* An individual step in this run by clicking the performance breakdown icon (![Performance breakdown icon](/solutions/images/observability-apmTrace.svg "")) next to one of the steps. This will take you to the view described below in [Details for one step](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step).

### Details for one run [synthetics-analyze-one-run]

The page detailing one run for a journey includes more information on each step in the current run and opportunities to compare each step to the same step in previous runs.

At the top of the page, see the *Code executed* and any *Console* output for each step. If the step failed, this will also include a *Stacktrace* tab that you can use to diagnose the cause of errors.

Navigate through each step using **![Previous icon](/solutions/images/observability-arrowLeft.svg "") Previous** and **Next ![Next icon](/solutions/images/observability-arrowRight.svg "")**.

:::{image} /solutions/images/observability-synthetics-analyze-one-run-code-executed.png
:alt: Step carousel on a page detailing one run of a browser monitor in the {{synthetics-app}}
:screenshot:
:::

Scroll down to dig into the steps in this journey run. Click the ![Arrow right icon](/solutions/images/observability-arrowRight.svg "") icon next to the step number to show details. The details include metrics for the step in the current run and the step in the last successful run. Read more about step-level metrics below in [Timing](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step-timing) and [Metrics](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step-metrics).

This is particularly useful to compare the metrics for a failed step to the last time it completed successfully when trying to diagnose the reason it failed.

![Step list on a page detailing one run of a browser monitor in the Synthetics UI](/solutions/images/observability-synthetics-analyze-one-run-compare-steps.png "")

Drill down to see even more details for an individual step by clicking the performance breakdown icon (![Performance breakdown icon](/solutions/images/observability-apmTrace.svg "")) next to one of the steps. This will take you to the view described below in [Details for one step](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step).

### Details for one step [synthetics-analyze-one-step]

After clicking the performance breakdown icon (![Performance breakdown icon](/solutions/images/observability-apmTrace.svg "")) you’ll see more detail for an individual step.

#### Screenshot [synthetics-analyze-one-step-screenshot]

By default the synthetics library will capture a screenshot for each step regardless of whether the step completed or failed.

::::{note}
Customize screenshot behavior for all monitors in the [configuration file](/solutions/observability/synthetics/configure-projects.md), for one monitor using [`monitor.use`](/solutions/observability/synthetics/configure-individual-browser-monitors.md), or for a run using the [CLI](/solutions/observability/synthetics/cli.md#elastic-synthetics-command).

::::

Screenshots can be particularly helpful to identify what went wrong when a step fails because of a change to the UI. You can compare the failed step to the last time the step successfully completed.

:::{image} /solutions/images/observability-synthetics-analyze-one-step-screenshot.png
:alt: Screenshot for one step in a browser monitor in the {{synthetics-app}}
:screenshot:
:::

#### Timing [synthetics-analyze-one-step-timing]

The **Timing** visualization shows a breakdown of the time spent in each part of the resource loading process for the step including:

* **Blocked**: The request was initiated but is blocked or queued.
* **DNS**: The DNS lookup to convert the hostname to an IP Address.
* **Connect**: The time it took the request to connect to the server. Lengthy connections could indicate network issues, connection errors, or an overloaded server.
* **TLS**: If your page is loading resources securely over TLS, this is the time it took to set up that connection.
* **Wait**: The time it took for the response generated by the server to be received by the browser. A lengthy Waiting (TTFB) time could indicate server-side issues.
* **Receive**: The time it took to receive the response from the server, which can be impacted by the size of the response.
* **Send**: The time spent sending the request data to the server.

Next to each network timing metric, there’s an icon that indicates whether the value is higher (![Value is higher icon](/solutions/images/observability-sortUp.svg "")), lower (![Value is lower icon](/solutions/images/observability-sortDown.svg "")), or the same (![Value is the same](/solutions/images/observability-minus.svg "")) compared to the median of all runs in the last 24 hours. Hover over the icon to see more details in a tooltip.

This gives you an overview of how much time is spent (and how that time is spent) loading resources. This high-level information may not help you diagnose a problem on its own, but it could act as a signal to look at more granular information in the [Network requests](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step-network) section.

:::{image} /solutions/images/observability-synthetics-analyze-one-step-timing.png
:alt: Network timing visualization for one step in a browser monitor in the {{synthetics-app}}
:screenshot:
:::

#### Metrics [synthetics-analyze-one-step-metrics]

The **Metrics** visualization gives you insight into the performance of the web page visited in the step and what a user would experience when going through the current step. Metrics include:

* **First contentful paint (FCP)** focuses on the initial rendering and measures the time from when the page starts loading to when any part of the page’s content is displayed on the screen.
* **Largest contentful paint (LCP)** measures loading performance. To provide a good user experience, LCP should occur within 2.5 seconds of when the page first starts loading.
* **Cumulative layout shift (CLS)** measures visual stability. To provide a good user experience, pages should maintain a CLS of less than 0.1.
* **`DOMContentLoaded` event (DCL)** is triggered when the browser completes parsing the document. Helpful when there are multiple listeners, or logic is executed: `domContentLoadedEventEnd - domContentLoadedEventStart`.
* **Transfer size** represents the size of the fetched resource. The size includes the response header fields plus the response payload body.

::::{note}
Largest contentful paint and Cumulative layout shift are part of Google’s [Core Web Vitals](https://web.dev/vitals/), an initiative that introduces a set of metrics that help categorize good and bad sites by quantifying the real-world user experience.

::::

Next to each metric, there’s an icon that indicates whether the value is higher (![Value is higher icon](/solutions/images/observability-sortUp.svg "")), lower (![Value is lower icon](/solutions/images/observability-sortDown.svg "")), or the same (![Value is the same](/solutions/images/observability-minus.svg "")) compared to all runs over the last 24 hours. Hover over the icon to see more details in a tooltip.

:::{image} /solutions/images/observability-synthetics-analyze-one-step-metrics.png
:alt: Metrics visualization for one step in a browser monitor in the {{synthetics-app}}
:screenshot:
:::

#### Object weight and count [synthetics-analyze-one-step-object]

The **Object weight** visualization shows the cumulative size of downloaded resources by type, and **Object count** shows the number of individual resources by type.

This provides a different kind of analysis. For example, you might have a large number of JavaScript files, each of which will need a separate download, but they may be collectively small. This could help you identify an opportunity to improve efficiency by combining multiple files into one.

:::{image} /solutions/images/observability-synthetics-analyze-one-step-object.png
:alt: Object visualization for one step in a browser monitor in the {{synthetics-app}}
:screenshot:
:::

#### Network requests [synthetics-analyze-one-step-network]

The **Network requests** visualization is a waterfall chart that shows every request the page made when a user executed it. Each line in the chart represents an HTTP network request and helps you quickly identify what resources are taking the longest to load and in what order they are loading.

The colored bars within each line indicate the time spent per resource. Each color represents a different part of that resource’s loading process (as defined in the [Timing](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-one-step-timing) section above) and includes the time spent downloading content for specific Multipurpose Internet Mail Extensions (MIME) types: HTML, JS, CSS, Media, Font, XHR, and Other.

Understanding each phase of a request can help you improve your site’s speed by reducing the time spent in each phase.

:::{image} /solutions/images/observability-synthetics-analyze-one-step-network.png
:alt: Network requests waterfall visualization for one step in a browser monitor in the {{synthetics-app}}
:screenshot:
:::

Without leaving the waterfall chart, you can view data points relating to each resource: resource details, request headers, response headers, and certificate headers. On the waterfall chart, select a resource name, or any part of each row, to display the resource details overlay.

For additional analysis, whether to check the content of a CSS file or to view a specific image, click the ![External link icon](/solutions/images/observability-popout.svg "") icon located beside each resource, to view its content in a new tab.

You can also navigate between steps and checks at the top of the page to view the corresponding waterfall charts.