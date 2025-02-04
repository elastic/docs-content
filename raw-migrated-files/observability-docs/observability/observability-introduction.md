# What is Elastic {{observability}}? [observability-introduction]

{{observability}} provides granular insights and context into the behavior of applications running in your environments. It’s an important part of any system that you build and want to monitor. Being able to detect and fix root cause events quickly within an observable system is a minimum requirement for any analyst.

[Elastic {{observability}}](https://www.elastic.co/observability) provides a single stack to unify your logs, infrastructure metrics, application traces, user experience data, synthetics, and universal profiling. Ingest your data directly to {{es}}, where you can further process and enhance the data, before visualizing it and adding alerts in {{kib}}.

:::{image} ../../../images/observability-what-is-observability.svg
:alt: Elastic {{observability}} overview diagram
:::


## Application performance monitoring (APM) [apm-overview]

Instrument your code and collect performance data and errors at runtime by installing APM agents like Java, Go, .NET, and many more.

On the {{observability}} **Overview** page, the **Services** chart shows the total number of services running within your environment and the total number of transactions per minute that were captured by the Elastic APM agent instrumenting those services.

:::{image} ../../../images/observability-apm.png
:alt: Summary of Services on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the Applications UI by clicking **Show service inventory** to quickly find the APM traces for underlying services.

For more information, see [Application performance monitoring (APM)](../../../solutions/observability/apps/application-performance-monitoring-apm.md).


## Infrastructure monitoring [metrics-overview]

Monitor system and service metrics from your servers, Docker, Kubernetes, Prometheus, and other services and applications.

On the {{observability}} **Overview** page, the **Hosts** table shows your top hosts with the most significant resource footprints. These metrics help you evaluate host efficiency and determine if resource consumption is impacting end users.

:::{image} ../../../images/observability-metrics-summary.png
:alt: Summary of Hosts on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the {{infrastructure-app}} by clicking **Show inventory**. Here you can monitor and filter your data by hosts, pods, containers,or EC2 instances and create custom groupings such as availability zones or namespaces.

For more information, see [Infrastructure Monitoring](https://www.elastic.co/guide/en/observability/current/analyze-metrics.html).


## Real user monitoring (RUM) [user-experience-overview]

Quantify and analyze the perceived performance of your web application with {{user-experience}} data, powered by the APM RUM agent. Unlike testing environments, {{user-experience}} data reflects real-world user experiences.

On the {{observability}} **Overview** page, the **{{user-experience}}** chart provides a snapshot of core web vitals for the service with the most traffic.

:::{image} ../../../images/observability-obs-overview-ue.png
:alt: Summary of {{user-experience}} metrics on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the {{user-experience}} dashboard by clicking **Show dashboard** too see data by URL, operating system, browser, and location.

For more information, see [{{user-experience}}](../../../solutions/observability/apps/real-user-monitoring-user-experience.md).


## Log monitoring [logs-overview]

Analyze log data from your hosts, services, Kubernetes, Apache, and many more.

On the {{observability}} **Overview** page, the **Log Events** chart helps you detect and inspect possible log anomalies across each of your ingested log sources to determine if the log rate is outside of your expected bounds.

:::{image} ../../../images/observability-log-rate.png
:alt: Summary of Log Events on the {{observability}} overview page
:class: screenshot
:::

You can then drill down into the {{logs-app}} by clicking **Show log stream** to view a live stream of your logs, and the filter, pin, or highlight the data you need.

For more information, see [Log monitoring](../../../solutions/observability/logs/explore-logs.md).


## Synthetic monitoring [synthetic-monitoring-overview]

Simulate actions and requests that an end user would perform on your site at predefined intervals and in a controlled environment. The end result is rich, consistent, and repeatable data that you can trend and alert on.

For more information, see [Synthetic monitoring](../../../solutions/observability/apps/synthetic-monitoring.md).


## Universal Profiling [universal-profiling-overview]

Build stack traces to get visibility into your system without application source code changes or instrumentation. Use flamegraphs to explore system performance and identify the most expensive lines of code, increase CPU resource efficiency, debug performance regressions, and reduce cloud spend.

For more information, see [Universal Profiling](../../../solutions/observability/infra-and-hosts/universal-profiling.md).


## Alerting [alerts-overview]

Stay aware of potential issues in your environments with {{kib}}’s alerting and actions feature that integrates with the {{logs-app}}, {{infrastructure-app}}, and Applications UI. It provides a set of built-in actions and specific threshold rules and enables central management of all rules from {{kib}} Management.

On the {{observability}} **Overview** page, the **Alerts** table provides a snapshot of alerts occurring within the specified time frame. The table includes the alert status, when it was last updated, the reason for the alert, and more.

:::{image} ../../../images/observability-alerts-overview.png
:alt: Summary of Alerts on the {{observability}} overview page
:class: screenshot
:::

You can then see more details on these alerts by clicking **Show alerts**.

For more information, see [Alerting](../../../solutions/observability/incident-management/alerting.md).
