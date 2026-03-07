---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious WMIC XSL Script Execution" prebuilt detection rule.
---

# Suspicious WMIC XSL Script Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious WMIC XSL Script Execution

Windows Management Instrumentation Command-line (WMIC) is a powerful tool for managing Windows systems. Adversaries exploit WMIC to bypass security measures by executing scripts via XSL files, often loading scripting libraries like jscript.dll or vbscript.dll. The detection rule identifies such suspicious activities by monitoring WMIC executions with atypical arguments and the loading of specific libraries, indicating potential misuse for defense evasion.

### Possible investigation steps

- Review the process execution details to confirm the presence of WMIC.exe or wmic.exe with suspicious arguments such as "format*:*", "/format*:*", or "*-format*:*" that deviate from typical usage patterns.
- Examine the command line used in the process execution to identify any unusual or unexpected parameters that could indicate malicious intent, excluding known benign patterns like "* /format:table *".
- Investigate the sequence of events to determine if there was a library or process event involving the loading of jscript.dll or vbscript.dll, which may suggest script execution through XSL files.
- Correlate the process.entity_id with other related events within the 2-minute window to identify any additional suspicious activities or processes that may have been spawned as a result of the initial execution.
- Check the parent process of the suspicious WMIC execution to understand the context and origin of the activity, which may provide insights into whether it was initiated by a legitimate application or a potentially malicious actor.
- Analyze the host's recent activity and security logs for any other indicators of compromise or related suspicious behavior that could be part of a broader attack campaign.

### False positive analysis

- Legitimate administrative tasks using WMIC with custom scripts may trigger alerts. Review the command line arguments and context to determine if the execution is part of routine system management.
- Automated scripts or software updates that utilize WMIC for legitimate purposes might load scripting libraries like jscript.dll or vbscript.dll. Identify these processes and consider adding them to an allowlist to prevent future false positives.
- Security tools or monitoring solutions that use WMIC for system checks can be mistaken for suspicious activity. Verify the source and purpose of the execution and exclude these known tools from triggering alerts.
- Scheduled tasks or maintenance scripts that use WMIC with non-standard arguments could be flagged. Document these tasks and create exceptions for their specific command line patterns to reduce noise.
- Custom applications developed in-house that rely on WMIC for functionality may inadvertently match the detection criteria. Work with development teams to understand these applications and adjust the detection rule to accommodate their legitimate use cases.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious WMIC processes identified by the alert to stop ongoing malicious script execution.
- Conduct a thorough review of the system's recent activity logs to identify any additional indicators of compromise or related malicious activities.
- Remove any unauthorized or suspicious XSL files and associated scripts from the system to prevent re-execution.
- Restore the system from a known good backup if any critical system files or configurations have been altered.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
