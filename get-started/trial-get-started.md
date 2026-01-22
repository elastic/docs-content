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

To make the most of your free 14-day {{ecloud}} trial, set up your top use case, ingest real data, test features, and gather the evidence you need to determine if Elastic is right for your organization.

## What you'll accomplish

By the end of the trial, you'll know whether Elastic solves your specific problem and what it costs at your scale.

**Time commitment**: 2-3 hours of hands-on work, plus 3-6 hours of user testing spread across the 14 days.

---

## Choose your evaluation path

Select the evaluation path for your top use case.

| Path | Choose this if... | Success metric |
|------|------------------|----------------|
| **Search** | Your users are unable to find information in documents, databases, or knowledge bases | Search result relevance and speed |
| **Observability** | You need to monitor applications, troubleshoot incidents faster, or reduce mean time to resolution | Time to identify root cause |
| **Security** | You need threat detection, security monitoring, or compliance visibility | Time to detect and respond to threats |

**Why one path?** With 14 days, focusing on one use case gives you actionable results. Evaluating everything superficially won't help you make a decision.

---

## Prerequisites

Gather these before starting:

- [ ] Production-representative data source (logs, documents, or security events)
- [ ] 2-3 end users who will test daily workflows
- [ ] Baseline metric for comparison (e.g., current time to resolve incidents)

---

## Day 1: Initial setup

**Goal**: Get Elastic running and ingest your first data

**Time**: 2 hours

### Start your trial

