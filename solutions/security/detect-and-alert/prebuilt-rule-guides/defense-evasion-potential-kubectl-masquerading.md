---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Kubectl Masquerading via Unexpected Process" prebuilt detection rule.
---

# Potential Kubectl Masquerading via Unexpected Process

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Kubectl Masquerading via Unexpected Process

Kubectl is a command-line tool for interacting with Kubernetes clusters, crucial for managing containerized applications. Adversaries may exploit this by renaming the kubectl binary or placing it in unusual directories to mimic legitimate activity and evade detection. The detection rule identifies such masquerading by monitoring for non-standard process names executing kubectl-related commands, thus highlighting potential evasion attempts.

### Possible investigation steps

- Review the process executable path to determine if it is located in a non-standard directory such as /tmp, /var/tmp, /dev/shm, or other specified paths in the query.
- Examine the process name to check if it deviates from the expected "kubectl" name, which could indicate an attempt to masquerade the process.
- Analyze the command line arguments used in the process to identify any kubectl-related commands, such as "get", "describe", "exec", "port-forward", or authentication commands, which may suggest unauthorized access or activity.
- Investigate the user account associated with the process to determine if it has legitimate access to execute kubectl commands or if it might be compromised.
- Check for any recent changes or anomalies in the Kubernetes cluster that could correlate with the suspicious process activity, such as unauthorized deployments or configuration changes.
- Review system logs and other security alerts around the time of the event to identify any additional indicators of compromise or related suspicious activities.
- If possible, capture and analyze network traffic associated with the process to detect any unusual or unauthorized communication with the Kubernetes API server or other cluster components.

### False positive analysis

- Processes running in development or testing environments may trigger alerts if kubectl is executed from non-standard directories. To manage this, create exceptions for known development paths where kubectl is legitimately used.
- Automated scripts or CI/CD pipelines that use kubectl from custom directories might be flagged. Identify these scripts and exclude their specific paths or process names from the rule.
- Some legitimate applications might wrap kubectl commands for functionality, leading to unexpected process names. Review these applications and add their process names to the exclusion list if they are verified as non-threatening.
- Users with custom kubectl installations in home directories could cause false positives. Verify these installations and exclude the specific user paths if they are deemed safe.
- Temporary or experimental setups where kubectl is renamed for testing purposes might be mistakenly flagged. Document these setups and apply temporary exclusions during the testing phase.

### Response and remediation

- Immediately isolate the affected host to prevent further unauthorized access or lateral movement within the network.
- Terminate any suspicious processes identified by the detection rule that are masquerading as kubectl to halt potential malicious activity.
- Conduct a thorough review of the affected system's logs and command history to identify any unauthorized kubectl commands executed and assess the scope of the compromise.
- Revoke any potentially compromised credentials or access tokens associated with the Kubernetes cluster to prevent further unauthorized access.
- Restore any altered or deleted Kubernetes resources from backups, ensuring the integrity and availability of the cluster's services.
- Implement stricter access controls and monitoring on the Kubernetes cluster, such as enforcing the principle of least privilege and enabling audit logging for kubectl commands.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been affected.

