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
  - id: observability
  - id: security
---

# {{managed-integrations}} FAQ [agentless-integration-faq]

Frequently asked questions about {{managed-integrations}} (previously known as agentless integrations).

## About {{managed-integrations}} [agentless-faq-about]

### What types of integrations are supported? [agentless-faq-supported]

{{managed-integrations}} are best suited for integrations that pull data from a cloud source through an API at moderate volumes. For a complete list, refer to [{{managed-integrations}} quick reference](integration-docs://reference/agentless_integrations.md). Elastic continually adds more integrations to this list.

### Why aren't some integrations available as {{managed-integrations}}? [agentless-faq-missing]

Not every integration in Elastic's catalog can run as an {{managed-integration}}. Only integrations that pull data from a cloud source through an API can be made available in this mode. To request that an integration be made available, open an enhancement request in the [`elastic/integrations`](https://github.com/elastic/integrations) repository.

### How many {{managed-integrations}} can I deploy? [agentless-faq-limit]

You can deploy up to 50 {{managed-integrations}} per project. Adding multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).

### Can I create alerts on data ingested by {{managed-integrations}}? [agentless-faq-alerting]

Yes. Data ingested through {{managed-integrations}} lands in your cluster like any other integration data, so all {{es}} and {{kib}} features apply — including [alerting](/explore-analyze/alerting.md).

## Pricing and SLAs [agentless-faq-pricing-slas]

### How am I charged for {{managed-integrations}}? [agentless-faq-pricing]

