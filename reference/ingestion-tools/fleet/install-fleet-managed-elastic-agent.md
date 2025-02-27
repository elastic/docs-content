---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-fleet-managed-elastic-agent.html
---

# Install Fleet-managed Elastic Agents [install-fleet-managed-elastic-agent]

::::{admonition}
{{fleet}} is a web-based UI in {{kib}} for [centrally managing {{agent}}s](/reference/ingestion-tools/fleet/manage-elastic-agents-in-fleet.md). To use {{fleet}}, you install {{agent}}, then enroll the agent in a policy defined in {{kib}}. The policy includes integrations that specify how to collect observability data from specific services and protect endpoints. The {{agent}} connects to a trusted [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) instance to retrieve the policy and report agent events.

::::



## Where to start [get-started]

To get up and running quickly, read one of our end-to-end guides:

* New to Elastic? Read our solution [Getting started guides](/get-started/index.md).
* Want to add data to an existing cluster or deployment? Read our [*Quick starts*](/reference/ingestion-tools/fleet/index.md).

Looking for upgrade info? Refer to [Upgrade {{agent}}s](/reference/ingestion-tools/fleet/upgrade-elastic-agent.md).

Just want to learn how to install {{agent}}? Continue reading this page.


## Prerequisites [elastic-agent-prereqs]

You will always need:

* **A {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}.** Since many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces.
* **[{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) running in a location accessible to {{agent}}.** {{agent}} must have a direct network connection to {{fleet-server}} and {{es}}. If you’re using {{ecloud}}, {{fleet-server}} is already available as part of the {{integrations-server}}. For self-managed deployments, refer to [Deploy on-premises and self-managed](/reference/ingestion-tools/fleet/add-fleet-server-on-prem.md).
* **Internet connection for {{kib}} to download integration packages from the {{package-registry}}.** Make sure the {{kib}} server can connect to `https://epr.elastic.co` on port `443`. If your environment has network traffic restrictions, there are ways to work around this requirement. See [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md) for more information.

If you are using a {{fleet-server}} that uses your organization’s certificate, you will also need:

* **A Certificate Authority (CA) certificate to configure Transport Layer Security (TLS) to encrypt traffic.** If your organization already uses the {{stack}}, you may already have a CA certificate. If you do not have a CA certificate, you can read more about generating one in [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).

If you’re running {{agent}} 7.9 or earlier, stop the agent and manually remove it from your host.


## Installation steps [elastic-agent-installation-steps]

::::{note}
You can install only a single {{agent}} per host.
::::


{{agent}} can monitor the host where it’s deployed, and it can collect and forward data from remote services and hardware where direct deployment is not possible.

To install an {{agent}} and enroll it in {{fleet}}:

1. In {{fleet}}, open the **Agents** tab and click **Add agent**.
2. In the **Add agent** flyout, select an existing agent policy or create a new one. If you create a new policy, {{fleet}} generates a new [{{fleet}} enrollment token](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md).

    ::::{note}
    For on-premises deployments, you can dedicate a policy to all the agents in the network boundary and configure that policy to include a specific {{fleet-server}} (or a cluster of {{fleet-server}}s).

    Read more in [Add a {{fleet-server}} to a policy](/reference/ingestion-tools/fleet/agent-policy.md#add-fleet-server-to-policy).

    ::::

3. Make sure **Enroll in Fleet** is selected.
4. Download, install, and enroll the {{agent}} on your host by selecting your host operating system and following the **Install {{agent}} on your host** step. Note that the commands shown are for AMD platforms, but ARM packages are also available. Refer to the {{agent}} [downloads page](https://www.elastic.co/downloads/elastic-agent) for the full list of available packages.

    1. If you are enrolling the agent in a {{fleet-server}} that uses your organization’s certificate you *must* add the `--certificate-authorities` option to the command provided in the in-product instructions. If you do not include the certificate, you will see the following error: "x509: certificate signed by unknown authority".

        :::{image} images/kibana-agent-flyout.png
        :alt: Add agent flyout in {kib}
        :class: screenshot
        :::


After about a minute, the agent will enroll in {{fleet}}, download the configuration specified in the agent policy, and start collecting data.

**Notes:**

* If you encounter an "x509: certificate signed by unknown authority" error, you might be trying to enroll in a {{fleet-server}} that uses self-signed certs. To fix this problem in a non-production environment, pass the `--insecure` flag. For more information, refer to the [troubleshooting guide](/troubleshoot/ingest/fleet/common-problems.md#agent-enrollment-certs).
* Optionally, you can use the `--tag` flag to specify a comma-separated list of tags to apply to the enrolled {{agent}}. For more information, refer to [Filter list of Agents by tags](/reference/ingestion-tools/fleet/filter-agent-list-by-tags.md).
* Refer to [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md) for the location of installed {{agent}} files.
* Because {{agent}} is installed as an auto-starting service, it will restart automatically if the system is rebooted.

To confirm that {{agent}} is installed and running, open the **Agents** tab in {{fleet}}.

:::{image} images/kibana-fleet-agents.png
:alt: {{fleet}} showing enrolled agents
:class: screenshot
:::

::::{tip}
If the status hangs at Enrolling, make sure the `elastic-agent` process is running.
::::


If you run into problems:

* Check the {{agent}} logs. If you use the default policy, agent logs and metrics are collected automatically unless you change the default settings. For more information, refer to [Monitor {{agent}} in {{fleet}}](/reference/ingestion-tools/fleet/monitor-elastic-agent.md).
* Refer to the [troubleshooting guide](/troubleshoot/ingest/fleet/common-problems.md).

For information about managing {{agent}} in {{fleet}}, refer to [Centrally manage {{agent}}s in {{fleet}}](/reference/ingestion-tools/fleet/manage-elastic-agents-in-fleet.md).
