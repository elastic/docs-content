---
navigation_title: FAQ
description: Frequently asked questions about Elastic Managed integrations, including limits, supportability, data residency, and common setup questions.
applies_to:
  stack: ga 9.5+, preview 9.0-9.4
  serverless: preview
products:
  - id: elastic-agent
  - id: fleet
  - id: cloud-serverless
  - id: cloud-hosted
  - id: elasticsearch
  - id: observability
  - id: security
---

# {{managed-integrations}} FAQ [managed-integrations-faq]

Frequently asked questions about {{managed-integrations}}.

## About {{managed-integrations}} [managed-integrations-faq-about]

### What types of integrations are supported? [managed-integrations-faq-supported]

{{managed-integrations}} are best suited for integrations that pull data from a cloud source through an API at lower volumes. For a complete list, refer to [{{managed-integrations}} quick reference](integration-docs://reference/managed_integrations.md). Elastic continually adds more integrations to this list.

### Why aren't some integrations available as {{managed-integrations}}? [managed-integrations-faq-missing]

Not every integration in Elastic's catalog can run as an {{managed-integration}}. Only integrations that pull data from a cloud source through an API can be made available in this mode. To request that an integration be made available, open an enhancement request in the [`elastic/integrations`](https://github.com/elastic/integrations) repository.

### How many {{managed-integrations}} can I deploy? [managed-integrations-faq-limit]

You can deploy up to 50 {{managed-integrations}} per {{serverless-short}} project or {{ech}} deployment. Adding multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).

### Can I create alerts on data ingested by {{managed-integrations}}? [managed-integrations-faq-alerting]

Yes. Data ingested through {{managed-integrations}} lands in your cluster like any other integration data, so all {{es}} and {{kib}} features apply — including [alerting](/explore-analyze/alerting.md).

## Pricing and SLAs [managed-integrations-faq-pricing-slas]

### How much do {{managed-integrations}} cost? [managed-integrations-faq-pricing]

On {{serverless-short}} projects, you can deploy {{managed-integrations}} at no additional cost.

On {{ech}}, each deployed {{managed-integration}} is charged per hour. On the Elastic price list, the unit appears as `[csp].managed-integration`, where `[csp]` is `aws`, `azure`, or `gcp`.

Most {{managed-integrations}} are metered at one unit per integration, per hour. The following integrations are exceptions:

| Integration | Unit cost (per integration, per hour) |
| --- | :---: |
| Microsoft Defender XDR Logs | 4 |
| Microsoft Defender for Endpoint | 4 |
| Rapid7 InsightVM logs | 4 |
| CrowdStrike Falcon Intelligence logs | 4 |
| abuse.ch API | 2 |

For current pricing details, refer to the [Elastic pricing page](https://www.elastic.co/pricing).

:::{note}
:applies_to: stack: preview 9.0-9.4
In these versions, {{managed-integrations}} are in technical preview and are free on {{ech}}.
:::

### What SLAs apply to {{managed-integrations}}? [managed-integrations-faq-slas]

{{managed-integrations}} run on Elastic-managed infrastructure that Elastic operates as part of {{serverless-full}}. As a result, the service follows the [{{serverless-full}} SLA](https://www.elastic.co/agreements/sla-elastic-cloud-serverless), whether the data it collects lands in an {{serverless-full}} project or an {{ech}} deployment.

:::{note}
:applies_to: stack: preview 9.0-9.4
In these versions, {{managed-integrations}} are in technical preview and are provided as-is, so no SLA applies.
:::

## Data and security [managed-integrations-faq-data-security]

### Where is my data stored? [managed-integrations-faq-data-storage]

Documents ingested through {{managed-integrations}} are stored in your project or {{ech}} deployment, the same as data ingested by agent-based integrations.

### Does my data travel over the public internet? [managed-integrations-faq-public-internet]

Usually not. Data flows from Elastic-managed infrastructure to your cluster over Elastic's internal network. However, if your {{ech}} deployment is in a region that isn't served by {{serverless-full}}, data might traverse the public internet to reach your cluster.

### Who at Elastic has access to my data? [managed-integrations-faq-data-access]

Elastic employees don't have access to data in your project or deployment. Data ingested through {{managed-integrations}} is stored in your cluster, with the same access controls as data ingested by any other method.

### Can {{managed-integrations}} use a specific range of static IP addresses? [managed-integrations-faq-static-ip]

No. {{managed-integrations}} run on shared infrastructure and don't use a fixed range of IP addresses for ingress or egress.

### Do {{managed-integrations}} work with traffic filtering? [managed-integrations-faq-traffic-filtering]

```{applies_to}
stack: ga 9.5+, preview 9.1+
serverless: preview
```

Yes. {{managed-integrations}} support traffic filtering, and no additional configuration is necessary.

## Limits and behavior [managed-integrations-faq-limits]

### Is there a maximum throughput? [managed-integrations-faq-throughput]

Yes. To ensure a consistent level of service and avoid issues caused by under-resourced clusters, each {{managed-integration}} is limited to 300 events per second (EPS). If throughput spikes above this limit, the service is throttled, and the UI shows when this happens. Continuously hitting this limit delays ingestion of your cloud data source. If you need higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).

### Does the service scale horizontally? [managed-integrations-faq-horizontal-scaling]

No. Deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).

