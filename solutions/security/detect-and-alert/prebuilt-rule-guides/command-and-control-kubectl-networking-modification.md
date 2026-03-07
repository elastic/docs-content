---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubectl Network Configuration Modification" prebuilt detection rule.'
---

# Kubectl Network Configuration Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubectl Network Configuration Modification

Kubectl is a command-line tool for interacting with Kubernetes clusters, allowing users to manage applications and network settings. Adversaries may exploit kubectl to alter network configurations, potentially establishing unauthorized access or data exfiltration channels. The detection rule identifies suspicious kubectl usage patterns, such as port-forwarding or proxy commands, especially when executed from atypical parent processes or directories, indicating possible malicious intent.

### Possible investigation steps

- Review the process command line to confirm the specific kubectl command and arguments used, focusing on "port-forward", "proxy", or "expose" to understand the intended network configuration change.
- Examine the parent process details, including the name and executable path, to determine if the kubectl command was initiated from an unusual or suspicious location, such as "/tmp/*" or "/var/tmp/*".
- Investigate the user account associated with the kubectl process to verify if the activity aligns with their typical behavior or if it indicates potential compromise.
- Check for any recent changes or anomalies in the Kubernetes cluster's network settings or configurations that could correlate with the detected kubectl activity.
- Look for additional related alerts or logs that might indicate a broader pattern of suspicious activity, such as other command and control tactics or protocol tunneling attempts.

### False positive analysis

- Legitimate administrative tasks using kubectl port-forward or proxy commands can trigger the rule. To manage this, create exceptions for known administrative scripts or users who frequently perform these tasks.
- Automated scripts or cron jobs that use kubectl for network configuration changes may cause false positives. Identify these scripts and exclude their specific command patterns or parent processes from the rule.
- Development environments where developers frequently use kubectl for testing purposes might generate alerts. Consider excluding specific user accounts or directories associated with development activities.
- Continuous integration/continuous deployment (CI/CD) pipelines that utilize kubectl for deployment processes can be a source of false positives. Exclude the CI/CD tool's process names or execution paths from the rule.
- Temporary directories like /tmp or /var/tmp used by legitimate applications for kubectl operations can trigger alerts. Review and whitelist these specific applications or their execution contexts.

### Response and remediation

- Immediately isolate the affected host to prevent further unauthorized access or data exfiltration. This can be done by removing the host from the network or applying network segmentation rules.
- Terminate any suspicious kubectl processes identified by the detection rule to halt any ongoing malicious activity.
- Review and revoke any unauthorized access credentials or tokens that may have been compromised or used in the attack.
- Conduct a thorough audit of Kubernetes network configurations and access controls to identify and rectify any unauthorized changes or vulnerabilities.
- Restore any altered network configurations to their original state using backups or configuration management tools.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been affected.
- Implement enhanced monitoring and logging for kubectl activities and network configuration changes to detect and respond to similar threats more effectively in the future.
