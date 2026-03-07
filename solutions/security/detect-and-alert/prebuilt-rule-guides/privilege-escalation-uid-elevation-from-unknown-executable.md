---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "UID Elevation from Previously Unknown Executable" prebuilt detection rule.'
---

# UID Elevation from Previously Unknown Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating UID Elevation from Previously Unknown Executable

In Linux environments, UID elevation is a process where a user's permissions are increased, often to root level, allowing full system control. Adversaries exploit this by using unknown executables to hijack execution flow, often via rootkits, to gain unauthorized root access. The detection rule identifies such activities by monitoring for UID changes initiated by non-standard executables, excluding known safe paths and processes, thus highlighting potential privilege escalation attempts.

### Possible investigation steps

- Review the process details to identify the unknown executable that triggered the alert, focusing on the process.executable field to determine its path and origin.
- Examine the parent process information using process.parent.name to understand the context in which the unknown executable was launched, checking for any unusual or unexpected shell activity.
- Investigate the user account associated with the UID change by analyzing the user.id field to determine if the account has a history of privilege escalation attempts or if it has been compromised.
- Check the system logs for any recent changes or installations that might have introduced the unknown executable, focusing on the time frame around the event.action:"uid_change".
- Assess the network activity around the time of the alert to identify any potential external connections or data exfiltration attempts that might correlate with the privilege escalation.
- Cross-reference the executable path and name against known threat intelligence databases to determine if it is associated with any known malicious activity or rootkits.
- If possible, perform a forensic analysis of the executable to understand its behavior and potential impact on the system, looking for signs of function or syscall hooking as indicated in the rule description.

### False positive analysis

- Executables in custom directories may trigger false positives if they are legitimate but not included in the known safe paths. Users can mitigate this by adding these directories to the exclusion list in the detection rule.
- Scripts or binaries executed by system administrators from non-standard locations for maintenance or deployment purposes might be flagged. To handle this, users should document and exclude these specific processes or paths if they are verified as safe.
- Development or testing environments where new executables are frequently introduced can cause alerts. Users should consider creating exceptions for these environments or paths to reduce noise while ensuring they are monitored separately for any unusual activity.
- Automated scripts or tools that perform legitimate UID changes but are not part of the standard system paths can be excluded by adding their specific executable paths or names to the rule's exception list.
- Temporary or ephemeral processes that are part of containerized applications might be flagged. Users should review and exclude these processes if they are confirmed to be part of normal operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule that are not part of the known safe paths or processes.
- Conduct a thorough review of the affected system's logs to identify any additional indicators of compromise or related suspicious activities.
- Remove any unauthorized or unknown executables found on the system, especially those involved in the UID elevation attempt.
- Restore the system from a known good backup if any rootkits or persistent threats are detected that cannot be easily removed.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems.
