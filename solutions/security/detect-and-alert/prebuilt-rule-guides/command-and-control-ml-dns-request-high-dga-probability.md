---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Machine Learning Detected a DNS Request With a High DGA Probability Score" prebuilt detection rule.'
---

# Machine Learning Detected a DNS Request With a High DGA Probability Score

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Machine Learning Detected a DNS Request With a High DGA Probability Score

Machine learning models analyze DNS requests to identify patterns indicative of Domain Generation Algorithms (DGAs), often used by attackers to establish command and control channels. These algorithms generate numerous domain names, making detection challenging. The detection rule leverages a model to flag DNS queries with high DGA probability, aiding in identifying potential malicious activity.

### Possible investigation steps

- Review the DNS query logs to identify the specific domain name associated with the high DGA probability score and gather additional context about the request, such as the timestamp and the source IP address.
- Cross-reference the identified domain name with threat intelligence databases to determine if it is a known malicious domain or associated with any known threat actors or campaigns.
- Investigate the source IP address to determine if it belongs to a legitimate user or system within the network, and check for any unusual or suspicious activity associated with this IP address.
- Analyze network traffic logs to identify any additional communication attempts to the flagged domain or other suspicious domains, which may indicate further command and control activity.
- Check endpoint security logs for any signs of compromise or suspicious behavior on the device that initiated the DNS request, such as unexpected processes or connections.
- Consider isolating the affected system from the network if there is strong evidence of compromise, to prevent further potential malicious activity while conducting a deeper forensic analysis.

### False positive analysis

- Legitimate software updates or services may use domain generation techniques for load balancing or redundancy, leading to false positives. Users can create exceptions for known update services or trusted software to reduce these alerts.
- Content delivery networks (CDNs) often use dynamically generated domains to optimize content delivery, which might be flagged. Identifying and whitelisting these CDN domains can help minimize unnecessary alerts.
- Some security tools and applications use DGA-like patterns for legitimate purposes, such as generating unique identifiers. Users should verify the source and purpose of these requests and consider excluding them if they are confirmed to be non-threatening.
- Internal testing environments or development tools might generate domains that resemble DGA activity. Users can exclude these environments from monitoring or adjust the rule to ignore specific internal IP ranges or domain patterns.

### Response and remediation

- Isolate the affected system from the network to prevent further potential command and control communication.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious software.
- Review and block the identified suspicious domain names at the network perimeter to prevent any further communication attempts.
- Analyze network traffic logs to identify any other systems that may have communicated with the flagged domains and apply similar containment measures.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement additional monitoring on the affected system and network segment to detect any signs of persistence or further malicious activity.
- Update and reinforce endpoint protection measures, ensuring all systems have the latest security patches and configurations to prevent similar threats in the future.