### What happens to my data if there's a service issue? [managed-integrations-faq-service-issue]

For an isolated issue with a single collector, Elastic restarts it and ingestion resumes. Any events in the collector's in-memory queue might be lost. For a service-wide outage, no data is collected until the infrastructure recovers, and some in-flight events might be lost.

## Setup and operation [managed-integrations-faq-operations]

### Why does my integration policy show "Add agent" instead of an agent? [managed-integrations-faq-add-agent-button]

After you create a new {{managed-integration}}, the integration policy might show an **Add agent** button for several minutes while Elastic provisions the collector. The button disappears automatically once provisioning is complete. Refresh the page if you want to view the updated status sooner — no other action is needed.

### Why aren't my {{managed-integration}} collectors shown in {{fleet}}? [managed-integrations-faq-fleet-visibility]

{{managed-integrations}} are a fully managed service, so the underlying collectors aren't shown in {{fleet}} — Elastic operates the infrastructure on your behalf. You can still view each integration's status in the **{{integrations}}** app and observe the ingested data itself in your cluster.

### How do I view my {{managed-integrations}}? [managed-integrations-faq-view]

Manage and monitor {{managed-integrations}} from the **{{integrations}}** app:

1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Do one of the following:
   - Open the **Installed integrations** tab and select **View policies** for the integration you want.
   - Open the integration's page and go to its **Integration policies** tab.

Each integration policy shows the integration's status, so you can check its health and take action — such as updating credentials — without using {{fleet}}.

### What should I do if an {{managed-integration}} is unhealthy? [managed-integrations-faq-health]

```{applies_to}
stack: ga 9.5+
serverless: preview
```

{{managed-integrations}} are a managed service, so you monitor them at the integration level rather than by inspecting the underlying collector. Each integration's status appears on its **Integration policies** tab in the **{{integrations}}** app. Hover over the status to see more detail about why an integration is unhealthy.

If an {{managed-integration}} is unhealthy:

