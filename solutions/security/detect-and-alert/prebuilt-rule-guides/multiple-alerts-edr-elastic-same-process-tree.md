---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multiple Elastic Defend Alerts from a Single Process Tree" prebuilt detection rule.
---

# Multiple Elastic Defend Alerts from a Single Process Tree

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multiple Elastic Defend Alerts from a Single Process Tree

Detects multiple Elastic Defend EDR alerts originating from the same process tree, indicating coordinated malicious activity.

### Possible investigation steps

- Review the alert details to identify the specific host involved and the different alerts that triggered.
- Examine the timeline of the alerts to understand the sequence of events and determine the root cause.
- Correlate the alert data with other logs and telemetry from the host, such as process creation, network connections, and file modifications, to gather additional context.
- Check for any indicators of compromise (IOCs) associated with the alerts, such as suspicious IP addresses, domains, or file hashes, and search for these across the network.
- Assess the impact and scope of the potential compromise by determining if other hosts or systems have similar alerts or related activity.

### False positive analysis

- Security tools running on the host might generate multiple alerts from same process tree.
- Automated scripts or batch processes can mimic adversarial behavior. Analyze and whitelist these processes if they are verified as non-threatening.
- Frequent alerts from development or testing environments can be misleading. Consider excluding these environments from the rule or applying a different risk score.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further lateral movement by the adversary.
- Conduct a thorough forensic analysis of the host to identify the specific vulnerabilities exploited and gather evidence of the attack phases involved.
- Remove any identified malicious software or unauthorized access tools from the host, ensuring all persistence mechanisms are eradicated.
- Apply security patches and updates to the host to address any exploited vulnerabilities and prevent similar attacks.
- Restore the host from a known good backup if necessary, ensuring that the backup is free from compromise.
- Monitor the host and network for any signs of re-infection or further suspicious activity, using enhanced logging and alerting based on the identified attack patterns.
- Escalate the incident to the appropriate internal or external cybersecurity teams for further investigation and potential legal action if the attack is part of a larger campaign.
