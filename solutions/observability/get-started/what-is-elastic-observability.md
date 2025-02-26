---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/observability-introduction.html
  - https://www.elastic.co/guide/en/serverless/current/observability-serverless-observability-overview.html
---

# What is Elastic {{observability}}? [observability-introduction]

{{observability}} provides granular insights and context into the behavior of applications running in your environments. It’s an important part of any system that you build and want to monitor. Being able to detect and fix root cause events quickly within an observable system is a minimum requirement for any analyst.

[Elastic {{observability}}](https://www.elastic.co/observability) provides a single stack to unify your logs, infrastructure metrics, application traces, user experience data, synthetics, and universal profiling. Ingest your data directly to {{es}}, where you can further process and enhance the data, before visualizing it and adding alerts in {{kib}}.

:::{image} ../../../images/observability-what-is-observability.svg
:alt: Elastic {{observability}} overview diagram
:::

## Log monitoring [apm-overview]

Analyze log data from your hosts, services, Kubernetes, Apache, and many more.

In **Logs Explorer** (powered by Discover), you can quickly search and filter your log data, get information about the structure of the fields, and display your findings in a visualization.

:::{image} ../../../images/serverless-log-explorer-overview.png
:alt: Logs Explorer showing log events
:class: screenshot
:::

[Learn more about log monitoring →](../../../solutions/observability/logs.md)


## Application performance monitoring (APM) [observability-serverless-observability-overview-application-performance-monitoring-apm]

Instrument your code and collect performance data and errors at runtime by installing APM agents like Java, Go, .NET, and many more. Then use Observability to monitor your software services and applications in real time:

* Visualize detailed performance information on your services.
* Identify and analyze errors.
* Monitor host-level and APM agent-specific metrics like JVM and Go runtime metrics.

The **Service** inventory provides a quick, high-level overview of the health and general performance of all instrumented services.

:::{image} ../../../images/serverless-services-inventory.png
:alt: Service inventory showing health and performance of instrumented services
:class: screenshot
:::

[Learn more about Application performance monitoring (APM) →](../../../solutions/observability/apps/application-performance-monitoring-apm.md)


## Infrastructure monitoring [metrics-overview]

Monitor system and service metrics from your servers, Docker, Kubernetes, Prometheus, and other services and applications.

On the {{observability}} **Overview** page, the **Hosts** table shows your top hosts with the most significant resource footprints. These metrics help you evaluate host efficiency and determine if resource consumption is impacting end users.

:::{image} ../../../images/observability-metrics-summary.png
:alt: Summary of Hosts on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the {{infrastructure-app}} by clicking **Show inventory**. Here you can monitor and filter your data by hosts, pods, containers,or EC2 instances and create custom groupings such as availability zones or namespaces.

[Learn more about infrastructure monitoring → ](../../../solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md)


% Stateful only for RUM.

## Real user monitoring (RUM) [user-experience-overview]

Quantify and analyze the perceived performance of your web application with {{user-experience}} data, powered by the APM RUM agent. Unlike testing environments, {{user-experience}} data reflects real-world user experiences.

On the {{observability}} **Overview** page, the **{{user-experience}}** chart provides a snapshot of core web vitals for the service with the most traffic.

:::{image} ../../../images/observability-obs-overview-ue.png
:alt: Summary of {{user-experience}} metrics on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the {{user-experience}} dashboard by clicking **Show dashboard** too see data by URL, operating system, browser, and location.

 [Learn more about {{user-experience}} →](../../../solutions/observability/apps/real-user-monitoring-user-experience.md).

## Synthetic monitoring [synthetic-monitoring-overview]

Simulate actions and requests that an end user would perform on your site at predefined intervals and in a controlled environment. The end result is rich, consistent, and repeatable data that you can trend and alert on.

[Learn more about Synthetic monitoring →](../../../solutions/observability/apps/synthetic-monitoring.md).

% Stateful only for Universal Profiling.

## Universal Profiling [universal-profiling-overview]

Build stack traces to get visibility into your system without application source code changes or instrumentation. Use flamegraphs to explore system performance and identify the most expensive lines of code, increase CPU resource efficiency, debug performance regressions, and reduce cloud spend.

[Learn more about Universal Profiling →](../../../solutions/observability/infra-and-hosts/universal-profiling.md).


## Alerting [observability-serverless-observability-overview-alerting]

Stay aware of potential issues in your environments with Observability’s alerting and actions feature that integrates with log monitoring and APM. It provides a set of built-in actions and specific threshold rules and enables central management of all rules.

On the **Alerts** page, the **Alerts** table provides a snapshot of alerts occurring within the specified time frame. The table includes the alert status, when it was last updated, the reason for the alert, and more.

:::{image} ../../../images/serverless-observability-alerts-overview.png
:alt: Summary of Alerts on the Observability overview page
:class: screenshot
:::

[Learn more about alerting → ](../../../solutions/observability/incident-management/alerting.md)


## Service-level objectives (SLOs) [observability-serverless-observability-overview-service-level-objectives-slos]

Set clear, measurable targets for your service performance, based on factors like availability, response times, error rates, and other key metrics. Then monitor and track your SLOs in real time, using detailed dashboards and alerts that help you quickly identify and troubleshoot issues.

From the SLO overview list, you can see all of your SLOs and a quick summary of what’s happening in each one:

:::{image} ../../../images/serverless-slo-dashboard.png
:alt: Dashboard showing list of SLOs
:class: screenshot
:::

[Learn more about SLOs → ](../../../solutions/observability/incident-management/service-level-objectives-slos.md)

## Cases [observability-serverless-observability-overview-cases]

Collect and share information about observability issues by creating cases. Cases allow you to track key investigation details, add assignees and tags to your cases, set their severity and status, and add alerts, comments, and visualizations. You can also send cases to third-party systems, such as ServiceNow and Jira.

:::{image} ../../../images/serverless-cases.png
:alt: Screenshot showing list of cases
:class: screenshot
:::

[Learn more about cases → ](../../../solutions/observability/incident-management/cases.md)

## Machine learning and AIOps [observability-serverless-observability-overview-aiops]

Reduce the time and effort required to detect, understand, investigate, and resolve incidents at scale by leveraging predictive analytics and machine learning:

* Detect anomalies by comparing real-time and historical data from different sources to look for unusual, problematic patterns.
* Find and investigate the causes of unusual spikes or drops in log rates.
* Detect distribution changes, trend changes, and other statistically significant change points in a metric of your time series data.

:::{image} ../../../images/serverless-log-rate-analysis.png
:alt: Log rate analysis page showing log rate spike
:class: screenshot
:::

[Learn more about machine learning and AIOps →](../../../explore-analyze/machine-learning/machine-learning-in-kibana/xpack-ml-aiops.md)