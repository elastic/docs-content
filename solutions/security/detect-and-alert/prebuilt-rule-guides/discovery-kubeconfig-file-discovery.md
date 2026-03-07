---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubeconfig File Discovery" prebuilt detection rule.'
---

# Kubeconfig File Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubeconfig File Discovery

Kubeconfig files are essential in Kubernetes, storing credentials and configurations for cluster access. Adversaries may target these files to gain unauthorized access or move laterally within clusters. The detection rule identifies suspicious processes interacting with kubeconfig files, especially from common shell environments or risky directories, flagging potential misuse by excluding benign commands like 'stat' or 'md5sum'.

### Possible investigation steps

- Review the process details to identify the parent process name and executable path, focusing on those originating from common shell environments or risky directories like /tmp, /var/tmp, or /dev/shm.
- Examine the process arguments to determine if they include references to sensitive kubeconfig files such as admin.conf, kubelet.conf, or any files within /etc/kubernetes or ~/.kube directories.
- Check the working directory of the process to see if it aligns with known Kubernetes configuration paths like /etc/kubernetes or ~/.kube, which may indicate an attempt to access or modify kubeconfig files.
- Investigate the user account associated with the process to assess whether it has legitimate access to Kubernetes configurations or if it might be compromised.
- Correlate the event with other recent activities from the same user or IP address to identify any patterns of suspicious behavior or potential lateral movement within the cluster.
- Review any related alerts or logs for the same host or container to gather additional context on the system's state and any other potential indicators of compromise.

### False positive analysis

- Processes like 'stat' and 'md5sum' are excluded from detection as they are commonly used for legitimate file checks. Ensure these exclusions are correctly configured to prevent unnecessary alerts.
- Scripts located in user directories such as '/home/*/.kube' may trigger alerts if they interact with kubeconfig files. Consider adding exceptions for known scripts or users that regularly access these files for legitimate purposes.
- Processes originating from world-writeable directories like '/tmp' or '/var/tmp' can be flagged. Review these alerts to identify routine operations and whitelist specific processes or directories that are part of regular maintenance tasks.
- Alerts triggered by processes with names matching patterns like '*.sh' may include legitimate scripts. Evaluate these scripts and exclude them if they are part of standard operations or administrative tasks.
- Regular administrative tasks involving kubeconfig files in directories like '/etc/kubernetes' may be flagged. Implement exceptions for known administrative processes to reduce false positives while maintaining security oversight.

### Response and remediation

- Immediately isolate the affected system to prevent further unauthorized access to the Kubernetes cluster.
- Revoke any compromised credentials associated with the kubeconfig files and issue new credentials to authorized users.
- Conduct a thorough review of recent access logs and audit trails for the Kubernetes cluster to identify any unauthorized access or lateral movement attempts.
- Restore any modified or deleted kubeconfig files from a secure backup to ensure the integrity of the cluster configuration.
- Implement stricter access controls and permissions for directories containing kubeconfig files, ensuring only authorized personnel have access.
- Escalate the incident to the security operations team for further investigation and to determine if additional clusters or systems are affected.
- Enhance monitoring and alerting for suspicious activities related to kubeconfig files, leveraging the MITRE ATT&CK framework to identify potential discovery tactics.
