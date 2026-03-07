---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Network Scan Detected" prebuilt detection rule.'
---

# Potential Network Scan Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Network Scan Detected

Network scanning is a technique used to identify open ports and services on a network, often exploited by attackers to find vulnerabilities. Adversaries may use this method to map out a network's structure and identify weak points for further exploitation. The detection rule identifies suspicious activity by monitoring for multiple connection attempts from a single source to numerous destination ports, indicating a potential scan. This helps in early detection and mitigation of reconnaissance activities.

### Possible investigation steps

- Review the source IP address involved in the alert to determine if it belongs to a known or trusted entity within the organization. Check if the IP falls within the specified ranges: 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16.
- Analyze the network flow logs to identify the specific destination ports that were targeted by the source IP. Determine if these ports are associated with critical services or known vulnerabilities.
- Correlate the detected activity with any recent changes or updates in the network infrastructure that might explain the scanning behavior, such as new devices or services being deployed.
- Investigate if there are any other alerts or logs indicating similar scanning activities from the same source IP or other IPs within the same subnet, which might suggest a coordinated scanning effort.
- Check for any historical data or past incidents involving the source IP to assess if this behavior is part of a recurring pattern or a new anomaly.
- Consult with network administrators to verify if the detected activity aligns with any scheduled network assessments or security tests that might have been conducted without prior notification.

### False positive analysis

- Internal network scanning tools used for legitimate security assessments can trigger this rule. To manage this, create exceptions for known IP addresses of authorized scanning tools.
- Automated network monitoring systems that check service availability across multiple ports may be flagged. Exclude these systems by identifying their IP addresses and adding them to an exception list.
- Load balancers and network devices that perform health checks on various services might cause false positives. Identify these devices and configure the rule to ignore their IP addresses.
- Development and testing environments where frequent port scanning is part of routine operations can be mistakenly flagged. Implement exceptions for these environments by specifying their IP ranges.
- Regularly scheduled vulnerability assessments conducted by internal security teams can appear as network scans. Document these activities and exclude the associated IPs from triggering the rule.

### Response and remediation

- Isolate the affected host: Immediately disconnect the source IP from the network to prevent further scanning or potential exploitation of identified vulnerabilities.
- Conduct a thorough investigation: Analyze the source IP's activity logs to determine if any unauthorized access or data exfiltration has occurred. This will help assess the extent of the threat.
- Update firewall rules: Implement stricter access controls to limit the number of open ports and restrict unnecessary inbound and outbound traffic from the affected IP range.
- Patch and update systems: Ensure all systems and services identified during the scan are up-to-date with the latest security patches to mitigate known vulnerabilities.
- Monitor for recurrence: Set up enhanced monitoring for the source IP and similar scanning patterns to quickly detect and respond to any future scanning attempts.
- Escalate to security operations: If the scan is part of a larger attack or if sensitive data is at risk, escalate the incident to the security operations team for further analysis and response.
- Review and enhance detection capabilities: Evaluate the effectiveness of current detection mechanisms and consider integrating additional threat intelligence sources to improve early detection of similar threats.
