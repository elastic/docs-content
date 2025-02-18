---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/cloud-native-security-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-cloud-native-security-overview.html
---

# Cloud Security

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/cloud-native-security-overview.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-cloud-native-security-overview.md

Elastic Security for Cloud helps you improve your cloud security posture by comparing your cloud configuration to best practices, and scanning for vulnerabilities. It also helps you monitor and investigate your cloud workloads inside and outside Kubernetes.

This page describes what each solution does and provides links to more information.


## Cloud Security Posture Management (CSPM) [_cloud_security_posture_management_cspm] 

Discovers and evaluates the services in your cloud environment — like storage, compute, IAM, and more — against configuration security guidelines defined by the [Center for Internet Security](https://www.cisecurity.org/) (CIS) to help you identify and remediate risks that could undermine the confidentiality, integrity, and availability of your cloud data.

[Read the CSPM docs](/solutions/security/cloud/cloud-security-posture-management.md).


## Kubernetes Security Posture Management (KSPM) [_kubernetes_security_posture_management_kspm] 

Allows you to identify configuration risks in the various components that make up your Kubernetes cluster. It does this by evaluating your Kubernetes clusters against secure configuration guidelines defined by the Center for Internet Security (CIS) and generating findings with step-by-step instructions for remediating potential security risks.

[Read the KSPM docs](/solutions/security/cloud/kubernetes-security-posture-management.md).


## Cloud Native Vulnerability Management (CNVM) [_cloud_native_vulnerability_management_cnvm] 

Scans your cloud workloads for known vulnerabilities. When it finds a vulnerability, it supports your risk assessment by quickly providing information such as the vulnerability’s CVSS and severity, which software versions it affects, and whether a fix is available.

[Read the CNVM docs](/solutions/security/cloud/cloud-native-vulnerability-management.md).


## Cloud Workload Protection for Kubernetes [_cloud_workload_protection_for_kubernetes] 

Provides cloud-native runtime protections for containerized environments by identifying and (optionally) blocking unexpected system behavior in Kubernetes containers. These capabilities are sometimes referred to as container drift detection and prevention. The solution also captures detailed process and file telemetry from monitored containers, allowing you to set up custom alerts and protection rules.

[Read the CWP for Kubernetes docs](/solutions/security/cloud/cloud-workload-protection-for-kubernetes.md).


## Cloud Workload Protection for VMs [_cloud_workload_protection_for_vms] 

Helps you monitor and protect your Linux VMs. It uses {{elastic-defend}} to instantly detect and prevent malicious behavior and malware, and captures workload telemetry data for process, file, and network activity. You can use this data with Elastic’s out-of-the-box detection rules and {{ml}} models. These detections generate alerts that quickly help you identify and remediate threats.

[Read the CWP for VMs docs](/solutions/security/cloud/cloud-workload-protection-for-vms.md).

