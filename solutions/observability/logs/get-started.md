---
navigation_title: Get started
description: Get one log source flowing into Elastic with an OpenTelemetry quickstart for your deployment type and explore it in Discover, then find the pages for planning the full logs setup.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Get started with logs [logs-get-started]

Start here to go from ingesting logs from a single source to using **Discover** to query and explore the data you ingest. You'll use a quickstart to install {{agent}} in OTel mode with sensible defaults, so you don't have to choose a collector, a field naming schema, or a retention policy yet. Once you have your logs flowing into {{es}}, follow the links in [Plan your full setup](#logs-get-started-next) to add more log sources, process logs, and set up data retention.

Use this page if you're trying Elastic for the first time, or if you want to see your own logs in Elastic before setting up a complete roll out.

## Before you begin [logs-get-started-prereqs]

::::{applies-switch}

:::{applies-item} stack:

You need an {{stack}} deployment with {{es}} and {{kib}}, and a {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}. Because many {{integrations}} assets are shared across spaces, the user needs those privileges in all spaces.

To get started quickly, create an {{ech}} deployment. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

:::

:::{applies-item} serverless:

You need an {{obs-serverless}} project and the **Admin** role or higher. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

If you only need logs, the Logs Essentials tier is enough. Refer to [Get started with Logs Essentials](/solutions/observability/get-started/logs-essentials.md) and [{{obs-serverless}} feature tiers](/solutions/observability/observability-serverless-feature-tiers.md).

:::

::::

You also need a host, container, or cluster you can install software on, with log files you want to see.

## Get your first logs in [logs-get-started-steps]

:::::{stepper}

::::{step} Get data flowing

Follow the quickstart for your deployment type and where your workloads run. Each one installs {{agent}} in OTel mode, which collects logs and metrics from the host, container, or cluster and sends them to Elastic:

| Deployment | {{k8s}} | Docker | Hosts or VMs |
|---|---|---|---|
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

Two other ways to get a first source in:

- **From the UI.** From the navigation menu, select **Add data** → **Host** and pick **OpenTelemetry: Full Observability**, or pick **Elastic Agent: Logs & Metrics** to scan the host and install the matching integrations, which come with parsing and dashboards. Refer to [Get started with system logs](/solutions/observability/logs/get-started-with-system-logs.md).
- **One specific log file.** Follow [Send any log file using OTel Collector](/solutions/observability/logs/stream-any-log-file-using-edot-collector.md), or [Send any log file using {{agent}}](/solutions/observability/logs/stream-any-log-file.md) if you already run {{agent}} with {{fleet}}.

Either collector is fine for a first look, and you can run both while you decide. The choice for your full setup is covered in [Ingest logs](/solutions/observability/logs/ingest.md).
::::

::::{step} Confirm logs are arriving

From the navigation menu, go to **Discover** and select the **All logs** {{data-source}}. You should see documents from your host, newest first, each with a timestamp and a message. Expand a document to see its fields.

If nothing appears after a few minutes, refer to [Troubleshoot logs](/troubleshoot/observability/troubleshoot-logs.md).
::::

::::{step} Explore your first logs

Try the following to get an understanding of how you can work with your data in Elastic. Each one links to the page that covers it in depth.

- **Filter to what matters.** In the query bar, enter a {{kib}} Query Language (KQL) query such as `log.level : "error"` to keep only error-level messages, then narrow the time picker to the last 15 minutes. For more filters, refer to [Filter logs in Discover](/solutions/observability/logs/filter-aggregate-logs.md#logs-filter-discover).
- **Read one log in context.** Expand a document and open the log details to see the message broken into fields, similar errors, and, for application logs, the stack trace and trace summary. Refer to [View log details](/solutions/observability/logs/discover-logs.md#view-log-details).
- **Count by level.** Switch **Discover** to **{{esql}}** mode and run:

    ```esql
    FROM logs-*
    | STATS count = COUNT(*) BY log.level
    ```

    If `log.level` is empty for your data, the source wasn't parsed into fields yet. That's what [Process logs](/solutions/observability/logs/process.md) fixes. For more aggregations, refer to [Aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md#logs-aggregate).
::::

:::::

## Plan your full setup [logs-get-started-next]

The quickstart chose defaults for you: one collector, one field naming schema (OpenTelemetry semantic conventions, or Elastic Common Schema if you used an integration), and the default retention, which is 30 days on {{serverless-full}}. Before you add more sources, make those choices once, because they decide your field names, which prebuilt dashboards work, and how you parse. Changing them later means reworking queries, dashboards, and alerts.

- [Ingest logs](/solutions/observability/logs/ingest.md): pick the collection path for each source and your deployment type, and learn what each path means for your schema.
- [Process logs](/solutions/observability/logs/process.md): decide where unstructured logs get their fields.
- [Manage logs storage](/solutions/observability/logs/manage-storage.md): set retention per data stream before volume grows.
- [Explore logs](/solutions/observability/logs/explore-logs.md): build the searches, dashboards, and alerts your team uses every day.
- [Migrate logs to Elastic](/solutions/observability/logs/migrate.md): if you're replacing another logging tool, run both side by side while you rebuild searches and alerts.
