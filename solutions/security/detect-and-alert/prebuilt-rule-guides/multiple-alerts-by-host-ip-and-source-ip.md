---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspected Lateral Movement from Compromised Host" prebuilt detection rule.'
---

# Suspected Lateral Movement from Compromised Host

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspected Lateral Movement from Compromised Host

The detection rule uses alert data to determine when multiple alerts from different integrations involving the same user.name are triggered.

### Possible investigation steps

- Review the alert details to identify the specific host involved and the different modules and rules that triggered the alert.
- Examine the timeline of the alerts to understand the sequence of events and determine if there is a pattern or progression in the tactics used.
- Correlate the alert data with other logs and telemetry from the host, such as process creation, network connections, and file modifications, to gather additional context.
- Investigate any known vulnerabilities or misconfigurations on the host that could have been exploited by the adversary.
- Check for any indicators of compromise (IOCs) associated with the alerts, such as suspicious IP addresses, domains, or file hashes, and search for these across the network.
- Assess the impact and scope of the potential compromise by determining if other hosts or systems have similar alerts or related activity.

### False positive analysis

- Vulnerability scanners.
- Jump hosts, NAT gateways and proxies.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further lateral movement by the adversary.
- Conduct a thorough forensic analysis of the host to identify the specific vulnerabilities exploited and gather evidence of the attack phases involved.
- Remove any identified malicious software or unauthorized access tools from the host, ensuring all persistence mechanisms are eradicated.
- Apply security patches and updates to the host to address any exploited vulnerabilities and prevent similar attacks.
- Restore the host from a known good backup if necessary, ensuring that the backup is free from compromise.
- Monitor the host and network for any signs of re-infection or further suspicious activity, using enhanced logging and alerting based on the identified attack patterns.
- Escalate the incident to the appropriate internal or external cybersecurity teams for further investigation and potential legal action if the attack is part of a larger campaign.
