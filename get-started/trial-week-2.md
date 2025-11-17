---
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  stack:
description: Week 2 of your Elastic trial. Expand your PoC, refine dashboards, measure success metrics, and prepare for team evaluation.
---

# Week 2: Expand and evaluate

In Week 2, you'll build on your foundation by expanding data sources, refining visualizations, and measuring success metrics. By the end of this week, you'll have a compelling PoC ready to demonstrate to stakeholders.

## Week 2 goals

By the end of this week, you'll have:

- Added 1-2 additional data sources.
- Created polished dashboards for stakeholders.
- Implemented advanced features (alerts, ML, custom queries).
- Measured and documented success metrics.
- Prepared your PoC presentation.
- Identified next steps and expansion plans.

**Estimated time**: 3-5 hours total.

::::::{stepper}

:::::{step} Expand your data sources

Now that you're comfortable with Elastic, add more data to demonstrate broader capabilities.

### Choose additional sources strategically

Select data sources that:

- Complement your Week 1 implementation.
- Address additional stakeholder needs.
- Demonstrate Elastic's integration capabilities.
- Provide more complete visibility.

### Add data sources

::::{tab-set}
:::{tab-item} Search

**Expand your search capabilities**:

1. **Add another data type**:
   - If you started with documents, add product catalogs or user data.
   - If you started with logs, add application events or metrics.
2. **Connect multiple sources**:
   - Go to **Management** → **Integrations**.
   - Add 1-2 more integrations relevant to your use case.
   - Create cross-index searches using multiple data views.
3. **Enrich your data**:
   - Use ingest pipelines to add calculated fields.
   - Go to **Management** → **Ingest Pipelines** → **Create pipeline**.
   - Add processors to enrich, transform, or parse data.

**Example expansions**:
- E-commerce: Add user behavior data alongside product catalog.
- Content management: Add user profiles alongside documents.
- Log analysis: Add application metrics alongside log data.

Refer to [data ingestion documentation](/manage-data/ingest.md) for advanced techniques.

:::

:::{tab-item} Observability

**Expand your observability coverage**:

1. **Add more hosts or services**:
   - Install Elastic Agent on 2-3 additional critical hosts.
   - Monitor a diverse set of services (web servers, databases, applications).
2. **Add APM to another application**:
   - If you haven't yet, instrument an application with APM.
   - Monitor both frontend (RUM) and backend services.
3. **Collect additional log sources**:
   - Add logs from databases, load balancers, or message queues.
   - Centralize logs from multiple applications.
4. **Enable uptime monitoring**:
   - Go to **Observability** → **Uptime**.
   - Add synthetic monitors to check endpoint availability.
   - Monitor APIs, websites, or internal services.

**Example expansions**:
- Monitor web tier, application tier, and database tier.
- Combine infrastructure metrics with application traces.
- Add cloud service metrics (AWS CloudWatch, Azure Monitor).

Refer to [observability get started](/solutions/observability/get-started.md) for more options.

:::

:::{tab-item} Security

**Expand your security coverage**:

1. **Add more endpoints**:
   - Deploy Elastic Defend to additional critical hosts.
   - Cover different OS types (Windows, macOS, Linux).
2. **Add cloud security logs**:
   - Connect AWS CloudTrail, Azure AD, or Google Cloud Audit Logs.
   - Go to **Management** → **Integrations** and search for your cloud provider.
3. **Add network or firewall logs**:
   - Ingest logs from firewalls, proxies, or DNS servers.
   - Provides network-level threat visibility.
4. **Enable additional security features**:
   - **Host risk scoring**: Identify high-risk hosts.
   - **User risk scoring**: Identify compromised accounts.
   - **Entity analytics**: Track user and host behavior.

**Example expansions**:
- Combine endpoint data with cloud security logs.
- Add authentication logs (Okta, Azure AD) for identity monitoring.
- Include firewall logs for network threat detection.

Refer to [security detection and alerting](/solutions/security/detect-and-alert.md) for integration options.

:::
::::

:::::

:::::{step} Refine dashboards and visualizations

Create polished, stakeholder-ready dashboards that tell a compelling story.

