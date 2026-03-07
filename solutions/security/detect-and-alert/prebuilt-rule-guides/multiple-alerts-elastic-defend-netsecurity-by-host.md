---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Elastic Defend and Network Security Alerts Correlation" prebuilt detection rule.'
---

# Elastic Defend and Network Security Alerts Correlation

## Triage and analysis

### Investigating Elastic Defend and Network Security Alerts Correlation

This rule correlate any Elastic Defend alert with suspicious events from Network Security datasources like Palo Alto Networks (PANW), Fortinet Fortigate and Suricata by host.ip and source.ip.

### Possible investigation steps

- Review the alert details to identify the specific host and users involved.
- Investiguate the network alerts by destination.ip and message.
- Examine the timeline of the alerts to understand the sequence of events and determine if there is a pattern or progression in the tactics used.
- Correlate the alert data with other logs and telemetry from the host, such as process creation, network connections, and file modifications, to gather additional context.
- Check for any indicators of compromise (IOCs) associated with the alerts, such as suspicious IP addresses, domains, or file hashes, and search for these across the network.
- Assess the impact and scope of the potential compromise by determining if other hosts or systems have similar alerts or related activity.

### False positive analysis

- IP address ranges overlap where the host.ip value from the Elastic Defend alert is unrelated to the source.ip value from the Network Security alert.
- Alerts from routine administrative tasks may trigger multiple alerts. Review and exclude known benign activities such as scheduled software updates or system maintenance.
- Security tools running on the host might generate alerts across different tactics. Identify and exclude alerts from trusted security applications to reduce noise.
- Automated scripts or batch processes can mimic adversarial behavior. Analyze and whitelist these processes if they are verified as non-threatening.
- Frequent alerts from development or testing environments can be misleading. Consider excluding these environments from the rule or applying a different risk score.
- User behavior anomalies, such as accessing multiple systems or applications, might trigger alerts. Implement user behavior baselines to differentiate between normal and suspicious activities.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further lateral movement by the adversary.
- Conduct a thorough forensic analysis of the host to identify the specific vulnerabilities exploited and gather evidence of the attack phases involved.
- Remove any identified malicious software or unauthorized access tools from the host, ensuring all persistence mechanisms are eradicated.
- Apply security patches and updates to the host to address any exploited vulnerabilities and prevent similar attacks.
- Restore the host from a known good backup if necessary, ensuring that the backup is free from compromise.
- Monitor the host and network for any signs of re-infection or further suspicious activity, using enhanced logging and alerting based on the identified attack patterns.
- Escalate the incident to the appropriate internal or external cybersecurity teams for further investigation and potential legal action if the attack is part of a larger campaign.
