---
navigation_title: Switch a self-installation
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-integration-upgrade-steps.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Switch a self-installation to the APM integration [apm-integration-upgrade-steps]

1. [Upgrade the {{stack}}](#apm-integration-upgrade-1)
2. [Add a {{fleet}} Server](#apm-integration-upgrade-2)
3. [Install a {{fleet}}-managed {{agent}}](#apm-integration-upgrade-3)
4. [Add the APM integration](#apm-integration-upgrade-4)
5. [Stop the APM Server](#apm-integration-upgrade-5)

## Upgrade the {{stack}} [apm-integration-upgrade-1]

The {{stack}} ({{es}} and {{kib}}) must be upgraded to version 7.14 or higher. See the [{{stack}} Installation and Upgrade Guide](/deploy-manage/upgrade/deployment-or-cluster.md) for guidance.

Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md) for important changes between your current APM version and this one.

## Add a {{fleet}} Server [apm-integration-upgrade-2]

{{fleet}} Server is a component of the {{stack}} used to centrally manage {{agent}}s. The APM integration requires a {{fleet}} Server to be running and accessible to your hosts. Add a {{fleet}} Server by following [this guide](/reference/fleet/deployment-models.md).

::::{tip}
If you’re upgrading a self-managed deployment of the {{stack}}, you’ll need to enable [{{es}} security](/deploy-manage/deploy/self-managed/installing-elasticsearch.md) and the [API key service](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md).
::::

After adding your {{fleet}} Server host and generating a service token, the in-product help in {{kib}} will provide a command to run to start an {{agent}} as a {{fleet}} Server. Commands may require administrator privileges.

Verify {{fleet}} Server is running by navigating to **{{fleet}}** > **Agents** in {{kib}}.

## Install a {{fleet}}-managed {{agent}} [apm-integration-upgrade-3]

::::{note}
It’s possible to install the Elastic APM integration on the same {{agent}} that is running the {{fleet}} Server integration. For this use case, skip this step.
::::

The {{fleet}}-managed {{agent}} will run the Elastic APM integration on your edge nodes, next to your applications. To install a {{fleet}}-managed {{agent}}, follow [this guide](/reference/fleet/install-fleet-managed-elastic-agent.md).

## Add the APM integration [apm-integration-upgrade-4]

The APM integration receives performance data from your APM agents, validates and processes it, and then transforms the data into {{es}} documents.

To add the APM integration, see [Step 2: Add and configure the APM integration](/solutions/observability/apm/apm-server/fleet-managed.md#add-apm-integration). Only complete the linked step (not the entire quick start guide). If you’re adding the APM integration to a {{fleet}}-managed {{agent}}, you can use the default policy. If you’re adding the APM integration to the {{fleet-server}}, use the policy that the {{fleet-server}} is running on.

::::{tip}
You’ll configure the APM integration in this step. See [Configure APM Server](/solutions/observability/apm/apm-server/configure.md) for a reference of all available settings. As long as the APM integration is configured with the same secret token or you have API keys enabled on the same host, no reconfiguration is required in your APM agents.
::::

## Stop the APM Server [apm-integration-upgrade-5]

Once data from upgraded APM agents is visible in the Applications UI, it’s safe to stop the APM Server process.

Congratulations — you now have the latest and greatest in Elastic APM!
