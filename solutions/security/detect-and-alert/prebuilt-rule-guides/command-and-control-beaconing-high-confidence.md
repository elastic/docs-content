---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Statistical Model Detected C2 Beaconing Activity with High Confidence" prebuilt detection rule.
---

# Statistical Model Detected C2 Beaconing Activity with High Confidence

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Statistical Model Detected C2 Beaconing Activity with High Confidence

Statistical models analyze network traffic patterns to identify anomalies indicative of C2 beaconing, a tactic where attackers maintain covert communication with compromised systems. Adversaries exploit this to issue commands, exfiltrate data, and sustain network presence. The detection rule leverages a high beaconing score to flag potential threats, aiding analysts in pinpointing suspicious activities linked to C2 operations.

### Possible investigation steps

- Review the network traffic logs to identify the source and destination IP addresses associated with the beaconing activity flagged by the beacon_stats.beaconing_score of 3.
- Correlate the identified IP addresses with known malicious IP databases or threat intelligence feeds to determine if they are associated with known C2 servers.
- Analyze the frequency and pattern of the beaconing activity to assess whether it aligns with typical C2 communication patterns, such as regular intervals or specific time frames.
- Investigate the domain names involved in the communication to check for any associations with malicious activities or suspicious registrations.
- Examine the payloads or data transferred during the flagged communication sessions to identify any potential exfiltration of sensitive information or receipt of malicious instructions.
- Cross-reference the involved systems with internal asset inventories to determine if they are critical assets or have been previously flagged for suspicious activities.
- Consult with the incident response team to decide on containment or remediation actions if the investigation confirms malicious C2 activity.

### False positive analysis

- Regularly scheduled software updates or patch management systems may generate network traffic patterns similar to C2 beaconing. Users can create exceptions for known update servers to reduce false positives.
- Automated backup systems that frequently communicate with cloud storage services might be flagged. Identifying and excluding these backup services from the analysis can help mitigate this issue.
- Network monitoring tools that periodically check connectivity or system health can mimic beaconing activity. Whitelisting these monitoring tools can prevent them from being incorrectly flagged.
- Internal applications that use polling mechanisms to check for updates or status changes may trigger alerts. Documenting and excluding these applications from the rule can minimize false positives.
- Frequent communication with trusted third-party services, such as content delivery networks, may appear as beaconing. Establishing a list of trusted domains and excluding them from the analysis can help manage this.

### Response and remediation

- Isolate the affected systems from the network to prevent further communication with the C2 server and contain the threat.
- Conduct a thorough analysis of the network traffic logs to identify any additional compromised systems or lateral movement within the network.
- Remove any malicious software or scripts identified on the compromised systems, ensuring all traces of the C2 communication channels are eradicated.
- Apply security patches and updates to all affected systems to close any vulnerabilities exploited by the attackers.
- Change all credentials and authentication tokens associated with the compromised systems to prevent unauthorized access.
- Monitor the network for any signs of re-infection or continued C2 activity, using enhanced detection rules and updated threat intelligence.
- Escalate the incident to the appropriate internal security team or external cybersecurity experts for further investigation and to assess the potential impact on the organization.
