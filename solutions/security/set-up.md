---
navigation_title: Set up
description: Deploy Elastic Security protections in your environment, including endpoint protection with Elastic Defend and cloud security features.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{elastic-sec}}

Deploy the {{elastic-sec}} protections that cover your hosts, cloud accounts, and Kubernetes clusters. You do these tasks once for each feature, when you first turn it on.

After setup, each feature sends its data to {{elastic-sec}}, where you can review alerts, findings, and risk scores. To tune policies, manage exceptions, and control access after deployment, refer to [Manage](/solutions/security/manage.md).

## How the protections cover your environment

Each protection covers a different part of your environment, so the features you set up depend on what you run:

- **{{elastic-defend}}**: Protects Windows, macOS, and Linux hosts, including Linux VMs in the cloud. It runs on {{agent}}, which you install on each host. It can detect or block malware, ransomware, and malicious behavior.
- **Cloud security**: Checks your cloud accounts and Kubernetes clusters against security best practices, list your cloud assets, and scan your cloud workloads for known vulnerabilities.
- **Defend for Containers**: Detects, and can block, unexpected behavior inside running Kubernetes containers.

## Where to start

| Your goal | Start here |
|---|---|
| Protect hosts from malware, ransomware, and malicious behavior | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| Check your cloud accounts and Kubernetes clusters for misconfigurations and vulnerabilities | [Set up cloud security](/solutions/security/set-up/set-up-cloud-security.md) |
| {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` Protect Kubernetes workloads at runtime | [Get started with Defend for Containers for Kubernetes](/solutions/security/cloud/d4c/get-started-with-d4c.md) |
| Check what you need for entity risk scoring, asset criticality, and the entity store | [Entity analytics requirements](/solutions/security/advanced-entity-analytics/entity-analytics-requirements.md) |
| Check what you need to run {{ml}} jobs and rules | [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) |

## Next steps

After you set up your protections, you can:

- [Manage {{elastic-sec}}](/solutions/security/manage.md) to tune policies, manage exceptions, and give users access to each feature.
- [Ingest data](/solutions/security/get-started/ingest-data-to-elastic-security.md) from third-party security tools and threat intelligence sources.
- [Detect and alert](/solutions/security/detect-and-alert.md) on threats with prebuilt and custom detection rules.
- [Hunt and assess posture](/solutions/security/hunt-and-assess-posture.md) to review findings and risk scores from the features you set up.
