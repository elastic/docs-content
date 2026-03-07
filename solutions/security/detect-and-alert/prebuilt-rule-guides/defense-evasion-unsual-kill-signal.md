---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Kill Signal" prebuilt detection rule.
---

# Unusual Kill Signal

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Kill Signal

In Linux environments, kill signals are used to manage process lifecycles. Signals in the range of 32-64 are less common and can be exploited by adversaries, such as rootkits, to manipulate processes stealthily, potentially leading to privilege escalation or evasion of security measures. The 'Unusual Kill Signal' detection rule identifies these rare signals, flagging potential misuse by monitoring specific syscall activities, thus aiding in early threat detection.

### Possible investigation steps

- Review the process details associated with the alert, focusing on the process name, PID, and parent process to understand the context of the kill signal usage.
- Examine the user account under which the process was executed to determine if it aligns with expected behavior or if it indicates potential unauthorized access.
- Investigate the command line arguments and environment variables of the process to identify any suspicious or unusual commands that may suggest malicious activity.
- Check the system logs around the time of the alert for any related events or anomalies that could provide additional context or indicate a broader attack pattern.
- Correlate the alert with other security events or alerts from the same host to identify if this is part of a larger attack or if there are other indicators of compromise.
- Assess the network activity of the host to identify any unusual outbound connections that could suggest data exfiltration or communication with a command and control server.

### False positive analysis

- Legitimate applications or services may use signals in the 32-64 range for custom inter-process communication, leading to false positives. Identify these applications and create exceptions for their specific processes.
- Some system monitoring or management tools might utilize these signals for legitimate process management tasks. Review the tools in use and whitelist their activities if they are verified as non-threatening.
- Development environments or testing frameworks might employ unusual signals for debugging or testing purposes. Ensure these environments are properly isolated and exclude their activities from triggering alerts.
- Custom scripts or automation tasks could be configured to use these signals for specific operations. Audit these scripts and, if deemed safe, add them to an exception list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes identified with unusual kill signals in the range of 32-64 to halt any ongoing malicious activity.
- Conduct a thorough forensic analysis of the affected system to identify any rootkits or malicious software that may have been installed, focusing on the processes and files associated with the unusual kill signals.
- Restore the system from a known good backup if rootkit presence is confirmed, ensuring that the backup is free from any compromise.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Implement enhanced monitoring and logging for unusual kill signals and related activities to detect any future attempts at similar attacks.
- Escalate the incident to the security operations center (SOC) or relevant cybersecurity team for further investigation and to assess the need for broader organizational response measures.

