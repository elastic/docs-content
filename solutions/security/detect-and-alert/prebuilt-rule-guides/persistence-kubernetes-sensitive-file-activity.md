---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Sensitive Configuration File Activity" prebuilt detection rule.
---

# Kubernetes Sensitive Configuration File Activity

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Sensitive Configuration File Activity

Kubernetes relies on configuration files to manage cluster operations, including manifests and PKI files. These files are crucial for defining the desired state and security of the cluster. Adversaries may exploit these files to gain persistence or deploy unauthorized containers. The detection rule monitors for unauthorized changes to these files, excluding legitimate processes, to identify potential security threats.

### Possible investigation steps

- Review the alert details to identify the specific file path that triggered the alert, focusing on paths like "/etc/kubernetes/manifests/*", "/etc/kubernetes/pki/*", or "/etc/kubernetes/*.conf".
- Check the process that attempted to modify the file by examining the process name and compare it against the list of excluded legitimate processes ("kubeadm", "kubelet", "dpkg", "sed") to determine if it is suspicious.
- Investigate the user account associated with the process that made the change to assess if the account has the necessary permissions and if it has been compromised.
- Analyze recent activity on the host to identify any other unusual or unauthorized actions that might correlate with the file modification, such as unexpected network connections or process executions.
- Review the history of changes to the affected file to determine if there have been other unauthorized modifications or if this is an isolated incident.
- Consult Kubernetes audit logs, if available, to gather additional context on the actions performed around the time of the alert, focusing on any anomalies or unauthorized access attempts.

### False positive analysis

- Routine updates or maintenance activities by system administrators can trigger alerts. To manage this, consider excluding processes or users known to perform regular maintenance from the rule.
- Automated scripts or configuration management tools like Ansible or Puppet may modify configuration files as part of their normal operation. Identify these tools and add them to the exclusion list to prevent unnecessary alerts.
- Scheduled backups or system snapshots might access or modify configuration files. Ensure that these processes are recognized and excluded if they are part of a regular, non-threatening operation.
- Legitimate software updates or patches may alter configuration files. Monitor update schedules and exclude these processes during known update windows to reduce false positives.
- Custom scripts developed in-house for cluster management might not be recognized by default. Review these scripts and add them to the exclusion list if they are verified as safe and necessary for operations.

### Response and remediation

- Immediately isolate the affected node or container to prevent further unauthorized access or changes to the Kubernetes configuration files.
- Review the modified configuration files to identify unauthorized changes and revert them to their last known good state using backups or version control systems.
- Conduct a thorough investigation to identify the source of the unauthorized changes, focusing on process names and user accounts involved in the modification.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems or nodes have been compromised.
- Implement additional access controls and monitoring on the affected systems to prevent recurrence, such as restricting write permissions to sensitive directories and files.
- Update and patch the Kubernetes environment and related components to address any vulnerabilities that may have been exploited.
- Enhance detection capabilities by ensuring that alerts are configured to notify the security team of any future unauthorized changes to critical Kubernetes configuration files.