### Design principles for effective dashboards

- **Focus on outcomes**: Show business impact, not just technical metrics.
- **Use clear titles**: Make it obvious what each panel shows.
- **Highlight key metrics**: Use metric visualizations for important KPIs.
- **Show trends**: Include time-series charts to demonstrate changes.
- **Enable interactivity**: Add filters so viewers can explore.

### Create stakeholder dashboards

::::{tab-set}
:::{tab-item} Search

**Search performance dashboard**:

1. Go to **Analytics** → **Dashboards** → **Create dashboard**.
2. Add visualizations that show:
   - **Total searches performed** (metric visualization)
   - **Search latency over time** (line chart)
   - **Top search queries** (table or tag cloud)
   - **Search result relevance** (if tracking clicks or conversions)
   - **Data volume indexed** (metric or line chart)
3. Add markdown panels to provide context and insights.
4. Save as "Search Performance Overview".

**Business value dashboard**:

1. Create a dashboard focused on business outcomes:
   - User engagement metrics
   - Conversion rates (if applicable)
   - Content discovery improvements
   - Time saved on search tasks
2. Include before/after comparisons if you have baseline data.

:::

:::{tab-item} Observability

**Service health dashboard**:

1. Go to **Analytics** → **Dashboards** → **Create dashboard**.
2. Add visualizations that show:
   - **Service uptime percentage** (metric visualization)
   - **Error rate over time** (line chart with threshold lines)
   - **Response time trends** (line chart showing p50, p95, p99)
   - **Active services and hosts** (metric counts)
   - **Top errors by service** (table)
3. Use color coding: green for healthy, yellow for warning, red for critical.
4. Save as "Service Health Overview".

**Incident response dashboard**:

1. Create a dashboard for troubleshooting:
   - Recent errors and warnings (data table)
   - Resource utilization (CPU, memory, disk)
   - Network traffic patterns
   - APM transaction traces (if available)
2. Add time controls to easily adjust timeframes during incidents.

**Business value dashboard**:

1. Create a dashboard showing:
   - Mean time to detect (MTTD) improvements
   - Mean time to resolve (MTTR) reductions
   - Uptime improvements
   - Cost savings from faster incident resolution

:::

:::{tab-item} Security

**Security operations dashboard**:

1. Go to **Analytics** → **Dashboards** → **Create dashboard**.
2. Add visualizations that show:
   - **Alert count by severity** (metric or bar chart)
   - **Alert trends over time** (line chart)
   - **Top alerts by rule name** (table)
   - **High-risk hosts and users** (tables with risk scores)
   - **Security event timeline** (area chart by event type)
3. Save as "Security Operations Overview".

**Threat detection dashboard**:

1. Create a dashboard focused on threats:
   - Recent high-severity alerts
   - Suspicious process executions
   - Unusual network connections
   - Failed authentication attempts
   - Malware detections

**Compliance dashboard**:

1. Create a dashboard for compliance reporting:
   - Security events by type
   - User activity logs
   - Privileged access events
   - File and system changes
2. Useful for demonstrating audit capabilities.

:::
::::

### Dashboard best practices

1. **Use Elastic's visualize options**:
   - **Lens**: Intuitive drag-and-drop for most visualizations.
   - **TSVB**: Time-series data with advanced calculations.
   - **Markdown**: Add explanatory text and links.
2. **Add filters**: Let viewers filter by time, host, service, or other dimensions.
3. **Use drill-downs**: Link visualizations to detailed views.
4. **Set refresh intervals**: Auto-refresh dashboards for live monitoring.
5. **Apply consistent styling**: Use the same color schemes and fonts.

Refer to [dashboard documentation](/explore-analyze/dashboards.md) for advanced features.

:::::

:::::{step} Implement advanced features

Demonstrate Elastic's powerful capabilities with advanced features.

### Choose features based on your use case

::::{tab-set}
:::{tab-item} Search

**Implement these advanced search features**:

1. **Relevance tuning**:
   - Go to **Search** → **Content** → **Elasticsearch indices**.
   - Experiment with boosting fields to improve search relevance.
   - Test different analyzer configurations.
