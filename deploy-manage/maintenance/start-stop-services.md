---
applies_to:
  deployment:
    ess:
    ece:
    self:
products:
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: elasticsearch
  - id: kibana
---

# Start and stop services

This section covers the recommended procedures for:

* [starting and stopping self-managed {{es}} nodes](start-stop-services/start-stop-elasticsearch.md)
* [starting and stopping self-managed {{kib}} instances](start-stop-services/start-stop-kibana.md)
* [restarting an ECE deployment](start-stop-services/restart-an-ece-deployment.md)
* [restarting {{ech}} deployments](start-stop-services/restart-cloud-hosted-deployment.md)
* [full cluster and rolling restarts for self-managed clusters](start-stop-services/full-cluster-restart-rolling-restart-procedures.md)

::::{note}
In ECK, when a resource – like {{es}} or {{kib}} – is declared, the reconciliation loop ensures the desired state is maintained. There is no built-in stop mechanism in Kubernetes because it’s designed for declarative state management. You either define a resource, and Kubernetes ensures it’s running, or you delete it. You can restart instances by deleting Pods, as the platform will start them immediately.

::::

Following these guidelines helps prevent data loss, minimize downtime, and maintain optimal performance across different environments.
