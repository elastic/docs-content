---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubeconfig File Creation or Modification" prebuilt detection rule.
---

# Kubeconfig File Creation or Modification

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubeconfig File Creation or Modification
Kubeconfig files are essential in Kubernetes environments, storing configurations for cluster access and management. Adversaries may target these files to gain unauthorized access or move laterally within clusters. The detection rule identifies suspicious creation or modification of kubeconfig files, excluding legitimate processes like kubeadm and minikube, to flag potential threats and mitigate risks associated with unauthorized access.

### Possible investigation steps

- Review the alert details to identify the specific file path involved in the creation or modification event, focusing on paths like "/root/.kube/config" or "/etc/kubernetes/admin.conf".
- Examine the process responsible for the file creation or modification, ensuring it is not one of the excluded legitimate processes such as "kubeadm", "kubelet", "vcluster", or "minikube".
- Check the user account associated with the process to determine if it has legitimate access to modify kubeconfig files and assess if the activity aligns with typical user behavior.
- Investigate the timing of the event to see if it coincides with any scheduled maintenance or deployment activities that could explain the modification.
- Look for any related alerts or logs that might indicate lateral movement or unauthorized access attempts within the Kubernetes cluster.
- Assess the network activity from the host where the modification occurred to identify any suspicious connections or data transfers that could suggest unauthorized access or exfiltration.

### False positive analysis

- Legitimate administrative tools like kubeadm, kubelet, vcluster, and minikube may create or modify kubeconfig files as part of normal operations. Ensure these processes are excluded from triggering alerts by maintaining the exclusion list in the detection rule.
- Automated scripts or configuration management tools that use sed to modify kubeconfig files might be flagged. Consider adding specific script names or paths to the exclusion list if they are verified as non-threatening.
- User-initiated changes to kubeconfig files for legitimate access or configuration updates can trigger alerts. Implement a process to verify and document such changes, allowing for quick exclusion of known user actions.
- Regular updates or maintenance activities that involve kubeconfig file modifications should be documented and excluded from detection. Coordinate with the operations team to identify and whitelist these activities.
- Development environments where frequent kubeconfig changes occur, such as in testing or staging, may generate false positives. Establish a separate monitoring policy for these environments to reduce noise while maintaining security oversight.

### Response and remediation

- Immediately isolate the affected system to prevent further unauthorized access or lateral movement within the Kubernetes cluster.
- Revoke any potentially compromised credentials associated with the kubeconfig files and issue new credentials to ensure secure access.
- Conduct a thorough review of recent access logs and audit trails to identify any unauthorized access or suspicious activity related to the kubeconfig files.
- Restore the kubeconfig files from a known good backup to ensure the integrity of the configuration and access settings.
- Implement additional monitoring and alerting for any future modifications to kubeconfig files, focusing on processes not typically involved in legitimate changes.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on the broader Kubernetes environment.
- Review and update Kubernetes access policies to ensure they align with best practices for security and least privilege, reducing the risk of unauthorized access.