2. **Search suggestions (autocomplete)**:
   - Add completion suggesters to your index mapping.
   - Refer to the Elasticsearch documentation for suggesters.
3. **Semantic search** (if on Elastic 8.8+):
   - Enable vector search for AI-powered semantic matching.
   - Refer to [semantic search documentation](/solutions/search/semantic-search.md).
4. **Saved searches**:
   - Create and save complex search queries for reuse.
   - Share searches with team members.

:::

:::{tab-item} Observability

**Implement these advanced observability features**:

1. **Service-level objectives (SLOs)**:
   - Go to **Observability** → **SLOs**.
   - Define SLOs for critical services (e.g., "99.9% uptime", "p95 latency < 200ms").
   - Track SLO compliance over time.
2. **Anomaly detection**:
   - Go to **Observability** → **AIOps** → **Anomaly detection**.
   - Create ML jobs to detect unusual patterns in metrics or logs.
   - Receive alerts when anomalies occur.
3. **Service maps**:
   - Go to **Observability** → **Applications** → **Service Map** (requires APM).
   - Visualize dependencies between services.
   - Identify performance bottlenecks.
4. **Log correlation**:
   - Link logs to traces and metrics for full context.
   - Use correlation IDs to track requests across services.

Refer to [observability features](/solutions/observability.md) for detailed guides.

:::

:::{tab-item} Security

**Implement these advanced security features**:

1. **Entity analytics**:
   - Go to **Security** → **Manage** → **Entity risk score**.
   - Enable entity analytics to calculate risk scores for hosts and users.
   - Alert on high-risk entities.
2. **Machine learning detection rules**:
   - Go to **Security** → **Rules** → **Detection rules (SIEM)**.
   - Enable ML-based rules for anomaly detection:
     - Unusual network activity
     - Suspicious login behavior
     - Anomalous process execution
3. **Case management**:
   - Go to **Security** → **Cases**.
   - Create a case from an alert.
   - Add notes, tasks, and track investigation progress.
4. **Threat intelligence**:
   - Go to **Security** → **Explore** → **Threat Intelligence**.
   - Import threat intel feeds to identify known bad indicators.

Refer to [security capabilities](/solutions/security.md) for more features.

:::
::::

:::::

:::::{step} Measure and document success metrics

Quantify the value of your PoC with concrete metrics.

### Define success metrics

Refer to your [PoC framework](/get-started/trial-poc-framework.md) for the success criteria you defined. Now it's time to measure them.

### Common metrics by use case

::::{tab-set}
:::{tab-item} Search

**Quantitative metrics**:
- Search queries processed per day.
- Average search response time.
- Number of documents indexed.
- Search relevance improvements (click-through rates, if available).
- Time saved on data discovery tasks.

**Qualitative metrics**:
- User satisfaction with search results.
- Ease of finding relevant information.
- Reduced time spent searching across multiple systems.

**ROI indicators**:
- Hours saved per employee per week.
- Increased productivity in finding information.
- Reduced time to answer customer queries.

:::

:::{tab-item} Observability

**Quantitative metrics**:
- Number of services and hosts monitored.
- Number of log entries ingested per day.
- Alert response time (time from alert to acknowledgment).
- Mean time to detect (MTTD) issues.
- Mean time to resolve (MTTR) incidents.

**Qualitative metrics**:
- Visibility into system health.
- Ease of troubleshooting.
- Confidence in meeting SLAs.

**ROI indicators**:
- Downtime reduced by X hours per month.
- Incidents detected Y minutes faster.
- Cost savings from faster incident resolution.

:::

:::{tab-item} Security

**Quantitative metrics**:
- Number of endpoints protected.
- Security events ingested per day.
- Alerts generated and resolved.
- Mean time to detect (MTTD) threats.
- Mean time to respond (MTTR) to incidents.

**Qualitative metrics**:
- Improved visibility into security posture.
- Confidence in threat detection capabilities.
- Streamlined incident investigation.

**ROI indicators**:
- Threats detected that would have been missed.
- Time saved on manual log analysis.
- Potential breach costs avoided.

