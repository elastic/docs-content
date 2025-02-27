---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-mobile-session-explorer.html
applies_to:
  stack: all
---

# Explore mobile sessions with Discover [apm-mobile-session-explorer]

Elastic Mobile APM provides session tracking by attaching a `session.id`, a guid, to every span and event. This allows for the recall of the activities of a specific user during a specific period of time. The best way recall these data points is using [Discover](../../../explore-analyze/discover/document-explorer.md). This guide will explain how to do that.


## Viewing sessions with Discover [viewing-sessions-with-discover]

The first step is to find the relevant `session.id`. In this example, we’ll walk through investigating a crash. Since all events and spans have `session.id` attributes, a crash is no different.

The steps to follow are:

* copy the `session.id` from the relevant document.
* Open the Discover page.
* Select the appropriate data view (use `APM` to search all data streams)
* set filter to the copied `session.id`

Here we can see the `session.id` guid in the metadata viewer in the error detail view:

:::{image} ../../../images/observability-mobile-session-error-details.png
:alt: Example of session.id in error details
:class: screenshot
:::

Copy this value and open the Discover page:

:::{image} ../../../images/observability-mobile-session-explorer-nav.png
:alt: Example view of navigation to Discover
:class: screenshot
:::

Set the data view. `APM` selected in the example:

:::{image} ../../../images/observability-mobile-session-explorer-apm.png
:alt: Example view of Explorer selecting APM data view
:class: screenshot
:::

Filter using the `session.id`: `session.id: "<copied session id guid>"`:

:::{image} ../../../images/observability-mobile-session-filter-discover.png
:alt: Filter Explor using session.id
:class: screenshot
:::

Explore all the documents associated with that session id including crashes, lifecycle events, network requests, errors, and other custom events!

