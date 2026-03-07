---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Hex Payload Execution via Command-Line" prebuilt detection rule.
---

# Potential Hex Payload Execution via Command-Line

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Hex Payload Execution via Command-Line

In Linux environments, command-line interfaces are pivotal for executing processes and scripts. Adversaries exploit this by embedding payloads in hexadecimal format to obfuscate their actions, evading detection. The detection rule identifies processes with lengthy command lines containing multiple hex patterns, signaling potential obfuscation. This approach targets defense evasion tactics, leveraging Elastic Defend to flag suspicious executions.

### Possible investigation steps

- Review the process.command_line field to identify the specific hexadecimal patterns and assess if they correspond to known malicious payloads or commands.
- Examine the process.parent.executable to determine the parent process that initiated the execution, which may provide context on whether the execution is expected or suspicious.
- Check the user account associated with the process execution to verify if the activity aligns with typical user behavior or if it indicates potential compromise.
- Investigate the host where the alert was triggered to identify any other related suspicious activities or anomalies that might indicate a broader compromise.
- Correlate the event with other logs or alerts from the same host or user to identify patterns or repeated attempts at obfuscation and execution.

### False positive analysis

- Legitimate software installations or updates may use hexadecimal encoding in command lines for legitimate purposes. Users can create exceptions for known software update processes by identifying their parent executable paths and excluding them from the rule.
- System administration scripts or tools that utilize hexadecimal encoding for configuration or data processing might trigger the rule. Review and whitelist these scripts by verifying their source and purpose, then exclude them based on their command line patterns or parent processes.
- Security tools or monitoring software that perform regular scans or data collection using hexadecimal encoding could be flagged. Confirm these tools' legitimacy and add them to an exception list by specifying their executable paths or command line characteristics.
- Custom applications developed in-house that use hexadecimal encoding for data handling or communication may be mistakenly identified. Document these applications and exclude them by their unique command line signatures or parent process identifiers.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the suspicious process identified by the detection rule to halt any ongoing malicious execution.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as modified files or unauthorized user accounts.
- Remove any identified malicious files or scripts from the system to ensure the threat is eradicated.
- Restore the system from a known good backup if any critical system files or configurations have been altered.
- Update and patch the system to close any vulnerabilities that may have been exploited by the adversary.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.

