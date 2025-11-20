---
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  stack:
description: Build a successful proof of concept during your Elastic trial. Learn how to define success criteria, choose the right deployment and use case, measure results, and prepare for production.
---

# Evaluate Elastic

If you're evaluating Elastic during a trial, this guide helps you build a meaningful proof of concept (PoC) that demonstrates clear value to your organization. Rather than prescribing specific technical steps, this guide focuses on the evaluation process itself, helping you make strategic decisions and measure success.

## What's included in your trial

Your Elastic trial gives you full access to explore our platform's capabilities:

- All features available across [Search](/solutions/search.md), [{{observability}}](/solutions/observability.md), and [Security](/solutions/security.md) solutions.
- Choice between {{serverless-full}} and {{ech}} deployment types.
- Access to integrations, {{ml-features}}, and advanced analytics.
- Support resources including documentation, community forums, and technical guidance.

:::{note}
During the trial, deployments have size and capacity limitations. You can increase deployment size after adding billing details.
:::

## Trial limitations

While your trial includes full feature access, be aware of these limitations:

- Trial duration varies by deployment type:
  - {{serverless-short}} projects: 14-day free trial (refer to [trial information](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial))
  - Self-managed clusters: 30-day trial (refer to [license documentation](/deploy-manage/license.md))
  - Cloud deployments through marketplaces may have different durations (refer to [subscribe from a marketplace](/deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md))
- Data ingested during the trial remains accessible, but consider your evaluation timeline.
- Trial deployments have size and capacity limitations compared to production environments.

For detailed information about features and licensing:

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
- Ideal for focusing on capabilities rather than infrastructure management.

:::

:::{tab-item} Elastic Cloud Hosted

- More control over cluster configuration and sizing.
- Traditional {{es}} architecture.
- Ideal for evaluating specific infrastructure requirements or migrating from self-managed deployments.

:::

::::

For detailed comparisons:

- [Deployment comparison](/deploy-manage/deploy/deployment-comparison.md): Side-by-side feature and capability comparison.
- [Differences from other {{es}} offerings](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand how {{ecloud}} differs from self-managed deployments.

:::{tip}
For most evaluations, {{serverless-short}} provides the fastest path to demonstrating value. You can always explore hosted options later or migrate to production with different requirements.
:::

### Identify your primary use case

Choose one use case to focus your initial evaluation. You can always expand to additional use cases after establishing initial success.

| Your challenge | Primary use case |
|----------------|-----------------|
| Users struggle to find relevant information across systems | **Search** |
| Need to build fast, relevant search experiences for applications or websites | **Search** |
| Limited visibility into application performance or system health | **Observability** |
| Slow incident response and troubleshooting | **Observability** |
| Need to detect and respond to security threats | **Security** |
| Security logs are difficult to analyze or correlate | **Security** |
| Compliance requires centralized security monitoring | **Security** |

To learn more about each solution, refer to the following sections:

- [Solutions overview](/solutions/index.md): Learn about the different solutions and use cases.
- [Search solutions](/solutions/search.md): Enterprise search, website search, and search-powered applications.
- [Observability solutions](/solutions/observability.md): APM, infrastructure monitoring, log management, and synthetic monitoring.
- [Security solutions](/solutions/security.md): SIEM, endpoint security, threat detection, and incident response.

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

- Set up your deployment.
- Connect your first data sources.
- Demonstrate basic capabilities.
- Validate that Elastic can address your use case.

The following activities are recommended for each use case:

::::{tab-set}

:::{tab-item} Search

1. Review [Search getting started guide](/solutions/search/get-started.md).
2. Ingest sample data or connect a data source.
3. Build basic search queries and test relevance.
4. Create simple visualizations of your data.

:::

:::{tab-item} Observability

1. Review [Observability getting started guide](/solutions/observability/get-started.md).
2. Deploy Elastic Agent to monitor 1-2 hosts or services.
3. Collect logs from a critical application.
4. Explore metrics and logs in Kibana.

:::

:::{tab-item} Security

1. Review [Security getting started guide](/solutions/security/get-started.md).
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

- Add 2-3 additional data sources relevant to your use case. Refer to [Fleet integrations](/reference/fleet/manage-integrations.md) for available integrations.
- Create dashboards that answer key stakeholder questions. Refer to [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md) for guidance.
- Focus on metrics that demonstrate clear business value. Use [Lens visualizations](/explore-analyze/visualize/lens.md) to highlight KPIs.
- Set up alerts for critical conditions or thresholds. Refer to [Alerting](/explore-analyze/alerts-cases.md) for configuration options.
- Compare results against your success criteria.
- Quantify time savings, efficiency gains, or risk reduction.

### Administrative considerations for evaluations

Beyond technical capabilities, consider these operational and business aspects during your evaluation.

#### Understanding costs

Familiarize yourself with Elastic's pricing and billing model:

- [Billing documentation](/deploy-manage/cloud-organization/billing.md): Understand how Elastic Cloud billing works.
- [Deployment sizing](/deploy-manage/production-guidance.md): Learn about capacity planning for production.

Consider:

- What will your expected data volume be in production?
- How many users will need access?
- What retention requirements do you have?

#### User and access management

If you're building a PoC to share with stakeholders:

- [Users and roles documentation](/deploy-manage/users-roles.md): Set up appropriate access controls.
- Create demo accounts for stakeholders with appropriate permissions.
- Consider role-based access for different organizational needs.

#### Planning for production

Even during evaluation, think ahead to production requirements:

- [Production guidance](/deploy-manage/production-guidance.md): Best practices for production deployments.
- [High availability and disaster recovery](/deploy-manage/distributed-architecture.md): Understand resilience options.
- [Security best practices](/deploy-manage/security.md): Plan for secure production deployment.

## Measuring success

Document your results to demonstrate value to decision-makers.

### Quantitative metrics

Capture concrete numbers that demonstrate impact:

**Performance metrics**:
- Response times (search queries, dashboard load times).
- Data ingestion rates and volumes.
- Query performance at scale.

**Operational metrics**:
- Time saved on common tasks.
- Reduction in mean time to detect (MTTD) or mean time to respond (MTTR).
- Number of systems or data sources consolidated.

**Business impact metrics**:
- Cost savings from operational efficiency.
- Risk reduction from improved visibility or security.
- Productivity improvements from better search or monitoring.

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

1.Based on your PoC, determine production sizing needs.
2. Review [license documentation](/deploy-manage/license.md) to choose the right tier.
3. If moving from trial to production, plan data migration and configuration transfer.
4. Discuss your evaluation results and production requirements with the Elastic team.

### Expanding your implementation

After proving value with one use case:

- Consider adding complementary solutions (for example, Observability + Security).
- Expand data sources and integrations.
- Implement advanced features (ML, custom applications, APIs).
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
- **[Deploy and manage guide](/deploy-manage/index.md)**: Comprehensive deployment and operational guidance.
- **[Manage data guide](/manage-data/index.md)**: Learn about data ingestion, storage, and lifecycle management.
- **[Explore and analyze guide](/explore-analyze/index.md)**: Master Kibana's visualization and analysis tools.

