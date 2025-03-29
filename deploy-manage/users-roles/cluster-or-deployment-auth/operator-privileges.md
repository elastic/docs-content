---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/operator-privileges.html
applies_to:
  deployment:
    ess: 
    ece: 
    eck: 
---

# Operator privileges [operator-privileges]

::::{admonition} Indirect use only
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::

With a typical {{es}} deployment, people who administer the cluster also operate the cluster at the infrastructure level. User authorization based on [role-based access control (RBAC)](user-roles.md) is effective and reliable for this environment. However, in more managed environments, such as [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body), there is a distinction between the operator of the cluster infrastructure and the administrator of the cluster.

Operator privileges limit some functionality to operator users *only*. Operator users are just regular {{es}} users with access to specific [operator-only functionality](operator-only-functionality.md). These privileges are not available to cluster administrators, even if they log in as a highly privileged user such as the `elastic` user or another user with the `superuser` role. By limiting system access, operator privileges enhance the {{es}} security model while safeguarding user capabilities.

Operator privileges are enabled on {{ecloud}}, which means that some infrastructure management functionality is restricted and cannot be accessed by your administrative users. This capability protects your cluster from unintended infrastructure changes.




