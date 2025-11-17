---
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  stack:
description: Build a successful proof of concept with Elastic. Learn how to define success criteria, identify stakeholders, and measure results that matter.
---

# Proof of concept framework

A successful proof of concept (PoC) demonstrates clear value and helps you make an informed decision about adopting Elastic. This framework guides you through defining objectives, identifying stakeholders, setting success criteria, and evaluating results.

## What is a PoC?

A proof of concept is a small-scale implementation that:

- **Tests feasibility**: Confirms Elastic can solve your specific problem
- **Demonstrates value**: Shows measurable benefits to stakeholders
- **Identifies requirements**: Reveals what you need for full implementation
- **Reduces risk**: Validates technical and business assumptions before committing resources

**A PoC is not**:
- A full production deployment
- An excuse to test every feature
- A replacement for strategic planning
- Open-ended exploration without goals

## Step 1: Define your objectives

Start by clearly articulating what you want to achieve.

### Good objectives are SMART

- **Specific**: Clearly defined and unambiguous
- **Measurable**: Quantifiable with metrics
- **Achievable**: Realistic within trial timeframe
- **Relevant**: Aligned with business needs
- **Time-bound**: Completed within your trial period

### Example objectives by use case

:::{tabs}
::::{tab} Search

**Poor objective**: "Evaluate Elasticsearch for search."

**Good objectives**:
- "Reduce time to find customer support tickets from 5 minutes to under 30 seconds."
- "Enable full-text search across 100,000 product descriptions with sub-second response times."
- "Improve search relevance so that 80% of users find what they need in the first 3 results."
- "Centralize search across 5 different data silos into a single interface."

::::

::::{tab} Observability

**Poor objective**: "Try out Elastic Observability."

**Good objectives**:
- "Reduce mean time to detect (MTTD) application errors from 15 minutes to under 2 minutes."
- "Centralize logs from 10 microservices to reduce troubleshooting time by 50%."
- "Monitor infrastructure across 20 hosts to prevent unplanned downtime."
- "Trace user requests across 3 services to identify performance bottlenecks."

::::

::::{tab} Security

**Poor objective**: "See if Elastic Security works for us."

**Good objectives**:
- "Detect malware execution on endpoints within 30 seconds of occurrence."
- "Centralize security logs from 50 endpoints and 3 cloud services for correlation."
- "Reduce security incident investigation time from 2 hours to under 30 minutes."
- "Identify and alert on unusual authentication patterns across Azure AD and AWS."

::::
:::

### Template: Define your objective

Use this template to write your PoC objective:

> **Objective**: [Action verb] [specific capability] to [achieve result] for [target audience/system] within [timeframe].
>
> **Example**: Enable full-text search across customer support tickets to reduce search time from 5 minutes to 30 seconds for support agents within 2 weeks.

## Step 2: Identify stakeholders

Successful PoCs involve the right people at the right time.

### Key stakeholders to involve

| Role | Why they matter | When to involve |
|------|----------------|-----------------|
| **Executive sponsor** | Provides budget and strategic alignment | Before starting, after completion |
| **Technical lead** | Owns implementation and architecture | Throughout entire PoC |
| **End users** | Validate usability and provide feedback | Week 1 (testing), Week 2 (feedback) |
| **IT operations** | Address integration and security | Week 1 (planning), Week 2 (evaluation) |
| **Security team** | Review security and compliance requirements | Before starting, during evaluation |
| **Finance/Procurement** | Understand licensing and costs | After successful PoC |

### Stakeholder communication plan

Create a simple plan to keep stakeholders informed:

| Stakeholder | Communication method | Frequency |
|-------------|---------------------|-----------|
| Executive sponsor | Email updates | Weekly |
| Technical team | Slack/Teams channel | Daily (as needed) |
| End users | Demo sessions | Week 1, Week 2 |
| IT operations | Status meetings | Mid-trial, end-of-trial |

## Step 3: Define success criteria

Success criteria are measurable indicators that your PoC has achieved its objectives.

### Types of success criteria

1. **Technical criteria**: Can Elastic do what you need?
2. **Business criteria**: Does it deliver measurable value?
3. **User criteria**: Do users find it useful and usable?
4. **Operational criteria**: Can you manage and maintain it?

### Define criteria by use case

:::{tabs}
::::{tab} Search

**Technical criteria**:
- [ ] Index at least [X] documents successfully
- [ ] Achieve search response time under [X] milliseconds
- [ ] Support required search features (filters, autocomplete, facets)
- [ ] Handle expected query volume (queries per second)
- [ ] Integrate with [list data sources]

**Business criteria**:
- [ ] Reduce time to find information by [X]%
- [ ] Increase user satisfaction scores by [X] points
- [ ] Decrease number of "information not found" incidents by [X]%
- [ ] Save [X] hours per week across team

**User criteria**:
- [ ] Users find it easier than current solution
- [ ] Search results are relevant for [X]% of queries
- [ ] Users can complete common tasks without training

