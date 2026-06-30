---
navigation_title: "{{eck}}"
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---

# Secure your {{eck}} orchestrator [eck-securing-considerations]

This section covers security settings for your {{eck}} orchestrator.

**Orchestrator-level security**

- [Restrict cross-namespace resources associations](/deploy-manage/deploy/cloud-on-k8s/restrict-cross-namespace-resource-associations.md)
- [Isolate pods with network policies](/deploy-manage/security/k8s-network-policies.md)
- [Secure the metrics endpoint](/deploy-manage/monitor/orchestrators/k8s-securing-metrics-endpoint.md)

Also refer to [](/deploy-manage/deploy/cloud-on-k8s/configure.md) for more information about configuring {{eck}}.

**Additional deployment-level security settings**

Additional security settings are available for you to configure individually for each deployment orchestrated using {{eck}}. Refer to [](secure-your-cluster-deployment.md) for more information.

