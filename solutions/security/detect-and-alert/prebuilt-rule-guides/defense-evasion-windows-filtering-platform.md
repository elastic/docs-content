---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Evasion via Windows Filtering Platform" prebuilt detection rule.
---

# Potential Evasion via Windows Filtering Platform

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Evasion via Windows Filtering Platform

The Windows Filtering Platform (WFP) is a set of API and system services that provide a platform for network filtering and packet processing. Adversaries may exploit WFP by creating malicious rules to block endpoint security processes, hindering their ability to send telemetry data. The detection rule identifies patterns of blocked network events linked to security software processes, signaling potential evasion tactics.

### Possible investigation steps

- Review the specific network events that triggered the alert, focusing on the event.action values "windows-firewall-packet-block" and "windows-firewall-packet-drop" to understand which processes were blocked.
- Identify the process names involved in the alert from the process.name field and verify if they are related to known endpoint security software, as listed in the query.
- Check the winlog.computer_name field to determine which systems are affected and assess if multiple systems are involved, indicating a broader issue.
- Investigate the recent changes to the Windows Filtering Platform rules on the affected systems to identify any unauthorized or suspicious modifications.
- Correlate the blocked events with any recent security incidents or alerts to determine if there is a pattern or ongoing attack.
- Consult system logs and security software logs on the affected systems for additional context or anomalies around the time of the alert.
- Engage with the system or network administrators to verify if any legitimate changes were made to the WFP rules that could explain the blocked events.

### False positive analysis

- Security software updates or installations can trigger multiple block events as they modify network configurations. Users should monitor for these events during known update windows and consider excluding them from alerts.
- Legitimate network troubleshooting or diagnostic tools may temporarily block network traffic as part of their operation. Identify these tools and create exceptions for their processes to prevent false alerts.
- Custom security configurations or policies in enterprise environments might intentionally block certain network activities. Review and document these configurations to differentiate between expected behavior and potential threats.
- Temporary network disruptions or misconfigurations can cause legitimate security processes to be blocked. Regularly audit network settings and ensure they align with security policies to minimize these occurrences.
- Scheduled maintenance or testing of security systems might result in blocked events. Coordinate with IT teams to whitelist these activities during planned maintenance periods.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and data exfiltration.
- Terminate any suspicious processes identified in the alert, particularly those related to endpoint security software, to restore normal security operations.
- Review and remove any unauthorized or suspicious Windows Filtering Platform rules that may have been added to block security processes.
- Conduct a thorough scan of the affected system using a trusted antivirus or endpoint detection and response (EDR) tool to identify and remove any malware or persistent threats.
- Restore any affected security software to its default configuration and ensure it is fully operational and updated.
- Monitor network traffic and system logs for any signs of continued evasion tactics or re-infection attempts.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
