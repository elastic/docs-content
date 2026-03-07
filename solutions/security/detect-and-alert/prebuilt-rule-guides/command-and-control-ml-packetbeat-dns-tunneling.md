---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "DNS Tunneling" prebuilt detection rule.'
---

# DNS Tunneling

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DNS Tunneling

DNS tunneling exploits the DNS protocol to covertly transmit data between a compromised system and an attacker-controlled server. Adversaries use it for stealthy command-and-control, persistence, or data exfiltration by embedding data within DNS queries. The detection rule leverages machine learning to identify anomalies, such as an unusually high volume of DNS queries to a single domain, indicating potential tunneling activity.

### Possible investigation steps

- Review the DNS query logs to identify the specific top-level domain generating the unusually high volume of queries. This can help pinpoint the potential source of tunneling activity.
- Analyze the source IP addresses associated with the DNS queries to determine if they originate from known or suspicious hosts within the network.
- Check for any recent changes or anomalies in the network traffic patterns related to the identified domain, which might indicate tunneling or exfiltration attempts.
- Investigate the history of the identified domain to assess its reputation and any known associations with malicious activities or threat actors.
- Correlate the DNS query activity with other security events or alerts in the network to identify any related suspicious behavior or indicators of compromise.

### False positive analysis

- High volume of DNS queries from legitimate software updates or patch management systems can trigger false positives. Users should identify and whitelist domains associated with trusted update services.
- Content delivery networks (CDNs) often generate numerous DNS queries due to their distributed nature. Exclude known CDN domains from the analysis to reduce false positives.
- Internal network monitoring tools that rely on DNS for service discovery may cause an increase in DNS queries. Consider excluding these internal domains if they are verified as non-threatening.
- Some cloud services use DNS for load balancing and may result in high query volumes. Users should review and whitelist these domains if they are confirmed to be safe.
- Automated scripts or applications that frequently query DNS for legitimate purposes can be excluded by identifying their specific patterns and adding them to an exception list.

### Response and remediation

- Isolate the affected system from the network to prevent further data exfiltration or command-and-control communication.
- Conduct a thorough analysis of DNS logs to identify the specific domain involved in the tunneling activity and block it at the network perimeter.
- Review and terminate any suspicious processes or services running on the compromised system that may be associated with the tunneling activity.
- Reset credentials and review access permissions for accounts that were active on the compromised system to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring for DNS traffic to detect similar tunneling activities in the future, focusing on high-frequency queries to single domains.
- Coordinate with IT and security teams to apply necessary patches and updates to the affected system to close any vulnerabilities exploited by the attacker.
