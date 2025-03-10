---
navigation_title: "{{ecloud}}"
applies_to:
  deployment:
    ess: ga
  serverless: ga
---

# Secure your Elastic Cloud organization [ec-securing-considerations]

:::{warning}
**This page is a work in progress.** 
:::


## TLS certificate management

TLS certificates apply security controls to network communications. They encrypt data in transit, verify the identity of connecting parties, and help prevent man-in-the-middle attacks.

For your **{{ech}}** deployments and serverless projects hosted on {{ecloud}}, TLS certificates are managed automatically.

## Access control

Define which users can access your {{ecloud}} organization using the following methods:

- [SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md)
- [Role-based access control](/deploy-manage/users-roles/cloud-organization/manage-users.md)
- [Cloud API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md)


## Next step: secure your deployments and clusters

This section covered security principles and options at the environment level. You can take further measures individually for each deployment or cluster that you're running on this environment. Refer to [](secure-your-cluster-deployment.md).
