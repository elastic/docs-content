---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/inspect.html
---

# Inspect [inspect]

The **Inspect** view in {{kib}} allows you to view information about all requests that were made to collect the data displayed on the current page.

:::{image} ../../images/observability-inspect-flyout.png
:alt: Inspector flyout in the {{uptime-app}}
:class: screenshot
:::

Many requests go into building visualizations in {{kib}}. For example, to render visualizations in the {{uptime-app}}, {{kib}} needs to request a list of all your monitors, data about the availability of each monitor over time, and more. If something goes wrong, the Inspect view can help you report an issue and troubleshoot with Elastic support.

Inspecting requests is available for the following UIs:

* Applications
* Uptime
* {{user-experience}}


## Enable inspect [inspect-enable]

To enable inspect across apps:

1. Go to {{kib}}'s [Advanced Settings](kibana://reference/advanced-settings.md).
2. Find the **Observability** section.
3. Turn on the **Inspect ES queries** option.
4. Click **Save changes**.

:::{image} ../../images/observability-inspect-enable.png
:alt: {{kib}} Advanced Settings {{observability}} section with Inspect ES queries enabled
:class: screenshot
:::


## Inspect [inspect-flyout]

Open the inspect flyout by clicking **Inspect** in the top bar.

Click the **Request** dropdown to see all the requests used to make the current page work. Select one to see information about the request below.

:::{image} ../../images/observability-inspect-flyout-dropdown.png
:alt: Inspector flyout dropdown for selecting a request to inspect
:class: screenshot
:::

Toggle between the **Statistics**, **Request**, and **Response** tabs to see details for a single request.

The **Statistics** tab provides information about the request including:

Hits
:   The number of documents returned by the query.

Hits (total)
:   The number of documents that match the query.

{{data-source-cap}}
:   The {{data-source}} that connected to the {{es}} indices.

{{kib}} API query parameters
:   The query parameters used in the {{kib}} API request that initiated the {{es}} request.

{{kib}} API route
:   The route of the {{kib}} API request that initiated the {{es}} request.

Query time
:   The time it took to process the query. Does not include the time to send the request or parse it in the browser.

Request timestamp
:   Time when the start of the request has been logged.

:::{image} ../../images/observability-inspect-flyout-statistics.png
:alt: Inspector flyout Statistics tab
:class: screenshot
:::

The **Request** tab shows the exact syntax used in the request. You can click **Copy to clipboard** to copy the request or **Open in Console** to open it in the [{{kib}} console](../../explore-analyze/query-filter/tools/console.md).

:::{image} ../../images/observability-inspect-flyout-request.png
:alt: Inspector flyout Request tab with exact syntax
:class: screenshot
:::

The **Response** tab shows the exact response used in the visualizations on the page. You can click **Copy to clipboard** to copy the response.

:::{image} ../../images/observability-inspect-flyout-response.png
:alt: Inspector flyout Response tab with exact response
:class: screenshot
:::