**Operational criteria**:
- [ ] Search indexes can be updated within [X] minutes
- [ ] System stays within allocated resource budget
- [ ] Integration with existing tools works reliably

::::

::::{tab} Observability

**Technical criteria**:
- [ ] Successfully ingest logs from [X] sources
- [ ] Collect metrics from [X] hosts/services
- [ ] Trace requests across [X] services with APM
- [ ] Set up [X] alerts with no false positives
- [ ] Achieve data ingestion latency under [X] seconds

**Business criteria**:
- [ ] Reduce mean time to detect (MTTD) by [X]%
- [ ] Reduce mean time to resolve (MTTR) by [X]%
- [ ] Prevent [X] hours of downtime
- [ ] Detect [X] issues proactively before user impact

**User criteria**:
- [ ] Engineers can troubleshoot issues faster
- [ ] Dashboards provide clear visibility into system health
- [ ] Alerts are actionable and timely

**Operational criteria**:
- [ ] Data retention meets compliance requirements
- [ ] System scales to handle [X] events per second
- [ ] Integration with incident management tools works

::::

::::{tab} Security

**Technical criteria**:
- [ ] Protect [X] endpoints with Elastic Defend
- [ ] Ingest security events from [X] sources
- [ ] Enable [X] detection rules successfully
- [ ] Achieve alert latency under [X] minutes
- [ ] Integrate with [list security tools]

**Business criteria**:
- [ ] Detect [X] security events that would have been missed
- [ ] Reduce incident investigation time by [X]%
- [ ] Increase threat detection coverage by [X]%
- [ ] Meet compliance requirements for [specific regulation]

**User criteria**:
- [ ] Analysts can investigate incidents more efficiently
- [ ] Alerts provide sufficient context for response
- [ ] Dashboards surface high-priority threats

**Operational criteria**:
- [ ] Security data retention meets compliance needs
- [ ] System integrates with existing SIEM/SOAR tools
- [ ] Endpoint deployment is manageable at scale

::::
:::

### Template: Success criteria checklist

Create your own success criteria using this template:

**Technical criteria**:
- [ ] [Specific technical capability or performance metric]
- [ ] [Integration requirement]
- [ ] [Scalability or reliability requirement]

**Business criteria**:
- [ ] [Quantifiable business outcome with target]
- [ ] [Cost savings or efficiency gain]
- [ ] [Risk reduction or compliance achievement]

**User criteria**:
- [ ] [User satisfaction or adoption metric]
- [ ] [Usability or ease-of-use measure]
- [ ] [Training or learning curve requirement]

**Operational criteria**:
- [ ] [Management or maintenance requirement]
- [ ] [Resource utilization metric]
- [ ] [Integration or compatibility need]

## Step 4: Create a timeline

Break your PoC into phases with clear milestones.

### Recommended timeline for trial period

| Phase | Duration | Key activities |
|-------|----------|----------------|
| **Planning** | 1-2 days | Define objectives, identify stakeholders, set success criteria |
| **Week 1: Foundation** | 3-5 days | Set up deployment, connect first data source, create basic dashboards |
| **Week 2: Expansion** | 3-5 days | Add data sources, refine dashboards, implement advanced features |
| **Evaluation** | 2-3 days | Measure results, prepare presentation, make recommendations |

### Adjust timeline based on complexity

- **Simple PoC** (single data source, basic features): 1 week
- **Standard PoC** (multiple data sources, dashboards, alerts): 2 weeks
- **Complex PoC** (many integrations, advanced features, multiple teams): 3-4 weeks

## Step 5: Measure results

At the end of your PoC, systematically evaluate whether you met your success criteria.

### Create a results scorecard

| Success criterion | Target | Actual | Met? | Notes |
|-------------------|--------|--------|------|-------|
| Search response time < 100ms | 100ms | 75ms | Yes | Exceeded expectations |
| Index 50,000 documents | 50,000 | 52,000 | Yes | All documents indexed successfully |
| Users find results in < 3 clicks | 3 clicks | 2.5 clicks | Yes | User feedback very positive |
| Integrate with 3 data sources | 3 sources | 3 sources | Yes | PostgreSQL, S3, and API |

### Gather qualitative feedback

In addition to metrics, collect feedback from stakeholders:

1. **User interviews**: Ask end users about their experience.
2. **Technical review**: Have your technical team assess architecture and implementation.
3. **Leadership feedback**: Present results to executive sponsor and get input.

**Sample interview questions**:
- What did you find most valuable about using Elastic?
- What challenges did you encounter?
- How does this compare to your current solution?
- Would you recommend moving forward with Elastic?
- What concerns do you have about production deployment?

## Step 6: Make your recommendation

Based on your results, make a clear recommendation with supporting evidence.

### Possible outcomes

#### 1. Strong success: Proceed to production

