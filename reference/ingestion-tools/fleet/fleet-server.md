---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-server.html
---

# What is Fleet Server? [fleet-server]

{{fleet-server}} is a component that connects {{agent}}s to {{fleet}}. It supports many {{agent}} connections and serves as a control plane for updating agent policies, collecting status information, and coordinating actions across {{agent}}s. It also provides a scalable architecture. As the size of your agent deployment grows, you can deploy additional {{fleet-server}}s to manage the increased workload.

* On-premises {{fleet-server}} is not currently available for use in an [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment. We recommend using the hosted {{fleet-server}} that is included and configured automatically in {{serverless-short}} {{observability}} and Security projects.

The following diagram shows how {{agent}}s communicate with {{fleet-server}} to retrieve agent policies:

:::{image} images/fleet-server-agent-policies-diagram.png
:alt: {{fleet-server}} Cloud deployment model
:::


1. When a new agent policy is created, the {{fleet}} UI saves the policy to a {{fleet}} index in {{es}}.
2. To enroll in the policy, {{agent}}s send a request to {{fleet-server}}, using the enrollment key generated for authentication.
3. {{fleet-server}} monitors {{fleet}} indices, picks up the new agent policy from {{es}}, then ships the policy to all {{agent}}s enrolled in that policy. {{fleet-server}} may also write updated policies to the {{fleet}} index to manage coordination between agents.
4. {{agent}} uses configuration information in the policy to collect and send data to {{es}}.
5. {{agent}} checks in with {{fleet-server}} for updates, maintaining an open connection.
6. When a policy is updated, {{fleet-server}} retrieves the updated policy from {{es}} and sends it to the connected {{agent}}s.
7. To communicate with {{fleet}} about the status of {{agent}}s and the policy rollout, {{fleet-server}} writes updates to {{fleet}} indices.

::::{admonition}
**Does {{fleet-server}} run inside of {{agent}}?**

{{fleet-server}} is a subprocess that runs inside a deployed {{agent}}. This means the deployment steps are similar to any {{agent}}, except that you enroll the agent in a special {{fleet-Server}} policy. Typically—​especially in large-scale deployments—​this agent is dedicated to running {{fleet-server}} as an {{agent}} communication host and is not configured for data collection.

::::



## Service account [fleet-security-account]

{{fleet-server}} uses a service token to communicate with {{es}}, which contains a `fleet-server` service account. Each {{fleet-server}} can use its own service token, and you can share it across multiple servers (not recommended). The advantage of using a separate token for each server is that you can invalidate each one separately.

You can create a service token by either using the {{fleet}} UI or the {{es}} API. For more information, refer to [Deploy {{fleet-server}} on-premises and {{es}} on Cloud](/reference/ingestion-tools/fleet/add-fleet-server-mixed.md) or [Deploy on-premises and self-managed](/reference/ingestion-tools/fleet/add-fleet-server-on-prem.md), depending on your deployment model.


## {{fleet-server}} High-availability operations [fleet-server-HA-operations]

{{fleet-server}} is stateless. Connections to the {{fleet-server}} therefore can be load balanced as long as the {{fleet-server}} has capacity to accept more connections. Load balancing is done on a round-robin basis.

How you handle high-availability, fault-tolerance, and lifecycle management of {{fleet-server}} depends on the deployment model you use.


## Learn more [_learn_more]

To learn more about deploying and scaling {{fleet-server}}, refer to:

* [Deploy on {{ecloud}}](/reference/ingestion-tools/fleet/add-fleet-server-cloud.md)
* [Deploy {{fleet-server}} on-premises and {{es}} on Cloud](/reference/ingestion-tools/fleet/add-fleet-server-mixed.md)
* [Deploy on-premises and self-managed](/reference/ingestion-tools/fleet/add-fleet-server-on-prem.md)
* [{{fleet-server}} scalability](/reference/ingestion-tools/fleet/fleet-server-scalability.md)
* [Monitor a self-managed {{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server-monitoring.md)


## {{fleet-server}} secrets configuration [fleet-server-secrets-config]

Secrets used to configure {{fleet-server}} can either be directly specified in configuration or provided through secret files. See [{{fleet-server}} Secrets](/reference/ingestion-tools/fleet/fleet-server-secrets.md) for more information.