1. Go to [cloud.elastic.co](https://cloud.elastic.co) and create an account
2. No credit card required for the trial
3. Select **Serverless** deployment type
   - Fully managed with automatic scaling
   - Recommended for trials—less configuration overhead
4. Choose your cloud provider (AWS, Google Cloud, or Azure)
5. Click **Create deployment**

Your deployment will be ready in under 5 minutes.

### Access Kibana

1. From your deployment page, click **Open Kibana**
2. Log in with your credentials
3. You'll see the Kibana home page with setup options

### Ingest your first data

Choose the section for your evaluation path:

#### Observability path

1. In Kibana, click **Add integrations**
2. Search for your technology stack:
   - Application servers (Nginx, Apache, Tomcat)
   - Container platforms (Kubernetes, Docker)
   - Cloud providers (AWS, Azure, GCP)
3. Select your integration and click **Add integration**
4. Follow the installation instructions:
   - Copy the provided command
   - Run it on your target system
   - Data appears in Kibana within 2-3 minutes
5. Recommended first integrations:
   - System metrics (CPU, memory, disk)
   - Application logs from your primary service

#### Search path

1. In Kibana, click **Create Elasticsearch index**
2. Choose the API method (REST API or client library)
3. Use the provided code sample to index documents:
   ```bash
   # Example using curl
   curl -X POST "https://your-deployment:9200/documents/_doc" \
     -H 'Content-Type: application/json' \
     -d '{"title": "Sample", "content": "Your content here"}'
   ```
4. Start with 100-500 sample documents from your actual data
5. Supported formats: JSON, CSV, or use connectors for databases

#### Security path

1. In Kibana, click **Add integrations**
2. Install one of these:
   - **Elastic Defend** for endpoint security
   - **Network Packet Capture** for network monitoring
   - Your existing security tool (if supported)
3. Follow the agent installation wizard
4. Deploy to 5-10 representative endpoints or network segments
5. Verify data flow in Security → Dashboards

### Verify data ingestion

1. Navigate to **Discover** in the left menu
2. Select the appropriate data view (created automatically)
3. Confirm you see your data in the timeline
4. Filter by a known field value to verify accuracy

**Checkpoint**: You have data flowing into Elastic. If you don't see data, check the integration status in **Fleet** or consult the [troubleshooting guide](https://www.elastic.co/guide/en/fleet/current/fleet-troubleshooting.html).

---

## Days 2-3: Build your core workflow

**Goal**: Create the dashboard or search experience you'll use daily

**Time**: 3-4 hours

### Observability: Create monitoring dashboards

1. Go to **Dashboards** → **Create dashboard**
2. Click **Create visualization**
3. Add these three core visualizations:

**Response time visualization**:
- Visualization type: Line chart
- Metrics: Average of `transaction.duration.us` 
- Breakdown: `service.name`
- Time range: Last 24 hours

**Error rate visualization**:
- Visualization type: Metric
- Formula: `count(error) / count(transaction)`
- Color threshold: >5% shows red

**Slow requests table**:
- Visualization type: Table
- Columns: Service, Endpoint, Duration
- Sort by: Duration descending
- Rows: Top 10

4. Save your dashboard as "Production Monitoring"
5. Set auto-refresh to 1 minute

**These three visualizations cover the majority of daily monitoring tasks.** You can add more later, but this is sufficient for evaluation.

### Search: Test query relevance

1. Navigate to **Discover**
2. Select your documents index
3. Run 10 realistic queries your users would perform:
   - Use the search bar at the top
   - Try both simple keywords and multi-word phrases
   - Test queries you know should return specific documents
4. For each query, record:
   - Did the correct document appear in top 5 results?
   - Search response time
   - Any missing or unexpected results
5. Adjust relevance (optional):
   - Go to **Search → Indices → [your index]**
   - Click **Mappings** to adjust field weights
   - Mark key fields as `searchable` with higher boost values

**Focus on whether users can find what they need**, not on perfect optimization.

### Security: Build your monitoring view

1. Navigate to **Security** → **Dashboards**
2. Click **Create dashboard**
3. Add these essential visualizations:

**Authentication failures**:
- Visualization type: Bar chart
- Count of `event.outcome: failure`
- Breakdown by: `user.name` and `source.ip`

**Geographic connections**:
- Visualization type: Map
- Plot: `source.ip` geocoded locations
- Size by: Event count

**Security events timeline**:
- Visualization type: Area chart
- Count of all security events
- Breakdown by: `event.category`

4. Save as "Security Operations Dashboard"

### Set up your first alert

1. Go to **Stack Management** → **Rules and Connectors**
2. Click **Create rule**
3. Configure based on your path:

**Observability alert**:
- Rule type: Threshold
- Condition: Error rate > 5% for 5 minutes
- Action: Send email notification

**Security alert**:
- Rule type: Threshold  
- Condition: Failed logins > 5 from same IP in 5 minutes
- Action: Send email notification

4. Configure email connector if not already set up
5. Test by triggering the condition manually

**Note**: Start with simple threshold alerts. Machine learning anomaly detection requires 2+ weeks of baseline data.

**Checkpoint**: You have a working dashboard or search interface. Test it with your own queries or by reviewing yesterday's activity.

---

## Days 4-6: User validation testing

**Goal**: Confirm real users can complete actual tasks

**Time**: 1 hour setup + 3-6 hours of user testing

### Prepare user accounts

1. Go to **Stack Management** → **Users**
2. Create accounts for 2-3 pilot users
3. Assign the `editor` role:
   - Can view and create content
   - Cannot delete indices or change security settings
4. Send users their login credentials and the Kibana URL

### Design daily test tasks

Assign one task per day for three consecutive days. Choose from your evaluation path:

**Observability tasks**:
- Day 1: "Identify which service caused the latency spike at 2pm yesterday"
- Day 2: "Find all errors from the checkout service in the last 6 hours"
- Day 3: "Compare this week's response times to last week for the API service"

**Search tasks**:
- Day 1: "Find the product specification document for [specific product]"
- Day 2: "Find all customer complaints mentioning [specific issue]"
- Day 3: "Locate the contract with [specific terms] signed in [date range]"

**Security tasks**:
- Day 1: "Investigate the failed login alert from this morning"
- Day 2: "Find all network connections from [suspicious IP]"
- Day 3: "List all file modifications on endpoint [hostname] yesterday"

### Collect task performance data

After each task, record:
- Time to complete (in minutes)
- Did they find the answer?
- Difficulty rating (1-5 scale)

Compare against their current tool using the same tasks.

### Gather qualitative feedback

Ask users:
- "What was easier than your current tool?"
- "What was harder or confusing?"
- "Would you want to use this daily?"

**Three users completing three tasks gives you nine data points**—enough to identify patterns without extensive analysis.

**Checkpoint**: You know whether actual users can successfully accomplish real tasks. This is your strongest evaluation signal.

---

## Days 7-9: Scale and stress testing

**Goal**: Verify Elastic performs at your production scale

**Time**: 3-4 hours

### Increase data volume

Expand to 3x your initial data volume:

**Observability**:
- Add integrations for 2-3 additional services
- Increase log levels to capture more detail
- Add infrastructure metrics from more hosts

**Search**:
- Index 10,000+ additional documents
- Include documents of varying sizes (1KB to 5MB)
- Add multiple document types if applicable

**Security**:
- Deploy agents to 10-20 more endpoints
- Enable additional log sources (DNS, firewall)
- Increase event capture settings

### Monitor performance under load

1. Open your dashboard and refresh continuously
2. Observe these metrics:
   - Query response time
   - Dashboard load time  
   - Data ingestion lag (check in **Stack Monitoring**)
3. Expected behavior:
   - Serverless automatically scales compute resources
   - Queries should remain under 2-3 seconds
   - No dropped data during ingestion spikes

If performance degrades significantly, this indicates you may need a Hosted deployment with larger instance sizes.

### Test alert reliability

Trigger your alert conditions 10+ times in rapid succession:

1. Generate events that meet your alert threshold
2. Verify you receive notifications
3. Check if alerts are properly grouped (not spamming individual emails)
4. Confirm alert recovery when conditions clear

If alerts spam you, configure throttling:
- Edit your rule
- Set **Notify** to "On status changes" instead of "Every time alert is active"

### Project production costs

1. Go to **Billing** → **Usage** in your Cloud console
2. Note these numbers from your trial:
   - Data ingested (GB)
   - Storage used (GB)
   - Compute hours
3. Calculate monthly costs:
   - Multiply trial numbers by (30 days / days tested)
   - Apply Elastic's pricing for your chosen tier
   - Typical costs: $0.10-0.20 per GB ingested, plus storage and compute

**Example calculation**:
```
Trial: 50GB ingested over 7 days = ~215GB/month
Standard tier: $0.15/GB = $32/month ingestion
Storage: 200GB × $0.125/GB = $25/month  
Serverless compute: ~$40/month (auto-scaled)
Total: ~$97/month
```

Visit the [Elastic pricing page](https://www.elastic.co/pricing) for current rates.

**Checkpoint**: You know whether Elastic handles your data volume and have a realistic cost estimate.

---

## Days 10-11: Gap analysis

**Goal**: Identify what works, what doesn't, and what's uncertain

**Time**: 2-3 hours

### Document successes

List three specific improvements Elastic provides:

**Use measurable outcomes**:
- ✓ "Reduced incident investigation time from 45 minutes to 8 minutes"
- ✗ "Better observability"

**Examples to look for**:
- Faster searches or queries
- Consolidated multiple tools into one
- Automated detection of issues you manually tracked
- Improved visibility into blind spots

### Document limitations

List three things that don't work well or are missing:

**Be specific about the impact**:
- Missing integration with [specific tool]
- No built-in support for [specific data format]
- Learning curve for KQL (Kibana Query Language)
- Lacks [feature] available in current tool

**Every tool has tradeoffs.** Understanding these now prevents surprises after purchase.

### Document open questions

List 2-3 questions you cannot answer from the trial:

**Common questions**:
- SSO integration compatibility
- Data residency requirements (EU, US regions)
- API rate limits at production scale
- Support response times and SLAs
- Historical data retention costs
- Disaster recovery procedures

**These questions are for Elastic sales**, not for trial research. Write them down now, ask on Day 12.

**Checkpoint**: You have a clear picture of Elastic's fit for your organization, including both strengths and weaknesses.

---

## Days 12-14: Decision and next steps

**Goal**: Make a purchase decision backed by data

**Time**: 3-4 hours

### Calculate ROI

Use this simple formula:

```
Monthly value = (Time saved per task × Tasks per month × Hourly rate)
Monthly cost = (Your projection from Day 9)
Monthly ROI = Monthly value - Monthly cost
```

**Example**:
```
Time saved: 20 minutes per incident investigation
Incidents: 30 per month  
Time saved total: 10 hours/month
Engineer hourly rate: $75
Monthly value: 10 × $75 = $750

Monthly Elastic cost: $200
Monthly ROI: $750 - $200 = $550 positive
```

If ROI is negative, Elastic may not be the right fit—or you need to find a higher-impact use case.

### Answer the decision question

**"If the trial ended today, would I pay for this?"**

- **Yes** → Proceed to subscription
- **No** → Document why and consider alternatives  
- **Maybe** → Contact Elastic sales with your open questions

### Subscribe (if proceeding)

1. In your Cloud console, click **Subscribe**
2. Select subscription tier:
   - **Standard**: Core functionality, suitable for most teams
   - **Gold**: Adds machine learning, canvas, advanced alerting
   - **Platinum/Enterprise**: SSO, RBAC, cross-cluster features
3. Choose billing:
   - **Monthly**: Higher cost but flexibility to cancel
   - **Annual**: 15-20% discount, requires commitment
4. **Recommendation**: Start with Standard + Monthly
   - Upgrade tier when you need specific features
   - Switch to annual after 3-6 months of validated usage

Your trial data and configuration automatically transfer to the paid subscription.

### Contact Elastic (if unsure)

Email your Day 11 open questions to Elastic sales or schedule a call:
- Explain your use case and trial results
- Share your ROI calculation
- Ask about extended evaluation if needed
- Discuss volume discounts or custom terms

### Document your evaluation

Create a brief summary for stakeholders:

**One-page format**:
1. Use case evaluated
2. Key metric improvement (with numbers)
3. User feedback summary
4. Monthly cost projection
5. ROI calculation
6. Recommendation (buy, don't buy, need more time)

This documentation helps you justify the decision and serves as a baseline for measuring post-purchase success.

**Checkpoint**: You've made an informed decision with supporting data.

---

## Understanding key tradeoffs

### Serverless vs. Hosted deployments

| Aspect | Serverless | Hosted |
|--------|-----------|--------|
| Management | Fully managed by Elastic | You manage versions and sizing |
| Scaling | Automatic | Manual configuration required |
| Cost model | Pay per use | Reserved capacity |
| Version control | Always latest | You choose version |
| **Best for trials** | ✓ Recommended | Only if specific requirements |

**Recommendation**: Use Serverless for trials. It reduces configuration overhead and automatically scales during testing.

### Subscription tier selection

| Tier | Includes | Choose this if... |
|------|----------|------------------|
| **Standard** | Core search, observability, and security | You need fundamental capabilities |
| **Gold** | + ML anomaly detection, Canvas | You need predictive alerting |
| **Platinum** | + SSO, field-level security | You have compliance requirements |
| **Enterprise** | + Cross-cluster search, support | You have multi-region deployments |

**Recommendation**: Start with Standard. Upgrade when you encounter a specific missing feature, not preemptively.

### Monthly vs. annual billing

| Option | Cost | Flexibility | Best for |
|--------|------|-------------|----------|
| **Monthly** | 15-20% higher | Cancel anytime | First 3-6 months |
| **Annual** | 15-20% discount | 12-month commitment | After validation period |

**Recommendation**: Pay the premium for monthly initially. Lock in annual pricing once you've validated production usage.

---

## What to skip during trials

These Elastic features are valuable but not essential for evaluation:

- **Canvas presentations**: Use existing reporting tools during trials
- **Machine Learning**: Requires 2+ weeks of data to train baselines
- **Cross-cluster search**: Only needed with multiple deployments  
- **Advanced ILM policies**: Store everything in hot tier during trials
- **Field-level security**: Role-based access is sufficient for evaluation
- **Custom deployment templates**: Use default configurations

**Focus on core functionality first.** Advanced features can be evaluated after purchase.

---

## After the trial ends

### If you're purchasing

1. Click **Subscribe** in your deployment dashboard
2. All data and configurations transfer automatically
3. No migration or re-setup required
4. Access continues uninterrupted

### If you're not purchasing

1. You have a 30-day grace period before data deletion
2. Download any important data or dashboards
3. Unsubscribe from notifications to stop reminder emails
4. Data is permanently deleted after 30 days

### If you need more time

Subscribe to a monthly Standard plan ($95-200/month depending on usage):
- Keeps your trial data and setup intact
- Continue evaluation in a paid environment
- Cancel within 30 days if you decide against it
- More cost-effective than losing trial work and starting over

---

## Troubleshooting common issues

### No data appears in Discover

**Check**:
1. Verify agent/integration status in **Fleet**
2. Confirm data view time range includes recent data
3. Check for ingestion errors in **Stack Monitoring**

**Solution**: Review integration logs or increase debug verbosity.

### Slow query performance

**Check**:
1. Time range of query (shorter = faster)
2. Number of fields being searched
3. Data volume in index

**Solution**: Use filters to narrow searches, or consult [query optimization guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html).

### Alert not triggering

**Check**:
1. Rule conditions are being met in data
2. Alert connectors are configured correctly
3. Rule is enabled (not muted)

**Solution**: Test with extreme thresholds that definitely trigger, then adjust.

### Exceeded trial limits

**Check**:
1. Data ingestion volume in **Billing**
2. Serverless auto-scaling may throttle at trial limits

**Solution**: Subscribe to continue or reduce data sources temporarily.

---

## Getting help

- **Documentation**: [elastic.co/guide](https://www.elastic.co/guide)
- **Community forums**: [discuss.elastic.co](https://discuss.elastic.co)
- **Trial support**: Email from your Cloud console
- **Sales questions**: [elastic.co/contact](https://www.elastic.co/contact)

---

## Key takeaways

1. **Focus on one use case** to get actionable results in 14 days
2. **Involve real users** from Days 4-6 for authentic validation  
3. **Test at scale** on Days 7-9 to avoid surprises after purchase
4. **Calculate concrete ROI** based on time savings and costs
5. **Start conservatively** with Standard + Monthly, then expand

Your evaluation is successful when you can confidently answer: "Does Elastic solve my specific problem better than alternatives, and is the ROI positive?"

Everything else is secondary.