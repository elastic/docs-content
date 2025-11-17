---
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  stack:
description: Week 1 of your Elastic trial. Set up your deployment, connect your first data source, and start seeing value within hours.
---

# Week 1: Foundation and first use case

Week 1 focuses on getting your Elastic environment up and running quickly and demonstrating initial value with your chosen use case. By the end of this week, you will have data flowing into Elastic and be able to search, visualize, or monitor it effectively.

## Week 1 goals

By the end of this week, you will have:

- Set up your Elastic deployment.
- Connect your first data source.
- Explore data in Kibana.
- Create your first visualization or dashboard.
- Set up basic alerting (optional but recommended).

**Estimated time**: 2-4 hours total.

::::::{stepper}

:::::{step} Set up your deployment

### Choose your deployment type

When you start your trial, select a deployment type:

- {{serverless-full}} (Recommended for trials): Fully managed, auto-scaling, simplified configuration.
- {{ech}}: Fully managed with more control over configuration and sizing.

:::{tip}
For most trials, {{serverless-short}} provides the fastest path to value with minimal configuration overhead.
:::

### Create your deployment

Create your deployment by following these steps:

1. Log in to your Elastic Cloud account at [cloud.elastic.co](https://cloud.elastic.co).
2. Click **Create deployment** or **Create project** (for serverless).
3. Select your solution type:
   - **Elasticsearch** for search use cases
   - **Observability** for monitoring applications and infrastructure
   - **Security** for threat detection and security analytics
4. Choose your cloud provider and region (select the region closest to your data sources).
5. Click **Create**.

Your deployment will be ready in 1-2 minutes. **Save your credentials** when prompted.

### Access Kibana

Once your deployment is ready:

1. Select **Open Kibana** from your deployment overview.
2. Log in with your saved credentials.

:::{tip}
Bookmark your Kibana URL for easy access throughout your trial.
:::

:::::

:::::{step} Connect your first data source

Choose the path based on your use case:

::::{tab-set}
:::{tab-item} Search

Your goal is to index data that you want to search and analyze. Choose one method:

**Option A: Upload a file (Quickest start)**

Best for: CSV, JSON, or log files you have on hand.

1. In Kibana, go to **Management** → **Integrations**.
2. Search for "Upload file" and select it.
3. Drag your file or browse to select it.
4. Review the field mappings and adjust as needed.
5. Select **Import** and name your index.

If you don't have data ready, Kibana includes sample datasets. Go to **Home** → **Try sample data** and add the "Sample web logs" or "Sample eCommerce orders" dataset.

**Option B: Use an integration**

Best for: Connecting to existing systems (databases, APIs, applications).

1. Go to **Management** → **Integrations**.
2. Browse or search for your data source (examples: PostgreSQL, MongoDB, MySQL, Apache, nginx).
3. Select **Add** and follow the configuration steps.
4. Verify data is flowing by checking the integration status.

**Option C: Use the API**

Best for: Custom applications or programmatic data ingestion.

1. Generate an API key in Kibana (**Management** → **API keys**).
2. Use the Elasticsearch REST API to index documents:

```bash
curl -X POST "https://your-deployment.elastic.cloud:9200/your-index/_doc" \
  -H "Authorization: ApiKey your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Example document",
    "content": "This is a test document for search",
    "timestamp": "2024-11-17T10:00:00Z"
  }'
```

3. Refer to the [Elasticsearch index API documentation](/manage-data/data-store/index-basics.md) for more options.

### Verify your data

1. Go to **Analytics** → **Discover** in Kibana.
2. Select your index or data view.
3. Check that your documents are listed with all their fields.

If you don't find your data, check your integration status or indexing logs.

:::

:::{tab-item} Observability

Your goal is to collect logs, metrics, and traces from your systems. Choose one method:

**Option A: Monitor infrastructure (Easiest)**

Best for: Getting started quickly with system metrics.

1. In Kibana, go to **Management** → **Integrations**.
2. Search for "System" and select the **System integration**.
3. Click **Add System**.
4. **Install Elastic Agent** on a host you want to monitor:
   - Copy the installation command shown in Kibana.
   - Run it on your Linux, Windows, or macOS host.
   - The agent will automatically start collecting metrics.
5. Wait 1-2 minutes for data to appear.
6. Go to **Observability** → **Infrastructure** to see your host.

**Option B: Collect application logs**

Best for: Aggregating logs from applications or services.

1. Go to **Management** → **Integrations**.
2. Search for your log source:
   - **Custom logs** for generic log files
   - Specific integrations for Apache, nginx, MySQL, PostgreSQL, and so on.
3. Select **Add** and configure the log file paths.
4. Install or configure Elastic Agent to collect the logs.
5. Go to **Observability** → **Logs** → **Stream** to see incoming logs.

**Option C: Monitor an application (APM)**

Best for: Understanding application performance and errors.

1. Go to **Observability** → **Applications** → **APM**.
2. Select **Add data**.
3. Select your application language (Java, Node.js, Python, .NET, and so on).
4. Follow the instrumentation instructions to add the APM agent to your application code.
5. Restart your application.
6. Generate some traffic to your application.
7. Return to **Applications** in Kibana to view traces and metrics.

Refer to [APM documentation](/solutions/observability/apm/index.md) for detailed setup instructions.

### Verify your data

1. Go to **Observability** → **Overview**.
2. You should see metrics, logs, or traces depending on what you configured.
3. Click into **Infrastructure**, **Logs**, or **Applications** for detailed views.

:::

:::{tab-item} Security

### Ingest security data

Your goal is to collect security events from endpoints, networks, and cloud services. Choose your starting point:

**Option A: Monitor endpoints (Recommended)**

Best for: Detecting threats on laptops, desktops, and servers.

1. In Kibana, go to **Management** → **Integrations**.
2. Search for "Endpoint Security" and select **Elastic Defend**.
3. Select **Add Elastic Defend**.
4. Create an integration policy with default protection settings.
5. **Install Elastic Agent with Elastic Defend** on endpoints:
   - Copy the installation command from Kibana.
   - Run it on Windows, macOS, or Linux endpoints.
   - The agent will install and begin protecting the endpoint.
6. Wait 1-2 minutes for the endpoint to appear in Kibana.
7. Go to **Security** → **Manage** → **Endpoints** to see protected hosts.

**Option B: Collect security logs**

Best for: Ingesting logs from firewalls, cloud providers, or security tools.

1. Go to **Management** → **Integrations**.
2. Search for your security data source:
   - AWS CloudTrail, Azure Activity Logs, Google Cloud Audit Logs
   - Palo Alto Networks, Cisco, Fortinet
   - Okta, Azure AD, Google Workspace
3. Selec **Add** and follow the configuration steps for your provider.
4. Verify data is flowing by checking the integration status.

**Option C: Collect network traffic**

Best for: Monitoring network activity for threats.

1. Go to **Management** → **Integrations**.
2. Search for "Network Packet Capture" or "Packetbeat".
3. Install Elastic Agent with the network integration on a host that can capture traffic.
4. Configure network interfaces to monitor.
5. Go to **Security** → **Network** to see network flows.

### Verify your data

1. Go to **Security** → **Overview**.
2. You should see security events and alerts.
3. Explore **Alerts**, **Hosts**, **Network**, or **Users** tabs for detailed information.

:::
::::

:::::

:::::{step} Explore your data

Now that data is flowing, let's explore it in Kibana.

::::{tab-set}
:::{tab-item} Search

### Explore with Discover

1. Go to **Analytics** → **Discover**.
2. Select your index pattern or data view.
3. **Try searching**:
   - Enter keywords in the search bar. For example, "error" or "user login".
   - Use the query language for more precision. For example, `status:200 AND method:GET`.
4. **Filter data**:
   - Select field values to add filters.
   - Use the time picker to focus on specific time ranges.
5. **Analyze fields**:
   - Expand a document to view all fields.
   - Select fields in the sidebar to view value distributions.
3. Choose a visualization type (try "Lens" for an intuitive drag-and-drop experience).
4. Select your data source.
5. Drag fields onto the canvas:
   - Add dimensions. For example, time or categories.
   - Add metrics. For example, count, sum, or average.
6. Customize colors, labels, and formatting.
7. Select **Save** and name your visualization.

:::

:::{tab-item} Observability

### Explore logs

1. Go to **Observability** → **Logs** → **Stream**.
2. **Filter logs**:
   - Use the search bar to find specific messages.
   - Filter by host, service, or log level.
3. **View log details**: Select a log entry to see all fields and context.

### Explore metrics

1. Go to **Observability** → **Infrastructure**.
2. View your hosts with CPU, memory, and disk metrics.
3. Select a host to view detailed metrics.
4. Switch views to view containers, Kubernetes pods, or services.

### Explore APM (if configured)

1. Go to **Observability** → **Applications**.
2. Select your service.
3. View latency, throughput, and error rates.
4. Select a transaction to view traces and spans.

### Create an observability dashboard

1. Go to **Analytics** → **Dashboards**.
2. Click **Create dashboard**.
3. Click **Add panel** and choose a visualization type.
4. Select your observability data source.
5. Build visualizations for:
   - Error rates over time
   - Response time trends
   - Resource utilization (CPU, memory)
6. Arrange panels and save your dashboard.

:::

:::{tab-item} Security

### Explore security events

1. Go to **Security** → **Explore** → **Events**.
2. **Filter events**:
   - Use the search bar or KQL to find specific activity.
   - Filter by host, user, process, or event type.
3. **Analyze an event**: Click on an event to see all details.

### View alerts

1. Go to **Security** → **Alerts**.
2. Review any alerts that have been generated by default detection rules.
3. Click on an alert to investigate further.

### Explore the security dashboard

1. Go to **Security** → **Overview**.
2. View the pre-built security dashboards showing:
   - Alert trends
   - Host and user activity
   - Network connections
   - Top threats and events

### Create a custom security query

1. Go to **Security** → **Timelines**.
2. Click **Create timeline**.
3. Add filters and queries to hunt for specific activity:
   - Example: `process.name: "powershell.exe" AND event.action: "network-connection"`
4. Save your timeline for future investigations.

:::
::::

:::::

:::::{step} Set up alerting (Optional)

Alerts help you stay informed about important events or conditions.

### Create a simple alert

::::{tab-set}
:::{tab-item} Search

1. Go to **Management** → **Stack Management** → **Rules**.
2. Click **Create rule**.
3. Select **Elasticsearch query** rule type.
4. Define your query (for example, `error:true`).
5. Set threshold conditions (for example, "more than 10 matches in 5 minutes").
6. Configure actions (for example, send an email or Slack message).
7. Save and enable the rule.

Refer to [alerting documentation](/solutions/observability/incident-management/alerting.md) for more options.

:::

:::{tab-item} Observability

1. Go to **Observability** → **Alerts**.
2. Click **Manage Rules** → **Create rule**.
3. Choose a rule type:
   - **Metric threshold**: Alert when CPU, memory, or custom metrics exceed limits.
   - **Log threshold**: Alert on specific log patterns.
   - **APM**: Alert on high error rates or slow transactions.
4. Define your conditions and thresholds.
5. Configure connectors (email, Slack, PagerDuty).
6. Save and enable the rule.

Refer to [observability alerting](/solutions/observability/incident-management/alerting.md) for detailed configuration.

:::

:::{tab-item} Security

1. Go to **Security** → **Rules**.
2. Click **Detection rules (SIEM)**.
3. **Enable prebuilt rules**:
   - Browse the rules library.
   - Enable 3-5 rules relevant to your environment (for example, "Unusual Login Activity", "Suspicious Process Execution").
4. Go back to **Alerts** to see any triggered alerts.

You can also create custom rules:

1. Click **Create new rule**.
2. Choose a rule type (query, threshold, machine learning, indicator match).
3. Define detection logic.
4. Set severity and risk scores.
5. Enable the rule.

Refer to [security detection rules](/solutions/security/detect-and-alert/about-detection-rules.md) for more information.

:::
::::

:::::

:::::{step} Document your progress

At the end of Week 1, take a moment to document:

- **Data sources connected**: List what data you're ingesting.
- **Initial insights**: What did you learn from exploring the data?
- **Visualizations created**: Screenshots or links to dashboards.
- **Alerts configured**: What conditions are you monitoring?
- **Challenges encountered**: Note any issues for follow-up.

This documentation will be valuable when presenting your PoC to stakeholders.

:::::

::::::

## Week 1 checklist

Before moving to Week 2, ensure you've completed:

- Deployment is running and accessible.
- At least one data source is connected and sending data.
- You can search or view your data in Kibana.
- You've created at least one visualization or dashboard.
- (Optional) You've configured at least one alert.

## Next steps

Great work. You've established your foundation. Now it's time to expand your PoC and demonstrate deeper value.

**Continue to [Week 2](/get-started/trial-week-2.md)** to add more data sources, refine your dashboards, and prepare for stakeholder evaluation.

## Need help

If you encountered issues during Week 1:

- [Troubleshooting documentation](/troubleshoot/index.md): Common issues and solutions.
- [Elastic Community forums](https://discuss.elastic.co/): Ask questions and get help from the community.
- Contact support: Reach out to your trial specialist for personalized assistance.

