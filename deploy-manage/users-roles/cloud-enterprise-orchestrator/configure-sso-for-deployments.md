---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-deployment-sso.html
---

# Configure SSO for deployments [ece-deployment-sso]

The single sign-on (SSO) feature in ECE allows `platform admins` and `deployment managers` to log in to their Kibana and Enterprise Search instances automatically once they are logged in to ECE.

::::{note} 
Single sign-on is not available for system deployments; you need to use credentials to log in to them.
::::


To use single sign-on you first need to [configure the API base URL](../../deploy/cloud-enterprise/change-ece-api-url.md). Once this is set, all new deployments are SSO-enabled automatically, and existing deployments become SSO-enabled after any plan changes are applied.

