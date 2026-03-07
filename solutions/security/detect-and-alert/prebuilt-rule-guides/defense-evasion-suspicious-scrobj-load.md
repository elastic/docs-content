---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Script Object Execution" prebuilt detection rule.'
---

# Suspicious Script Object Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Script Object Execution

The scrobj.dll is a legitimate Windows library used for executing scriptlets, often in automation tasks. However, adversaries can exploit it to run malicious scripts within trusted processes, evading detection. The detection rule identifies unusual loading of scrobj.dll in non-standard processes, flagging potential misuse. By excluding common executables, it focuses on anomalous activity, aiding in early threat detection.

### Possible investigation steps

- Review the process executable path to confirm if it is indeed non-standard for loading scrobj.dll, as specified in the query.
- Check the parent process of the flagged executable to understand how it was initiated and assess if it aligns with typical behavior.
- Investigate the user account associated with the process execution to determine if it is a legitimate user or potentially compromised.
- Analyze recent activity on the host for any other suspicious behavior or anomalies that might correlate with the alert.
- Examine network connections from the host to identify any unusual or unauthorized external communications that could indicate malicious activity.
- Review historical data for similar alerts on the same host to identify patterns or repeated suspicious behavior.

### False positive analysis

- Legitimate administrative scripts may trigger the rule if they are executed using non-standard processes. To handle this, identify and document regular administrative tasks that use scriptlets and exclude these specific processes from the rule.
- Custom enterprise applications that utilize scrobj.dll for legitimate automation purposes might be flagged. Review these applications and add them to the exclusion list if they are verified as safe.
- Scheduled tasks or maintenance scripts that load scrobj.dll in non-standard processes can cause false positives. Regularly audit scheduled tasks and exclude known safe processes from the detection rule.
- Development or testing environments where scriptlets are frequently used for automation may generate alerts. Consider creating a separate rule set for these environments to reduce noise while maintaining security monitoring.

### Response and remediation

- Isolate the affected system from the network to prevent further execution of potentially malicious scripts and lateral movement.
- Terminate any suspicious processes identified as loading scrobj.dll in non-standard executables to halt malicious activity.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious scripts or files.
- Review and restore any altered system configurations or settings to their default state to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement application whitelisting to prevent unauthorized execution of scripts and binaries, focusing on the processes identified in the detection rule.
- Update detection mechanisms to monitor for similar activities across the network, ensuring that any future attempts to exploit scrobj.dll are promptly identified and addressed.
