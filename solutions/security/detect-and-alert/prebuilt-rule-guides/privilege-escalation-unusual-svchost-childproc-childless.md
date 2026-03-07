---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Service Host Child Process - Childless Service" prebuilt detection rule.
---

# Unusual Service Host Child Process - Childless Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Service Host Child Process - Childless Service

Service Host (svchost.exe) is a critical Windows process that hosts multiple services to optimize resource usage. Typically, certain services under svchost.exe do not spawn child processes. Adversaries exploit this by injecting malicious code to execute unauthorized processes, evading detection. The detection rule identifies anomalies by monitoring child processes of traditionally childless services, flagging potential exploitation attempts.

### Possible investigation steps

- Review the process details of the child process, including its name and executable path, to determine if it is a known legitimate process or potentially malicious.
- Examine the parent process arguments to confirm if the svchost.exe instance is associated with a service that traditionally does not spawn child processes, as listed in the query.
- Check the process creation time and correlate it with any other suspicious activities or alerts in the system around the same timeframe.
- Investigate the user account under which the child process was executed to assess if it has the necessary privileges and if the activity aligns with typical user behavior.
- Analyze any network connections or file modifications made by the child process to identify potential malicious actions or data exfiltration attempts.
- Cross-reference the child process with known false positives listed in the query to rule out benign activities.
- Utilize threat intelligence sources to determine if the child process or its executable path is associated with known malware or attack patterns.

### False positive analysis

- Processes like WerFault.exe, WerFaultSecure.exe, and wermgr.exe are known to be legitimate Windows error reporting tools that may occasionally be spawned by svchost.exe. To handle these, add them to the exclusion list in the detection rule to prevent unnecessary alerts.
- RelPost.exe associated with WdiSystemHost can be a legitimate process in certain environments. If this is a common occurrence, consider adding an exception for this executable when it is spawned by WdiSystemHost.
- Rundll32.exe executing winethc.dll with ForceProxyDetectionOnNextRun arguments under WdiServiceHost may be a benign operation in some network configurations. If verified as non-malicious, exclude this specific process and argument combination.
- Processes under the imgsvc service, such as lexexe.exe from Kodak directories, might be legitimate in environments using specific imaging software. Validate these occurrences and exclude them if they are confirmed to be non-threatening.
- Regularly review and update the exclusion list to ensure it reflects the current environment and does not inadvertently allow malicious activity.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious child processes spawned by svchost.exe that are not typically associated with legitimate operations, as identified in the alert.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any injected malicious code or associated malware.
- Review and analyze the process tree and parent-child relationships to understand the scope of the compromise and identify any additional affected processes or systems.
- Restore the affected system from a known good backup if malicious activity is confirmed and cannot be fully remediated through cleaning.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement enhanced monitoring and logging for svchost.exe and related processes to detect similar anomalies in the future, ensuring that alerts are configured to notify the appropriate personnel promptly.