1. **Check your credentials and configuration.** Most issues are caused by expired or invalid credentials, or by missing permissions at the source. Edit the integration to update its credentials or configuration.
2. **Contact [Elastic Support](https://support.elastic.co)** if the problem persists. You don't need to inspect or debug the collector yourself — Elastic operates it for you, monitors the service, and can collect diagnostics on your behalf.

A healthy status means the integration is connected and ready, but it doesn't necessarily mean data is currently flowing. If an integration is healthy but you don't see data, confirm that the source has data available and check the integration's throughput. If data still doesn't appear, contact [Elastic Support](https://support.elastic.co).

### How do I get support and collect diagnostics? [managed-integrations-faq-support]

{{managed-integrations}} are a fully managed service, so you usually don't need to collect diagnostics yourself. Errors that are relevant to you are surfaced for each integration in the **{{integrations}}** app. If you suspect a problem with the service or your deployment, contact [Elastic Support](https://support.elastic.co) — they'll collect diagnostics on your behalf and investigate.

### How do I make the underlying collectors visible in {{fleet}}? [managed-integrations-faq-fleet-show]

```{applies_to}
stack: preview 9.1-9.4
serverless: unavailable
```

On {{stack}} 9.1 through 9.4, you can override the default and expose the underlying collectors in {{fleet}}:

:::::{include} /manage-data/ingest/managed-integrations/_snippets/show-agentless-resources.md
:::::

### How do I troubleshoot an Offline agent? [managed-integrations-troubleshoot-offline]

```{applies_to}
stack: preview 9.0-9.4
```

For {{managed-integrations}} to connect to your cluster, the {{fleet-server}} host value must be the default. Otherwise, the agent shows as `Offline` on the **{{fleet}}** page, and logs include the error `[elastic_agent][error] Cannot checkin in with fleet-server, retrying`.

To troubleshoot:

1. Find **{{fleet}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Go to the **Settings** tab.
2. Under **Fleet server hosts**, click the **Edit** icon {icon}`pencil` for the host named `Default`. This opens the **Edit Fleet Server** flyout. The host named `Default` must have the **Make this Fleet Server the default one** setting enabled. If not, enable it, then delete and re-create your integration.

If the setting was already enabled but problems persist, the default {{fleet-server}} URL might have been changed. Contact [Elastic Support](https://support.elastic.co) to recover the original URL.

::::{note}
On {{ech}} deployments with {{stack}} versions before 9.1.6, the connection between {{managed-integrations}} and {{fleet-server}} can break if the default {{fleet-server}} host URL is modified or if a different host URL is set as the default.

This issue is resolved in {{stack}} 9.1.6 and later. In those versions, {{managed-integration}} policies are assigned to a default managed {{fleet-server}} host that can't be modified.
::::

### How do I troubleshoot an Unhealthy agent? [managed-integrations-troubleshoot-unhealthy]

```{applies_to}
stack: preview 9.1-9.4
```

On the **Fleet** → **Agents** page, agents associated with {{managed-integrations}} have names that begin with `agentless`. When an agentless agent is `Unhealthy`:

1. **Check the integration configuration.** Most `Unhealthy` states are caused by expired or invalid credentials, or by source-side permission issues. Confirm that the credentials and configuration you provided for the integration are still valid.
2. **Contact [Elastic Support](https://support.elastic.co).** If the configuration looks correct but the agent remains unhealthy, support will collect diagnostics and investigate on your behalf.

::::::{dropdown} Collect diagnostics yourself

If you want to collect a diagnostics bundle before contacting support:

1. Make agentless agents visible in {{fleet}}:

   :::::{include} /manage-data/ingest/managed-integrations/_snippets/show-agentless-resources.md
   :::::

2. In **{{fleet}}**, select the unhealthy agent.
3. From the actions menu {icon}`ellipsis`, select **Maintenance and diagnostics** → **Request diagnostics .zip**.
4. Download and unzip the [diagnostics bundle](/troubleshoot/ingest/fleet/diagnostics.md). For more information, refer to [Common problems with {{fleet}} and {{agent}}](/troubleshoot/ingest/fleet/common-problems.md).
::::::

### Why can't I upgrade my {{managed-integration}} to a later version? [managed-integrations-faq-upgrade]

```{applies_to}
stack: preview 9.0-9.1
```

On {{stack}} versions before 9.2, {{managed-integrations}} can't be upgraded to later versions of the integration. To get a later version, upgrade to {{stack}} 9.2 or later, or delete and re-install the integration.

### How do I delete an {{managed-integration}}? [managed-integrations-faq-delete]

::::{important}
Deleting an {{managed-integration}} removes all associated resources and stops data ingestion.
::::


1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then search for your integration.
2. Go to the integration's **Integration policies** tab.
3. Find the integration policy to delete. Click the actions icon {icon}`ellipsis`, then select **Delete integration**.
4. Confirm by clicking **Delete integration** again.
