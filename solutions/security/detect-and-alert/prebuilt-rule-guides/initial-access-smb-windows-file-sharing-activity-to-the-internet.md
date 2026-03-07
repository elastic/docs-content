---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SMB (Windows File Sharing) Activity to the Internet" prebuilt detection rule.'
---

# SMB (Windows File Sharing) Activity to the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SMB (Windows File Sharing) Activity to the Internet

SMB, a protocol for sharing files and resources within trusted networks, is vulnerable when exposed to the Internet. Adversaries exploit it for unauthorized access or data theft. The detection rule identifies suspicious SMB traffic from internal IPs to external networks, flagging potential threats by monitoring specific ports and excluding known safe IP ranges.

### Possible investigation steps

- Review the source IP address from the alert to identify the internal system initiating the SMB traffic. Check if this IP belongs to a known device or user within the organization.
- Investigate the destination IP address to determine if it is associated with any known malicious activity or if it belongs to a legitimate external service that might require SMB access.
- Analyze network logs to identify any patterns or anomalies in the SMB traffic, such as unusual data transfer volumes or repeated access attempts, which could indicate malicious activity.
- Check for any recent changes or updates on the source system that might explain the SMB traffic, such as new software installations or configuration changes.
- Correlate the alert with other security events or logs, such as authentication logs or endpoint security alerts, to gather additional context and determine if this is part of a broader attack or isolated incident.
- Consult threat intelligence sources to see if there are any known vulnerabilities or exploits related to the SMB traffic observed, which could provide insight into potential attack vectors.

### False positive analysis

- Internal testing environments may generate SMB traffic to external IPs for legitimate reasons. Identify and whitelist these IPs to prevent false positives.
- Cloud services or remote backup solutions might use SMB for data transfer. Verify these services and add their IP ranges to the exception list if they are trusted.
- VPN connections can sometimes appear as external traffic. Ensure that VPN IP ranges are included in the list of known safe IPs to avoid misclassification.
- Misconfigured network devices might inadvertently route SMB traffic externally. Regularly audit network configurations and update the rule exceptions to include any legitimate device IPs.
- Some third-party applications may use SMB for updates or data synchronization. Confirm the legitimacy of these applications and exclude their associated IPs from the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of firewall and network configurations to ensure SMB traffic is not allowed to the Internet, and block any unauthorized outbound SMB traffic on ports 139 and 445.
- Perform a comprehensive scan of the isolated system for malware or unauthorized access tools, focusing on identifying any backdoors or persistence mechanisms.
- Reset credentials and review access permissions for any accounts that may have been compromised or used in the suspicious activity.
- Notify the security operations center (SOC) and relevant stakeholders about the incident for further analysis and potential escalation.
- Implement additional monitoring and logging for SMB traffic to detect any future unauthorized attempts to access the Internet.
- Review and update security policies and procedures to prevent similar incidents, ensuring that SMB services are only accessible within trusted network segments.
