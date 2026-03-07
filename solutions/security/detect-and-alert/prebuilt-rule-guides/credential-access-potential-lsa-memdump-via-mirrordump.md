---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Credential Access via DuplicateHandle in LSASS" prebuilt detection rule.
---

# Potential Credential Access via DuplicateHandle in LSASS

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Credential Access via DuplicateHandle in LSASS

The Local Security Authority Subsystem Service (LSASS) is crucial for enforcing security policies and managing user credentials in Windows environments. Adversaries may exploit the DuplicateHandle function to access LSASS memory, bypassing traditional API calls to avoid detection. The detection rule identifies suspicious LSASS handle access attempts from unknown modules, flagging potential credential dumping activities.

### Possible investigation steps

- Review the event logs for the specific event code "10" to gather more details about the suspicious activity, focusing on the process name "lsass.exe" and the granted access "0x40".
- Investigate the call trace details where the event data indicates "*UNKNOWN*" to identify any unknown or suspicious modules that may have initiated the DuplicateHandle request.
- Correlate the suspicious activity with other security events or alerts on the same host to determine if there are additional indicators of compromise or related malicious activities.
- Check the process tree and parent-child relationships of the lsass.exe process to identify any unusual or unauthorized processes that may have interacted with LSASS.
- Analyze the timeline of events to understand the sequence of actions leading up to and following the alert, which may help in identifying the adversary's objectives or next steps.
- Review recent changes or updates to the system that might have introduced the unknown module or altered the behavior of legitimate processes.

### False positive analysis

- Legitimate software or security tools that interact with LSASS for monitoring or protection purposes may trigger this rule. Users should identify and whitelist these trusted applications to prevent unnecessary alerts.
- System management or administrative scripts that perform legitimate operations on LSASS might be flagged. Review these scripts and, if verified as safe, add them to an exception list to reduce false positives.
- Custom in-house applications that require access to LSASS for valid reasons could be mistakenly identified. Conduct a thorough review of these applications and exclude them from the rule if they are deemed non-threatening.
- Security testing or penetration testing activities may mimic malicious behavior. Coordinate with security teams to recognize these activities and temporarily adjust the rule settings during testing periods to avoid false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes associated with the unknown executable region accessing LSASS to halt potential credential dumping activities.
- Conduct a thorough memory analysis of the affected system to identify any malicious artifacts or indicators of compromise related to the DuplicateHandle exploitation.
- Reset credentials for all accounts that may have been accessed or compromised, prioritizing high-privilege accounts.
- Review and update endpoint protection configurations to ensure they are capable of detecting and blocking similar unauthorized access attempts in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for LSASS and related processes to detect any future attempts to exploit the DuplicateHandle function.
