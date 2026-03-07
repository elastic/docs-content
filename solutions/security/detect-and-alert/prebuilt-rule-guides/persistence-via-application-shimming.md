---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Application Shimming via Sdbinst" prebuilt detection rule.'
---

# Potential Application Shimming via Sdbinst

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Application Shimming via Sdbinst

Application shimming is a Windows feature designed to ensure software compatibility across different OS versions. However, attackers exploit this by using the `sdbinst.exe` tool to execute malicious code under the guise of legitimate processes, achieving persistence. The detection rule identifies suspicious invocations of `sdbinst.exe` by filtering out benign arguments, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the process execution details to confirm the presence of sdbinst.exe with suspicious arguments that do not include the benign flags -m, -bg, or -mm.
- Investigate the parent process of sdbinst.exe to determine if it is a legitimate and expected process or if it is potentially malicious.
- Check the timeline of events around the execution of sdbinst.exe to identify any related or preceding suspicious activities, such as unusual file modifications or network connections.
- Analyze the user account associated with the execution of sdbinst.exe to verify if it is a legitimate user and if there are any signs of account compromise.
- Examine the system for any newly installed or modified application compatibility databases (.sdb files) that could be associated with the suspicious execution of sdbinst.exe.
- Correlate the alert with other security tools and logs, such as Microsoft Defender for Endpoint or Sysmon, to gather additional context and confirm the presence of malicious activity.

### False positive analysis

- Legitimate software installations or updates may trigger sdbinst.exe with arguments that are not typically malicious. Users should verify the source and purpose of the software to determine if it is expected behavior.
- System administrators might use sdbinst.exe for deploying compatibility fixes across an organization. In such cases, document these activities and create exceptions for known administrative tasks.
- Some enterprise applications may use sdbinst.exe as part of their normal operation. Identify these applications and exclude their specific command-line arguments from triggering alerts.
- Scheduled tasks or scripts that include sdbinst.exe for maintenance purposes can be a source of false positives. Review these tasks and scripts, and whitelist them if they are part of routine operations.
- Regularly review and update the list of exceptions to ensure that only verified and necessary exclusions are maintained, minimizing the risk of overlooking genuine threats.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes associated with `sdbinst.exe` that do not match known legitimate usage patterns.
- Remove any unauthorized or suspicious application compatibility databases (.sdb files) that may have been installed using `sdbinst.exe`.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional malicious files or persistence mechanisms.
- Review and restore any altered system configurations or registry settings to their default or secure state.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for `sdbinst.exe` executions across the network to detect and respond to future attempts at application shimming.
