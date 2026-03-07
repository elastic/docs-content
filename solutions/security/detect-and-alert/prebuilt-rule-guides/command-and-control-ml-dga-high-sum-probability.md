---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential DGA Activity" prebuilt detection rule.'
---

# Potential DGA Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential DGA Activity
Domain Generation Algorithms (DGAs) are used by malware to dynamically generate domain names for command and control (C2) communication, making it difficult to block malicious domains. Adversaries exploit this by frequently changing domains to evade detection. The 'Potential DGA Activity' detection rule leverages machine learning to analyze DNS requests from source IPs, identifying patterns indicative of DGA usage, thus flagging potential threats for further investigation.

### Possible investigation steps

- Review the source IP address identified in the alert to determine if it belongs to a known or trusted entity within the organization.
- Analyze the DNS request patterns from the source IP to identify any unusual or suspicious domain names that may indicate DGA activity.
- Cross-reference the flagged domains with threat intelligence feeds to check for known malicious domains or patterns associated with DGAs.
- Investigate the network traffic associated with the source IP to identify any additional indicators of compromise or communication with known malicious IPs.
- Check for any recent changes or anomalies in the system or network configurations that could explain the detected activity.
- Assess the risk score and severity in the context of the organization's environment to prioritize the investigation and response efforts.

### False positive analysis

- Legitimate software updates or cloud services may generate high volumes of DNS requests that resemble DGA patterns. Users can create exceptions for known update servers or cloud service domains to reduce false positives.
- Content delivery networks (CDNs) often use dynamically generated subdomains for load balancing and distribution, which can trigger DGA alerts. Identifying and excluding these CDN domains from analysis can help mitigate false positives.
- Large organizations with complex internal networks might have internal applications that generate DNS requests similar to DGA activity. Conducting a thorough review of internal DNS traffic and whitelisting known internal domains can prevent these false positives.
- Some security tools or network appliances may perform DNS lookups as part of their normal operation, which could be misclassified as DGA activity. Identifying these tools and excluding their IP addresses from the analysis can help manage false positives.

### Response and remediation

- Isolate the affected systems: Immediately disconnect any systems identified as making suspicious DNS requests from the network to prevent further communication with potential C2 servers.
- Block identified domains: Use firewall and DNS filtering solutions to block the domains flagged by the detection rule, preventing any further communication attempts.
- Conduct a thorough system scan: Use updated antivirus and anti-malware tools to scan the isolated systems for any signs of infection or malicious software.
- Analyze network traffic: Review network logs to identify any additional suspicious activity or other systems that may be affected, focusing on unusual DNS requests and connections.
- Patch and update systems: Ensure all systems, especially those identified in the alert, are fully patched and updated to mitigate vulnerabilities that could be exploited by malware.
- Restore from backups: If malware is confirmed, restore affected systems from clean backups to ensure no remnants of the infection remain.
- Escalate to incident response team: If the threat is confirmed and widespread, escalate the incident to the organization's incident response team for further investigation and coordinated response efforts.
