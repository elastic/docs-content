---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Connection to External Network via Telnet" prebuilt detection rule.
---

# Connection to External Network via Telnet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Connection to External Network via Telnet

Telnet is a protocol offering a command-line interface for remote communication, often used for device management. However, its lack of encryption makes it vulnerable to interception, allowing adversaries to exploit it for unauthorized access or data exfiltration. The detection rule identifies Telnet connections to external IPs, flagging potential lateral movement by excluding known internal and reserved IP ranges.

### Possible investigation steps

- Review the alert details to identify the specific process.entity_id and destination IP address involved in the Telnet connection.
- Verify the legitimacy of the destination IP address by checking if it belongs to a known or trusted external entity, using threat intelligence sources or IP reputation services.
- Investigate the process details associated with the process.entity_id to determine the user account and command line arguments used during the Telnet session.
- Check the system logs and user activity on the host to identify any unusual behavior or unauthorized access attempts around the time of the Telnet connection.
- Assess whether the Telnet connection aligns with expected business operations or if it indicates potential lateral movement or data exfiltration attempts.

### False positive analysis

- Internal device management using Telnet may trigger false positives if the destination IPs are not included in the known internal ranges. Users should verify and update the list of internal IP ranges to include any additional internal networks used for legitimate Telnet connections.
- Automated scripts or monitoring tools that use Telnet for legitimate purposes can cause false positives. Identify these scripts and consider creating exceptions for their specific IP addresses or process names to prevent unnecessary alerts.
- Testing environments that simulate external connections for development purposes might be flagged. Ensure that IP addresses used in these environments are documented and excluded from the detection rule to avoid false positives.
- Legacy systems that rely on Telnet for communication with external partners or services may be mistakenly flagged. Review these systems and, if deemed secure, add their IP addresses to an exception list to reduce false alerts.
- Misconfigured network devices that inadvertently use Telnet for external communication can trigger alerts. Regularly audit network configurations and update the detection rule to exclude known benign IPs associated with these devices.

### Response and remediation

- Immediately isolate the affected Linux host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any active Telnet sessions on the affected host to stop ongoing malicious activity.
- Conduct a thorough review of the affected system's logs and processes to identify any unauthorized changes or additional compromised accounts.
- Change all passwords associated with the affected system and any other systems that may have been accessed using Telnet.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Implement network segmentation to limit Telnet access to only necessary internal systems and block Telnet traffic to external networks.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
