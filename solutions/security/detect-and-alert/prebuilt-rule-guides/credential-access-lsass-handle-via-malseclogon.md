---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious LSASS Access via MalSecLogon" prebuilt detection rule.'
---

# Suspicious LSASS Access via MalSecLogon

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious LSASS Access via MalSecLogon

The Local Security Authority Subsystem Service (LSASS) is crucial for managing security policies and user authentication in Windows environments. Adversaries may exploit the Secondary Logon service to gain unauthorized access to LSASS, aiming to extract sensitive credentials. The detection rule identifies this threat by monitoring for unusual access patterns involving LSASS, specifically when the seclogon.dll is involved, indicating potential credential dumping activities.

### Possible investigation steps

- Review the event logs for the specific event code "10" to gather more details about the process that triggered the alert, focusing on the time of occurrence and any associated user accounts.
- Examine the process details for "svchost.exe" to determine if it is running under an expected service or if there are any anomalies in its execution context, such as unusual parent processes or command-line arguments.
- Investigate the call trace involving "seclogon.dll" to understand the sequence of events leading to the LSASS access, and check for any other suspicious modules or DLLs loaded in the process.
- Analyze the granted access value "0x14c0" to confirm if it aligns with typical access patterns for legitimate processes interacting with LSASS, and identify any deviations that could indicate malicious intent.
- Correlate the alert with other security events or logs from the same host or user account to identify any patterns or additional indicators of compromise, such as failed login attempts or other suspicious process activities.
- Check for any recent changes or updates to the system that might explain the unusual behavior, such as software installations, patches, or configuration changes that could affect the Secondary Logon service or LSASS.

### False positive analysis

- Legitimate administrative tools or scripts that require access to LSASS for system management tasks may trigger this rule. Users can create exceptions for known tools by excluding specific process names or paths that are verified as safe.
- Security software or endpoint protection solutions that perform regular scans and require access to LSASS might be flagged. Coordinate with security vendors to identify these processes and exclude them from the rule.
- System updates or patches that involve the Secondary Logon service could cause temporary access patterns that mimic suspicious behavior. Monitor update schedules and temporarily adjust the rule to prevent false alerts during these periods.
- Custom enterprise applications that utilize the Secondary Logon service for legitimate purposes may inadvertently match the rule criteria. Work with application developers to understand these access patterns and whitelist the associated processes.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes associated with svchost.exe that are accessing LSASS with the identified suspicious access rights.
- Conduct a thorough review of user accounts and privileges on the affected system to identify any unauthorized changes or access.
- Reset passwords for all accounts that may have been compromised, focusing on high-privilege accounts first.
- Collect and preserve relevant logs and forensic data from the affected system for further analysis and potential legal action.
- Escalate the incident to the security operations center (SOC) or incident response team for a comprehensive investigation and to determine the full scope of the breach.
- Implement additional monitoring and alerting for similar suspicious activities involving LSASS and seclogon.dll to enhance detection capabilities.
