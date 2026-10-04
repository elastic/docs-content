---
description: Configure Elastic Security runtime protection for Linux VMs and Kubernetes workloads after you deploy it.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Manage cloud workload protection

Cloud workload protection detects and blocks threats on your cloud compute while it runs. Use these pages to configure protection after you deploy it. To deploy it, refer to [Set up](/solutions/security/set-up.md).

## Linux VMs

Cloud workload protection for VMs uses {{elastic-defend}} to detect and prevent malicious behavior and malware on your Linux VMs. It also captures process, file, and network activity, which you can use with Elastic's prebuilt detection rules and {{ml}} models.

- [Cloud workload protection for VMs](/solutions/security/cloud/cloud-workload-protection-for-vms.md)
- [Capture environment variables](/solutions/security/cloud/capture-environment-variables.md)

## Kubernetes

```{applies_to}
stack: beta 9.3
serverless:
  security: beta
```

Cloud workload protection for Kubernetes uses the Defend for Containers (D4C) integration to identify, and optionally block, unexpected system behavior in Kubernetes containers.

- [Cloud workload protection for Kubernetes](/solutions/security/cloud/d4c/d4c-overview.md)
- [Container workload protection policies](/solutions/security/cloud/d4c/d4c-policies.md)
- [Kubernetes dashboard](/solutions/security/cloud/d4c/kubernetes-dashboard.md)
