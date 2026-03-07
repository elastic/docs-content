---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network Traffic to Rare Destination Country" prebuilt detection rule.
---

# Network Traffic to Rare Destination Country

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Traffic to Rare Destination Country

Machine learning models analyze network logs to identify traffic to uncommon destination countries, which may indicate malicious activities like unauthorized access or data exfiltration. Adversaries exploit this by directing traffic to servers in atypical locations, often linked to command-and-control operations. The detection rule flags such anomalies, aiding in early threat identification and response.

### Possible investigation steps

- Review the network logs to identify the specific destination country flagged as rare and assess its historical presence in the network traffic.
- Analyze the source IP addresses and user accounts associated with the flagged traffic to determine if they are legitimate or potentially compromised.
- Investigate the nature of the traffic, such as the protocols and ports used, to identify any unusual patterns or connections to known malicious infrastructure.
- Check for any recent phishing attempts or suspicious emails that may have led to the initiation of this traffic, focusing on links or attachments that could have been used to download malicious payloads.
- Correlate the flagged traffic with any other security alerts or incidents to identify potential patterns or coordinated attacks involving the rare destination country.
- Consult threat intelligence sources to determine if the destination country or specific IP addresses are associated with known threat actors or command-and-control servers.

### False positive analysis

- Legitimate business communications with partners or clients in rare destination countries may trigger alerts. Users should review and whitelist these known entities to prevent future false positives.
- Routine software updates or patches from international vendors might be flagged. Identify and exclude these update servers from the detection rule to avoid unnecessary alerts.
- Employees traveling abroad and accessing company resources can generate alerts. Implement a process to temporarily whitelist these destinations based on travel schedules.
- Cloud services with global data centers may route traffic through uncommon countries. Verify the service's IP ranges and exclude them if they are part of normal operations.
- Research or market expansion activities targeting new regions might cause alerts. Document and exclude these activities if they align with business objectives.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough scan of the isolated system for malware or unauthorized software, focusing on identifying any command-and-control (C2) communication channels.
- Block network traffic to and from the identified rare destination country at the firewall or proxy level to prevent further communication with potential malicious servers.
- Review and analyze logs from the affected system and network devices to identify any additional indicators of compromise or related suspicious activities.
- If malware is detected, remove it using appropriate tools and techniques, ensuring that all persistence mechanisms are eradicated.
- Restore the affected system from a clean backup if necessary, ensuring that all security patches and updates are applied.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
