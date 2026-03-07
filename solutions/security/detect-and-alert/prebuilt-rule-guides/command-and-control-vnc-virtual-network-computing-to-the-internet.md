---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "VNC (Virtual Network Computing) to the Internet" prebuilt detection rule.'
---

# VNC (Virtual Network Computing) to the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating VNC (Virtual Network Computing) to the Internet

VNC is a tool that allows remote control of computers, often used by administrators for maintenance. However, when exposed to the internet, it becomes a target for attackers seeking unauthorized access. Adversaries exploit VNC to establish backdoors or gain initial access. The detection rule identifies suspicious VNC traffic by monitoring specific TCP ports and filtering out internal IP addresses, flagging potential threats when VNC is accessed from external networks.

### Possible investigation steps

- Review the source IP address to determine if it belongs to a known internal asset or user, and verify if the access was authorized.
- Check the destination IP address to confirm if it is an external address and investigate its reputation or any known associations with malicious activity.
- Analyze the network traffic logs for the specified TCP ports (5800-5810) to identify any unusual patterns or volumes of VNC traffic.
- Correlate the VNC traffic event with other security events or logs to identify any related suspicious activities or anomalies.
- Investigate the user account associated with the VNC session to ensure it has not been compromised or misused.
- Assess the system or application logs on the destination machine for any signs of unauthorized access or changes during the time of the VNC connection.

### False positive analysis

- Internal maintenance activities may trigger the rule if VNC is used for legitimate remote administration. To manage this, create exceptions for known internal IP addresses that frequently use VNC for maintenance.
- Automated scripts or tools that use VNC for legitimate purposes might be flagged. Identify these tools and whitelist their IP addresses to prevent unnecessary alerts.
- Testing environments that simulate external access to VNC for security assessments can cause false positives. Exclude IP ranges associated with these environments to avoid confusion.
- Cloud-based services that use VNC for remote management might be misidentified as threats. Verify these services and add their IP addresses to an exception list if they are trusted.
- Temporary remote access setups for troubleshooting or support can be mistaken for unauthorized access. Document these instances and apply temporary exceptions to reduce false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any active VNC sessions that are identified as originating from external networks to cut off potential attacker access.
- Conduct a thorough review of system logs and network traffic to identify any unauthorized access or data transfer that may have occurred during the VNC exposure.
- Change all passwords and credentials associated with the affected system and any other systems that may have been accessed using the same credentials.
- Apply necessary patches and updates to the VNC software and any other vulnerable applications on the affected system to mitigate known vulnerabilities.
- Implement network segmentation to ensure that VNC services are only accessible from trusted internal networks and not exposed to the internet.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems may be compromised.
