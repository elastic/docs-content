---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Machine Learning Detected DGA activity using a known SUNBURST DNS domain" prebuilt detection rule.'
---

# Machine Learning Detected DGA activity using a known SUNBURST DNS domain

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Machine Learning Detected DGA activity using a known SUNBURST DNS domain

Domain Generation Algorithms (DGAs) are used by adversaries to dynamically generate domain names for command and control (C2) communication, making it difficult to block malicious domains. The SUNBURST malware utilized such techniques. The detection rule leverages machine learning to identify DNS queries linked to these generated domains, specifically targeting those associated with SUNBURST, by analyzing patterns and predicting malicious activity, thus aiding in early threat detection and mitigation.

### Possible investigation steps

- Review the DNS logs to identify the source IP address associated with the DNS query for avsvmcloud.com to determine the affected host within the network.
- Check historical DNS query logs for the identified host to see if there are additional queries to other suspicious or known malicious domains, indicating further compromise.
- Investigate the network traffic from the identified host around the time of the alert to detect any unusual patterns or connections to external IP addresses that may suggest command and control activity.
- Examine endpoint security logs and alerts for the affected host to identify any signs of SUNBURST malware or other related malicious activity.
- Correlate the alert with other security events in the environment to determine if there are any related incidents or patterns that could indicate a broader attack campaign.
- Assess the risk and impact of the detected activity on the organization and determine if immediate containment or remediation actions are necessary.

### False positive analysis

- Legitimate software updates or network services may occasionally use domain generation algorithms for load balancing or redundancy, leading to false positives. Users should monitor and whitelist these known benign services.
- Internal testing environments or security tools that simulate DGA behavior for research or training purposes might trigger alerts. Exclude these environments by adding them to an exception list.
- Some cloud services might use dynamic DNS techniques that resemble DGA patterns. Identify and document these services, then configure exceptions to prevent unnecessary alerts.
- Frequent legitimate access to avsvmcloud.com by security researchers or analysts could be misclassified. Ensure these activities are logged and reviewed, and create exceptions for known research IPs or user accounts.
- Regularly review and update the exception list to ensure it reflects current network behavior and does not inadvertently allow new threats.

### Response and remediation

- Isolate the affected systems immediately to prevent further communication with the malicious domain avsvmcloud.com and halt potential data exfiltration or lateral movement.
- Conduct a thorough scan of the isolated systems using updated antivirus and anti-malware tools to identify and remove any SUNBURST malware or related malicious files.
- Review and block any outbound traffic to the domain avsvmcloud.com at the network perimeter to prevent future connections from other potentially compromised systems.
- Analyze network logs and DNS query records to identify any other systems that may have communicated with the domain, and apply the same isolation and scanning procedures to those systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the full scope of the compromise.
- Implement enhanced monitoring and alerting for any DNS queries or network traffic patterns indicative of DGA activity, particularly those resembling SUNBURST characteristics, to detect and respond to similar threats promptly.
- Review and update incident response and recovery plans to incorporate lessons learned from this incident, ensuring faster and more effective responses to future threats.
