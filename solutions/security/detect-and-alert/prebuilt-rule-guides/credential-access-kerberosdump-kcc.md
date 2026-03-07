---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kerberos Cached Credentials Dumping" prebuilt detection rule.'
---

# Kerberos Cached Credentials Dumping

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kerberos Cached Credentials Dumping

Kerberos is a network authentication protocol designed to provide secure identity verification for users and services. It uses tickets to allow nodes to prove their identity in a secure manner. Adversaries may exploit tools like the Kerberos credential cache utility to extract these tickets, enabling unauthorized access and lateral movement within a network. The detection rule identifies suspicious activity by monitoring for specific processes and arguments on macOS systems, flagging potential credential dumping attempts.

### Possible investigation steps

- Review the alert details to confirm the presence of the process name 'kcc' and the argument 'copy_cred_cache' in the process execution logs on macOS systems.
- Identify the user account associated with the process execution to determine if the activity aligns with expected behavior or if it indicates potential unauthorized access.
- Examine the timeline of the process execution to identify any preceding or subsequent suspicious activities, such as unusual login attempts or lateral movement within the network.
- Check for any other alerts or logs related to the same host or user account to assess if this is part of a broader attack pattern.
- Investigate the source and destination of any network connections made by the process to identify potential data exfiltration or communication with known malicious IP addresses.
- Consult with the user or system owner to verify if the use of the 'kcc' utility was legitimate or if it requires further investigation.

### False positive analysis

- Routine administrative tasks using the kcc utility may trigger the rule. Identify and document these tasks to create exceptions for known benign activities.
- Automated scripts or maintenance processes that involve copying Kerberos credential caches can be mistaken for malicious activity. Review and whitelist these scripts if they are verified as safe.
- Developers or IT personnel testing Kerberos configurations might use the kcc utility in a non-malicious context. Establish a process to log and approve such activities to prevent false alarms.
- Security tools or monitoring solutions that interact with Kerberos tickets for legitimate purposes may inadvertently trigger the rule. Coordinate with security teams to ensure these tools are recognized and excluded from detection.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or lateral movement.
- Terminate the suspicious process identified as 'kcc' with the argument 'copy_cred_cache' to stop any ongoing credential dumping activity.
- Conduct a thorough review of the system's Kerberos ticket cache to identify any unauthorized access or anomalies, and invalidate any compromised tickets.
- Reset passwords and regenerate Kerberos tickets for any accounts that may have been affected to prevent further unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Implement additional monitoring on the affected system and similar endpoints to detect any recurrence of the credential dumping activity.
- Review and update access controls and Kerberos configurations to enhance security and reduce the risk of similar attacks in the future.
