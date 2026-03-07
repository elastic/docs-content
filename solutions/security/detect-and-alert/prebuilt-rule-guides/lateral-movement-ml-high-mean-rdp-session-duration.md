---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "High Mean of RDP Session Duration" prebuilt detection rule.'
---

# High Mean of RDP Session Duration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating High Mean of RDP Session Duration

Remote Desktop Protocol (RDP) enables remote access to systems, facilitating administrative tasks. However, adversaries exploit prolonged RDP sessions to maintain persistent access, potentially conducting lateral movements undetected. The 'High Mean of RDP Session Duration' detection rule leverages machine learning to identify anomalies in session lengths, flagging potential misuse indicative of malicious activity.

### Possible investigation steps

- Review the specific RDP session details, including the start and end times, to understand the duration and identify any patterns or anomalies in session lengths.
- Correlate the flagged RDP session with user activity logs to determine if the session aligns with expected user behavior or if it deviates from normal patterns.
- Check for any concurrent or subsequent suspicious activities, such as file transfers or command executions, that might indicate lateral movement or data exfiltration.
- Investigate the source and destination IP addresses involved in the RDP session to identify if they are known, trusted, or associated with any previous security incidents.
- Analyze the user account involved in the RDP session for any signs of compromise, such as recent password changes, failed login attempts, or unusual access patterns.
- Review any recent changes in the network or system configurations that might have affected RDP session durations or security settings.

### False positive analysis

- Extended RDP sessions for legitimate administrative tasks can trigger false positives. To manage this, identify and whitelist IP addresses or user accounts associated with routine administrative activities.
- Scheduled maintenance or software updates often require prolonged RDP sessions. Exclude these activities by setting time-based exceptions during known maintenance windows.
- Remote support sessions from trusted third-party vendors may appear as anomalies. Create exceptions for these vendors by verifying their IP addresses and adding them to an allowlist.
- Training sessions or demonstrations using RDP can result in longer session durations. Document and exclude these events by correlating them with scheduled training times and user accounts involved.
- Automated scripts or processes that maintain RDP sessions for monitoring purposes can be mistaken for threats. Identify these scripts and exclude their associated user accounts or machine names from the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious or unauthorized RDP sessions to cut off potential adversary access.
- Conduct a thorough review of user accounts and permissions on the affected system to identify and disable any compromised accounts.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Restore the system from a known good backup if any unauthorized changes or malware are detected.
- Monitor network traffic and logs for any signs of further exploitation attempts or related suspicious activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation.
