---
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  deployment:
    ess: ga
description: Build a successful proof of concept during your Elastic trial. Learn how to define success criteria, choose the right deployment and use case, measure results, and prepare for production.
---

# Evaluate Elastic during a trial

To make the most of your free 14-day {{ecloud}} trial, set up high-value use cases, explore the most powerful Elastic features, and gather the evidence you need to determine whether Elastic is the right choice for your organization.

You have 14 days to get the most value from your trial, so don’t just click around. Ingest real data, focus on your highest priority use case, and validate the capabilities that will save you time, reduce costs, and prevent operational challenges in production.

By the end of this guide, you'll know how to structure your trial, make strategic Elastic product decisions, and measure success so you can build a meaningful proof of concept (PoC).

For a quick intro, start with learning more about [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md).

## What is included in your trial

Your {{ecloud}} trial gives you full access to explore the following features and capabilities:

- All features available in the [Search](/solutions/search.md), [{{observability}}](/solutions/observability.md), and [Security](/solutions/security.md) solutions, depending on your choice of deployment and project type.
- Access to the following: 
  - Integrations so you can ingest your data using the simplest method that meets your use case.
  - {{ml-cap}} features to evaluate anomaly detection results, search relevance, and explore visualization tools from our trained models.
  - Advanced analytics so you can test {{es}} as a vector database for building modern GenAI and semantic search applications.

:::{tip}
If you prefer to set up {{es}} and {{kib}} in Docker for local development or testing, refer to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). By default, new installations have a Basic license that never expires. To explore all the available solutions and features, start a 30-day free trial by following the instructions in [](/deploy-manage/license/manage-your-license-in-self-managed-cluster.md).  
:::

## Trial limitations

:::{include} ../deploy-manage/deploy/_snippets/trial-limitations.md
:::

## Before you begin

A successful trial starts with clarity about what you want to achieve. Three foundational decisions shape your trial: defining your trial goal, identifying your primary use case, and choosing the deployment type that best supports it.

### Define your trial goal

To achieve the best results, clarify what success looks like for your trial.

Consider the following questions:

- **What is the main problem you're trying to solve?** Examples: slow root-cause analysis, rising infrastructure costs, missing search relevance, or too many disconnected data sources.
- **If you choose to move forward, which team will use Elastic?**
- **What would a successful PoC show?** Faster investigations? Better visibility? Reduced spend?
- **Have you identified the KPIs or metrics that matter most?** Examples: time to detect, ingestion speed, relevance scores, or dashboard load times.

Document your trial goal now. This clarity will guide your use case selection and help you measure success at the end of your trial.

### Identify your primary use case

With your trial goal in mind, identify which Elastic solution best addresses your challenge. Elastic can support many workloads, but a focused trial generates clearer results. You can always expand to additional use cases after establishing initial success.

| Your challenge | Primary use case |
|----------------|-----------------|
| Users struggle to find relevant information across systems | [Search](/solutions/search.md) |
| Build your first search application | [Search](/solutions/search.md) |
| Limited visibility into application performance or system health | [Observability](/solutions/observability.md) |
| Slow incident response and troubleshooting | [Observability](/solutions/observability.md) |
| Identify unknown unknowns through logs, traces, and metrics | [Observability](/solutions/observability.md) |
| Detect and respond to endpoint security threats | [Security](/solutions/security.md) |
| Security logs are difficult to analyze or correlate | [Security](/solutions/security.md) |
| Compliance requires centralized security monitoring | [Security](/solutions/security.md) |

### Choose your deployment type

Once you know what you want to evaluate, choose the deployment option that best supports your goals. Elastic offers two primary deployment options on {{ecloud}}.

::::{tab-set}

:::{tab-item} {{serverless-full}}

- Fully managed with automatic scaling.
- Simplified configuration and maintenance.
- Project-based organization (Search, {{observability}}, or Security).
- Ideal for fast setup and focused trials of a single use case.

:::

:::{tab-item} {{ech}}

- Access to all solutions in a single deployment.
- More control over cluster configuration and sizing.
- Traditional {{es}} architecture.
- Best for evaluating multiple use cases together or when you need specific configuration options.

:::

::::

:::{tip}
For most trials, {{serverless-short}} provides the fastest path to demonstrating value. You can always explore hosted options later or migrate to production with different requirements.
:::

For detailed comparisons, refer to:

- [Deployment comparison](/deploy-manage/deploy/deployment-comparison.md): Side-by-side feature and capability comparison.
- [Differences from other {{es}} offerings](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand how {{ecloud}} differs from self-managed deployments.

## Build your proof of concept

With your trial goal defined, follow this framework to build a PoC that demonstrates clear value and helps you make an informed decision about adopting Elastic.

### Example success criteria by use case

::::{tab-set}

:::{tab-item} Search

- Reduce time to find information by X%.
- Index and search Y documents with sub-second response times.
- Demonstrate relevance tuning for domain-specific searches.

:::

:::{tab-item} Observability

- Reduce mean time to detect (MTTD) incidents by X minutes.
- Gain visibility into application performance across Y services.
- Centralize logs from Z disparate systems.

:::

:::{tab-item} Security

- Detect X types of threats that current tools miss.
- Reduce investigation time by Y%.
- Demonstrate compliance reporting for Z requirements.

:::

::::

### Ingest real data

To build a meaningful PoC, you need real-world data and not just sample datasets.

#### Why real data matters

- Results are more trustworthy for stakeholders.
- Dashboards and alerts reflect real use cases.
- Search and relevance testing becomes meaningful.
- Performance benchmarks are accurate.

#### Recommended ingestion methods

- [Elastic Agent](/reference/fleet/index.md) for logs, metrics, traces, and security data
- [Beats](beats://reference/index.md) or [Logstash](logstash://reference/index.md) for existing pipelines
- [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) for transformations and enrichment
- Elasticsearch APIs for custom application ingestion

Start with a minimal dataset if needed, then expand.

### Explore key Elastic features

Once data is flowing, use the trial to validate the features that will determine long-term adoption. Take notes on what works well and where follow-up questions might be needed.

::::{tab-set}

:::{tab-item} Search

| Feature | Why it matters | How to try it |
|---------|----------------|---------------|
| Vector search and hybrid search | Combine semantic understanding with keyword precision | [Semantic search quickstart](/solutions/search/get-started/semantic-search.md) |
| Relevance tuning | Ensure users find the most relevant results | [Query rules](/solutions/search/query-rules-ui.md) |
| Search analytics | Understand what users search for and what they find | [Search relevance](/solutions/search/full-text/search-relevance.md) |
| Performance at scale | Validate response times with production-like volumes | Index a representative dataset and benchmark queries |

:::

:::{tab-item} {{observability}}

| Feature | Why it matters | How to try it |
|---------|----------------|---------------|
| Log, metric, and trace correlation | Get full-stack visibility in one place | [Correlate data in the Applications UI](/solutions/observability/apm/find-transaction-latency-failure-correlations.md) |
| {{product.apm}} instrumentation | Identify slow transactions and errors | [{{product.apm}} quickstart](/solutions/observability/get-started/quickstart-monitor-your-application-performance.md) |
| Dashboards and alerts | Monitor SLOs and respond to incidents | [Create custom threshold alerts](/solutions/observability/incident-management/create-custom-threshold-rule.md) |
| {{ml-cap}} {{anomaly-detect}} | Automatically detect latency, throughput, and error anomalies | [Enable {{anomaly-detect}}](/solutions/observability/incident-management/create-an-apm-anomaly-rule.md) |

:::

:::{tab-item} Security

| Feature | Why it matters | How to try it |
|---------|----------------|---------------|
| Prebuilt detection rules | Detect threats without writing custom rules | [Enable detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md) |
| SIEM dashboards | Visualize security posture and trends | [Security dashboards](/solutions/security/dashboards.md) |
| Endpoint protection | Prevent malware and ransomware | [Configure {{elastic-defend}}](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md) |
| Timeline investigations | Investigate and document security events | [Investigate with Timeline](/solutions/security/investigate/timeline.md) |
| Threat intelligence | Enrich alerts with threat context | [Threat intelligence integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md) |

:::

::::

### Build your PoC deliverables

A strong PoC is essential for a good trial. Keep it simple but meaningful.

Your PoC should:

- Address the priority problem you identified in your trial goal.
- Include dashboards, searches, or workflows that matter to your teams.
- Show how Elastic improves speed, accuracy, or cost.
- Prove that Elastic can scale with your use case.
- Include metrics that stakeholders can quickly understand.

Suggested PoC deliverables:

- A short summary of your trial goal.
- A live dashboard or search interface.
- Example alerts or detections.
- Performance benchmarks or response time comparisons.
- A brief explanation of how Elastic handled your real data.

### Document your trial findings

**Track:**

- Time to ingest data.
- Performance and query speed.
- Feature coverage for your use case.
- Ease of use for developers and analysts.

**Save:**

- Screenshots of dashboards.
- Queries and scripts you tested.
- Notes on what worked well and what was missing.

### Suggested trial timeline

Most trials run for two weeks. Here's a suggested approach to maximize your trial.

#### Week 1: Foundation and initial value

For the first week, focus on the following activities:

- Set up your deployment or project.
- Connect your first data sources.
- Demonstrate basic capabilities.
- Validate that Elastic can address your use case.

We recommend the following activities for each use case:

::::{tab-set}

:::{tab-item} Search

Follow the steps in [](/solutions/search/get-started.md), which include:
  
  1. Identify your search goals.
  2. Ingest sample data or connect a data source.
  3. Build basic search queries and test relevance.

For targeted learning paths, go to [](/solutions/search/get-started/quickstarts.md).
In particular, [Index and search basics](/solutions/search/get-started/index-basics.md) and [Semantic search](/solutions/search/get-started/semantic-search.md).
:::

:::{tab-item} Observability

1. Review the [Observability getting started guide](/solutions/observability/get-started.md).
2. Deploy Elastic Agent to monitor 1-2 hosts or services.
3. Collect logs from a critical application.
4. Explore metrics and logs in Kibana.

:::

:::{tab-item} Security

1. Review the [Security getting started guide](/solutions/security/get-started.md).
2. [Ingest security data](/solutions/security/get-started/ingest-data-to-elastic-security.md) from your environment.
3. Deploy Elastic Defend to protect critical endpoints.
4. Enable prebuilt detection rules.
5. Investigate sample security events.

:::

::::

The following resources are recommended for all use cases:

- [Data ingestion overview](/manage-data/ingest.md): Learn how to bring data into Elastic.
- [Fleet and Elastic Agent](/reference/fleet/index.md): Learn about Elastic Agent and integrations for connecting data sources.
- [Discover data in Kibana](/explore-analyze/discover.md): Learn to explore and search your data.

#### Week 2: Expansion and measurement

For the second week, focus on the following activities:

- Add a few additional data sources relevant to your use case. Refer to [Fleet integrations](/reference/fleet/manage-integrations.md) for available integrations.
- Focus on metrics that demonstrate clear business value. Use [Lens visualizations](/explore-analyze/visualize/lens.md) to highlight KPIs.
- Set up alerts for critical conditions or thresholds. Refer to [Alerting](/explore-analyze/alerts-cases.md) for configuration options.
- Create dashboards that answer key stakeholder questions. Refer to [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md) for guidance.
- Compare results against your success criteria.
- Quantify time savings, efficiency gains, or risk reduction.

## Next steps after your trial

When you're ready to move beyond your trial into production:

1. Based on your PoC, determine production sizing needs. Refer to [Production guidance](/deploy-manage/production-guidance.md).
2. Review [license documentation](/deploy-manage/license.md) to choose the right tier, and [billing documentation](/deploy-manage/cloud-organization/billing.md) to understand costs.
3. If moving from trial to production, plan data migration and configuration transfer. Use [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md) to preserve your work.
4. [Contact Elastic Sales](https://www.elastic.co/contact) to discuss your trial results and production requirements.

To retain your {{ech}} deployment or {{serverless-short}} project, refer to [Remove trial limitations](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#remove-trial-limitations) and [Maintain access to your trial projects and data](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-happens-at-the-end-of-the-trial).

::::{tip}
Depending on your organization's needs, you might want to evaluate different deployment options. Elastic offers multiple deployment types including {{ece}} and {{eck}}. Explore the [deployment options](/deploy-manage/deploy.md) to find the best fit for your infrastructure.
::::

### Expand your implementation

After proving value with one use case:

- Consider additional solutions, such as {{observability}} + Security.
- Add data sources and integrations.
- Implement additional features such as {{ml}}, custom applications, and more.
- Onboard additional users in your organization.

### Getting help

- **[Elastic Community](https://discuss.elastic.co/)**: Ask questions and learn from other users.
- **[Elastic Training](https://www.elastic.co/training)**: Develop team expertise with official courses.
- **[Elastic Consulting](https://www.elastic.co/services)**: Get expert help with implementation and optimization.
- **[Elastic customer stories](https://www.elastic.co/customers/success-stories)**: Learn from organizations with similar use cases.

## Additional resources

Continue exploring Elastic's capabilities:

- **[Solutions overview](/solutions/index.md)**: Deep dive into Search, Observability, and Security capabilities.
- **[Deploy and manage](/deploy-manage/index.md)**: Comprehensive deployment and operational guidance.
- **[Manage data](/manage-data/index.md)**: Learn about data ingestion, storage, and lifecycle management.
- **[Explore and analyze](/explore-analyze/index.md)**: Master {{kib}}'s visualization and analysis tools.