**Indicators**:
- Met or exceeded all critical success criteria
- Strong stakeholder support
- Clear ROI demonstrated
- Technical feasibility confirmed

**Recommendation**: Move forward with production planning and implementation.

**Next steps**:
- Finalize architecture and sizing
- Plan data migration and onboarding
- Obtain budget approval
- Begin team training

#### 2. Partial success: Proceed with adjustments

**Indicators**:
- Met most success criteria, but some gaps identified
- Stakeholder support with reservations
- ROI promising but needs refinement
- Technical concerns that can be addressed

**Recommendation**: Address identified gaps and move forward.

**Next steps**:
- Work with Elastic to resolve technical issues
- Refine PoC in specific areas
- Adjust implementation plan to address concerns
- Consider phased rollout

#### 3. Unsuccessful: Do not proceed

**Indicators**:
- Failed to meet critical success criteria
- Lack of stakeholder support
- No clear ROI
- Significant technical or operational blockers

**Recommendation**: Do not proceed at this time.

**Next steps**:
- Document lessons learned
- Identify root causes of failure
- Consider alternative solutions
- Revisit in the future if needs change

### Recommendation template

Use this template for your final recommendation:

> **Recommendation**: [Proceed / Proceed with adjustments / Do not proceed]
>
> **Summary**: [1-2 sentences on overall results]
>
> **Evidence**:
> - [Key success metric and result]
> - [Key success metric and result]
> - [Key success metric and result]
>
> **Business impact**: [Quantified ROI or business value]
>
> **Risks and mitigation**: [Any concerns and how to address them]
>
> **Next steps**: [Immediate actions to take]

## PoC best practices

### Do's

- **Start small**: Focus on one use case and a few data sources.
- **Use real data**: Demonstrate with actual organizational data, not samples.
- **Involve users early**: Get feedback from people who will use the system.
- **Document everything**: Keep notes on decisions, challenges, and results.
- **Set clear boundaries**: Define what's in scope and out of scope.
- **Communicate regularly**: Keep stakeholders informed of progress.
- **Plan for production**: Think about what full implementation would require.

### Don'ts

- **Don't boil the ocean**: Trying to do too much leads to incomplete results.
- **Don't skip planning**: Define objectives and success criteria upfront.
- **Don't work in isolation**: Involve stakeholders throughout the process.
- **Don't ignore challenges**: Document problems and work to resolve them.
- **Don't rush evaluation**: Take time to measure results properly.
- **Don't oversell**: Be honest about capabilities and limitations.
- **Don't forget operational needs**: Consider ongoing management and maintenance.

## Example PoC: E-commerce search

### Scenario

An e-commerce company wants to improve product search on their website.

### Objective

Enable full-text search across 100,000 products to reduce time-to-find from an average of 3 minutes to under 30 seconds, improving customer satisfaction and conversion rates.

### Success criteria

**Technical**:
- [ ] Index 100,000 products with complete metadata
- [ ] Search response time under 200ms at p95
- [ ] Support filters by category, price, brand, and availability
- [ ] Provide autocomplete suggestions

**Business**:
- [ ] Reduce average search time by 80%
- [ ] Increase search-to-purchase conversion by 10%
- [ ] Decrease "product not found" support tickets by 50%

**User**:
- [ ] Users rate search experience 4/5 or higher
- [ ] Relevant results appear in top 3 for 90% of searches

### Implementation

**Week 1**:
- Set up Elasticsearch serverless deployment
- Index product catalog from PostgreSQL database
- Create basic search interface
- Configure relevance tuning

**Week 2**:
- Add autocomplete and suggestions
- Implement faceted filtering
- Create analytics dashboard to track search metrics
- Conduct user testing with 10 internal users

### Results

| Criterion | Target | Result | Status |
|-----------|--------|--------|--------|
| Products indexed | 100,000 | 102,500 | Met |
| Response time | <200ms | 145ms | Met |
| Filters supported | 4 types | 5 types | Met |
| Search time reduction | 80% | 85% | Met |
| User satisfaction | 4/5 | 4.3/5 | Met |

### Recommendation

**Proceed to production**. The PoC exceeded expectations, demonstrating significant improvements in search speed, relevance, and user satisfaction. Estimated ROI: $150K annually from increased conversions and reduced support costs.

## Additional resources

- **[Trial getting started guide](/get-started/trial-getting-started.md)**: Overview of your trial journey.
- **[Week 1 guide](/get-started/trial-week-1.md)**: Set up and initial implementation.
- **[Week 2 guide](/get-started/trial-week-2.md)**: Expansion and evaluation.
- **[Production guidance](/deploy-manage/production-guidance/production-guidance.md)**: Planning for production deployment.

## Need help?

If you need assistance with your PoC:

- **Contact your trial specialist**: Get personalized guidance.
- **[Elastic Community](https://discuss.elastic.co/)**: Ask questions and learn from others.
- **[Elastic Professional Services](https://www.elastic.co/services)**: Get expert help with planning and implementation.

