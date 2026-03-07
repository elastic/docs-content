---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network Activity Detected via Kworker" prebuilt detection rule.
---

# Network Activity Detected via Kworker

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Activity Detected via Kworker

Kworker processes are integral to Linux systems, handling kernel tasks like interrupts and background activities. Adversaries may exploit these processes to mask malicious network activities, evading detection by blending in with legitimate kernel operations. The detection rule identifies suspicious network connections initiated by kworker processes, excluding trusted IP ranges and ports, to uncover potential command and control activities.

### Possible investigation steps

- Review the alert details to confirm the kworker process is indeed initiating network connections, focusing on the process.name field.
- Examine the destination IP address and port to determine if the connection is to an untrusted or suspicious external network, as the rule excludes trusted IP ranges and ports.
- Check historical data for any previous alerts or network activity involving the same kworker process to identify patterns or repeated behavior.
- Investigate the source host for any signs of compromise or unusual activity, such as unauthorized access attempts or unexpected process executions.
- Correlate the network activity with other security events or logs from the same timeframe to identify potential indicators of compromise or related malicious activities.

### False positive analysis

- Network monitoring tools or legitimate applications may occasionally use kworker processes for routine checks or updates, leading to false positives. Users can create exceptions for these specific applications by identifying their typical IP ranges and ports.
- Internal network scanning or monitoring activities might trigger alerts. To mitigate this, users should exclude known internal IP ranges and ports used by these activities from the detection rule.
- Automated backup or synchronization services that operate in the background could be mistaken for suspicious activity. Users should identify these services and adjust the rule to exclude their associated network traffic.
- Some system updates or maintenance tasks might temporarily use kworker processes for network communication. Users can whitelist the IP addresses and ports associated with these tasks to prevent false alerts.
- If a specific kworker process consistently triggers alerts without any malicious intent, users should investigate the process's behavior and, if deemed safe, add it to an exception list to avoid future false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and potential lateral movement by the attacker.
- Terminate any suspicious kworker processes identified as initiating unauthorized network connections to halt ongoing malicious activities.
- Conduct a thorough forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized files or processes, and remove them.
- Update and patch the affected system to the latest security standards to close any vulnerabilities that may have been exploited.
- Monitor network traffic for any further suspicious activity originating from other systems, indicating potential spread or persistence of the threat.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement enhanced monitoring and logging for kworker processes and network activities to improve detection of similar threats in the future.
