---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/security-agentless-integrations.html
applies_to:
  stack: all
  serverless:
    security: all
---

# Agentless integrations [agentless-integrations]

Agentless integrations provide a means to ingest data while avoiding the orchestration, management, and maintenance needs associated with standard ingest infrastructure. Using agentless integrations makes manual agent deployment unnecessary, allowing you to focus on your data instead of the agent that collects it.

We support the following agentless integrations: 

## Generally available (GA) agentless integrations

::::{note}
For a single {{serverless-full}} project, a maxium of 30 agentless deployments are supported.
::::

Cloud security posture management (CSPM). Using this integration’s agentless deployment option, you can enable Elastic’s CSPM capabilities just by providing the necessary credentials. Agentless CSPM deployments support AWS, Azure, and GCP accounts.

To learn more about agentless CSPM deployments, refer to the getting started guides for CSPM on [AWS](../cloud/get-started-with-cspm-for-aws.md),  [Azure](../cloud/get-started-with-cspm-for-azure.md), or [GCP](../cloud/get-started-with-cspm-for-gcp.md)

## Beta agentless integrations

::::{warning}
Agentless deployment for the following integrations is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.

While agentless deployment for these integrations is in beta, for a single {{serverless-full}} project a maxium of five agentless deployments are currently supported.
::::

1. AbuseCH
2. CrowdStrike  
3. Google SecOps 
4. Google Security Command Center
5. Google Workspace
6. Microsoft 365 Defender
7. Microsoft Defender for Endpoint
8. Microsoft Sentinel
9. Okta
10. Qualys VMDR
11. SentinelOne Zscaler
12. Tenable IO
13. Wiz
14. Zscaler ZIA

To learn more about these integrations and find setup guides, refer to [Elastic integrations](https://docs.elastic.co/en/integrations/).