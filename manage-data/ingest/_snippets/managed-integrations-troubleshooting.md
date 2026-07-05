Resolve common issues with {{managed-integrations}}. For more general questions, refer to the [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md).

## Get diagnostics and support [agentless-troubleshoot-support]

{{managed-integrations}} are a fully managed service, so you usually don't need to collect diagnostics yourself. If you suspect a problem with the service or your deployment, contact [Elastic Support](https://support.elastic.co) — they'll collect diagnostics on your behalf and investigate.

## Troubleshoot an Offline agent [agentless-troubleshoot-offline]

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

## Troubleshoot an Unhealthy agent [agentless-troubleshoot-unhealthy]

On the **Fleet** → **Agents** page, agents associated with {{managed-integrations}} have names that begin with `agentless`. When an agentless agent is `Unhealthy`:

1. **Check the integration configuration.** Most `Unhealthy` states are caused by expired or invalid credentials, or by source-side permission issues. Confirm that the credentials and configuration you provided for the integration are still valid.
2. **Contact [Elastic Support](https://support.elastic.co).** If the configuration looks correct but the agent remains unhealthy, support will collect diagnostics and investigate on your behalf.

:::{dropdown} Collect diagnostics yourself
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
:::
