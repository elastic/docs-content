---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Network Traffic" prebuilt detection rule.'
---

# Spike in Network Traffic

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Network Traffic
Machine learning models analyze network traffic patterns to identify anomalies, such as unexpected spikes. These spikes may indicate malicious activities like data exfiltration or denial-of-service attacks. Adversaries exploit network vulnerabilities to flood traffic or extract data. The 'Spike in Network Traffic' rule leverages ML to flag unusual traffic surges, aiding in early threat detection and response.

### Possible investigation steps

- Review the timestamp and duration of the traffic spike to determine if it correlates with any scheduled business activities or known events.
- Analyze the source and destination IP addresses involved in the traffic spike to identify any unfamiliar or suspicious entities.
- Examine the types of network protocols and services involved in the spike to assess if they align with typical network usage patterns.
- Check for any recent changes in network configurations or security policies that might explain the unusual traffic patterns.
- Investigate any associated user accounts or devices to determine if they have been compromised or are exhibiting unusual behavior.
- Cross-reference the spike with other security alerts or logs to identify potential patterns or related incidents.

### False positive analysis

- Business-related traffic surges: Regular spikes due to legitimate business activities, such as marketing campaigns or software updates, can trigger false positives. Users should analyze historical traffic patterns and create exceptions for known business events.
- Scheduled data backups: Routine data backups can cause significant network traffic. Users can exclude these by identifying backup schedules and configuring the rule to ignore traffic during these times.
- Software updates and patches: Large-scale updates from software vendors can lead to temporary traffic spikes. Users should maintain a list of update schedules and whitelist these events to prevent false alerts.
- Internal network scans: Regular security scans or inventory checks within the organization may cause traffic spikes. Users should document these activities and adjust the rule to recognize them as non-threatening.
- Cloud service synchronization: Synchronization activities with cloud services can generate high traffic volumes. Users should identify and exclude these regular sync patterns to reduce false positives.

### Response and remediation

- Immediately isolate affected systems from the network to prevent further data exfiltration or traffic flooding.
- Conduct a thorough analysis of network logs to identify the source and destination of the traffic spike, focusing on any unauthorized or suspicious IP addresses.
- Block identified malicious IP addresses and domains at the firewall and update intrusion prevention systems to prevent further access.
- If data exfiltration is suspected, perform a data integrity check to assess any potential data loss or compromise.
- Notify the incident response team to assess the situation and determine if further escalation is necessary, including potential involvement of law enforcement if data theft is confirmed.
- Review and update network access controls and permissions to ensure only authorized users and devices have access to sensitive data and systems.
- Implement enhanced monitoring and alerting for similar traffic patterns to improve early detection and response to future incidents.
