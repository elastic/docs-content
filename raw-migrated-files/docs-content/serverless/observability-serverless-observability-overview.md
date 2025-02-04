# Observability overview [observability-serverless-observability-overview]

{{obs-serverless}} provides granular insights and context into the behavior of applications running in your environments. It’s an important part of any system that you build and want to monitor. Being able to detect and fix root cause events quickly within an observable system is a minimum requirement for any analyst.

{{obs-serverless}} provides a single stack to unify your logs, metrics, and application traces. Ingest your data directly to your Observability project, where you can further process and enhance the data, before visualizing it and adding alerts.

:::{image} ../../../images/serverless-serverless-capabilities.svg
:alt: {{obs-serverless}} overview diagram
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

Instrument your code and collect performance data and errors at runtime by installing APM agents like Java, Go, .NET, and many more. Then use {{obs-serverless}} to monitor your software services and applications in real time:

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

The **Infrastructure** UI provides a couple ways to view and analyze metrics across your infrastructure:

The **Infrastructure inventory** page provides a view of your infrastructure grouped by resource type.

:::{image} ../../../images/serverless-metrics-app.png
:alt: {{infrastructure-app}} in {kib}
:class: screenshot
:::

The **Hosts** page provides a dashboard-like view of your infrastructure and is backed by an easy-to-use interface called Lens.

:::{image} ../../../images/serverless-hosts.png
:alt: Screenshot of the Hosts page
:class: screenshot
:::

From either page, you can view health and performance metrics to get visibility into the overall health of your infrastructure. You can also drill down into details about a specific host, including performance metrics, host metadata, running processes, and logs.

[Learn more about infrastructure monitoring → ](../../../solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md)


## Synthetic monitoring [observability-serverless-observability-overview-synthetic-monitoring]

Simulate actions and requests that an end user would perform on your site at predefined intervals and in a controlled environment. The end result is rich, consistent, and repeatable data that you can trend and alert on.

For more information, see [Synthetic monitoring](../../../solutions/observability/apps/synthetic-monitoring.md).


## Alerting [observability-serverless-observability-overview-alerting]

Stay aware of potential issues in your environments with {{obs-serverless}}’s alerting and actions feature that integrates with log monitoring and APM. It provides a set of built-in actions and specific threshold rules and enables central management of all rules.

On the **Alerts** page, the **Alerts** table provides a snapshot of alerts occurring within the specified time frame. The table includes the alert status, when it was last updated, the reason for the alert, and more.

:::{image} ../../../images/serverless-observability-alerts-overview.png
:alt: Summary of Alerts on the {{obs-serverless}} overview page
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

[Learn more about machine learning and AIOps →](../../../explore-analyze/machine-learning/aiops-labs.md)
