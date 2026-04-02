---
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
  serverless:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
---

# Uninstall

Uninstalling Elastic components, such as {{es}} clusters, deployments, or orchestrators, may be necessary for several reasons. You might need to decommission a host, scale down a self-managed cluster, recover from an installation issue that can't be resolved, or start fresh with a clean setup.

Different Elastic environments require different uninstallation steps. Choose the guide that matches your setup:

* Uninstall an orchestrator:
  * [Uninstall an {{ece}} host](/deploy-manage/uninstall/uninstall-elastic-cloud-enterprise.md)
  * [Uninstall {{eck}} operator](/deploy-manage/uninstall/uninstall-elastic-cloud-on-kubernetes.md)

* Delete an orchestrated deployment:
  * [{{ech}} deployments](/deploy-manage/uninstall/delete-a-cloud-deployment.md#elastic-cloud-hosted)
  * [Serverless projects](/deploy-manage/uninstall/delete-a-cloud-deployment.md#serverless)
  * [{{ece}} deployments](/deploy-manage/uninstall/delete-a-cloud-deployment.md#ece)

:::{note}
You can uninstall {{es}} nodes or {{kib}} instances on self-managed clusters, but step-by-step instructions are not currently available. For more details on the implications of removing {{es}} nodes, refer to [](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md).
:::

