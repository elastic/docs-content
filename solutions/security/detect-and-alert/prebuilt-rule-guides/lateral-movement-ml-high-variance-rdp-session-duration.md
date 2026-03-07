---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "High Variance in RDP Session Duration" prebuilt detection rule.
---

# High Variance in RDP Session Duration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating High Variance in RDP Session Duration

Remote Desktop Protocol (RDP) enables remote access to systems, facilitating legitimate administrative tasks. However, adversaries exploit prolonged RDP sessions to maintain persistent access, often for lateral movement within networks. The detection rule leverages machine learning to identify anomalies in session duration, flagging potential misuse by highlighting sessions with unusually high variance, which may indicate malicious activity.

### Possible investigation steps

- Review the specific RDP session details, including the start and end times, to understand the duration and identify any patterns or anomalies in session length.
- Correlate the flagged RDP session with user activity logs to determine if the session aligns with known user behavior or scheduled administrative tasks.
- Investigate the source and destination IP addresses involved in the RDP session to identify any unusual or unauthorized access points.
- Check for any concurrent alerts or logs indicating lateral movement or other suspicious activities originating from the same source or targeting the same destination.
- Analyze the user account associated with the RDP session for any signs of compromise, such as recent password changes, failed login attempts, or unusual access times.
- Review the network traffic during the RDP session for any signs of data exfiltration or communication with known malicious IP addresses.

### False positive analysis

- Long RDP sessions for legitimate administrative tasks can trigger false positives. To manage this, identify and whitelist IP addresses or user accounts associated with routine administrative activities.
- Scheduled maintenance or updates often require extended RDP sessions. Exclude these sessions by setting time-based exceptions during known maintenance windows.
- Automated scripts or tools that require prolonged RDP access for monitoring or data collection can be mistaken for anomalies. Document and exclude these processes by recognizing their unique session patterns.
- Remote support sessions from trusted third-party vendors may appear as high variance. Establish a list of trusted vendor IPs or accounts to prevent these from being flagged.
- Training or demonstration sessions that involve extended RDP use should be accounted for by creating exceptions for specific user groups or departments involved in such activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further lateral movement and potential data exfiltration.
- Terminate the suspicious RDP session to disrupt any ongoing unauthorized activities.
- Conduct a thorough review of the affected system for signs of compromise, including checking for unauthorized user accounts, installed software, and changes to system configurations.
- Reset credentials for any accounts that were accessed during the suspicious RDP session to prevent further unauthorized access.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Monitor network traffic and system logs for any signs of continued or related suspicious activity, focusing on RDP connections and lateral movement patterns.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
