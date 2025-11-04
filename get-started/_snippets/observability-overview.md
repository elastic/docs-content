Elastic {{observability}} provides unified observability across applications and infrastructure. It combines logs, metrics, application traces, user experience data, and more into a single, integrated platform.
This consolidation allows for powerful, cross-referenced analysis, enabling teams to move from detecting issues to understanding their root causes quickly and efficiently.
By leveraging the search and analytics capabilities of {{es}}, it offers a holistic view of system behavior.

Elastic {{observability}} embraces open standards like OpenTelemetry for flexible data collection, and offers scalable, cost-efficient data retention with tiered storage.

:::{tip}
New to Elastic? Refer to [Elastic Fundamentals](/get-started/index.md) to understand the Elastic Stack and its components, and your deployment options.
:::

## Use cases [observability-use-cases]

Apply {{observability}} to various scenarios to improve operational awareness and system reliability. 

:::{dropdown} Use cases
:open:
* **[Log monitoring and analytics](/solutions/observability/logs.md):** Centralize and analyze petabytes of log data from any source. This enables quick searching, ad-hoc queries with ES|QL, and visualization with prebuilt dashboards to diagnose issues.
* **[Application Performance Monitoring (APM)](/solutions/observability/applications/index.md):** Gain code-level visibility into application performance. By collecting and analyzing traces with native OTel support, teams can identify bottlenecks, track errors, and optimize the end-user experience.
* **[Infrastructure monitoring](/solutions/observability/infra-and-hosts.md):** Monitor metrics from servers, virtual machines, containers, and serverless environments with over 400 out-of-the-box integrations, including OpenTelemetry. This provides deep insights into resource utilization and overall system health.
* **[AI-powered log analysis with Streams](/solutions/observability/streams/streams.md):** Ingest raw logs in any format directly to a single endpoint without the need for complex agent management or manual parsing pipelines. Streams leverages AI to automatically parse, structure, and analyze log data on the fly.
* **Digital experience monitoring:**
  * **[Real User Monitoring (RUM)](/solutions/observability/applications/user-experience.md):** Capture and analyze data on how real users interact with web applications to improve perceived performance.
  * **[Synthetic monitoring](/solutions/observability/synthetics/index.md):** Proactively simulate user journeys and API calls to test application availability and functionality.
  * **[Uptime monitoring](/solutions/observability/uptime/index.md):** Continuously check the status of services and applications to ensure they are available.
* **[LLM Observability](/solutions/observability/applications/llm-observability.md):** Gain deep insights into the performance, usage, and costs of Large Language Model (LLM) prompts and responses.
* **[Incident response and management](/solutions/observability/incident-management.md):** Investigate operational incidents by correlating data from multiple sources, accelerating root cause analysis and resolution.
* **[Universal Profiling](/solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md):** Gain visibility into system performance and identify expensive lines of code without application instrumentation, helping to increase CPU efficiency and reduce cloud spend.
:::

To start your {{observability}} journey, read the [**Get started**](/solutions/observability/get-started.md) guide, which presents all the essential steps, with links to valuable resources. You can also browse the {{observability}} [**Quickstart guides**](/solutions/observability/get-started/quickstarts.md).

## Core concepts [observability-concepts]

At the heart of Elastic {{observability}} are several key components that enable its capabilities. 

:::{dropdown} Concepts
:open:
* The three pillars of {{observability}} are:

  * [**Logs:**](/solutions/observability/logs.md) Timestamped records of events that provide detailed, contextual information.
  * [**Metrics:**](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) Numerical measurements of system performance and health over time.
  * [**Traces:**](/solutions/observability/apm/traces.md) Representations of end-to-end journeys of requests as they travel through distributed systems.
* [**OpenTelemetry:**](/solutions/observability/apm/opentelemetry/index.md) {{Observability}} offers first-class, production-grade support for OpenTelemetry. This allows organizations to use vendor-neutral instrumentation and stream native OTel data without proprietary agents, leveraging the {{edot}} (EDOT).
* [**AIOps and AI Assistant:**](/solutions/observability/observability-ai-assistant.md) Leverages predictive analytics and an LLM-powered AI Assistant to reduce the time required to detect, investigate, and resolve incidents. This includes zero-config {{anomaly-detect}}, pattern analysis, and the ability to surface correlations and root causes.
* **[Alerting](/solutions/observability/incident-management/alerting.md)**: Allows you to create  rules to detect complex conditions and perform actions. 
* **[Cases](/solutions/observability/incident-management/cases.md):** Cases allows teams to stay aware of potential issues and track investigation details, assign tasks, and collaborate on resolutions.
* [**Service Level Objectives (SLOs):**](/solutions/observability/incident-management/service-level-objectives-slos.md) A framework for defining and monitoring the reliability of a service. Elastic {{observability}} allows for creating and tracking SLOs to ensure you meet your performance targets.
:::