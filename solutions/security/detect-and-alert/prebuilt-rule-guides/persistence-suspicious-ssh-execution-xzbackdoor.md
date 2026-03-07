---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Execution via SSH Backdoor" prebuilt detection rule.
---

# Potential Execution via SSH Backdoor

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Execution via SSH Backdoor

Linux SSH backdoors, such as the XZBackdoor, leverage SSH, a secure protocol for remote access, to execute malicious commands stealthily. Adversaries exploit SSH by initiating sessions that mimic legitimate activity, then abruptly terminate them post-execution to evade detection. The detection rule identifies anomalies by tracking SSH processes that start and end unexpectedly, especially when non-standard executables are invoked, signaling potential backdoor activity.

### Possible investigation steps

- Review the SSH session logs on the affected host to identify any unusual or unauthorized access attempts, focusing on sessions that match the process.pid and process.entity_id from the alert.
- Examine the command history and executed commands for the user associated with the user.id in the alert to identify any suspicious or unexpected activities.
- Investigate the non-standard executables invoked by the SSH session by checking the process.executable field to determine if they are legitimate or potentially malicious.
- Analyze the network activity associated with the SSH session, particularly any disconnect_received events, to identify any unusual patterns or connections to suspicious IP addresses.
- Check the exit codes of the SSH processes, especially those with a non-zero process.exit_code, to understand the reason for the abrupt termination and whether it aligns with typical error codes or indicates malicious activity.

### False positive analysis

- Legitimate administrative SSH sessions may trigger the rule if they involve non-standard executables. To manage this, create exceptions for known administrative scripts or tools that are frequently used in your environment.
- Automated processes or scripts that use SSH for routine tasks might mimic the behavior of the XZBackdoor. Identify these processes and exclude them by specifying their executable paths or command-line patterns in the rule exceptions.
- Security tools or monitoring solutions that perform SSH-based checks could be mistaken for malicious activity. Review these tools and add their signatures to the exclusion list to prevent false alerts.
- Custom applications that use SSH for communication might be flagged. Document these applications and adjust the rule to recognize their specific execution patterns as non-threatening.
- Temporary network issues causing abrupt SSH session terminations could be misinterpreted as suspicious behavior. Monitor network stability and consider excluding known transient disconnections from triggering alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious SSH sessions identified by the detection rule to stop ongoing malicious activity.
- Conduct a thorough review of the affected host's SSH configuration and logs to identify unauthorized changes or access patterns.
- Reset credentials for any user accounts involved in the suspicious SSH activity to prevent further unauthorized access.
- Restore the affected system from a known good backup if any unauthorized changes or malware are detected.
- Implement network segmentation to limit SSH access to critical systems and reduce the attack surface.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems are compromised.
