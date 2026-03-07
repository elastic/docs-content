---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Rare SMB Connection to the Internet" prebuilt detection rule.'
---

# Rare SMB Connection to the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Rare SMB Connection to the Internet

Server Message Block (SMB) is a protocol used for sharing files and printers within a network. Adversaries exploit SMB to exfiltrate data by injecting rogue paths to capture NTLM credentials. The detection rule identifies unusual SMB traffic from internal IPs to external networks, flagging potential exfiltration attempts by monitoring specific ports and excluding known safe IP ranges.

### Possible investigation steps

- Review the alert details to identify the internal source IP address involved in the SMB connection and verify if it belongs to a known or authorized device within the organization.
- Check the destination IP address to determine if it is associated with any known malicious activity or if it belongs to an external network that should not be receiving SMB traffic from internal systems.
- Investigate the process with PID 4 on the source host, which typically corresponds to the Windows System process, to identify any unusual activity or recent changes that could indicate compromise or misuse.
- Analyze network logs to trace the SMB traffic flow and identify any patterns or additional connections that may suggest data exfiltration attempts.
- Correlate the alert with other security events or logs from data sources like Microsoft Defender for Endpoint or Sysmon to gather additional context and determine if this is part of a larger attack campaign.
- Consult with the IT or network team to verify if there are any legitimate business reasons for the detected SMB traffic to the external network, and if not, consider blocking the connection and conducting a deeper investigation into the source host.

### False positive analysis

- Internal network scanning tools may trigger alerts if they simulate SMB traffic to external IPs. Exclude IPs associated with these tools from the rule to prevent false positives.
- Legitimate business applications that require SMB connections to external cloud services might be flagged. Identify and whitelist these specific external IPs or domains to avoid unnecessary alerts.
- Backup solutions that use SMB for data transfer to offsite locations can be mistaken for exfiltration attempts. Ensure these backup service IPs are added to the exception list.
- Misconfigured network devices that inadvertently route SMB traffic externally could cause false alerts. Regularly audit and correct device configurations to minimize these occurrences.
- Security testing or penetration testing activities might generate SMB traffic to external IPs. Coordinate with security teams to temporarily disable the rule or add exceptions during testing periods.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further data exfiltration or lateral movement.
- Conduct a thorough review of the host's network connections and processes to identify any unauthorized SMB traffic or suspicious activities.
- Reset credentials for any accounts that may have been exposed or compromised, focusing on those with elevated privileges.
- Apply patches and updates to the affected system and any other vulnerable systems to mitigate known SMB vulnerabilities.
- Implement network segmentation to limit SMB traffic to only necessary internal communications, reducing the risk of external exposure.
- Enhance monitoring and logging for SMB traffic, particularly for connections to external IPs, to detect and respond to future anomalies more effectively.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
