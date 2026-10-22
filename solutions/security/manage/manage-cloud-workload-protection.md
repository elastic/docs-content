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

Cloud workload protection detects threats on your Linux VMs and Kubernetes workloads while they run, and can block some of them. It also sends process, file, and network activity to {{elastic-sec}}, where Elastic's prebuilt detection rules and {{ml}} models can use it to find threats.

To deploy cloud workload protection first, refer to [Set up](/solutions/security/set-up.md). To review cloud configuration findings and benchmarks instead, refer to [Cloud Security](/solutions/security/cloud.md).

## How protection works on VMs and Kubernetes

Cloud workload protection uses one integration for VMs and another for Kubernetes containers:

- **Linux VMs**: Use {{elastic-defend}}, the same integration that protects your other hosts. It detects and prevents malicious behavior, memory threats, and malware. To collect session data by default, select one of the **Cloud workloads** presets when you configure the integration.
- {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` **Kubernetes containers**: Use the Defend for Containers (D4C) integration. Each D4C policy has selectors, which match file and process operations, and responses, which log, alert on, or block the operations that match. The default policy logs process activity for threat detection, and alerts on drift, which is a change to a container's executables.

## Where to start

| Your goal | Start here |
|---|---|
| Understand how {{elastic-defend}} protects Linux VMs | [Cloud workload protection for VMs](/solutions/security/cloud/cloud-workload-protection-for-vms.md) |
| Add environment variables to the process data that {{agent}} collects | [Capture environment variables](/solutions/security/cloud/capture-environment-variables.md) |
| {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` Learn how D4C protects Kubernetes containers, and which platforms it supports | [Cloud workload protection for Kubernetes](/solutions/security/cloud/d4c/d4c-overview.md) |
| {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` Allow expected container behavior and block drift | [Container workload protection policies](/solutions/security/cloud/d4c/d4c-policies.md) |
| {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` Monitor your Kubernetes clusters and workloads | [Kubernetes dashboard](/solutions/security/dashboards/kubernetes-dashboard.md) |

## Next steps

After you configure cloud workload protection, you can:

- [Manage {{elastic-defend}}](/solutions/security/manage-elastic-defend.md) to tune policies and exceptions for your Linux VMs.
- [Install prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that detect threats in container and cloud workload data.
- Review a Linux process session in [Session View](/solutions/security/investigate/session-view.md) to investigate suspicious activity.
