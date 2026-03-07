---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Kworker UID Elevation" prebuilt detection rule.'
---

# Suspicious Kworker UID Elevation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Kworker UID Elevation

Kworker processes are integral to Linux, handling tasks like interrupts and background activities within the kernel. Adversaries may exploit these processes by disguising malicious activities as legitimate kernel operations, often using rootkits to hijack execution flow and gain root access. The detection rule identifies anomalies by monitoring for kworker processes that unexpectedly change session IDs and elevate privileges to root, signaling potential misuse.

### Possible investigation steps

- Review the process details for the kworker process with a session ID change and user ID of 0 to confirm the legitimacy of the process and its parent process.
- Check the system logs around the time of the session ID change event for any unusual activities or errors that might indicate tampering or exploitation attempts.
- Investigate any recent changes to the system, such as new software installations or updates, that could have introduced vulnerabilities or unauthorized modifications.
- Analyze the system for signs of rootkit presence, such as hidden files or processes, by using rootkit detection tools or manual inspection techniques.
- Correlate the event with other security alerts or anomalies in the network to determine if this is part of a broader attack campaign or isolated incident.

### False positive analysis

- Regular system updates or maintenance activities may trigger session ID changes in kworker processes. Users can monitor scheduled maintenance windows and exclude these time frames from triggering alerts.
- Custom kernel modules or legitimate software that interacts with kernel processes might cause kworker to change session IDs. Identify and whitelist these known modules or software to prevent false positives.
- Automated scripts or tools that require elevated privileges for legitimate tasks could inadvertently cause kworker processes to appear suspicious. Review and document these scripts, then create exceptions for their expected behavior.
- Certain system configurations or optimizations might lead to benign kworker session ID changes. Conduct a baseline analysis of normal system behavior and adjust the detection rule to accommodate these patterns without compromising security.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Terminate the suspicious kworker process identified in the alert to stop any ongoing malicious activity.
- Conduct a thorough review of system logs and process trees to identify any additional compromised processes or indicators of rootkit installation.
- Restore the system from a known good backup if rootkit presence is confirmed, as rootkits can deeply embed themselves into the system.
- Change all credentials and keys that may have been exposed or used on the compromised system to prevent unauthorized access using stolen credentials.
- Implement enhanced monitoring and logging for kworker processes and session ID changes to detect similar activities in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems.
