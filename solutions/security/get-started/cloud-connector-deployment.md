---
navigation_title: Cloud connector authentication for agentless
applies_to:
  stack: preview 9.2
  serverless:
    security: preview
---

# Quickly authenticate agentless integrations using cloud connector

Cloud connector authentication for agentless integrations allows you to quickly provide Elastic with access to your third-party cloud service provider accounts. This authentication method reduces administrative burden by eliminating the need to keep track of credentials such as API keys or passwords. Cloud connectors provide a simple, reusable means of authentication, making it easier to manage deployments with many integrations collecting data from multiple cloud security providers.

## Where is cloud connector deployment supported?

At the current stage of this technical preview, a limited selection of cloud providers and integrations are supported.

You can use cloud connector deployment to authenticate with AWS and Azure while deploying either Elastic's Cloud Security Posture Management (CSPM) or Asset Discovery integration. For deployment instructions, refer to:

- Asset Discovery: Asset Discovery on Azure; Asset Discovery on AWS
- CSPM: CSPM on Azure; CSPM on AWS