On {{serverless-short}} projects, the cost of {{managed-integrations}} is included in your subscription. During technical preview, there are no additional costs on {{ech}} either. For current pricing details, refer to the [Elastic pricing page](https://www.elastic.co/pricing).

### What SLAs apply to {{managed-integrations}}? [agentless-faq-slas]

On {{serverless-full}}, {{managed-integrations}} follow the [{{serverless-full}} SLA](https://www.elastic.co/agreements/sla-elastic-cloud-serverless). On {{ech}}, {{managed-integrations}} are in technical preview and aren't covered by the {{ech}} SLA.

## Data and security [agentless-faq-data-security]

### Where is my data stored? [agentless-faq-data-storage]

Documents ingested through {{managed-integrations}} are stored in your project or {{ech}} deployment, the same as data ingested by agent-based integrations.

### Does my data travel over the public internet? [managed-integrations-faq-public-internet]

Usually not. Data flows from Elastic-managed infrastructure to your cluster over Elastic's internal network. However, if your {{ech}} deployment is in a region that isn't served by {{serverless-full}}, data might traverse the public internet to reach your cluster.

### Who at Elastic has access to my data? [agentless-faq-data-access]

Elastic employees don't have access to data in your project or deployment. Data ingested through {{managed-integrations}} is stored in your cluster, with the same access controls as data ingested by any other method.

### Can {{managed-integrations}} use a specific range of static IP addresses? [agentless-faq-static-ip]

No. {{managed-integrations}} run on shared infrastructure and don't use a fixed range of IP addresses for ingress or egress.

### Do {{managed-integrations}} work with traffic filtering? [agentless-faq-traffic-filtering]

```{applies_to}
stack: preview 9.1
serverless: preview
```

Yes. {{managed-integrations}} support traffic filtering, and no additional configuration is necessary.

## Limits and behavior [agentless-faq-limits]

### Is there a maximum throughput? [agentless-faq-throughput]

Yes. To preserve quality of service across all {{managed-integrations}}, throughput is rate-limited on {{serverless-short}} for integrations whose underlying input type is `httpjson` or `cel` (two common pull-based input mechanisms in {{agent}}). Rate limiting uses back-pressure rather than dropping events, so collection slows down until the source catches up.

### Does the service scale horizontally? [agentless-faq-horizontal-scaling]

No. Deploying multiple {{managed-integrations}} for the same source doesn't increase ingest throughput. For higher throughput, consider the [{{edot}} Cloud Forwarder](opentelemetry://reference/edot-cloud-forwarder/index.md).

### What happens to my data if there's a service issue? [managed-integrations-faq-service-issue]

For an isolated issue with a single collector, Elastic restarts it and ingestion resumes. Any events in the collector's in-memory queue might be lost. For a service-wide outage, no data is collected until the infrastructure recovers, and some in-flight events might be lost.

## Setup and operation [agentless-faq-operations]

### Why does my integration policy show "Add agent" instead of an agent? [agentless-faq-add-agent-button]

After you create a new {{managed-integration}}, the integration policy might show an **Add agent** button for several minutes while Elastic provisions the collector. The button disappears automatically once provisioning is complete. Refresh the page if you want to view the updated status sooner — no other action is needed.

### Why aren't my {{managed-integrations}} collectors shown in {{fleet}}? [agentless-faq-fleet-visibility]

{{managed-integrations}} are a fully managed service, so the underlying collectors aren't shown in **{{fleet}}** — Elastic operates the infrastructure on your behalf. You can still view each integration's status in the **{{integrations}}** app and observe the ingested data itself in your cluster.

### How do I make the underlying collectors visible in {{fleet}}? [agentless-faq-fleet-show]

```{applies_to}
stack: preview 9.1-9.4
serverless: unavailable
```

On {{stack}} 9.1 through 9.4, you can override the default and expose the underlying collectors in **{{fleet}}**:

::::{applies-switch}

:::{applies-item} stack: preview 9.2-9.4
Go to the **Settings** tab of the **{{fleet}}** page. In the **Advanced Settings** section, enable **Show agentless resources**.
:::

:::{applies-item} stack: preview =9.1
Add the query parameter `?showAgentless=true` to the end of the **{{fleet}}** page's URL.
:::

::::

### How do I get support and collect diagnostics? [agentless-faq-support]

{{managed-integrations}} are a fully managed service, so you usually don't need to collect diagnostics yourself. If you suspect a problem with the service or your deployment, contact [Elastic Support](https://support.elastic.co) — they'll collect diagnostics on your behalf and investigate.

### How do I troubleshoot an Offline agent? [agentless-troubleshoot-offline]

```{applies_to}
ech: preview
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

### How do I troubleshoot an Unhealthy agent? [agentless-troubleshoot-unhealthy]

On the **Fleet** → **Agents** page, agents associated with {{managed-integrations}} have names that begin with `agentless`. When an agentless agent is `Unhealthy`:

1. **Check the integration configuration.** Most `Unhealthy` states are caused by expired or invalid credentials, or by source-side permission issues. Confirm that the credentials and configuration you provided for the integration are still valid.
2. **Contact [Elastic Support](https://support.elastic.co).** If the configuration looks correct but the agent remains unhealthy, support will collect diagnostics and investigate on your behalf.

:::::{dropdown} Collect diagnostics yourself
:applies_to: stack: preview 9.1-9.4

If you want to collect a diagnostics bundle before contacting support:

1. Make agentless agents visible in **{{fleet}}**:

   ::::{applies-switch}

   :::{applies-item} stack: preview 9.2-9.4
   Go to the **Settings** tab of the **{{fleet}}** page. In the **Advanced Settings** section, enable **Show agentless resources**.
   :::

   :::{applies-item} stack: preview =9.1
   Add the query parameter `?showAgentless=true` to the end of the **{{fleet}}** page's URL.
   :::

   ::::

2. In **{{fleet}}**, select the unhealthy agent.
3. From the actions menu {icon}`ellipsis`, select **Maintenance and diagnostics** → **Request diagnostics .zip**.
4. Download and unzip the [diagnostics bundle](/troubleshoot/ingest/fleet/diagnostics.md). For more information, refer to [Common problems with {{fleet}} and {{agent}}](/troubleshoot/ingest/fleet/common-problems.md).
:::::

### Why can't I upgrade my {{managed-integration}} to a later version? [agentless-faq-upgrade]

```{applies_to}
stack: preview 9.0-9.1
```

On {{stack}} versions before 9.2, {{managed-integrations}} can't be upgraded to later versions of the integration. To get a later version, upgrade to {{stack}} 9.2 or later, or delete and re-install the integration.

### How do I delete an {{managed-integration}}? [agentless-faq-delete]

::::{note}
Deleting an {{managed-integration}} removes all associated resources and stops data ingestion.
::::


1. In {{kib}}, find **{{integrations}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then search for your integration.
2. Go to the integration's **Integration policies** tab.
3. Find the integration policy to delete. Click the actions icon {icon}`ellipsis`, then select **Delete integration**.
4. Confirm by clicking **Delete integration** again.
