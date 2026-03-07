---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential LSASS Memory Dump via PssCaptureSnapShot" prebuilt detection rule.
---

# Potential LSASS Memory Dump via PssCaptureSnapShot

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential LSASS Memory Dump via PssCaptureSnapShot

PssCaptureSnapShot is a Windows feature used for capturing process snapshots, aiding in diagnostics and debugging. Adversaries exploit this to access LSASS memory, aiming to extract credentials. The detection rule identifies suspicious behavior by monitoring for repeated access to LSASS by the same process, targeting different instances, which may indicate an evasion attempt to dump credentials stealthily.

### Possible investigation steps

- Review the event logs for the specific event code 10 to gather details about the process that accessed the LSASS handle, including the process name, process ID, and the time of access.
- Check the process execution history on the host to determine if the process accessing LSASS is legitimate or potentially malicious. Look for any unusual or unexpected processes that might have been executed around the time of the alert.
- Investigate the parent process of the suspicious process to understand how it was initiated and whether it was spawned by a legitimate application or a known malicious process.
- Analyze the network activity of the host around the time of the alert to identify any suspicious outbound connections that might indicate data exfiltration attempts.
- Correlate the alert with other security events or alerts from the same host or user account to identify any patterns or additional indicators of compromise.
- Verify the integrity and security posture of the host by checking for any unauthorized changes to system files or configurations, especially those related to security settings.

### False positive analysis

- Legitimate diagnostic tools or software that utilize PssCaptureSnapShot for debugging purposes may trigger this rule. Users should identify and whitelist these trusted applications to prevent false positives.
- System administrators or security tools performing regular health checks on LSASS might access LSASS memory in a non-malicious manner. Exclude these known processes by creating exceptions based on their process names or hashes.
- Automated scripts or maintenance tasks that interact with LSASS for legitimate reasons could be flagged. Review and document these tasks, then configure the rule to ignore these specific activities.
- Security software updates or patches that temporarily access LSASS for validation or configuration purposes may cause alerts. Monitor update schedules and adjust the rule to accommodate these temporary accesses.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified as accessing LSASS memory using PssCaptureSnapShot to halt potential credential dumping activities.
- Conduct a thorough review of the affected system's event logs, focusing on event code 10, to identify any additional instances of suspicious LSASS access and determine the scope of the compromise.
- Change all potentially compromised credentials, especially those with administrative privileges, to mitigate the risk of unauthorized access using dumped credentials.
- Apply the latest security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Enhance monitoring and detection capabilities by ensuring that similar suspicious activities are logged and alerted on, using the specific query fields and threat indicators identified in this alert.
