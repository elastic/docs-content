---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Process Spawned by a Parent Process" prebuilt detection rule.'
---

# Unusual Process Spawned by a Parent Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Spawned by a Parent Process

In Windows environments, processes are often spawned by parent processes to perform legitimate tasks. However, adversaries can exploit this by using legitimate tools, known as LOLbins, to execute malicious activities stealthily. The detection rule leverages machine learning to identify anomalies in process creation patterns, flagging processes that deviate from typical behavior, thus uncovering potential threats that evade traditional detection methods.

### Possible investigation steps

- Review the parent process and child process names to determine if they are known legitimate applications or if they are commonly associated with LOLbins or other malicious activities.
- Check the process creation time and correlate it with any known user activity or scheduled tasks to identify if the process execution aligns with expected behavior.
- Investigate the command line arguments used by the suspicious process to identify any unusual or potentially malicious commands or scripts being executed.
- Analyze the network activity associated with the process to detect any suspicious outbound connections or data exfiltration attempts.
- Examine the file path and hash of the executable to verify its legitimacy and check against known malware databases or threat intelligence sources.
- Review any recent changes to the system, such as software installations or updates, that might explain the unusual process behavior.
- Consult endpoint detection and response (EDR) logs or other security tools to gather additional context and evidence related to the process and its activities.

### False positive analysis

- Legitimate administrative tools like PowerShell or command prompt may be flagged when used for routine tasks. Users can create exceptions for these tools when executed by known and trusted parent processes.
- Software updates or installations often spawn processes that might appear unusual. Exclude these processes by identifying their typical parent-child relationships during updates.
- Custom scripts or automation tools used within the organization might trigger alerts. Document these scripts and their expected behavior to create exceptions for them.
- Frequent use of remote management tools can lead to false positives. Ensure these tools are whitelisted when used by authorized personnel.
- Regularly review and update the list of exceptions to accommodate changes in legitimate process behaviors over time.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the suspicious process identified by the alert to stop any ongoing malicious actions.
- Conduct a thorough analysis of the process and its parent to understand the scope of the compromise and identify any additional malicious activities or files.
- Remove any malicious files or artifacts associated with the process from the system to ensure complete remediation.
- Restore the system from a known good backup if the integrity of the system is compromised beyond repair.
- Update and patch the system to close any vulnerabilities that may have been exploited by the adversary.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
