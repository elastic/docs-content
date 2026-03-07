---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Firewall Denies" prebuilt detection rule.
---

# Spike in Firewall Denies

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Firewall Denies

Firewalls and ACLs are critical in controlling network traffic, blocking unauthorized access. Adversaries may exploit misconfigurations or launch attacks like reconnaissance or denial-of-service to overwhelm these defenses. The 'Spike in Firewall Denies' detection rule leverages machine learning to identify unusual surges in denied traffic, signaling potential misconfigurations or malicious activities.

### Possible investigation steps

- Review the time frame and source IP addresses associated with the spike in denied traffic to identify any patterns or anomalies.
- Check the firewall and ACL logs for any recent changes or misconfigurations that could have led to the increase in denied traffic.
- Investigate the destination IP addresses and ports targeted by the denied traffic to determine if they are associated with known malicious activity or if they are legitimate services.
- Analyze the volume and frequency of the denied requests to assess whether they align with typical denial-of-service attack patterns or reconnaissance activities.
- Correlate the denied traffic with other security alerts or logs to identify any related suspicious activities or potential indicators of compromise within the network.

### False positive analysis

- Routine network scans by security tools or IT teams may trigger spikes in denied traffic. Regularly review and whitelist known IP addresses or tools to prevent these from being flagged.
- Misconfigured applications that frequently attempt unauthorized access can cause false positives. Identify and correct these configurations to reduce unnecessary alerts.
- Legitimate but high-volume business applications might generate traffic patterns similar to reconnaissance activities. Monitor and document these applications, and create exceptions for their traffic patterns.
- Scheduled maintenance or updates can lead to temporary spikes in denied traffic. Coordinate with IT teams to anticipate these events and adjust monitoring rules accordingly.
- Internal network changes, such as new device deployments or network architecture updates, might cause unexpected traffic patterns. Ensure these changes are communicated and accounted for in the firewall rules to minimize false positives.

### Response and remediation

- Immediately isolate affected systems or segments of the network to prevent further unauthorized access or potential spread of malicious activity.
- Analyze the denied traffic logs to identify the source IP addresses and block them at the firewall or ACL level to prevent further attempts.
- Review and correct any misconfigurations in firewall rules or ACLs that may have contributed to the spike in denied traffic.
- Conduct a thorough investigation to determine if the spike is related to a denial-of-service attack and, if confirmed, engage with your internet service provider (ISP) for additional support and mitigation strategies.
- If malicious activity is suspected, escalate the incident to the security operations center (SOC) or incident response team for further analysis and response.
- Implement additional monitoring and alerting for similar patterns of denied traffic to enhance early detection of potential threats.
- Document the incident, including actions taken and lessons learned, to improve future response efforts and update incident response plans accordingly.