:::
::::

### Document your findings

Create a summary document with:

1. **Metrics dashboard**: Screenshot or link to key metrics.
2. **Success criteria met**: Checklist showing which criteria you achieved.
3. **Insights gained**: What you learned about your systems, data, or users.
4. **Problems solved**: Specific issues that Elastic helped you address.
5. **Time and cost savings**: Quantify business value.

:::::

:::::{step} Prepare your PoC presentation

You've built a compelling PoC — now it's time to present it effectively.

### Create a presentation structure

1. **Executive summary** (1-2 slides):
   - Problem statement
   - Solution overview
   - Key results and ROI
2. **Use case overview** (2-3 slides):
   - Which Elastic solution you evaluated
   - Data sources connected
   - Timeline of implementation
3. **Live demo** (5-10 minutes):
   - Show your dashboards in action
   - Demonstrate key features
   - Walk through a real-world scenario
4. **Results and metrics** (2-3 slides):
   - Success criteria met
   - Quantitative results
   - Qualitative benefits
5. **Next steps and recommendations** (1-2 slides):
   - Expansion opportunities
   - Pricing and licensing options
   - Implementation timeline

### Tips for an effective demo

- **Tell a story**: Walk through a real problem and how Elastic solves it.
- **Keep it focused**: Show 2-3 key capabilities, not everything.
- **Use real data**: Demonstrate with your actual data, not samples.
- **Prepare for questions**: Anticipate technical and business questions.
- **Have a backup plan**: Record a video in case of technical issues.

### Presenting to different audiences

| Audience | Focus on |
|----------|----------|
| **Executives** | ROI, cost savings, business impact, time to value |
| **IT leadership** | Scalability, integration, security, operational efficiency |
| **Technical teams** | Features, APIs, ease of use, troubleshooting capabilities |
| **Security teams** | Threat detection, compliance, incident response |

:::::

:::::{step} Plan your expansion

Identify what comes next after your successful PoC.

### Expansion options

1. Scale horizontally: Add more data sources, hosts, or users.
2. Scale vertically: Implement advanced features (ML, custom apps, APIs).
3. Add use cases: Combine search, observability, and security.
4. Production deployment: Move from trial to production-ready configuration.
5. Team onboarding: Train additional users and stakeholders.

### Next steps checklist

Create a plan for moving forward:

- [ ] Determine production data volume and retention needs
- [ ] Estimate licensing costs based on usage
- [ ] Identify team members who need training
- [ ] Plan data source migration and onboarding
- [ ] Set up production deployment architecture
- [ ] Define ongoing maintenance and support processes

### Getting help with production planning

- **[Production guidance](/deploy-manage/production-guidance.md)**: Best practices for production deployments and sizing.
- **[Contact sales](https://www.elastic.co/contact)**: Discuss licensing and support options.

:::::

::::::

## Week 2 checklist

Before completing your trial, ensure you've:

- Added 1-2 additional data sources.
- Created polished, stakeholder-ready dashboards.
- Implemented at least one advanced feature.
- Measured and documented success metrics.
- Prepared a presentation or demo.
- Identified next steps and expansion plans.

## Congratulations!

You've completed a comprehensive Elastic trial and built a meaningful proof of concept. You now have:

- Real data flowing into Elastic.
- Dashboards demonstrating value.
- Measurable success metrics.
- A clear understanding of Elastic's capabilities.
- A plan for moving forward.

## Additional resources

- **[PoC framework](/get-started/trial-poc-framework.md)**: Review your success criteria and evaluation approach.
- **[Solutions documentation](/solutions/index.md)**: Dive deeper into your chosen use case.
- **[Community forums](https://discuss.elastic.co/)**: Connect with other Elastic users.
- **[Elastic training](https://www.elastic.co/training)**: Continue learning with courses and certifications.

## Need help?

If you have questions or need assistance:

- Contact your trial specialist: Reach out for personalized guidance.
- Schedule a follow-up: Arrange a technical review with Elastic experts.
- Join the community: Ask questions in the [Elastic forums](https://discuss.elastic.co/).

