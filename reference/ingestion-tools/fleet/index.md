---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/fleet-and-elastic-agent.html
  - https://www.elastic.co/guide/en/fleet/current/fleet-elastic-agent-quick-start.html
  - https://www.elastic.co/guide/en/kibana/current/fleet.html
  - https://www.elastic.co/guide/en/fleet/current/fleet-overview.html
  - https://www.elastic.co/guide/en/fleet/current/index.html
---

# Fleet and Elastic Agent [fleet-and-elastic-agent]

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):
$$$package-registry-intro$$$

## {{agent}} [elastic-agent]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. A single agent makes it easier and faster to deploy monitoring across your infrastructure. Each agent has a single policy you can update to add integrations for new data sources, security protections, and more.

As the following diagram illustrates, {{agent}} can monitor the host where it's deployed, and it can collect and forward data from remote services and hardware where direct deployment is not possible.

:::{image} images/agent-architecture.png
:alt: Image showing {{agent}} collecting data from local host and remote services
:::

To learn about installation options, refer to [](/reference/ingestion-tools/fleet/install-elastic-agents.md).

:::{note}
Using {{fleet}} and {{agent}} {{serverless-full}}? Please note these [restrictions](/reference/ingestion-tools/fleet/fleet-agent-serverless-restrictions.md).
:::

:::{tip}
Looking for a general guide that explores all of your options for ingesting data? Check out [Adding data to Elasticsearch](/manage-data/ingest.md).
:::

## {{integrations}}

