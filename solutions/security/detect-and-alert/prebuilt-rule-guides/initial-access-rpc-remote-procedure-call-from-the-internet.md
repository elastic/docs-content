---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "RPC (Remote Procedure Call) from the Internet" prebuilt detection rule.'
---

# RPC (Remote Procedure Call) from the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating RPC (Remote Procedure Call) from the Internet

RPC enables remote management and resource sharing, crucial for system administration. However, when exposed to the Internet, it becomes a target for attackers seeking initial access or backdoor entry. The detection rule identifies suspicious RPC traffic by monitoring TCP port 135 and filtering out internal IP addresses, flagging potential threats from external sources.

### Possible investigation steps

- Review the source IP address of the alert to determine if it is from a known malicious actor or if it has been flagged in previous incidents.
- Check the destination IP address to confirm it belongs to a critical internal system that should not be exposed to the Internet.
- Analyze network traffic logs to identify any unusual patterns or volumes of traffic associated with the source IP, focusing on TCP port 135.
- Investigate any related alerts or logs from the same source IP or destination IP to identify potential patterns or repeated attempts.
- Assess the potential impact on the affected system by determining if any unauthorized access or changes have occurred.
- Consult threat intelligence sources to gather additional context on the source IP or any related indicators of compromise.

### False positive analysis

- Internal testing or development environments may generate RPC traffic that appears to originate from external sources. To manage this, add the IP addresses of these environments to the exception list in the detection rule.
- Legitimate remote management activities by trusted third-party vendors could trigger the rule. Verify the IP addresses of these vendors and include them in the exception list if they are known and authorized.
- Misconfigured network devices or proxies might route internal RPC traffic through external IP addresses. Review network configurations to ensure proper routing and add any necessary exceptions for known devices.
- Cloud-based services or applications that use RPC for legitimate purposes might be flagged. Identify these services and adjust the rule to exclude their IP ranges if they are verified as non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Conduct a thorough examination of the system logs and network traffic to identify any unauthorized access or data exfiltration attempts.
- Apply the latest security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Change all administrative and user credentials on the affected system and any other systems that may have been accessed using the same credentials.
- Implement network segmentation to limit the exposure of critical systems and services, ensuring that RPC services are not accessible from the Internet.
- Monitor the network for any signs of re-infection or further suspicious activity, focusing on traffic patterns similar to those identified in the initial alert.
- Escalate the incident to the security operations center (SOC) or relevant cybersecurity team for further investigation and to determine if additional systems are compromised.
