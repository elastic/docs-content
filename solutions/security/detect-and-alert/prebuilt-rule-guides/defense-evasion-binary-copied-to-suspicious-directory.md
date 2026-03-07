---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System Binary Moved or Copied" prebuilt detection rule.'
---

# System Binary Moved or Copied

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Binary Moved or Copied

System binaries are essential executables in Linux environments, crucial for system operations. Adversaries may move or copy these binaries to alternate locations to evade detection, often renaming them to blend in with legitimate processes. The detection rule identifies unusual movements or copies of these binaries, excluding common system processes and paths, to flag potential malicious activity. This helps in identifying attempts at masquerading, a tactic used to bypass security measures.

### Possible investigation steps

- Review the file path and name in the alert to determine if the binary was moved or copied to a suspicious or unusual location, which could indicate an attempt to masquerade.
- Examine the process name and executable path that triggered the alert to identify if it is associated with known legitimate processes or if it appears suspicious or unexpected.
- Check the user account associated with the process to determine if the action was performed by a privileged or unauthorized user, which could suggest malicious intent.
- Investigate the historical activity of the process and user involved to identify any patterns or previous suspicious behavior that might correlate with the current alert.
- Correlate the alert with other security events or logs from the same timeframe to identify any related activities or anomalies that could provide additional context or evidence of malicious activity.

### False positive analysis

- System updates and package installations often involve legitimate movement or copying of binaries. Exclude processes like dpkg, rpm, and apt-get from triggering alerts by adding them to the exception list.
- Development and testing environments may frequently rename or move binaries for testing purposes. Consider excluding paths like /tmp or /dev/fd from monitoring if they are commonly used for non-malicious activities.
- Automated scripts or configuration management tools such as Puppet or Chef may move binaries as part of their normal operations. Add these tools to the exception list to prevent unnecessary alerts.
- Temporary files created during software installations or updates, such as those with extensions like .tmp or .dpkg-new, can trigger false positives. Exclude these extensions from monitoring to reduce noise.
- Custom scripts or applications that mimic system processes for legitimate reasons might be flagged. Review and whitelist these specific scripts or applications if they are verified as non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are associated with the unauthorized movement or copying of system binaries.
- Restore any altered or moved system binaries to their original locations and verify their integrity using known good backups or checksums.
- Conduct a thorough review of system logs and the alert details to identify any additional indicators of compromise or related malicious activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of the activity, focusing on the specific paths and processes identified in the alert.
- Review and update access controls and permissions to ensure that only authorized users and processes can modify or move system binaries, reducing the risk of similar incidents in the future.
