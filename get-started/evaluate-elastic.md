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

If you're evaluating Elastic during a trial, this guide helps you build a meaningful proof of concept (PoC) that demonstrates clear value to your organization.

Rather than prescribing specific technical steps, this guide focuses on the evaluation process itself, helping you make strategic decisions and measure success.

For an overview, check out [Explore Elastic Cloud with your 14‑day free trial](https://www.elastic.co/cloud/cloud-trial-overview).

## What's included in your trial

Your Elastic trial gives you full access to explore our platform's capabilities:

- All features available across [Search](/solutions/search.md), [{{observability}}](/solutions/observability.md), and [Security](/solutions/security.md) solutions, depending on your choice of deployment and project type.
- A choice between {{serverless-full}} and {{ech}} deployment types.
- Access to integrations, {{ml-features}}, and advanced analytics.
- Support resources including documentation, community forums, and technical guidance.

During the trial, deployments have size and capacity limitations. You can increase deployment size after adding billing details.

:::{tip}
If you prefer to set up {{es}} and {{kib}} in Docker for local development or testing, refer to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). By default, new installations have a Basic license that never expires. To explore all the available solutions and features, start a 30-day free trial by following the instructions in [](/deploy-manage/license/manage-your-license-in-self-managed-cluster.md).  
:::

## Trial limitations

While your trial includes full feature access, be aware of these limitations:

:::{include} ../deploy-manage/deploy/_snippets/trial-limitations.md
:::
For detailed information about features and licensing, refer to the following:

- [License and support levels](/deploy-manage/license.md): Understand the different license tiers and what they include.
- [Billing documentation](/deploy-manage/cloud-organization/billing.md): Learn how billing works when moving from trial to production.

## Before you begin

Two foundational decisions shape your evaluation: which deployment type to use and which use case to focus on first.

### Choose your deployment type

Elastic offers two primary deployment options on {{ecloud}}. For most evaluations, we recommend starting with one approach and focusing your PoC there.

::::{tab-set}

:::{tab-item} Elastic Cloud Serverless

- Fully managed with automatic scaling.
- Simplified configuration and maintenance.
- Project-based organization.
- Ideal for those who want to offload infrastructure management and scale flexibly based on demand.

:::

:::{tab-item} Elastic Cloud Hosted

- More control over cluster configuration and sizing.
- Traditional {{es}} architecture.
- Best for users seeking full control over the environment while utilizing managed services for maintenance and updates.

:::

::::

For detailed comparisons, check out:

