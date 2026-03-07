---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Powershell Script" prebuilt detection rule.
---

# Suspicious Powershell Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Powershell Script

PowerShell is a powerful scripting language used for task automation and configuration management in Windows environments. Adversaries often exploit its capabilities to execute malicious scripts, leveraging obfuscation to evade detection. The 'Suspicious Powershell Script' detection rule employs machine learning to identify unusual script characteristics, such as obfuscation, indicating potential threats. By analyzing these anomalies, the rule aids in early threat detection and mitigation.

### Possible investigation steps

- Review the alert details to identify the specific PowerShell script or command that triggered the detection, focusing on any obfuscated elements.
- Examine the source endpoint and user account associated with the alert to determine if the activity aligns with expected behavior or if it appears suspicious.
- Check the execution history on the affected endpoint for any other unusual or unauthorized PowerShell commands or scripts executed around the same time.
- Investigate the network activity from the source endpoint to identify any connections to known malicious IP addresses or domains.
- Correlate the alert with other security events or logs, such as antivirus alerts or firewall logs, to gather additional context and assess the potential impact.
- Consult threat intelligence sources to determine if the detected script or its components are associated with known malware or attack campaigns.

### False positive analysis

- Legitimate administrative scripts may trigger the rule due to obfuscation techniques used for efficiency or security. Review the script's purpose and source to determine its legitimacy.
- Automated deployment tools often use PowerShell scripts that appear obfuscated. Identify and whitelist these tools to prevent unnecessary alerts.
- Security software updates might use obfuscated scripts for protection against tampering. Verify the update source and add exceptions for known trusted vendors.
- Custom scripts developed in-house for specific tasks may use obfuscation for intellectual property protection. Document and exclude these scripts after confirming their safety.
- Regularly review and update the list of exceptions to ensure that only verified non-threatening scripts are excluded, maintaining the effectiveness of the detection rule.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate any suspicious PowerShell processes identified on the affected system to halt the execution of potentially harmful scripts.
- Conduct a thorough review of the PowerShell script logs and execution history on the affected system to identify any unauthorized or malicious commands executed.
- Restore the affected system from a known good backup if any malicious activity is confirmed, ensuring that the backup is free from compromise.
- Update and patch the affected system to the latest security standards to close any vulnerabilities that may have been exploited.
- Implement enhanced monitoring for PowerShell activity across the network, focusing on detecting obfuscation and unusual script characteristics.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
