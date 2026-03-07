---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kernel Load or Unload via Kexec Detected" prebuilt detection rule.
---

# Kernel Load or Unload via Kexec Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Load or Unload via Kexec Detected

Kexec is a Linux feature allowing a new kernel to load without rebooting, streamlining updates and recovery. However, attackers can exploit kexec to bypass security, escalate privileges, or hide activities by loading malicious kernels. The detection rule identifies suspicious kexec usage by monitoring process actions and arguments, excluding benign parent processes, to flag potential threats.

### Possible investigation steps

- Review the process details to confirm the presence of the kexec command with suspicious arguments such as "--exec", "-e", "--load", "-l", "--unload", or "-u".
- Investigate the parent process of the kexec command to ensure it is not a benign process like "kdumpctl" or "unload.sh", which are excluded from the detection rule.
- Check the user account associated with the kexec process to determine if it has the necessary privileges and if the activity aligns with their typical behavior.
- Analyze recent system logs and security events for any signs of privilege escalation or unauthorized kernel modifications around the time the kexec command was executed.
- Examine the system for any signs of persistence mechanisms or other indicators of compromise that may suggest a broader attack campaign.
- Correlate this event with other alerts or anomalies in the environment to assess if this is part of a larger attack pattern or isolated incident.

### False positive analysis

- Kdump operations may trigger false positives as kdumpctl is a benign parent process for kexec. Ensure kdumpctl is included in the exclusion list to prevent unnecessary alerts.
- Custom scripts for kernel unloading, such as unload.sh, can cause false positives. Verify these scripts are legitimate and add them to the exclusion list if they are frequently used in your environment.
- Routine administrative tasks involving kernel updates or testing may involve kexec. Confirm these activities are authorized and consider excluding specific administrative accounts or processes from detection.
- Automated system recovery processes that utilize kexec might be flagged. Identify these processes and exclude them if they are part of a known and secure recovery mechanism.
- Security tools or monitoring solutions that use kexec for legitimate purposes should be reviewed and excluded to avoid false alerts, ensuring they are recognized as trusted applications.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the attacker.
- Terminate any suspicious kexec processes identified by the detection rule to halt any ongoing malicious kernel loading activities.
- Conduct a thorough review of system logs and process histories to identify any unauthorized kernel loads or modifications, and revert to a known good state if necessary.
- Restore the system from a clean backup taken before the suspicious activity was detected to ensure system integrity and remove any potential backdoors or malicious kernels.
- Update and patch the system to the latest security standards to mitigate any vulnerabilities that could be exploited by similar attacks in the future.
- Implement strict access controls and monitoring on systems with kexec capabilities to prevent unauthorized usage and ensure only trusted personnel can perform kernel operations.
- Escalate the incident to the security operations center (SOC) or relevant incident response team for further investigation and to assess the potential impact on other systems within the network.
