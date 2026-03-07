---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Special Logon Events" prebuilt detection rule.
---

# Spike in Special Logon Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Special Logon Events

Special logon events are crucial for tracking privileged access, often indicating administrative actions. Adversaries exploit these by gaining elevated access to perform unauthorized activities, such as lateral movement or privilege escalation. The detection rule leverages machine learning to identify unusual spikes in these events, signaling potential misuse and enabling timely investigation of suspicious privileged access activities.

### Possible investigation steps

- Review the user account associated with the spike in special logon events to determine if the account is expected to have privileged access.
- Check the time and frequency of the special logon events to identify any unusual patterns or times that deviate from the user's normal behavior.
- Investigate the source IP addresses and devices from which the special logon events originated to verify if they are known and trusted.
- Examine recent changes or activities performed by the user account to identify any unauthorized or suspicious actions that may indicate privilege escalation or lateral movement.
- Correlate the special logon events with other security alerts or logs, such as failed login attempts or changes in user permissions, to gather additional context and evidence of potential malicious activity.

### False positive analysis

- Regular administrative tasks by IT staff can trigger spikes in special logon events. To manage this, create exceptions for known administrative accounts that frequently perform legitimate privileged actions.
- Scheduled automated processes or scripts that require elevated access may cause false positives. Identify these processes and exclude them from the detection rule to prevent unnecessary alerts.
- Software updates or system maintenance activities often involve multiple privileged logons. Document these events and adjust the detection thresholds temporarily during known maintenance windows to reduce false positives.
- Users with roles that inherently require frequent privileged access, such as system administrators or security personnel, may trigger alerts. Maintain a list of such roles and apply exclusions where appropriate to avoid constant alerts for expected behavior.

### Response and remediation

- Immediately isolate the affected user account to prevent further unauthorized access. Disable the account or change its credentials to stop any ongoing malicious activity.
- Conduct a thorough review of recent activities associated with the affected account to identify any unauthorized changes or access to sensitive systems and data.
- If lateral movement is suspected, isolate any systems accessed by the compromised account to prevent further spread of the threat.
- Escalate the incident to the security operations center (SOC) or incident response team for a detailed investigation and to determine the full scope of the breach.
- Implement additional monitoring on the affected systems and accounts to detect any further suspicious activities or attempts to regain access.
- Review and update access controls and permissions to ensure that only necessary privileges are granted, reducing the risk of privilege escalation.
- Enhance detection capabilities by tuning existing monitoring tools to better identify similar spikes in special logon events, leveraging insights from the current incident.
