---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Deprecated - Potential PowerShell Obfuscated Script" prebuilt detection rule.
---

# Deprecated - Potential PowerShell Obfuscated Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Deprecated - Potential PowerShell Obfuscated Script

PowerShell is a powerful scripting language used for task automation and configuration management in Windows environments. Adversaries exploit its flexibility to obfuscate scripts, evading security measures like AMSI. The detection rule identifies obfuscation patterns, such as string manipulation and encoding techniques, to flag potentially malicious scripts, aiding in defense evasion detection.

### Possible investigation steps

- Review the PowerShell script block text captured in the alert to identify any suspicious patterns or obfuscation techniques, such as string manipulation or encoding methods like "[string]::join" or "-Join".
- Check the process execution details, including the parent process and command line arguments, to understand the context in which the PowerShell script was executed.
- Investigate the source and destination of the script execution by examining the host and user details to determine if the activity aligns with expected behavior or if it originates from an unusual or unauthorized source.
- Analyze any network connections or file modifications associated with the PowerShell process to identify potential data exfiltration or lateral movement activities.
- Correlate the alert with other security events or logs, such as Windows Event Logs or network traffic logs, to gather additional context and identify any related suspicious activities.
- Assess the risk and impact of the detected activity by considering the severity and risk score provided in the alert, and determine if immediate remediation actions are necessary.

### False positive analysis

- Legitimate administrative scripts may use string manipulation and encoding techniques for benign purposes, such as data processing or configuration management. Review the context of the script execution and verify the source and intent before flagging it as malicious.
- Scripts that automate complex tasks might use obfuscation-like patterns to handle data securely or efficiently. Consider whitelisting known scripts or trusted sources to reduce false positives.
- Development and testing environments often run scripts with obfuscation patterns for testing purposes. Exclude these environments from the rule or create exceptions for specific users or groups involved in development.
- Security tools and monitoring solutions might generate PowerShell scripts with obfuscation patterns as part of their normal operation. Identify these tools and exclude their activities from triggering the rule.
- Regularly update the list of exceptions and whitelisted scripts to ensure that new legitimate scripts are not mistakenly flagged as threats.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of potentially malicious scripts.
- Terminate any suspicious PowerShell processes identified by the detection rule to halt ongoing malicious activity.
- Conduct a thorough review of the PowerShell script block logs to identify and remove any obfuscated scripts or malicious code remnants.
- Restore the system from a known good backup if malicious activity is confirmed and system integrity is compromised.
- Update and patch the affected system to ensure all security vulnerabilities are addressed, reducing the risk of exploitation.
- Monitor the system and network for any signs of re-infection or similar obfuscation patterns to ensure the threat has been fully mitigated.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
