---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "UAC Bypass via DiskCleanup Scheduled Task Hijack" prebuilt detection rule.'
---

# UAC Bypass via DiskCleanup Scheduled Task Hijack

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating UAC Bypass via DiskCleanup Scheduled Task Hijack

User Account Control (UAC) is a security feature in Windows that helps prevent unauthorized changes. Adversaries may exploit the DiskCleanup Scheduled Task to bypass UAC, executing code with elevated privileges. The detection rule identifies suspicious processes using specific arguments and executables not matching known safe paths, flagging potential UAC bypass attempts for further investigation.

### Possible investigation steps

- Review the process details to confirm the presence of suspicious arguments "/autoclean" and "/d" in the process execution.
- Verify the executable path of the process to ensure it does not match known safe paths such as "C:\Windows\System32\cleanmgr.exe" or "C:\Windows\SysWOW64\cleanmgr.exe".
- Investigate the parent process to determine how the suspicious process was initiated and assess if it was triggered by a legitimate application or script.
- Check the user account under which the process was executed to identify if it aligns with expected user behavior or if it indicates potential compromise.
- Analyze recent system changes or scheduled tasks to identify any unauthorized modifications that could facilitate UAC bypass.
- Correlate the event with other security alerts or logs from data sources like Microsoft Defender for Endpoint or Sysmon to gather additional context on the activity.
- Assess the risk and impact of the event by considering the severity and risk score, and determine if further containment or remediation actions are necessary.

### False positive analysis

- Legitimate system maintenance tools or scripts may trigger the rule if they use similar arguments and executables not listed in the safe paths. Review the process origin and context to determine if it is part of routine maintenance.
- Custom administrative scripts that automate disk cleanup tasks might be flagged. Verify the script's source and purpose, and consider adding it to an exception list if it is deemed safe.
- Software updates or installations that temporarily use disk cleanup functionalities could be misidentified. Monitor the timing and context of these events, and exclude known update processes from the rule.
- Third-party disk management tools that mimic or extend Windows disk cleanup features may cause alerts. Validate the tool's legitimacy and add it to the exclusion list if it is a trusted application.
- Scheduled tasks created by IT departments for system optimization might match the rule's criteria. Confirm the task's legitimacy and adjust the rule to exclude these specific tasks if they are verified as non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule that are not using the legitimate DiskCleanup executables.
- Conduct a thorough review of scheduled tasks on the affected system to identify and remove any unauthorized or malicious tasks that may have been created or modified.
- Restore any altered system files or configurations to their original state using known good backups or system restore points.
- Update and patch the affected system to the latest security updates to mitigate any known vulnerabilities that could be exploited for UAC bypass.
- Monitor the affected system and network for any signs of recurring unauthorized activity or similar UAC bypass attempts.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
