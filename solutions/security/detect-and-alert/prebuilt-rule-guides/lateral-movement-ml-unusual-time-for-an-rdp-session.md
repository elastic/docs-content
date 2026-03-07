---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Time or Day for an RDP Session" prebuilt detection rule.'
---

# Unusual Time or Day for an RDP Session

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Time or Day for an RDP Session

Remote Desktop Protocol (RDP) enables remote access to systems, crucial for IT management but also a target for adversaries seeking unauthorized access. Attackers exploit RDP by initiating sessions at odd hours to avoid detection. The detection rule leverages machine learning to identify atypical RDP session timings, flagging potential lateral movement attempts for further investigation.

### Possible investigation steps

- Review the timestamp of the RDP session to determine the specific unusual time or day it was initiated, and correlate it with known business hours or scheduled maintenance windows.
- Identify the source and destination IP addresses involved in the RDP session to determine if they are internal or external, and check for any known associations with previous security incidents.
- Examine the user account used to initiate the RDP session, verifying if it is a legitimate account and if the login aligns with the user's typical behavior or role within the organization.
- Check for any additional suspicious activities or alerts involving the same user account or IP addresses around the time of the unusual RDP session, such as failed login attempts or access to sensitive files.
- Investigate any recent changes or anomalies in the network or system configurations that could have facilitated the unusual RDP session, such as newly opened ports or modified firewall rules.
- Consult logs from other security tools or systems, such as SIEM or endpoint detection and response (EDR) solutions, to gather more context on the RDP session and any related activities.

### False positive analysis

- Regular maintenance activities by IT staff during off-hours can trigger false positives. Identify and document these activities to create exceptions in the detection rule.
- Scheduled automated tasks or scripts that initiate RDP sessions at unusual times may be misclassified. Review and whitelist these tasks to prevent unnecessary alerts.
- Time zone differences for remote employees accessing systems outside of standard business hours can lead to false positives. Adjust detection parameters to account for these time zone variations.
- Third-party vendors or contractors who require access at non-standard times should be documented and their access patterns reviewed to establish exceptions.
- Emergency access situations where IT staff need to respond to critical incidents outside normal hours should be logged and considered when analyzing alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate the suspicious RDP session to halt any ongoing unauthorized activities.
- Conduct a thorough review of the affected system's logs and processes to identify any malicious activities or changes made during the session.
- Reset credentials for any accounts accessed during the unusual RDP session to prevent further unauthorized use.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are compromised.
- Implement enhanced monitoring on the affected system and related network segments to detect any further suspicious activities or attempts at unauthorized access.
