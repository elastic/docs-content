---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html
applies_to:
  deployment:
    ece:
    eck:
    ess:
    self:
products:
  - id: elasticsearch
---

# {{es}} privileges [security-privileges]

Roles are governed by a set of configurable privileges grouped into these categories:

* **cluster**, which you can use to manage core operations like snapshots, managing API keys, autoscaling, and cross-cluster functionality.
* **indices**, which govern document-level access, index and data stream metadata information, and more.
* **run-as**, which allows for secure impersonation.
* **application**, which enable external applications to define and store their privilege models within {{es}} roles.

When creating roles, refer to [{{es}} privileges](elasticsearch://reference/elasticsearch/security-privileges.md) for a complete list of available privileges. 

To learn how to assign privileges to a role, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).