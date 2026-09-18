Elastic {{observability}} provides unified observability across applications and infrastructure. It combines logs, metrics, application traces, user experience data, and more into a single, integrated platform.
Use the search and analytics capabilities of {{es}} to analyze and correlate these signals.

Elastic {{observability}} supports OpenTelemetry data collection and tiered data storage.

:::{tip}
New to Elastic? Refer to [Elastic Fundamentals](/get-started/index.md) to understand the Elastic Stack, its components, and your deployment options.
:::

## Use cases [observability-use-cases]

Apply {{observability}} to various scenarios to improve operational awareness and system reliability.

:::{dropdown} Use cases
:open:
* **[Log monitoring and analytics](/solutions/observability/logs.md):** Centralize log data, search it, run ad hoc ES|QL queries, and visualize it with dashboards.
* **[Application Performance Monitoring (APM)](/solutions/observability/applications/index.md):** Collect and analyze traces to identify bottlenecks, track errors, and inspect application performance.
* **[Infrastructure monitoring](/solutions/observability/infra-and-hosts.md):** Monitor servers, virtual machines, containers, and serverless environments with hundreds of integration and input packages, including OpenTelemetry inputs.
* **[AI-powered log analysis with Streams](/solutions/observability/streams/streams.md):** Send logs to a managed endpoint, then use AI-assisted partition and processing-pipeline suggestions or configure processing manually. Saved processors structure matching logs during ingestion.
* **Digital experience monitoring:**
    * **[Real User Monitoring (RUM)](/solutions/observability/applications/user-experience.md):** Capture and analyze data about how users interact with web applications.
    * **[Synthetic monitoring](/solutions/observability/synthetics/index.md):** Run browser journeys and lightweight HTTP, TCP, and ICMP checks to test application availability and functionality.
* **[LLM Observability](/solutions/observability/applications/llm-observability.md):** Analyze available large language model (LLM) prompt and response data, performance, token usage, and provider cost data. Cost visibility depends on the provider and integration.
* **[Incident response and management](/solutions/observability/incident-management.md):** Investigate operational incidents by correlating data from multiple sources.
* **[Universal Profiling](/solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md):** Analyze system performance and identify expensive lines of code without instrumenting or restarting applications.
:::

To start using {{observability}}, follow the [**Get started**](/solutions/observability/get-started.md) guide or browse the {{observability}} [**Quickstart guides**](/solutions/observability/get-started/quickstarts.md).

## Core concepts [observability-concepts]

At the heart of Elastic {{observability}} are several key components that enable its capabilities.

:::{dropdown} Concepts
:open:
* The three pillars of {{observability}} are:

  * [**Logs:**](/solutions/observability/logs.md) Timestamped records of events that provide detailed, contextual information.
  * [**Metrics:**](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) Numerical measurements of system performance and health over time.
  * [**Traces:**](/solutions/observability/apm/traces.md) Representations of end-to-end journeys of requests as they travel through distributed systems.
* [**OpenTelemetry:**](/solutions/observability/apm/opentelemetry/index.md) Collect vendor-neutral OpenTelemetry data with {{edot}} or upstream OpenTelemetry components.
* [**AIOps and Elastic AI Agent:**](/solutions/observability/ai/observability-ai-assistant.md) Use anomaly detection, pattern analysis, and agent tools that surface correlations across observability data.
* **[Alerting](/solutions/observability/incident-management/alerting.md):** Create rules to detect conditions and perform actions.
* **[Cases](/solutions/observability/incident-management/observability-cases.md):** Track investigation details, assign cases to users, add comments and attachments, and push cases to external systems.
* [**Service level objectives (SLOs):**](/solutions/observability/incident-management/service-level-objectives-slos.md) Define and track reliability targets, error budgets, and SLO status for your services.
:::