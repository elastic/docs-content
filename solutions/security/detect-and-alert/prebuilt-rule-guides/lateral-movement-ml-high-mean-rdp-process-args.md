---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "High Mean of Process Arguments in an RDP Session" prebuilt detection rule.
---

# High Mean of Process Arguments in an RDP Session

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating High Mean of Process Arguments in an RDP Session

Remote Desktop Protocol (RDP) facilitates remote access to systems, often targeted by adversaries for lateral movement. Attackers may exploit RDP by executing complex commands with numerous arguments to obfuscate their actions. The detection rule leverages machine learning to identify anomalies in process arguments, flagging potential misuse indicative of sophisticated attacks.

### Possible investigation steps

- Review the specific RDP session details, including the source and destination IP addresses, to identify any unusual or unauthorized access patterns.
- Analyze the process arguments flagged by the machine learning model to determine if they include known malicious commands or patterns indicative of obfuscation or redirection.
- Check the user account associated with the RDP session for any signs of compromise, such as recent password changes or login attempts from unusual locations.
- Correlate the alert with other security events or logs, such as firewall logs or intrusion detection system alerts, to identify any related suspicious activities or lateral movement attempts.
- Investigate the historical behavior of the involved systems and users to determine if the high number of process arguments is an anomaly or part of a regular pattern.

### False positive analysis

- Routine administrative tasks may generate a high number of process arguments, such as batch scripts or automated maintenance operations. Users can create exceptions for known scripts or processes that are regularly executed by trusted administrators.
- Software updates or installations often involve complex commands with multiple arguments. To mitigate false positives, users should whitelist update processes from trusted vendors.
- Monitoring and management tools that perform extensive logging or diagnostics can trigger this rule. Users should identify and exclude these tools if they are verified as non-threatening.
- Custom applications or scripts developed in-house may use numerous arguments for configuration purposes. Users should document and exclude these applications if they are part of normal business operations.
- Scheduled tasks that run during off-hours might appear suspicious due to their complexity. Users can adjust the rule to ignore these tasks if they are part of a regular, approved schedule.

### Response and remediation

- Isolate the affected system from the network to prevent further lateral movement and potential data exfiltration.
- Terminate any suspicious RDP sessions and associated processes that exhibit high numbers of arguments to halt ongoing malicious activities.
- Conduct a thorough review of the affected system's event logs and process execution history to identify any unauthorized access or changes made during the RDP session.
- Reset credentials for any accounts that were accessed during the suspicious RDP session to prevent unauthorized access using compromised credentials.
- Apply security patches and updates to the affected system and any other systems within the network to mitigate vulnerabilities that could be exploited for similar attacks.
- Enhance monitoring and logging for RDP sessions across the network to detect and respond to similar anomalies more quickly in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems have been compromised.
