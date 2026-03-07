---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential SYN-Based Port Scan Detected" prebuilt detection rule.'
---

# Potential SYN-Based Port Scan Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential SYN-Based Port Scan Detected

SYN-based port scanning is a reconnaissance technique where attackers send SYN packets to multiple ports to identify open services. This method helps adversaries map network vulnerabilities for potential exploitation. The detection rule identifies such scans by flagging connection attempts from internal IPs to multiple ports with minimal packet exchange, indicating a low-risk reconnaissance activity.

### Possible investigation steps

- Review the source IP address involved in the alert to determine if it belongs to a known or authorized device within the network. Check for any recent changes or unusual activity associated with this IP.
- Analyze the destination ports targeted by the scan to identify any patterns or specific services that may be of interest to the attacker. Determine if these ports are associated with critical or vulnerable services.
- Examine historical logs to identify any previous scanning activity from the same source IP or similar patterns of behavior. This can help establish whether the activity is part of a larger reconnaissance effort.
- Correlate the alert with other security events or alerts to assess if there is a broader attack campaign underway. Look for related alerts that might indicate subsequent exploitation attempts.
- Investigate the timing and frequency of the scan attempts to understand if they coincide with other suspicious activities or known attack windows. This can provide context on the attacker's intent and urgency.
- Assess the network's current security posture and ensure that appropriate defenses, such as firewalls and intrusion detection systems, are configured to mitigate potential exploitation of identified open ports.

### False positive analysis

- Internal network scanning tools or scripts used by IT teams for legitimate network mapping can trigger this rule. To manage this, create exceptions for known internal IP addresses or subnets used by IT for network discovery.
- Automated monitoring systems or security appliances that perform regular port checks might be flagged. Identify these systems and exclude their IP addresses from the rule to prevent false positives.
- Software updates or patch management systems that check multiple ports for service availability can be mistaken for a SYN-based port scan. Whitelist these systems to avoid unnecessary alerts.
- Load balancers or network devices that perform health checks across multiple ports may trigger the rule. Exclude these devices from the rule to ensure accurate detection.
- Development or testing environments where multiple port scans are part of routine operations can cause false positives. Implement exceptions for these environments to maintain focus on genuine threats.

### Response and remediation

- Isolate the affected internal IP address to prevent further reconnaissance or potential exploitation of identified open ports.
- Conduct a thorough review of firewall and network access control lists to ensure that only necessary ports are open and accessible from internal networks.
- Implement rate limiting on SYN packets to reduce the risk of successful port scanning and reconnaissance activities.
- Monitor the network for any unusual outbound traffic from the affected IP address, which may indicate further malicious activity or data exfiltration attempts.
- Escalate the incident to the security operations team for further analysis and to determine if additional network segments or systems are affected.
- Update intrusion detection and prevention systems to enhance detection capabilities for similar SYN-based port scanning activities.
- Review and update network segmentation policies to limit the exposure of critical services and systems to internal reconnaissance activities.
