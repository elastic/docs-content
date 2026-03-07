---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Endpoint Security (Elastic Defend)" prebuilt detection rule.'
---

# Endpoint Security (Elastic Defend)

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Endpoint Security (Elastic Defend)

Elastic Defend is a robust endpoint security solution that monitors and protects systems by analyzing events and generating alerts for suspicious activities. Adversaries may exploit endpoints by executing unauthorized code or manipulating system processes. The detection rule leverages event data to identify alerts from Elastic Defend, focusing on potential threats while excluding non-relevant modules, thus enabling timely investigation of endpoint anomalies.

### Possible investigation steps

- Review the alert details to understand the specific event.kind:alert and event.module: endpoint that triggered the alert, ensuring it is not related to the excluded endgame module.
- Examine the timeline of events leading up to the alert to identify any unusual or unauthorized activities, such as unexpected process executions or system changes.
- Correlate the alert with other security events or logs from the same endpoint to gather additional context and determine if there is a pattern of suspicious behavior.
- Investigate the source and destination of any network connections associated with the alert to identify potential command and control activity or data exfiltration attempts.
- Check for any recent changes or updates to the endpoint's software or configuration that could explain the alert, ensuring they are legitimate and authorized.
- Assess the risk score and severity of the alert in conjunction with other alerts from the same endpoint to prioritize the investigation and response efforts.

### False positive analysis

- Alerts triggered by routine software updates can be false positives. Users can create exceptions for known update processes to prevent unnecessary alerts.
- System maintenance activities, such as scheduled scans or backups, may generate alerts. Exclude these activities by identifying their specific event signatures and adding them to the exception list.
- Legitimate administrative actions, like remote desktop sessions or script executions by IT staff, might be flagged. Define exceptions for these actions by correlating them with authorized user accounts or IP addresses.
- Frequent alerts from non-malicious applications that interact with system processes can be excluded by whitelisting these applications based on their hash or path.
- Network monitoring tools that simulate attack patterns for testing purposes may trigger alerts. Exclude these tools by specifying their known behaviors and IP ranges in the exception settings.

### Response and remediation

- Isolate the affected endpoint immediately to prevent further unauthorized access or lateral movement within the network.
- Analyze the alert details to identify the specific unauthorized code or process manipulation involved, and terminate any malicious processes identified.
- Remove any unauthorized code or files from the affected endpoint, ensuring that all traces of the threat are eradicated.
- Conduct a thorough review of system logs and event data to identify any additional indicators of compromise or related suspicious activities.
- Update endpoint security configurations and signatures to prevent similar threats from exploiting the same vulnerabilities in the future.
- Restore the affected endpoint from a known good backup if necessary, ensuring that the system is free from any residual threats.
- Escalate the incident to the security operations center (SOC) or relevant team for further analysis and to determine if additional systems may be affected.
