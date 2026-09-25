---
navigation_title: Protect cloud workloads
description: Detect and prevent threats on Linux virtual machines and in Kubernetes containers with Elastic Defend and Defend for Containers.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Protect cloud workloads [protect-cloud-workloads]

Cloud workload protection detects and prevents threats at runtime on the virtual machines and containers that run your cloud applications. To evaluate your cloud configuration against security best practices or scan for vulnerabilities instead, refer to [Cloud Security](/solutions/security/cloud.md).

| Workload | What it does |
|---|---|
| [Linux virtual machines](/solutions/security/cloud/cloud-workload-protection-for-vms.md) | Uses {{elastic-defend}} to detect and prevent malicious behavior and malware on your Linux VMs, and captures process, file, and network telemetry for use with Elastic's out-of-the-box detection rules and {{ml}} models. |
| [Kubernetes containers](/solutions/security/cloud/d4c/d4c-overview.md) {applies_to}`stack: beta 9.3` {applies_to}`serverless: beta` | Uses the Defend for Containers (D4C) integration to identify and optionally block unexpected system behavior in Kubernetes containers. |
