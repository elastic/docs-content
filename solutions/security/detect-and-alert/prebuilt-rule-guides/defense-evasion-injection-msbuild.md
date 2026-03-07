---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Process Injection by the Microsoft Build Engine" prebuilt detection rule.'
---

# Process Injection by the Microsoft Build Engine

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Injection by the Microsoft Build Engine

The Microsoft Build Engine (MSBuild) is a platform for building applications, often used in software development environments. Adversaries exploit MSBuild to perform process injection, a technique to execute malicious code within the address space of another process, thereby evading detection and potentially escalating privileges. The detection rule identifies suspicious MSBuild activity by monitoring for thread creation in other processes, leveraging Sysmon data to flag potential abuse.

### Possible investigation steps

- Review the alert details to confirm that the process name is "MSBuild.exe" and the event action is "CreateRemoteThread detected (rule: CreateRemoteThread)".
- Examine the parent process of MSBuild.exe to determine if it was launched by a legitimate application or user, which could indicate whether the activity is expected or suspicious.
- Check the timeline of events to see if there are any other related alerts or activities around the same time, such as unusual network connections or file modifications, which could provide additional context.
- Investigate the target process where the thread was created to assess its normal behavior and determine if it is a common target for injection or if it has been compromised.
- Analyze the command line arguments used to launch MSBuild.exe to identify any unusual or suspicious parameters that could indicate malicious intent.
- Review the user account associated with the MSBuild.exe process to verify if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Consult threat intelligence sources to check if there are any known campaigns or malware that utilize MSBuild for process injection, which could help in understanding the potential threat actor or objective.

### False positive analysis

- Development environments often use MSBuild for legitimate purposes, which can trigger false positives. Users should monitor and establish a baseline of normal MSBuild activity to differentiate between benign and suspicious behavior.
- Automated build systems may frequently invoke MSBuild, leading to false positives. Consider excluding known build server IP addresses or specific user accounts associated with these systems from the detection rule.
- Some legitimate software may use MSBuild for plugin or extension loading, which could appear as process injection. Identify and whitelist these applications by their process hashes or paths to reduce noise.
- Regular updates or installations of software development tools might cause MSBuild to create threads in other processes. Temporarily disable the rule during scheduled maintenance windows to prevent unnecessary alerts.
- Collaborate with development teams to understand their use of MSBuild and adjust the detection rule to exclude known safe operations, ensuring that only unexpected or unauthorized uses are flagged.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate the MSBuild.exe process if it is confirmed to be involved in unauthorized thread creation, using task management tools or scripts.
- Conduct a memory analysis on the affected system to identify and extract any injected code or payloads for further investigation.
- Review and restore any altered or compromised system files and configurations to their original state using known good backups.
- Escalate the incident to the security operations center (SOC) or incident response team for a comprehensive investigation and to determine the scope of the intrusion.
- Implement application whitelisting to prevent unauthorized execution of MSBuild.exe or similar tools in non-development environments.
- Enhance monitoring and detection capabilities by ensuring Sysmon is configured to log detailed process creation and thread injection events across the network.
