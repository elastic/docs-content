---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-service-maps.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-service-map.html
---

# Service Map [apm-service-maps]

A service map is a real-time visual representation of the instrumented services in your application’s architecture. It shows you how these services are connected, along with high-level metrics like average transaction duration, requests per minute, and errors per minute. If enabled, service maps also integrate with machine learning—​for real time health indicators based on anomaly detection scores. All of these features can help you quickly and visually assess your services' status and health.

We currently surface two types of service maps:

* **Global**: All services instrumented with APM agents and the connections between them are shown.
* **Service-specific**: Highlight connections for a selected service.


## How do service maps work? [service-maps-how]

Service Maps rely on distributed traces to draw connections between services. As [distributed tracing](/solutions/observability/apps/traces.md) is enabled out-of-the-box for supported technologies, so are service maps. However, if a service isn’t instrumented, or a `traceparent` header isn’t being propagated to it, distributed tracing will not work, and the connection will not be drawn on the map.


## Visualize your architecture [visualize-your-architecture]

Select the **Service Map** tab to get started. By default, all instrumented services and connections are shown. Whether you’re onboarding a new engineer, or just trying to grasp the big picture, drag things around, zoom in and out, and begin to visualize how your services are connected.

Customize what the service map displays using either the query bar or the environment selector. The query bar enables you to use [advanced queries](../../../solutions/observability/apps/use-advanced-queries-on-application-data.md) to customize the service map based on your needs. The environment selector allows you to narrow displayed results to a specific environment. This can be useful if you have two or more services, in separate environments, but with the same name. Use the environment drop-down to only see the data you’re interested in, like `dev` or `production`.

If there’s a specific service that interests you, select that service to highlight its connections. Click **Focus map** to refocus the map on the selected service and lock the connection highlighting. Click the **Transactions** tab to jump to the Transaction overview for the selected service. You can also use the tabs at the top of the page to easily jump to the **Errors** or **Metrics** overview.


:::{image} ../../../images/observability-service-maps-java.png
:alt: Example view of service maps in the Applications UI in Kibana
:class: screenshot
:::


## Anomaly detection with machine learning [service-map-anomaly-detection]

You can create machine learning jobs to calculate anomaly scores on APM transaction durations within the selected service. When these jobs are active, service maps will display a color-coded anomaly indicator based on the detected anomaly score:

|  |  |
| --- | --- |
| ![APM green service](../../../images/observability-green-service.png "") | Max anomaly score **≤25**. Service is healthy. |
| ![APM yellow service](../../../images/observability-yellow-service.png "") | Max anomaly score **26-74**. Anomalous activity detected. Service may be degraded. |
| ![APM red service](../../../images/observability-red-service.png "") | Max anomaly score **≥75**. Anomalous activity detected. Service is unhealthy. |

:::{image} ../../../images/observability-apm-service-map-anomaly.png
:alt: Example view of anomaly scores on service maps in the Applications UI
:class: screenshot
:::

If an anomaly has been detected, click **View anomalies** to view the anomaly detection metric viewer. This time series analysis will display additional details on the severity and time of the detected anomalies.

To learn how to create a machine learning job, refer to [Integrate with machine learning](../../../solutions/observability/apps/integrate-with-machine-learning.md).


## Legend [service-maps-legend]

Nodes appear on the map in one of two shapes:

* **Circle**: Instrumented services. Interior icons are based on the language of the APM agent used.
* **Diamond**: Databases, external, and messaging. Interior icons represent the generic type, with specific icons for known entities, like Elasticsearch. Type and subtype are based on `span.type`, and `span.subtype`.


## Supported APM agents [service-maps-supported]

Service Maps are supported for the following APM agent versions:

|  |  |
| --- | --- |
| Go agent | ≥ v1.7.0 |
| Java agent | ≥ v1.13.0 |
| .NET agent | ≥ v1.3.0 |
| Node.js agent | ≥ v3.6.0 |
| PHP agent | ≥ v1.2.0 |
| Python agent | ≥ v5.5.0 |
| Ruby agent | ≥ v3.6.0 |
| Real User Monitoring (RUM) agent (**Elastic Stack only**)| ≥ v4.7.0 |