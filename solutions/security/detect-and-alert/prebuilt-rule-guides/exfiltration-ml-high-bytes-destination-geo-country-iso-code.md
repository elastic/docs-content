---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Data Exfiltration Activity to an Unusual ISO Code" prebuilt detection rule.
---

# Potential Data Exfiltration Activity to an Unusual ISO Code

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Data Exfiltration Activity to an Unusual ISO Code

Machine learning models analyze network traffic patterns to identify anomalies, such as data transfers to unexpected geo-locations. Adversaries exploit command and control channels to exfiltrate data to these unusual regions. The detection rule leverages ML to flag deviations from normal traffic, indicating potential exfiltration activities, thus aiding in early threat identification.

### Possible investigation steps

- Review the alert details to identify the specific unusual ISO code and geo-location involved in the data transfer.
- Analyze network logs to determine the volume and frequency of data transfers to the identified geo-location, comparing it against baseline traffic patterns.
- Investigate the source IP addresses and devices involved in the data transfer to assess whether they are legitimate or potentially compromised.
- Check for any recent changes or anomalies in user behavior or access patterns associated with the source devices or accounts.
- Correlate the alert with other security events or logs, such as authentication logs or endpoint detection alerts, to identify any related suspicious activities.
- Consult threat intelligence sources to determine if the unusual geo-location is associated with known malicious activities or threat actors.

### False positive analysis

- Legitimate business operations involving data transfers to new or infrequent geo-locations may trigger false positives. Users should review these activities and whitelist known safe destinations.
- Regularly scheduled data backups or transfers to international offices or cloud services can be mistaken for exfiltration. Implement exceptions for these routine operations by updating the model's baseline.
- Temporary projects or collaborations with partners in unusual regions might cause alerts. Document these activities and adjust the detection parameters to accommodate such temporary changes.
- Changes in business operations, such as expansion into new markets, can alter normal traffic patterns. Update the model to reflect these changes to prevent unnecessary alerts.
- Use historical data to identify patterns of benign traffic to unusual regions and adjust the model's sensitivity to reduce false positives while maintaining security vigilance.

### Response and remediation

- Immediately isolate the affected systems from the network to prevent further data exfiltration.
- Conduct a thorough analysis of the network traffic logs to identify the source and destination of the unusual data transfer, focusing on the specific geo-location flagged by the alert.
- Block the identified IP addresses or domains associated with the unusual ISO code in the organization's firewall and intrusion prevention systems.
- Review and update access controls and permissions to ensure that only authorized personnel have access to sensitive data, reducing the risk of unauthorized data transfers.
- Restore any compromised systems from clean backups, ensuring that all security patches and updates are applied before reconnecting to the network.
- Escalate the incident to the organization's security operations center (SOC) or incident response team for further investigation and to determine if additional systems or data were affected.
- Implement enhanced monitoring and alerting for similar anomalies in network traffic to improve early detection of potential exfiltration activities in the future.
