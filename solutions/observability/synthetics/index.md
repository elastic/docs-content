---
description: Synthetic monitoring with Elastic. Run HTTP, TCP, and ICMP checks and browser monitors from Elastic's global locations or your own private locations.
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-uptime-synthetics.html
  - https://www.elastic.co/guide/en/serverless/current/observability-monitor-synthetics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Synthetic monitoring [monitor-uptime-synthetics]

Use the Synthetics UI to view results from monitors you create and manage directly in the [Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md) or externally through a [Synthetics project](/solutions/observability/synthetics/create-monitors-with-projects.md). You can run lightweight or browser-based monitors from Elastic's global managed testing infrastructure or from your own [{{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md).

::::{important}
The {{synthetics-app}} runs active checks against URLs and user journeys. It does not discover infrastructure or {{k8s}} targets on its own.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The Synthetics UI lists monitors that {{heartbeat}} or {{agent}} runs, including autodiscovered ones, as read-only entries. Refer to [Autodiscovered monitors](/solutions/observability/synthetics/analyze-data.md#synthetics-analyze-autodiscovered-monitors) for more information.

For infrastructure or {{k8s}} uptime monitoring, refer to [monitoring infrastructure and {{k8s}}](/solutions/observability/synthetics/scale-architect-synthetics-deployment.md#synthetics-no-autodiscovery-for-k8s-infra).
::::

Synthetics periodically checks the status of your services and applications. Monitor the availability of network endpoints and services using the following types of monitors:

* [Lightweight HTTP/S, TCP, and ICMP monitors](/solutions/observability/synthetics/index.md#monitoring-uptime)
* [Browser monitors](/solutions/observability/synthetics/index.md#monitoring-synthetics)

:::{image} /solutions/images/observability-synthetics-monitor-page.png
:alt: Synthetics Overview in 9.6 with monitor status counts, ping history, and monitor cards
:screenshot:
:::

## Lightweight HTTP/S, TCP, and ICMP monitors [monitoring-uptime]

You can monitor the status of network endpoints using the following lightweight checks:

|     |     |
| --- | --- |
| **HTTP monitor** | Monitor your website. The HTTP monitor checks to make sure specific endpoints return the correctstatus code and display the correct text. |
| **ICMP monitor** | Check the availability of your hosts. The ICMP monitor uses ICMP (v4 and v6) EchoRequests to check the network reachability of the hosts you are pinging. This will tell you whether thehost is available and connected to the network, but doesn’t tell you if a service on the host is running ornot. |
| **TCP monitor** | Monitor the services running on your hosts. The TCP monitor checks individual ports to make sure the service is accessible and running. |

To set up your first monitor, refer to [Get started](/solutions/observability/synthetics/get-started.md).

## Browser monitors [monitoring-synthetics]

Real browser synthetic monitoring enables you to test critical actions and requests that an end-user would make on your site at predefined intervals and in a controlled environment. Synthetic monitoring extends traditional end-to-end testing techniques because it allows your tests to run continuously on the cloud. The result is rich, consistent, and repeatable data that you can trend and alert on.

For example, you can test popular user journeys, like logging in, adding items to a cart, and checking out — actions that need to work for your users consistently.

You can run an automated Synthetics project on a real Chromium browser and view each synthetic monitoring journey in your Observability project side-by-side with your other monitors.

Alerting helps you detect degraded performance or broken actions before your users do. By receiving alerts early, you can fix issues before they impact your bottom line or customer experience.

To set up your first monitor, refer to [Get started](/solutions/observability/synthetics/get-started.md).
