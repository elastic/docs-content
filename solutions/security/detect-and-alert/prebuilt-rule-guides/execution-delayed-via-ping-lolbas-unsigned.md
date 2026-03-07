---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Delayed Execution via Ping" prebuilt detection rule.
---

# Delayed Execution via Ping

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Delayed Execution via Ping

Ping, a network utility, can be misused by attackers to delay execution of malicious commands, aiding in evasion. Adversaries may use ping to introduce pauses, allowing them to execute harmful scripts or binaries stealthily. The detection rule identifies suspicious ping usage followed by execution of known malicious utilities, flagging potential threats by monitoring specific command patterns and excluding benign processes.

### Possible investigation steps

- Review the process tree to understand the sequence of events, focusing on the parent-child relationship between cmd.exe, ping.exe, and any subsequent suspicious processes like rundll32.exe or powershell.exe.
- Examine the command line arguments used with ping.exe to determine the delay introduced and assess if it aligns with typical malicious behavior.
- Investigate the user account associated with the process execution, especially if the user.id is not S-1-5-18, to determine if the account has been compromised or is being misused.
- Check the file path and code signature of any executables launched from the user's AppData directory to verify if they are trusted or potentially malicious.
- Analyze the command line arguments and working directory of any suspicious processes to identify any known malicious patterns or scripts being executed.
- Correlate the alert with any other recent alerts or logs from the same host or user to identify potential patterns or ongoing malicious activity.

### False positive analysis

- Legitimate administrative scripts or maintenance tasks may use ping to introduce delays, especially in batch files executed by system administrators. To handle this, identify and exclude specific scripts or command lines that are known to be safe.
- Software installations or updates might use ping for timing purposes. Review the command lines and parent processes involved, and create exceptions for trusted software paths or signatures.
- Automated testing environments may use ping to simulate network latency or wait for services to start. Exclude these processes by identifying the testing framework or environment and adding it to the exception list.
- Some legitimate applications might use ping as part of their normal operation. Monitor these applications and, if verified as safe, exclude their specific command patterns or executable paths.
- Regularly review and update the exception list to ensure it reflects the current environment and any new legitimate use cases that arise.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified in the alert, such as those involving ping.exe followed by the execution of known malicious utilities.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malware or unauthorized software.
- Review and analyze the command history and logs of the affected system to understand the scope of the attack and identify any additional compromised systems.
- Restore the system from a known good backup if malware removal is not feasible or if the system's integrity is in question.
- Implement application whitelisting to prevent unauthorized execution of scripts and binaries, focusing on the utilities identified in the alert.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
