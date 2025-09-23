---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-deployment-sso.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure SSO for deployments [ece-deployment-sso]

The single sign-on (SSO) feature in ECE allows `platform admins` and `deployment managers` to log in to their {{kib}} instances automatically after they are logged in to ECE.

::::{note} 
Single sign-on is not available for system deployments; you need to use credentials to log in to them.
::::


To use single sign-on, you first need to [configure the API base URL](/deploy-manage/deploy/cloud-enterprise/change-ece-api-url.md). After this is set, all new deployments are SSO-enabled automatically, and existing deployments become SSO-enabled after any plan changes are applied.

