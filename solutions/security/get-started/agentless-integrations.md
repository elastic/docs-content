---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/security-agentless-integrations.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Agentless integrations [agentless-integrations]

Agentless integrations provide a means to ingest data while avoiding the orchestration, management, and maintenance needs associated with standard ingest infrastructure. Using agentless integrations makes manual agent deployment unnecessary, allowing you to focus on your data instead of the agent that collects it.

::::{important}
During technical preview, there are no additional costs associated with deploying agentless integrations. 
There is a limit of 5 agentless integrations per project. 
::::

## Requirements

* Agentless integrations are supported only on {{ech}}, {{sec-serverless}}, and {{obs-serverless}} deployments.
* On {{ech}}, agentless integrations require a working [{{fleet-server}}](/reference/fleet/fleet-server).
* To set up a new agentless integration, you need the `Actions and connectors: all` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Generally available (GA) agentless integrations

Elastic fully supports agentless deployment for the Cloud Security Posture Management (CSPM) integration. Using this integration’s agentless deployment option, you can enable Elastic’s CSPM capabilities just by providing the necessary credentials. Agentless CSPM deployments support AWS, Azure, and GCP accounts.

To learn more about agentless CSPM deployments, refer to the getting started guides for CSPM on [AWS](../cloud/get-started-with-cspm-for-aws.md), [Azure](../cloud/get-started-with-cspm-for-azure.md), or [GCP](../cloud/get-started-with-cspm-for-gcp.md)


## Beta agentless integrations

Agentless deployment for other integrations is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.

For setup guides and to learn more about Elastic's integrations, including whether each supports agentless deployment, refer to [Elastic integrations](https://docs.elastic.co/en/integrations/).

## Filter the integrations page to find agentless integrations

```{applies_to}
stack: ga 9.2
serverless: ga 
```

To identify which integrations support agentless deployment:

1. In {{kib}}, go to **Integrations**.
2. On the left, enable the **Only agentless integrations** toggle. 
