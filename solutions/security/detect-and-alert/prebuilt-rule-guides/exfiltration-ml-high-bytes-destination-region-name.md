---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Data Exfiltration Activity to an Unusual Region" prebuilt detection rule.'
---

# Potential Data Exfiltration Activity to an Unusual Region

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Data Exfiltration Activity to an Unusual Region

Machine learning models analyze network traffic patterns to identify anomalies, such as data transfers to atypical regions. Adversaries exploit command and control channels to exfiltrate data to these regions, bypassing traditional security measures. This detection rule leverages ML to flag unusual geo-locations, indicating potential exfiltration activities, thus aiding in early threat identification.

### Possible investigation steps

- Review the geo-location details flagged by the alert to determine if the region is indeed unusual for the organization's typical network traffic patterns.
- Analyze the network traffic logs associated with the alert to identify the volume and type of data being transferred to the unusual region.
- Cross-reference the IP addresses involved in the data transfer with threat intelligence databases to check for any known malicious activity or associations.
- Investigate the user accounts and devices involved in the data transfer to assess if they have been compromised or are exhibiting other suspicious behaviors.
- Check for any recent changes in network configurations or security policies that might have inadvertently allowed data transfers to atypical regions.
- Collaborate with the organization's IT and security teams to verify if there are legitimate business reasons for the data transfer to the flagged region.

### False positive analysis

- Legitimate business operations involving data transfers to new or infrequent regions may trigger false positives. Users should review and whitelist these regions if they are part of regular business activities.
- Scheduled data backups or transfers to cloud services located in atypical regions can be mistaken for exfiltration. Identify and exclude these services from the rule's scope.
- Remote work scenarios where employees connect from different regions might cause alerts. Maintain an updated list of remote work locations to prevent unnecessary alerts.
- Partner or vendor data exchanges that occur outside usual geographic patterns should be documented and excluded if they are verified as non-threatening.
- Temporary projects or collaborations with international teams may result in unusual data flows. Ensure these are accounted for in the rule's configuration to avoid false positives.

### Response and remediation

- Isolate the affected systems immediately to prevent further data exfiltration. Disconnect them from the network to stop ongoing communication with the unusual geo-location.
- Conduct a thorough analysis of the network traffic logs to identify the scope of the exfiltration and determine which data was accessed or transferred.
- Revoke any compromised credentials and enforce a password reset for affected accounts to prevent unauthorized access.
- Implement geo-blocking measures to restrict data transfers to the identified unusual region, ensuring that only approved regions can communicate with the network.
- Review and update firewall and intrusion detection system (IDS) rules to detect and block similar command and control traffic patterns in the future.
- Escalate the incident to the security operations center (SOC) and relevant stakeholders, providing them with detailed findings and actions taken for further investigation and response.
- Conduct a post-incident review to assess the effectiveness of the response and identify any gaps in the security posture, implementing necessary improvements to prevent recurrence.
