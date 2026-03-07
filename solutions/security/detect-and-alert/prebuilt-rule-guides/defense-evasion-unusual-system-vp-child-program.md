---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Child Process from a System Virtual Process" prebuilt detection rule.
---

# Unusual Child Process from a System Virtual Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Child Process from a System Virtual Process

In Windows environments, the System process (PID 4) is a critical component responsible for managing system-level operations. Adversaries may exploit this by injecting malicious code to spawn unauthorized child processes, evading detection. The detection rule identifies anomalies by flagging unexpected child processes originating from the System process, excluding known legitimate executables, thus highlighting potential threats.

### Possible investigation steps

- Review the process details of the suspicious child process, including the executable path and command line arguments, to determine if it matches known malicious patterns or anomalies.
- Check the parent process (PID 4) to confirm it is indeed the System process and verify if any legitimate processes are excluded as per the rule (e.g., Registry, MemCompression, smss.exe).
- Investigate the timeline of events leading up to the process start event to identify any preceding suspicious activities or anomalies that might indicate process injection or exploitation.
- Correlate the alert with other security telemetry from data sources like Microsoft Defender for Endpoint or Sysmon to identify any related alerts or indicators of compromise.
- Examine the network activity associated with the suspicious process to detect any unauthorized connections or data exfiltration attempts.
- Consult threat intelligence sources to determine if the process executable or its behavior is associated with known malware or threat actor techniques.
- If necessary, isolate the affected system to prevent further potential malicious activity and conduct a deeper forensic analysis.

### False positive analysis

- Legitimate system maintenance tools may occasionally spawn child processes from the System process. Users should monitor and verify these tools and add them to the exclusion list if they are confirmed to be safe.
- Some security software might create child processes from the System process as part of their normal operation. Identify these processes and configure exceptions to prevent unnecessary alerts.
- Windows updates or system patches can sometimes trigger unexpected child processes. Ensure that these processes are part of a legitimate update cycle and exclude them if they are verified.
- Custom scripts or administrative tools used for system management might also cause false positives. Review these scripts and tools, and if they are deemed safe, add them to the exclusion list.
- Virtualization software or sandbox environments may mimic or interact with the System process in ways that trigger alerts. Validate these interactions and exclude them if they are part of normal operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of the potential threat.
- Terminate any suspicious child processes identified as originating from the System process (PID 4) that are not part of the known legitimate executables.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any injected malicious code.
- Review recent system changes and installed software to identify any unauthorized modifications or installations that could have facilitated the process injection.
- Restore the system from a known good backup if malicious activity is confirmed and cannot be fully remediated through other means.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for the affected system and similar environments to detect any recurrence of the threat, focusing on process creation events and anomalies related to the System process.
