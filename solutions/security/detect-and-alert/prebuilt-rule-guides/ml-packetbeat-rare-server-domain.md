---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Network Destination Domain Name" prebuilt detection rule.
---

# Unusual Network Destination Domain Name

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Network Destination Domain Name

Machine learning models analyze network traffic to identify atypical domain names, which may indicate malicious activities like phishing or malware communication. Adversaries exploit uncommon domains for initial access or command-and-control. This detection rule leverages ML to flag these anomalies, aiding analysts in identifying potential threats early.

### Possible investigation steps

- Review the domain name flagged by the alert to determine if it is known for malicious activity or if it is newly registered, using threat intelligence sources and domain reputation services.
- Analyze the network traffic associated with the domain to identify the source IP address and any related communication patterns, such as frequency and data volume.
- Check the user or system that initiated the connection to the unusual domain for any recent changes or suspicious activities, such as software installations or configuration changes.
- Investigate any related alerts or logs that might provide additional context, such as other unusual domain requests or failed login attempts, to identify potential patterns or correlations.
- Assess the endpoint security logs for signs of malware or unauthorized access attempts that could be linked to the unusual domain activity.

### False positive analysis

- Legitimate software updates or downloads from uncommon domains can trigger false positives. Users should maintain a list of known software vendors and their associated domains to exclude these from alerts.
- Internal testing or development environments may use non-standard domain names. Organizations should document these domains and configure exceptions to prevent unnecessary alerts.
- Newly registered domains for legitimate business purposes might be flagged. Regularly update the list of approved domains as new business initiatives arise.
- Third-party services or APIs that use unique domain names can cause false positives. Identify and whitelist these services to reduce noise in alerts.
- Temporary or one-time use domains for events or campaigns should be monitored and excluded as needed to avoid repeated false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further communication with the suspicious domain and potential spread of malware.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious software.
- Review and analyze network logs to identify any other systems that may have communicated with the unusual domain and apply similar isolation and scanning procedures to those systems.
- Change passwords and credentials associated with the affected system and any potentially compromised accounts to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional containment measures are necessary.
- Implement network-level blocking of the identified unusual domain across the organization to prevent future access attempts.
- Update threat intelligence feeds and detection systems with indicators of compromise (IOCs) related to the unusual domain to enhance future detection capabilities.
