---
applies_to:
  deployment:
    ess:
    ece:
    eck:
navigation_title: Orchestrator-managed users
products:
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elasticsearch
  - id: kibana
---

# Orchestrator-managed users

The {{es}} provides default user credentials to help you get up and running.

In self-managed clusters, these users are created as [built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

In orchestrated deployments (ECH, ECE, and ECK), the `elastic` user is managed by the platform, while other default users are not accessible to end users. The way that credentials are managed for this and other internal users depends on your orchestrator.
In this section, you'll learn how to manage credentials for orchestrator-managed users:

* In {{ece}} and {{ech}}, [learn how to reset password for the `elastic` user](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md).
* In {{eck}}, [learn how to manage the `elastic` user, and how to rotate all auto-generated credentials used by ECK](/deploy-manage/users-roles/cluster-or-deployment-auth/managed-credentials-eck.md).

:::{{tip}}
To learn more about built-in users in self-managed clusters, and how to reset built-in user passwords, refer to: 

* [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md)
* [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-sm.md).