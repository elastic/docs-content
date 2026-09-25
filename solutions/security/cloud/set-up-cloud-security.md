---
navigation_title: Set up cloud security
description: Connect your cloud accounts and Kubernetes clusters to Elastic Security and grant the privileges needed for CSPM, KSPM, Cloud Asset Discovery, and CNVM.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up cloud security [set-up-cloud-security]

Use these pages to connect your cloud accounts and Kubernetes clusters to {{elastic-sec}} and grant the privileges each cloud security capability needs. For an overview of what each capability does, refer to [Cloud Security](/solutions/security/cloud.md).

In {{sec-serverless}}, first [enable cloud security features](/solutions/security/cloud/enable-cloud-security-features.md) for your project.

| Capability | Setup pages |
|---|---|
| [Cloud Security Posture Management (CSPM)](/solutions/security/cloud/cloud-security-posture-management.md) | [AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md), [GCP](/solutions/security/cloud/get-started-with-cspm-for-gcp.md), [Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md), [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md) |
| [Kubernetes Security Posture Management (KSPM)](/solutions/security/cloud/kubernetes-security-posture-management.md) | [Get started with KSPM](/solutions/security/cloud/get-started-with-kspm.md) |
| [Cloud Asset Discovery](/solutions/security/cloud/asset-disc.md) {applies_to}`stack: preview 9.1` {applies_to}`serverless: preview` | [AWS](/solutions/security/cloud/asset-disc-aws.md), [GCP](/solutions/security/cloud/asset-disc-gcp.md), [Azure](/solutions/security/cloud/asset-disc-azure.md) |
| [Cloud Native Vulnerability Management (CNVM)](/solutions/security/cloud/cloud-native-vulnerability-management.md) | [Get started with CNVM](/solutions/security/cloud/get-started-with-cnvm.md), [CNVM privilege requirements](/solutions/security/cloud/cnvm-privilege-requirements.md) |

After setup, you review findings, benchmarks, and dashboards for each capability in [Cloud Security](/solutions/security/cloud.md).
