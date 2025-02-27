---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/observability-get-started.html
  - https://www.elastic.co/guide/en/observability/current/observability-get-started.html
  - https://www.elastic.co/guide/en/observability/current/index.html

navigation_title: "Get started"
---

# Get started with Elastic Observability [observability-get-started]


New to Elastic {{observability}}? Discover more about our observability features and how to get started.


## Learn about Elastic {{observability}} [_learn_about_elastic_observability]

Learn about key features available to help you get value from your observability data:

* [What is Elastic {{observability}}?](../../solutions/observability/get-started/what-is-elastic-observability.md)
* [What’s new in Elastic Stack](https://www.elastic.co/guide/en/observability/current/whats-new.html)
* [{{obs-serverless}} billing dimensions](../../deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md)


## Get started with your use case [get-started-with-use-case]

Learn how to spin up a deployment on {{ech}} or create an Observability Serverless project and use Elastic Observability to gain deeper insight into the behavior of your applications and systems.

:::{image} ../../images/observability-get-started.svg
:alt: get started
:::

1. **Choose your source.** Elastic integrates with hundreds of data sources for unified visibility across all your applications and systems.
2. **Ingest your data.** Turn-key integrations provide a repeatable workflow to ingest data from all your sources: you install an integration, configure it, and deploy an agent to collect your data.
3. **View your data.** Navigate seamlessly between Observabilty UIs and dashboards to identify and resolve problems quickly.
4. **Customize.** Expand your deployment and add features like alerting and anomaly detection.

To get started with on serverless, [create an Observability project](../../solutions/observability/get-started/create-an-observability-project.md), then follow one of our [quickstarts](../../solutions/observability/get-started.md#quickstarts-overview) to learn how to ingest and visualize your observability data.

### Quickstarts [quickstarts-overview]

Our quickstarts dramatically reduce your time-to-value by offering a fast path to ingest and visualize your Observability data. Each quickstart provides:

* A highly opinionated, fast path to data ingestion
* Sensible configuration defaults with minimal configuration required
* Auto-detection of logs and metrics for monitoring hosts
* Quick access to related dashboards and visualizations

Follow the steps in these guides to get started quickly:

* [Quickstart: Monitor hosts with {{agent}}](../../solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md)
* [Quickstart: Monitor your Kubernetes cluster with {{agent}}](../../solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md)
* [Quickstart: Monitor hosts with OpenTelemetry](../../solutions/observability/get-started/quickstart-monitor-hosts-with-opentelemetry.md)
* [Quickstart: Unified Kubernetes Observability with Elastic Distributions of OpenTelemetry (EDOT)](../../solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md)
* [Quickstart: Collect data with AWS Firehose](../../solutions/observability/get-started/quickstart-collect-data-with-aws-firehose.md)


### Get started with other features [_get_started_with_other_features]

Want to use {{fleet}} or some other feature not covered in the quickstarts? Follow the steps in these guides to get started:

% Stateful only for Universal profiling

* [Get started with system metrics](../../solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)
* [Get started with application traces and APM](../../solutions/observability/apps/fleet-managed-apm-server.md)
* [Get started with synthetic monitoring](../../solutions/observability/apps/synthetic-monitoring.md)
* [Get started with Universal Profiling](../../solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md)


## Additional guides [_additional_guides]

Ready to dig into more features of Elastic Observability? See these guides:

* [Create an alert](../../solutions/observability/incident-management/alerting.md)
* [Create a service-level objective (SLO)](../../solutions/observability/incident-management/create-an-slo.md)

## Related content for Elastic Stack [_related_content]

* [Starting with the {{es}} Platform and its Solutions](/get-started/index.md) for new users
* [Adding data to {{es}}](../../manage-data/ingest.md) for other ways to ingest data