[{{integrations}}](integration-docs://docs/reference/index.md) provide an easy way to connect Elastic to external services and systems, and quickly get insights or take action. They can collect new sources of data, and they often ship with out-of-the-box assets like dashboards, visualizations, and pipelines to extract structured fields out of logs and events. This makes it easier to get insights within seconds. Integrations are available for popular services and platforms like Nginx or AWS, as well as many generic input types like log files.

{{kib}} provides a web-based UI to add and manage integrations. You can browse a unified view of available integrations that shows both {{agent}} and {{beats}} integrations.

:::{image} images/integrations.png
:alt: Integrations page
:::

## {{agent}} policies [configuring-integrations]

Agent policies specify which integrations you want to run and on which hosts. You can apply an {{agent}} policy to multiple agents, making it even easier to manage configuration at scale.

:::{image} images/add-integration.png
:alt: Add integration page
:::

When you add an integration, you configure inputs for logs and metrics, such as the path to your Nginx access logs. When you're done, you save the integration to an {{agent}} policy. The next time enrolled agents check in, they receive the update. Having the policies automatically deployed is more convenient than doing it yourself by using SSH, Ansible playbooks, or some other tool.

For more information, refer to [](/reference/ingestion-tools/fleet/agent-policy.md).

If you prefer infrastructure as code, you may use YAML files and APIs. {{fleet}} has an API-first design. Anything you can do in the UI, you can also do using the API. This makes it easy to automate and integrate with other systems.

## {{package-registry}} [package-registry-intro]

The {{package-registry}} is an online package hosting service for the {{agent}} integrations available in {{kib}}.

{{kib}} connects to the {{package-registry}} at `epr.elastic.co` using the Elastic Package Manager, downloads the latest integration package, and stores its assets in {{es}}. This process typically requires an internet connection because integrations are updated and released periodically. You can find more information about running the {{package-registry}} in air-gapped environments in the section about [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md).

## Elastic Artifact Registry [artifact-registry-intro]

{{fleet}} and {{agent}} require access to the public Elastic Artifact Registry. The {{agent}} running on any of your internal hosts should have access to `artifacts.elastic.co` in order to perform self-upgrades and install of certain components which are needed for some of the data integrations.

Additionally, access to `artifacts.security.elastic.co` is needed for {{agent}} updates and security artifacts when using {{elastic-defend}}.

You can find more information about running the above mentioned resources in air-gapped environments in the section about [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md).

## Central management in {{fleet}} [central-management]

{{fleet}} provides a web-based UI in {{kib}} for centrally managing {{agents}} and their policies.

You can see the state of all your {{agents}} in {{fleet}}. On the **Agents** page, you can see which agents are healthy or unhealthy, and the last time they checked in. You can also see the version of the {{agent}} binary and policy.

:::{image} images/kibana-fleet-agents.png
:alt: Agents page
:::

{{fleet}} in {{kib}} enables you to manage {{elastic-agent}} installations in standalone or {{fleet}} mode.

Standalone mode requires you to manually configure and manage the agent locally. It is recommended for advanced users only.

{{fleet}} mode offers several advantages:

* A central place to configure and monitor your {{agents}}.
* Ability to trigger {{agent}} binary and policy upgrades remotely.
* An overview of the data ingest in your {{es}} cluster.

:::{image} images/fleet-start.png
:alt: {{fleet}} app in {{kib}}
:class: screenshot
:::

{{fleet}} serves as the communication channel back to the {{agents}}. Agents check in for the latest updates on a regular basis. You can have any number of agents enrolled into each agent policy, which allows you to scale up to thousands of hosts.

When you make a change to an agent policy, all the agents receive the update during their next check-in. You no longer have to distribute policy updates yourself.

When you're ready to upgrade your {{agent}} binaries or integrations, you can initiate upgrades in {{fleet}}, and the {{agents}} running on your hosts will upgrade automatically.

### Roll out changes to many {{agents}} quickly [selective-agent-management]

Some subscription levels support bulk select operations, including:

* Selective binary updates
* Selective agent policy reassignment
* Selective agent unenrollment

This capability enables you to apply changes and trigger updates across many {{agents}} so you can roll out changes quickly across your organization.

For more information, refer to [{{stack}} subscriptions](https://www.elastic.co/subscriptions).

## {{fleet-server}} [fleet-server-intro]

{{fleet-server}} is the mechanism to connect {{agents}} to {{fleet}}. It allows for a scalable infrastructure and is supported in {{ecloud}} and self-managed clusters. {{fleet-server}} is a separate process that communicates with the deployed {{agents}}. It can be started from any available x64 architecture {{agent}} artifact.

For more information, refer to [](/reference/ingestion-tools/fleet/fleet-server.md).

:::{admonition} {{fleet-server}} with {{serverless-full}}
On-premises {{fleet-server}} is not currently available for use with
{{serverless-full}} projects. In a {{serverless-short}}
environment we recommend using {{fleet-server}} on {{ecloud}}.
:::

## {{es}} as the communication layer [fleet-communication-layer]

All communication between the {{fleet}} UI and {{fleet-server}} happens through {{es}}. {{fleet}} writes policies, actions, and any changes to the `fleet-*` indices in {{es}}. Each {{fleet-server}} monitors the indices, picks up changes, and ships them to the {{agents}}. To communicate to {{fleet}} about the status of the {{agents}} and the policy rollout, the Fleet Servers write updates to the `fleet-*` indices.

## {{agent}} self-protection [agent-self-protection]

On macOS and Windows, when the {{elastic-defend}} integration is added to the agent policy, {{elastic-endpoint}} can prevent malware from executing on the host. For more information, refer to [{{elastic-endpoint}} self-protection](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md).

## Data streams make index management easier [data-streams-intro]

The data collected by {{agent}} is stored in indices that are more granular than you'd get by default with the {{beats}} shippers or APM Server. This gives you more visibility into the sources of data volume, and control over lifecycle management policies and index permissions. These indices are called [data streams](/reference/ingestion-tools/fleet/data-streams.md).

## Quick starts [fleet-elastic-agent-quick-start]

Want to get up and running with {{fleet}} and {{agent}} quickly? Read our getting started guides:

* [Get started with logs and metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)
* [Get started with APM](/solutions/observability/apps/get-started-with-apm.md)
