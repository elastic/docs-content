---
description: Set up Cloud Security Posture Management, Kubernetes Security Posture Management, Cloud Asset Discovery, and Cloud Native Vulnerability Management in Elastic Security.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up cloud security

{{elastic-sec}}'s cloud security features find risks in your cloud accounts and Kubernetes clusters. They check your configuration against security best practices, list your cloud assets, and scan your cloud workloads for known vulnerabilities.

You set up each feature by adding its integration and connecting it to your cloud provider or cluster. After setup, each integration sends its results to {{elastic-sec}}, where you can review them in [Cloud Security](/solutions/security/cloud.md).

## How the cloud security features work

Each feature answers a different question about your cloud environment:

- **Cloud Security Posture Management (CSPM)**: Checks the services in your AWS, GCP, and Azure accounts, such as storage, compute, and identity and access management (IAM), against benchmarks from the Center for Internet Security (CIS).
- **Kubernetes Security Posture Management (KSPM)**: Checks the components of your Kubernetes clusters against CIS benchmarks.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1` **Cloud Asset Discovery**: Builds an inventory of the resources in your AWS, GCP, and Azure accounts.
- **Cloud Native Vulnerability Management (CNVM)**: Scans your AWS EC2 Linux workloads for known vulnerabilities.

## Where to start

| Your goal | Start here |
|---|---|
| Check your AWS, GCP, or Azure accounts for misconfigurations | [CSPM for AWS](/solutions/security/cloud/get-started-with-cspm-for-aws.md), [CSPM for GCP](/solutions/security/cloud/get-started-with-cspm-for-gcp.md), or [CSPM for Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md) |
| Give users access to view or manage CSPM data | [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md) |
| Check your Kubernetes clusters for misconfigurations | [Get started with KSPM](/solutions/security/cloud/get-started-with-kspm.md) |
| {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1` List the resources in your cloud accounts | [Cloud Asset Discovery for AWS](/solutions/security/cloud/asset-disc-aws.md), [Cloud Asset Discovery for GCP](/solutions/security/cloud/asset-disc-gcp.md), or [Cloud Asset Discovery for Azure](/solutions/security/cloud/asset-disc-azure.md) |
| Scan your cloud workloads for known vulnerabilities | [Get started with CNVM](/solutions/security/cloud/get-started-with-cnvm.md) → [CNVM privilege requirements](/solutions/security/cloud/cnvm-privilege-requirements.md) |
| Turn on cloud security features in a {{serverless-short}} project | [Enable cloud security features in {{serverless-short}}](/solutions/security/cloud/enable-cloud-security-features.md) |

## Next steps

After you set up cloud security, you can:

- Review findings, benchmarks, and vulnerabilities in [Cloud Security](/solutions/security/cloud.md).
- Monitor posture at a glance on the [Cloud Security Posture dashboard](/solutions/security/dashboards/cloud-security-posture-dashboard.md).
- [Manage cloud workload protection](/solutions/security/manage/manage-cloud-workload-protection.md) to detect and block threats on your Linux VMs and Kubernetes workloads at runtime.
