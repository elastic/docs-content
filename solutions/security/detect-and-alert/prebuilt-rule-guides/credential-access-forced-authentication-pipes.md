---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Active Directory Forced Authentication from Linux Host - SMB Named Pipes" prebuilt detection rule.
---

# Active Directory Forced Authentication from Linux Host - SMB Named Pipes

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Active Directory Forced Authentication from Linux Host - SMB Named Pipes

Active Directory (AD) and SMB named pipes facilitate network resource access and inter-process communication. Adversaries exploit these by forcing authentication from a Linux host to capture credentials or perform relay attacks. The detection rule identifies suspicious SMB connection attempts from Linux to Windows hosts, focusing on specific named pipes indicative of forced authentication attempts, thus highlighting potential credential access threats.

### Possible investigation steps

- Review the network logs to identify the Linux host IP address that attempted the SMB connection on port 445 and verify if this activity is expected or authorized.
- Check the Windows host logs for event code 5145 to determine which named pipes were accessed and assess if these accesses align with normal operations or indicate suspicious activity.
- Investigate the source IP address from the Windows logs to determine if it matches the Linux host IP and evaluate if this connection is part of a known and legitimate process.
- Analyze historical data for any previous similar connection attempts from the same Linux host to identify patterns or repeated unauthorized access attempts.
- Consult with system administrators to confirm if there have been any recent changes or updates in the network configuration that could explain the connection attempts.

### False positive analysis

- Routine administrative tasks from Linux hosts may trigger alerts. Identify and document these tasks to create exceptions for known IP addresses or hostnames involved in regular operations.
- Automated backup or monitoring systems that connect to Windows hosts using SMB may cause false positives. Review and whitelist these systems by their IP addresses or specific named pipes they access.
- Development or testing environments where Linux hosts frequently interact with Windows systems can generate alerts. Establish a separate monitoring policy or exclude these environments from the rule to reduce noise.
- Security tools or scripts that perform network scans or audits might mimic suspicious behavior. Verify these tools and exclude their activities by specifying their source IPs or associated user accounts.
- Cross-platform file sharing services that use SMB for legitimate purposes may be flagged. Identify these services and adjust the rule to ignore their specific connection patterns or named pipes.

### Response and remediation

- Isolate the affected Linux host from the network to prevent further unauthorized SMB connection attempts and potential credential capture.
- Conduct a thorough review of the Linux host's network activity logs to identify any unauthorized access or data exfiltration attempts.
- Reset passwords for any accounts that may have been exposed or compromised during the forced authentication attempt to mitigate the risk of credential misuse.
- Implement network segmentation to limit SMB traffic between Linux and Windows hosts, reducing the attack surface for similar threats.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional hosts or systems are affected.
- Deploy enhanced monitoring on the identified named pipes and associated network traffic to detect and respond to future forced authentication attempts promptly.
- Review and update firewall rules to restrict unnecessary SMB traffic and ensure only authorized systems can communicate over port 445.
