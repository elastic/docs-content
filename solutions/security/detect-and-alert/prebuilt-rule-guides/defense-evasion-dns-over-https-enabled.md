---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "DNS-over-HTTPS Enabled via Registry" prebuilt detection rule.
---

# DNS-over-HTTPS Enabled via Registry

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DNS-over-HTTPS Enabled via Registry

DNS-over-HTTPS (DoH) encrypts DNS queries to enhance privacy and security, preventing eavesdropping and manipulation. However, adversaries can exploit DoH to conceal malicious activities, such as data exfiltration, by bypassing traditional DNS monitoring. The detection rule identifies registry changes enabling DoH in browsers like Edge, Chrome, and Firefox, signaling potential misuse for defense evasion.

### Possible investigation steps

- Review the registry path and data values from the alert to determine which browser and setting were modified. Check if the change aligns with known user activity or policy.
- Investigate the user account associated with the registry change to assess if the activity is expected or if the account has a history of suspicious behavior.
- Examine recent network traffic from the host to identify any unusual or unauthorized DNS queries that could indicate data exfiltration or other malicious activities.
- Check for any other recent registry changes or system modifications on the host that might suggest further attempts at defense evasion or persistence.
- Correlate the alert with other security events or logs from the same host or user to identify patterns or additional indicators of compromise.

### False positive analysis

- Legitimate software updates or installations may enable DNS-over-HTTPS settings in browsers. Monitor software update schedules and correlate registry changes with known update events to identify benign changes.
- Organizational policies might require DNS-over-HTTPS for privacy compliance. Document these policies and create exceptions in the detection rule for systems where this is a known requirement.
- User-initiated privacy settings changes can trigger the rule. Educate users on the implications of enabling DNS-over-HTTPS and establish a process for them to report intentional changes, allowing for exclusion of these events.
- Security tools or privacy-focused applications may enable DNS-over-HTTPS as part of their functionality. Identify these tools within the organization and adjust the detection rule to exclude registry changes associated with their operation.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential data exfiltration or further malicious activity.
- Review and revert any unauthorized registry changes related to DNS-over-HTTPS settings in Edge, Chrome, and Firefox to restore standard DNS monitoring capabilities.
- Conduct a thorough scan of the affected system using updated antivirus and endpoint detection tools to identify and remove any malicious software or scripts.
- Analyze network traffic logs to identify any unusual or unauthorized DNS queries or data transfers that may have occurred during the period of DoH activation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring for registry changes related to DNS settings across the organization to detect similar threats in the future.
- Review and update security policies to ensure that DNS-over-HTTPS is only enabled through approved channels and for legitimate purposes, reducing the risk of misuse.
