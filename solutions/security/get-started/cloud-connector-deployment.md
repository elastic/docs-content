---
applies_to:
  stack: preview 9.2
  serverless:
    security: preview
---

# Deploy integrations using cloud connector

Cloud connector deployment for integrations allows you to quickly provide Elastic with access to your third-party cloud service provider accounts. This deployment method reduces administrative burden by eliminating the need to keep track of authentication details such as API keys or passwords. Ultimately, cloud connectors are meant to make it easy to manage deployments with many integrations collecting data from CSPs, by providing a simple, reusable means of authentication. 

## Where is cloud connector deployment supported?

At the current stage of this technical preview, a limited selection of cloud providers and integrations are supported.

You can use cloud connector deployment to authenticate with AWS and Azure while deploying either Elastic's Cloud Security Posture Management (CSPM) or Asset Discovery integration. For deployment instructions, refer to:

- Asset Discovery: Asset Discovery on Azure; Asset Discovery on AWS
- CSPM: CSPM on Azure; CSPM on AWS