- [Deployment comparison](/deploy-manage/deploy/deployment-comparison.md): Side-by-side feature and capability comparison.
- [Differences from other {{es}} offerings](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand how {{ecloud}} differs from self-managed deployments.

:::{tip}
For most evaluations, {{serverless-short}} provides the fastest path to demonstrating value. You can always explore hosted options later or migrate to production with different requirements.
:::

### Identify your primary use case

Choose a use case to focus your initial evaluation.
In {{serverless-full}}, your use case indicates which type of project will serve your purposes.
In {{ech}}, you have access to all solutions and use cases in a single hosted deployment, but you can get the most value from the trial by focusing your investigation.
You can always expand to additional use cases after establishing initial success.

| Your challenge | Primary use case |
|----------------|-----------------|
| Users struggle to find relevant information across systems | [Search](/solutions/search.md) |
| Need to build fast, relevant search experiences for applications or websites | [Search](/solutions/search.md) |
| Limited visibility into application performance or system health | [Observability](/solutions/observability.md) |
| Slow incident response and troubleshooting | [Observability](/solutions/observability.md) |
| Need to detect and respond to security threats | [Security](/solutions/security.md) |
| Security logs are difficult to analyze or correlate | [Security](/solutions/security.md) |
| Compliance requires centralized security monitoring | [Security](/solutions/security.md) |

## Build your proof of concept

A successful PoC demonstrates clear value and helps you make an informed decision about adopting Elastic. Follow this framework to structure your evaluation.

Before starting technical work, establish what success looks like for your organization.

- What specific problem are you trying to solve?
- Who are the stakeholders who will evaluate the results?
- What metrics matter most to your organization?
- What would make this evaluation successful in the eyes of decision-makers?

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

### Suggested evaluation timeline

Most trials run for two weeks. Here's a suggested approach to maximize your evaluation time.

#### Week 1: Foundation and initial value

For the first week, focus on the following activities:

- Set up your deployment or project.
- Connect your first data sources.
- Demonstrate basic capabilities.
- Validate that Elastic can address your use case.

We recommend the following activities for each use case:

::::{tab-set}

:::{tab-item} Search

1. Review the [Search getting started guide](/solutions/search/get-started.md).
2. Ingest sample data or connect a data source.
3. Build basic search queries and test relevance.
4. Create simple visualizations of your data.

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
- Create dashboards that answer key stakeholder questions. Refer to [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md) for guidance.
- Focus on metrics that demonstrate clear business value. Use [Lens visualizations](/explore-analyze/visualize/lens.md) to highlight KPIs.
- Set up alerts for critical conditions or thresholds. Refer to [Alerting](/explore-analyze/alerts-cases.md) for configuration options.
- Compare results against your success criteria.
- Quantify time savings, efficiency gains, or risk reduction.

### Administrative considerations for evaluations

Beyond technical capabilities, consider these operational and business aspects during your evaluation.

::::{tab-set}

:::{tab-item} Understanding costs

Familiarize yourself with Elastic's pricing and billing model:

- [Billing documentation](/deploy-manage/cloud-organization/billing.md): Understand how Elastic Cloud billing works.
- [Deployment sizing](/deploy-manage/production-guidance.md): Learn about capacity planning for production.

Consider:

- What will your expected data volume be in production?
- How many users will need access?
- What retention requirements do you have?

:::

:::{tab-item} User and access management

If you're building a PoC to share with stakeholders:

- [Users and roles documentation](/deploy-manage/users-roles.md): Set up appropriate access controls.
- Create demo accounts for stakeholders with appropriate permissions.
- Consider role-based access for different organizational needs.

:::

:::{tab-item} Planning for production

Even during evaluation, think ahead to production requirements:

- [Production guidance](/deploy-manage/production-guidance.md): Best practices for production deployments.
- [High availability and disaster recovery](/deploy-manage/distributed-architecture.md): Understand resilience options.
- [Security best practices](/deploy-manage/security.md): Plan for secure production deployment.

:::

::::

## Measuring success

Document your results to demonstrate value to decision-makers.

### Quantitative metrics

Capture concrete numbers that demonstrate impact:

::::{tab-set}

:::{tab-item} Performance metrics

- Response times (search queries, dashboard load times).
- Data ingestion rates and volumes.
- Query performance at scale.

:::

:::{tab-item} Operational metrics

- Time saved on common tasks.
- Reduction in mean time to detect (MTTD) or mean time to respond (MTTR).
- Number of systems or data sources consolidated.

:::

:::{tab-item} Business impact metrics

- Cost savings from operational efficiency.
- Risk reduction from improved visibility or security.
- Productivity improvements from better search or monitoring.

:::

::::

### Qualitative assessment

Document the experience and capabilities:

- Ease of setup and configuration.
- Learning curve for your team.
- Quality of documentation and support resources.
- Fit with existing workflows and tools.

### Preparing your findings

Create a summary document or presentation that includes:

1. The challenge you set out to address.
2. What you evaluated and how.
3. Metrics and outcomes achieved during the PoC.
4. Screenshots, dashboards, or specific use cases.
5. Next steps and production readiness.

## Next steps after your trial

When you're ready to move beyond evaluation:

1. Based on your PoC, determine production sizing needs.
2. Review [license documentation](/deploy-manage/license.md) to choose the right tier.
3. If moving from trial to production, plan data migration and configuration transfer.
4. Discuss your evaluation results and production requirements [with the Elastic team](https://www.elastic.co/contact).

::::{note}
Depending on your organization's needs, conventions, and preferences, you might want to evaluate different deployment options. Elastic offers multiple deployment types including {{ecloud}}, {{ece}}, and {{eck}}. Explore the [deployment options](/deploy-manage/deploy.md) to find the best fit for your infrastructure and requirements.
::::

### Expanding your implementation

After proving value with one use case:

- Consider adding complementary solutions (for example, Observability + Security).
- Expand data sources and integrations.
- Implement advanced features ({{ml-cap}}, custom applications, APIs).
- Onboard additional teams and users.

### Getting help

Resources available to support your evaluation and production planning:

- **[Elastic Community forums](https://discuss.elastic.co/)**: Ask questions and learn from other users.
- **[Elastic training and certification](https://www.elastic.co/training)**: Develop team expertise with official courses.
- **[Professional services](https://www.elastic.co/services)**: Get expert help with implementation and optimization.
- **[Customer success stories](https://www.elastic.co/customers/success-stories)**: Learn from organizations with similar use cases.

## Additional resources

Continue exploring Elastic's capabilities:

- **[Solutions overview](/solutions/index.md)**: Deep dive into Search, Observability, and Security capabilities.
- **[Deploy and manage](/deploy-manage/index.md)**: Comprehensive deployment and operational guidance.
- **[Manage data](/manage-data/index.md)**: Learn about data ingestion, storage, and lifecycle management.
- **[Explore and analyze](/explore-analyze/index.md)**: Master {{kib}}'s visualization and analysis tools.

