---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Connection to Internal Network via Telnet" prebuilt detection rule.
---

# Connection to Internal Network via Telnet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Connection to Internal Network via Telnet

Telnet is a protocol offering a command-line interface for remote device management, often used in network environments. Adversaries may exploit Telnet to move laterally within a network, accessing non-public IPs to execute commands or exfiltrate data. The detection rule identifies Telnet connections to internal IP ranges, flagging potential unauthorized access attempts, thus aiding in early threat detection and response.

### Possible investigation steps

- Review the process details to confirm the Telnet connection initiation by examining the process.entity_id and process.name fields to ensure the process is indeed Telnet.
- Analyze the destination IP address to determine if it falls within the specified non-public IP ranges, indicating an internal network connection attempt.
- Check the event.type field to verify that the Telnet process event is of type "start", confirming the initiation of a connection.
- Investigate the source host by reviewing host.os.type and other relevant host details to understand the context and legitimacy of the connection attempt.
- Correlate the Telnet activity with any other suspicious network or process activities on the same host to identify potential lateral movement or data exfiltration attempts.
- Consult historical logs and alerts to determine if there have been previous similar Telnet connection attempts from the same source, which might indicate a pattern or ongoing threat.

### False positive analysis

- Routine administrative tasks using Telnet within internal networks can trigger false positives. To manage this, create exceptions for known IP addresses or specific user accounts that regularly perform these tasks.
- Automated scripts or monitoring tools that use Telnet for legitimate purposes may be flagged. Identify these scripts and whitelist their associated processes or IP addresses to prevent unnecessary alerts.
- Internal testing environments often simulate network activities, including Telnet connections. Exclude IP ranges associated with these environments to reduce false positives.
- Legacy systems that rely on Telnet for communication might generate alerts. Document these systems and apply exceptions based on their IP addresses or hostnames to avoid repeated false positives.
- Regularly review and update the list of excluded IPs and processes to ensure that only legitimate activities are exempted, maintaining the effectiveness of the detection rule.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further lateral movement or data exfiltration.
- Terminate any active Telnet sessions on the affected host to stop unauthorized access.
- Conduct a thorough review of the affected host's system logs and Telnet session logs to identify any unauthorized commands executed or data accessed.
- Change all credentials that may have been exposed or used during the unauthorized Telnet sessions to prevent further unauthorized access.
- Apply security patches and updates to the affected host and any other systems that may be vulnerable to similar exploitation.
- Implement network segmentation to limit Telnet access to only necessary systems and ensure that Telnet is disabled on systems where it is not required.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems have been compromised.
