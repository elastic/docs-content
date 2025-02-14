---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/security-agentless-integrations.html
---

# Agentless integrations [agentless-integrations]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


Agentless integrations provide a means to ingest data while avoiding the orchestration, management, and maintenance needs associated with standard ingest infrastructure. Using agentless integrations makes manual agent deployment unnecessary, allowing you to focus on your data instead of the agent that collects it.

We currently support one agentless integration: cloud security posture management (CSPM). Using this integration’s agentless deployment option, you can enable Elastic’s CSPM capabilities just by providing the necessary credentials. Agentless CSPM deployments support AWS, Azure, and GCP accounts.

To learn more about agentless CSPM deployments, refer to the getting started guides for CSPM on [AWS](../cloud/get-started-with-cspm-for-aws.md),  [Azure](../cloud/get-started-with-cspm-for-azure.md), or [GCP](../cloud/get-started-with-cspm-for-gcp.md)
