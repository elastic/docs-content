---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-uptime-synthetics.html
  - https://www.elastic.co/guide/en/serverless/current/observability-monitor-synthetics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
description: Monitor endpoints and user journeys with Elastic Synthetics using lightweight, API Journey, and browser monitors from managed or private locations.
---

# Synthetic monitoring [monitor-uptime-synthetics]

Use the Synthetics UI to view results from monitors you create and manage directly in the [Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md) or externally through a [Synthetics project](/solutions/observability/synthetics/create-monitors-with-projects.md). Depending on the monitor type, you can run monitors from Elastic managed locations or your own [{{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md).

:::{note}
:applies_to: {"stack": "ga 9.6+", "serverless": "ga"}
The **Overview** tab also shows read-only monitors run by {{heartbeat}} or {{agent}}, including monitors created through {{k8s}} or Docker autodiscovery. Refer to [View autodiscovered Heartbeat and Elastic Agent monitors](/solutions/observability/synthetics/scale-architect-synthetics-deployment.md#synthetics-autodiscovered-monitors).
:::

Synthetics periodically checks the status of your services and applications. Monitor the availability of network endpoints and services using the following types of monitors:

* [Lightweight HTTP/S, TCP, and ICMP monitors](/solutions/observability/synthetics/index.md#monitoring-uptime)
* [API Journey monitors](/solutions/observability/synthetics/index.md#monitoring-api-journeys)
* [Browser monitors](/solutions/observability/synthetics/index.md#monitoring-synthetics)

:::{image} /solutions/images/observability-synthetics-monitor-page.png
:alt: Synthetics Overview page showing monitor status and duration
:screenshot:
:::

## Lightweight HTTP/S, TCP, and ICMP monitors [monitoring-uptime]

Run lightweight monitors from Elastic managed locations or {{private-location}}s. You can monitor network endpoints using these checks:

|     |     |
| --- | --- |
| **HTTP monitor** | Check an HTTP or HTTPS endpoint. You can validate its status code, headers, response body, and JSON content. |
| **ICMP monitor** | Check ICMP reachability. The monitor uses ICMP (v4 and v6) echo requests, but an absent reply doesn't prove the host is unavailable because a firewall can block ICMP. |
| **TCP monitor** | Attempt a TCP connection to a host and port. You can optionally send data and validate the response. |

To set up your first monitor, refer to [Get started](/solutions/observability/synthetics/get-started.md).

## API Journey monitors [monitoring-api-journeys]
```{applies_to}
stack: beta 9.6+
serverless: unavailable
```

API Journey monitors use [Playwright](https://playwright.dev/docs/api-testing) to run multi-step HTTP checks without opening a browser. They run from {{private-location}}s by default. To allow them on Elastic managed locations, set `xpack.uptime.enableApiJourneyPublicLocations` to `true` in `kibana.yml`.

## Browser monitors [monitoring-synthetics]

Run browser monitors from Elastic managed locations or {{private-location}}s. Real browser synthetic monitoring lets you test actions and requests that a user makes on your site at predefined intervals in a controlled environment. Browser journeys run in Chromium and produce results that you can analyze over time.

For example, you can test popular user journeys, like logging in, adding items to a cart, and checking out — actions that need to work for your users consistently.

A Synthetics project can define browser journeys, API journeys, and lightweight monitors. You can view these project monitors alongside monitors created in the Synthetics UI.

Create monitor status rules to alert when a monitor is down and TLS certificate rules to alert about certificate problems.

To set up your first monitor, refer to [Get started](/solutions/observability/synthetics/get-started.md).
